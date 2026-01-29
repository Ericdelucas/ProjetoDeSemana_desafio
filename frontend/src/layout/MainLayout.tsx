import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { useMemo, useState } from "react";

import styles from "./MainLayout.module.css";
import { TopBar } from "../shared/components/TopBar/TopBar";
import { SideNav } from "../shared/components/SideNav/SideNav";
import { ChatWidget } from "../shared/components/ChatWidget/ChatWidget";

export function MainLayout() {
  const [is_menu_open, set_is_menu_open] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const title = useMemo(() => {
    if (location.pathname.startsWith("/unidades")) return "Unidades";
    if (location.pathname.startsWith("/triagem")) return "Triagem rápida";
    if (location.pathname.startsWith("/recomendadas")) return "Unidades recomendadas";
    return "SmartSaúde SUS";
  }, [location.pathname]);

  const can_go_back = location.pathname !== "/";

  function handle_back() {
    if (can_go_back) navigate(-1);
  }

  return (
    <div className={styles.shell}>
      <TopBar
        title={title}
        is_menu_open={is_menu_open}
        on_toggle_menu={() => set_is_menu_open((v) => !v)}
        show_back={can_go_back}
        on_back={handle_back}
      />

      <div className={styles.body}>
        <SideNav is_open={is_menu_open} on_close={() => set_is_menu_open(false)} />

        <main className={styles.content}>
          <Outlet />
        </main>
      </div>

      <ChatWidget />
    </div>
  );
}