/**
 * Componente raíz de la aplicación.
 * Define las rutas públicas y privadas.
 */

import { Routes, Route } from "react-router-dom";
import { Pagina_Landing } from "@/Paginas/Pagina_Landing";
import { Pagina_Login } from "@/Paginas/Pagina_Login";
import { Pagina_Pipeline } from "@/Paginas/Pagina_Pipeline";
import { Layout_Privado } from "@/Componentes/Layout_Privado";

export function App() {
  return (
    <Routes>
      {/* Rutas públicas. */}
      <Route path="/" element={<Pagina_Landing />} />
      <Route path="/login" element={<Pagina_Login />} />

      {/* Rutas privadas (con sidebar). */}
      <Route element={<Layout_Privado />}>
        <Route path="/pipeline" element={<Pagina_Pipeline />} />
        <Route
          path="/biblioteca"
          element={
            <div className="text-gray-500">
              Biblioteca — próximamente
            </div>
          }
        />
        <Route
          path="/configuracion"
          element={
            <div className="text-gray-500">
              Configuración — próximamente
            </div>
          }
        />
      </Route>
    </Routes>
  );
}
