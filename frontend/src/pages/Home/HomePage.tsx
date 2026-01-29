import styles from "./HomePage.module.css";
import { useNavigate } from "react-router-dom";

export function HomePage() {
  const navigate = useNavigate();

  return (
    <div className={styles.wrap}>
      <div className={styles.panel}>
        <div className={styles.hero}>
          <h2 className={styles.title}>SmartSaúde SUS</h2>
          <p className={styles.sub}>
            Bem-vindo(a) ao SmartSaúde SUS, sistema inteligente de apoio ao atendimento do SUS.
          </p>
        </div>

        <div className={styles.search_area}>
          <label className={styles.label}>Buscar unidade de saúde…</label>
          <input className={styles.input} placeholder="Digite um bairro, rua ou unidade..." />

          <label className={styles.label}>Buscar medicamento…</label>
          <input className={styles.input} placeholder="Ex.: dipirona, amoxicilina..." />

          <div className={styles.actions}>
            <button className={styles.btn} onClick={() => navigate("/unidades")}>
              Procurar unidades
            </button>
            <button className={styles.btn_secondary} onClick={() => navigate("/recomendadas")}>
              Unidades recomendadas
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}