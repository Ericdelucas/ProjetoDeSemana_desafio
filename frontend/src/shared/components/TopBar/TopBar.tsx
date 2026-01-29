import styles from "./TopBar.module.css";

type Props = {
  title: string;
  is_menu_open: boolean;
  on_toggle_menu: () => void;
  show_back?: boolean;
  on_back?: () => void;
};

export function TopBar({ title, on_toggle_menu, show_back, on_back }: Props) {
  return (
    <header className={styles.topbar}>
      <div className={styles.left}>
        {show_back ? (
          <button className={styles.icon_btn} onClick={on_back} aria-label="Voltar">
            ←
          </button>
        ) : (
          <button className={styles.icon_btn} onClick={on_toggle_menu} aria-label="Menu">
            ☰
          </button>
        )}

        <h1 className={styles.title}>{title}</h1>
      </div>

      <button className={styles.plus_btn} aria-label="Ação">
        +
      </button>
    </header>
  );
}