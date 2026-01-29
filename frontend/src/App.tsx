import { useMemo, useState } from "react";
import "./index.css";
import { apiGet, apiPost } from "./lib/api";

type Unidade = {
  id: number;
  nome: string;
  endereco?: string;
  tipo?: string;
  lat?: number;
  lng?: number;
  medicos_ativos?: number;
  pacientes_fila?: number;
};

type TriagemResp = {
  risco_cor: string;
  justificativa: string;
};

function Badge({ text }: { text: string }) {
  const cls = useMemo(() => {
    const t = text.toLowerCase();
    if (t.includes("vermel")) return "badge badge-red";
    if (t.includes("laranj")) return "badge badge-orange";
    if (t.includes("amarel")) return "badge badge-yellow";
    if (t.includes("verde")) return "badge badge-green";
    if (t.includes("azul")) return "badge badge-blue";
    return "badge";
  }, [text]);

  return <span className={cls}>{text}</span>;
}

export default function App() {
  const [tab, setTab] = useState<"home" | "unidades" | "triagem">("home");

  return (
    <div className="page">
      <header className="topbar">
        <div className="brand">
          <div className="logo">SS</div>
          <div>
            <div className="title">SmartSaúde</div>
            <div className="subtitle">MVP • backend + front</div>
          </div>
        </div>

        <nav className="nav">
          <button className={tab === "home" ? "btn active" : "btn"} onClick={() => setTab("home")}>Home</button>
          <button className={tab === "unidades" ? "btn active" : "btn"} onClick={() => setTab("unidades")}>Unidades</button>
          <button className={tab === "triagem" ? "btn active" : "btn"} onClick={() => setTab("triagem")}>Triagem</button>
        </nav>
      </header>

      <main className="content">
        {tab === "home" && <Home />}
        {tab === "unidades" && <Unidades />}
        {tab === "triagem" && <Triagem />}
      </main>

      <footer className="footer">
        Backend: <code>{import.meta.env.VITE_API_URL}</code>
      </footer>
    </div>
  );
}

function Home() {
  const [health, setHealth] = useState<string>("não verificado");
  const [err, setErr] = useState<string>("");

  async function ping() {
    setErr("");
    try {
      // Se você não tiver /health, troque para "/" ou "/openapi.json"
      const data = await apiGet<any>("/openapi.json");
      setHealth(`OK (openapi: ${data?.info?.title ?? "FastAPI"})`);
    } catch (e: any) {
      setHealth("falhou");
      setErr(e.message ?? String(e));
    }
  }

  return (
    <section className="card">
      <h2>Entrega mínima funcional</h2>
      <p>Este front só depende de 2 coisas do backend: <code>GET /unidades</code> e <code>POST /atendimento/triagem</code>.</p>

      <div className="row">
        <button className="btn primary" onClick={ping}>Testar conexão</button>
        <div className="muted">Status: <strong>{health}</strong></div>
      </div>

      {err && <pre className="error">{err}</pre>}
    </section>
  );
}

function Unidades() {
  const [items, setItems] = useState<Unidade[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function load() {
    setLoading(true);
    setErr("");
    try {
      const data = await apiGet<any>("/unidades");
      // Aceita tanto array direto quanto {items: []}
      const arr = Array.isArray(data) ? data : (data?.items ?? []);
      setItems(arr);
    } catch (e: any) {
      setErr(e.message ?? String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="card">
      <div className="row space">
        <h2>Unidades</h2>
        <button className="btn primary" onClick={load} disabled={loading}>
          {loading ? "Carregando..." : "Carregar"}
        </button>
      </div>

      {err && <pre className="error">{err}</pre>}

      {items.length === 0 ? (
        <p className="muted">Nenhuma unidade carregada ainda.</p>
      ) : (
        <div className="grid">
          {items.map((u) => (
            <div key={u.id} className="panel">
              <div className="row space">
                <strong>{u.nome}</strong>
                {u.tipo ? <span className="chip">{u.tipo}</span> : null}
              </div>
              {u.endereco ? <div className="muted">{u.endereco}</div> : null}
              <div className="muted">
                lat/lng: {u.lat ?? "?"}, {u.lng ?? "?"}
              </div>
              {(u.medicos_ativos != null || u.pacientes_fila != null) && (
                <div className="muted">
                  médicos: {u.medicos_ativos ?? "?"} • fila: {u.pacientes_fila ?? "?"}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

function Triagem() {
  const [lat, setLat] = useState("-23.55052");
  const [lng, setLng] = useState("-46.63331");
  const [res, setRes] = useState<TriagemResp | null>(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function submit() {
    setLoading(true);
    setErr("");
    setRes(null);

    try {
      const data = await apiPost<TriagemResp>("/atendimento/triagem", {
        lat: Number(lat),
        lng: Number(lng),
      });
      setRes(data);
    } catch (e: any) {
      setErr(e.message ?? String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="card">
      <h2>Triagem</h2>
      <p className="muted">Envia coordenadas e recebe <code>risco_cor</code> + <code>justificativa</code>.</p>

      <div className="form">
        <label>
          Latitude
          <input value={lat} onChange={(e) => setLat(e.target.value)} />
        </label>
        <label>
          Longitude
          <input value={lng} onChange={(e) => setLng(e.target.value)} />
        </label>

        <button className="btn primary" onClick={submit} disabled={loading}>
          {loading ? "Enviando..." : "Rodar triagem"}
        </button>
      </div>

      {err && <pre className="error">{err}</pre>}

      {res && (
        <div className="result">
          <div className="row space">
            <h3>Resultado</h3>
            <Badge text={res.risco_cor} />
          </div>
          <p>{res.justificativa}</p>
        </div>
      )}
    </section>
  );
}