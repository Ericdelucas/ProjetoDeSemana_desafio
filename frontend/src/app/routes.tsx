import { createBrowserRouter } from "react-router-dom";
import { MainLayout } from "../layout/MainLayout";

import { HomePage } from "../pages/Home/HomePage";
import { UnidadesPage } from "../pages/Unidades/UnidadesPage";
import { TriagemPage } from "../pages/Triagem/TriagemPage";
import { UnidadesRecomendadasPage } from "../pages/UnidadesRecomendadas/UnidadesRecomendadasPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "unidades", element: <UnidadesPage /> },
      { path: "triagem", element: <TriagemPage /> },
      { path: "recomendadas", element: <UnidadesRecomendadasPage /> },
    ],
  },
]);