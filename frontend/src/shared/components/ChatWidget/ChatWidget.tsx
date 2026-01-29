import { useMemo, useState } from "react";
import styles from "./ChatWidget.module.css";

type Msg = { from: "bot" | "user"; text: string };

export function ChatWidget() {
  const [is_open, set_is_open] = useState(false);
  const [input, set_input] = useState("");
  const [messages, set_messages] = useState<Msg[]>([
    { from: "bot", text: "Olá! Em que posso ajudar?" },
  ]);

  const hint = useMemo(() => "Ex.: Onde tem dipirona disponível?", []);

  function send() {
    const text = input.trim();
    if (!text) return;

    set_messages((m) => [...m, { from: "user", text }]);
    set_input("");

    // mock de resposta (depois a gente liga no backend)
    window.setTimeout(() => {
      set_messages((m) => [
        ...m,
        {
          from: "bot",
          text: "Entendi. Vou te orientar com base nas unidades e disponibilidade (em breve com dados reais).",
        },
      ]);
    }, 350);
  }

  return (
    <>
      <button className={styles.fab} onClick={() => set_is_open((v) => !v)} aria-label="Chat">
        💬
      </button>

      {is_open && (
        <div className={styles.panel}>
          <div className={styles.header}>
            <div className={styles.header_left}>
              <div className={styles.plus}>+</div>
              <div>
                <div className={styles.title}>Assistente do SUS</div>
              </div>
            </div>

            <button className={styles.close} onClick={() => set_is_open(false)} aria-label="Fechar">
              ×
            </button>
          </div>

          <div className={styles.body}>
            {messages.map((m, idx) => (
              <div key={idx} className={m.from === "bot" ? styles.bot_row : styles.user_row}>
                <div className={m.from === "bot" ? styles.bubble_bot : styles.bubble_user}>{m.text}</div>
              </div>
            ))}
          </div>

          <div className={styles.footer}>
            <input
              value={input}
              onChange={(e) => set_input(e.target.value)}
              placeholder={hint}
              className={styles.input}
              onKeyDown={(e) => (e.key === "Enter" ? send() : null)}
            />
            <button className={styles.send} onClick={send}>
              Enviar
            </button>
          </div>
        </div>
      )}
    </>
  );
}
