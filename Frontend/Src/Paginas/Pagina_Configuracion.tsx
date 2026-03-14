/**
 * Página de configuración de cuenta.
 * Perfil, suscripción, apariencia, exportación,
 * reglas de marcas, Notion, confirmaciones.
 */

import { useState } from "react";
import { Usar_Store_Auth } from "@/Stores/Store_Auth";

interface Regla_Marca {
  Marca: string;
  Tipo_Semantico: string;
}

const Reglas_Default: Regla_Marca[] = [
  { Marca: "###", Tipo_Semantico: "heading" },
  { Marca: ">", Tipo_Semantico: "quote" },
  { Marca: "!", Tipo_Semantico: "callout" },
  { Marca: "~", Tipo_Semantico: "toggle" },
];

export function Pagina_Configuracion() {
  const { Usuario } = Usar_Store_Auth();

  const [Seccion, Set_Seccion] = useState("perfil");
  const [Tema, Set_Tema] = useState("claro");
  const [Formato_Pref, Set_Formato] = useState("pdf");
  const [Reglas, Set_Reglas] = useState<Regla_Marca[]>(
    Reglas_Default
  );
  const [Nueva_Marca, Set_Nueva_Marca] = useState("");
  const [Nuevo_Tipo, Set_Nuevo_Tipo] = useState("paragraph");

  const Secciones = [
    { Id: "perfil", Etiqueta: "Perfil" },
    { Id: "suscripcion", Etiqueta: "Suscripción" },
    { Id: "apariencia", Etiqueta: "Apariencia" },
    { Id: "exportacion", Etiqueta: "Exportación" },
    { Id: "reglas", Etiqueta: "Reglas de marcas" },
    { Id: "notion", Etiqueta: "Notion" },
    { Id: "confirmaciones", Etiqueta: "Confirmaciones" },
  ];

  const Agregar_Regla = () => {
    if (!Nueva_Marca) return;
    Set_Reglas([
      ...Reglas,
      { Marca: Nueva_Marca, Tipo_Semantico: Nuevo_Tipo },
    ]);
    Set_Nueva_Marca("");
    Set_Nuevo_Tipo("paragraph");
  };

  const Eliminar_Regla = (Indice: number) => {
    Set_Reglas(Reglas.filter((_, I) => I !== Indice));
  };

  return (
    <div className="flex gap-8">
      {/* Sidebar de secciones. */}
      <nav className="w-44 space-y-1">
        {Secciones.map((S) => (
          <button
            key={S.Id}
            onClick={() => Set_Seccion(S.Id)}
            className={`w-full text-left px-3 py-2 rounded-md text-sm ${
              Seccion === S.Id
                ? "bg-gray-100 font-medium"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            {S.Etiqueta}
          </button>
        ))}
      </nav>

      {/* Contenido. */}
      <div className="flex-1 max-w-xl">
        {Seccion === "perfil" && (
          <div className="space-y-4">
            <h3 className="text-lg font-bold">Perfil</h3>
            <div>
              <label className="block text-sm text-gray-500 mb-1">Email</label>
              <p className="text-sm">{Usuario?.Email || "—"}</p>
            </div>
            <div>
              <label className="block text-sm text-gray-500 mb-1">Nickname</label>
              <input
                type="text"
                defaultValue={Usuario?.Nickname || ""}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
              />
            </div>
          </div>
        )}

        {Seccion === "suscripcion" && (
          <div className="space-y-4">
            <h3 className="text-lg font-bold">Suscripción</h3>
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="font-medium">
                Plan {Usuario?.Tipo_Suscripcion === "premium" ? "Premium" : "Free"}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                {Usuario?.Tipo_Suscripcion === "premium"
                  ? "Highlights ilimitados"
                  : "Hasta 50 highlights"}
              </p>
            </div>
            {Usuario?.Tipo_Suscripcion !== "premium" && (
              <button className="bg-black text-white px-6 py-2 rounded-lg text-sm">
                Upgrade a Premium
              </button>
            )}
          </div>
        )}

        {Seccion === "apariencia" && (
          <div className="space-y-4">
            <h3 className="text-lg font-bold">Apariencia</h3>
            <div>
              <label className="block text-sm text-gray-500 mb-1">Tema</label>
              <select
                value={Tema}
                onChange={(e) => Set_Tema(e.target.value)}
                className="border border-gray-300 rounded-md px-3 py-2 text-sm"
              >
                <option value="claro">Claro</option>
                <option value="oscuro">Oscuro</option>
              </select>
            </div>
          </div>
        )}

        {Seccion === "exportacion" && (
          <div className="space-y-4">
            <h3 className="text-lg font-bold">Exportación por defecto</h3>
            <div>
              <label className="block text-sm text-gray-500 mb-1">
                Formato preferido
              </label>
              <select
                value={Formato_Pref}
                onChange={(e) => Set_Formato(e.target.value)}
                className="border border-gray-300 rounded-md px-3 py-2 text-sm"
              >
                {["pdf", "docx", "doc", "odt", "csv", "xlsx", "xls", "txt", "notion", "obsidian"].map(
                  (F) => (
                    <option key={F} value={F}>{F.toUpperCase()}</option>
                  )
                )}
              </select>
            </div>
          </div>
        )}

        {Seccion === "reglas" && (
          <div className="space-y-4">
            <h3 className="text-lg font-bold">Reglas de marcas</h3>
            <p className="text-sm text-gray-500">
              Definí qué prefijo en un DOCX se convierte en qué tipo semántico.
            </p>

            {/* Tabla de reglas. */}
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left p-2">Marca</th>
                    <th className="text-left p-2">Tipo</th>
                    <th className="w-16 p-2"></th>
                  </tr>
                </thead>
                <tbody>
                  {Reglas.map((R, I) => (
                    <tr key={I} className="border-t border-gray-100">
                      <td className="p-2 font-mono">{R.Marca}</td>
                      <td className="p-2">{R.Tipo_Semantico}</td>
                      <td className="p-2">
                        <button
                          onClick={() => Eliminar_Regla(I)}
                          className="text-red-500 text-xs hover:underline"
                        >
                          Eliminar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Agregar regla. */}
            <div className="flex gap-2">
              <input
                type="text"
                value={Nueva_Marca}
                onChange={(e) => Set_Nueva_Marca(e.target.value)}
                placeholder="Marca"
                className="w-20 border border-gray-300 rounded-md px-3 py-2 text-sm font-mono"
              />
              <select
                value={Nuevo_Tipo}
                onChange={(e) => Set_Nuevo_Tipo(e.target.value)}
                className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm"
              >
                <option value="paragraph">paragraph</option>
                <option value="heading">heading</option>
                <option value="callout">callout</option>
                <option value="quote">quote</option>
                <option value="toggle">toggle</option>
              </select>
              <button
                onClick={Agregar_Regla}
                className="px-4 py-2 bg-black text-white rounded-md text-sm"
              >
                Agregar
              </button>
            </div>

            <button
              onClick={() => Set_Reglas(Reglas_Default)}
              className="text-sm text-gray-500 hover:underline"
            >
              Resetear a predefinidas
            </button>
          </div>
        )}

        {Seccion === "notion" && (
          <div className="space-y-4">
            <h3 className="text-lg font-bold">Notion</h3>
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm">
                Estado de conexión: placeholder
              </p>
            </div>
            <button className="text-sm text-red-600 hover:underline">
              Desconectar Notion
            </button>
          </div>
        )}

        {Seccion === "confirmaciones" && (
          <div className="space-y-4">
            <h3 className="text-lg font-bold">Confirmaciones</h3>
            <p className="text-sm text-gray-500">
              Reactivá los diálogos de confirmación que silenciaste.
            </p>
            <button className="px-4 py-2 border border-gray-300 rounded-md text-sm hover:bg-gray-50">
              Resetear todas las confirmaciones
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
