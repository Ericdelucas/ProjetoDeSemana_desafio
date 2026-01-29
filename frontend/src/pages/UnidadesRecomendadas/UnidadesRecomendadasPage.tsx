import styles from "./UnidadesRecomendadasPage.module.css";

type Item = {
  title: string;
  distance: string;
  wait: string;
  status: string;
  level: "melhor" | "moderado" | "lotado";
};

const mock: Item[] = [
  { title: "UPA 1", distance: "2.4 km", wait: "15 minutos", status: "Disponível", level: "melhor" },
  { title: "UPA 2", distance: "15 km", wait: "46 minutos", status: "Um pouco lotado", level: "moderado" },
  { title: "UPA 3", distance: "50 km", wait: "—", status: "Lotado", level: "lotado" },
];

export function UnidadesRecomendadasPage() {
  return (
    <div className={styles.wrap}>
      <div className={styles.list}>
        {mock.map((i) => (
          <div key={i.title} className={styles.card}>
            <div className={`${styles.ribbon} ${styles[i.level]}`}>
              {i.level === "melhor" ? "Melhor opção" : i.level === "moderado" ? "Moderado" : "Lotado"}
            </div>

            <div className={styles.content}>
              <div className={styles.left}>
                <div className={styles.title}>{i.title}</div>

                <div className={styles.meta}>
                  <div>✔ Distância: {i.distance}</div>
                  <div>✔ Estimativa de espera: {i.wait}</div>
                  <div className={styles.status}>✔ {i.status}</div>
                </div>
              </div>

              <div className={styles.icon}>🏥</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
