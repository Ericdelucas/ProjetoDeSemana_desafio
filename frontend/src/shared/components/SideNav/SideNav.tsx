import { NavLink } from "react-router-dom";
import styles from "./SideNav.module.css";

type Props = {
  is_open: boolean;
  on_close: () => void;
};

export function SideNav({ is_open, on_close }: Props) {
  return (
    <>
      <aside className={`${styles.sidenav} ${is_open ? styles.open : ""}`}>
        <div className={styles.brand}>
          <div className={styles.badge}>SS</div>
          <div>
            <div className={styles.name}>SmartSaúde SUS</div>
            <div className={styles.sub}>MVP • backend + front</div>
          </div>
        </div>

        <nav className={styles.nav}>
          <NavLink to="/" className={({ isActive }) => (isActive ? styles.active : styles.link)}>
            Início
          </NavLink>
          <NavLink to="/unidades" className={({ isActive }) => (isActive ? styles.active : styles.link)}>
            Unidades
          </NavLink>
          <NavLink to="/triagem" className={({ isActive }) => (isActive ? styles.active : styles.link)}>
            Triagem
          </NavLink>
          <NavLink to="/recomendadas" className={({ isActive }) => (isActive ? styles.active : styles.link)}>
            Recomendadas
          </NavLink>
        </nav>
      </aside>

      {is_open && <div className={styles.backdrop} onClick={on_close} />}
    </>
  );
}