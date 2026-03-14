/**
 * Layout para usuarios autenticados.
 * Sidebar con navegación + contenido principal.
 */

import { Link, Outlet, useLocation } from "react-router-dom";
import { Usar_Store_Auth } from "@/Stores/Store_Auth";

const Enlaces_Nav = [
  { Ruta: "/pipeline", Etiqueta: "Pipeline" },
  { Ruta: "/biblioteca", Etiqueta: "Biblioteca" },
  { Ruta: "/configuracion", Etiqueta: "Config" },
];

export function Layout_Privado() {
  const Location = useLocation();
  const { Usuario, Cerrar_Sesion } = Usar_Store_Auth();

  return (
    <div className="flex min-h-screen">
      {/* Sidebar. */}
      <aside className="w-56 bg-gray-50 border-r border-gray-200 p-4 flex flex-col">
        <h2 className="text-lg font-bold mb-6">
          Highlighter
        </h2>

        <nav className="flex flex-col gap-1 flex-1">
          {Enlaces_Nav.map((E) => (
            <Link
              key={E.Ruta}
              to={E.Ruta}
              className={`px-3 py-2 rounded-md text-sm ${
                Location.pathname.startsWith(E.Ruta)
                  ? "bg-black text-white"
                  : "text-gray-700 hover:bg-gray-100"
              }`}
            >
              {E.Etiqueta}
            </Link>
          ))}
        </nav>

        <div className="mt-auto pt-4 border-t border-gray-200">
          <p className="text-xs text-gray-500 mb-2">
            {Usuario?.Email}
          </p>
          <button
            onClick={Cerrar_Sesion}
            className="text-xs text-red-600 hover:underline"
          >
            Cerrar sesión
          </button>
        </div>
      </aside>

      {/* Contenido principal. */}
      <main className="flex-1 p-8">
        <Outlet />
      </main>
    </div>
  );
}
