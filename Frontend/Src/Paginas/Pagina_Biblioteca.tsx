/**
 * Biblioteca de highlights.
 * Dos vistas: por archivo y unificada.
 */

import { useState, useEffect } from "react";
import { Api_Fetch } from "@/Lib/Api_Cliente";

interface Archivo_Item {
  Id_Archivo: string;
  Nombre_Original: string;
  Tipo_Archivo: string;
  Cantidad_Highlights: number;
  Fecha_Subida: string;
}

interface Highlight_Item {
  Id_Highlight: string;
  Texto: string;
  Autor: string | null;
  Libro: string | null;
  Pagina: string | null;
  Tipo_Semantico: string;
}

export function Pagina_Biblioteca() {
  const [Vista, Set_Vista] = useState<"archivos" | "unificada">(
    "archivos"
  );
  const [Archivos, Set_Archivos] = useState<Archivo_Item[]>([]);
  const [Highlights, Set_Highlights] = useState<Highlight_Item[]>([]);
  const [Archivo_Sel, Set_Archivo_Sel] = useState<string | null>(null);
  const [Cargando, Set_Cargando] = useState(true);
  const [Filtro_Autor, Set_Filtro_Autor] = useState("");
  const [Filtro_Libro, Set_Filtro_Libro] = useState("");

  // Cargar archivos al montar.
  useEffect(() => {
    Cargar_Archivos();
  }, []);

  const Cargar_Archivos = async () => {
    Set_Cargando(true);
    try {
      const Datos = await Api_Fetch<{
        Archivos: Archivo_Item[];
      }>("/files/");
      Set_Archivos(Datos.Archivos);
    } catch {
      // Silenciar.
    } finally {
      Set_Cargando(false);
    }
  };

  const Cargar_Highlights = async (
    Id_Archivo?: string
  ) => {
    Set_Cargando(true);
    try {
      const Params: Record<string, string> = {
        Limite: "100",
      };
      if (Id_Archivo) {
        Params.Id_Archivo = Id_Archivo;
      }
      if (Filtro_Autor) {
        Params.Autor = Filtro_Autor;
      }
      if (Filtro_Libro) {
        Params.Libro = Filtro_Libro;
      }

      const Datos = await Api_Fetch<{
        Highlights: Highlight_Item[];
      }>("/highlights/", { Params });
      Set_Highlights(Datos.Highlights);
    } catch {
      // Silenciar.
    } finally {
      Set_Cargando(false);
    }
  };

  const Seleccionar_Archivo = (Id: string) => {
    Set_Archivo_Sel(Id);
    Cargar_Highlights(Id);
  };

  const Cambiar_A_Unificada = () => {
    Set_Vista("unificada");
    Set_Archivo_Sel(null);
    Cargar_Highlights();
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">
        Biblioteca
      </h2>

      {/* Tabs. */}
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => {
            Set_Vista("archivos");
            Set_Highlights([]);
          }}
          className={`px-4 py-2 text-sm rounded-md ${
            Vista === "archivos"
              ? "bg-black text-white"
              : "bg-gray-100 text-gray-600"
          }`}
        >
          Por archivo
        </button>
        <button
          onClick={Cambiar_A_Unificada}
          className={`px-4 py-2 text-sm rounded-md ${
            Vista === "unificada"
              ? "bg-black text-white"
              : "bg-gray-100 text-gray-600"
          }`}
        >
          Vista unificada
        </button>
      </div>

      {/* Vista por archivo. */}
      {Vista === "archivos" && !Archivo_Sel && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Archivos.map((A) => (
            <button
              key={A.Id_Archivo}
              onClick={() => Seleccionar_Archivo(A.Id_Archivo)}
              className="text-left p-4 border border-gray-200 rounded-lg hover:border-gray-400 transition"
            >
              <p className="font-medium text-sm">
                {A.Nombre_Original}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {A.Cantidad_Highlights} highlights
                &middot; {new Date(A.Fecha_Subida).toLocaleDateString()}
              </p>
            </button>
          ))}
          {Archivos.length === 0 && !Cargando && (
            <p className="text-gray-400 text-sm col-span-2">
              No hay archivos subidos todavía.
            </p>
          )}
        </div>
      )}

      {/* Vista por archivo: highlights. */}
      {Vista === "archivos" && Archivo_Sel && (
        <div>
          <button
            onClick={() => {
              Set_Archivo_Sel(null);
              Set_Highlights([]);
            }}
            className="text-sm text-gray-500 hover:underline mb-4"
          >
            &larr; Volver a archivos
          </button>
          {_Renderizar_Tabla(Highlights, Cargando)}
        </div>
      )}

      {/* Vista unificada. */}
      {Vista === "unificada" && (
        <div>
          {/* Filtros. */}
          <div className="flex gap-3 mb-4">
            <input
              type="text"
              value={Filtro_Autor}
              onChange={(e) => Set_Filtro_Autor(e.target.value)}
              placeholder="Filtrar por autor"
              className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
            <input
              type="text"
              value={Filtro_Libro}
              onChange={(e) => Set_Filtro_Libro(e.target.value)}
              placeholder="Filtrar por libro"
              className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
            <button
              onClick={() => Cargar_Highlights()}
              className="px-4 py-2 bg-gray-100 rounded-md text-sm hover:bg-gray-200"
            >
              Filtrar
            </button>
          </div>
          {_Renderizar_Tabla(Highlights, Cargando)}
        </div>
      )}
    </div>
  );
}

function _Renderizar_Tabla(
  Highlights: Highlight_Item[],
  Cargando: boolean
) {
  if (Cargando) {
    return <p className="text-gray-400 text-sm">Cargando...</p>;
  }

  if (Highlights.length === 0) {
    return <p className="text-gray-400 text-sm">No hay highlights.</p>;
  }

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden">
      <table className="w-full text-sm">
        <thead className="bg-gray-50">
          <tr>
            <th className="text-left p-2">Autor</th>
            <th className="text-left p-2">Libro</th>
            <th className="text-left p-2 w-12">Pág.</th>
            <th className="text-left p-2">Highlight</th>
          </tr>
        </thead>
        <tbody>
          {Highlights.map((H) => (
            <tr
              key={H.Id_Highlight}
              className="border-t border-gray-100 hover:bg-gray-50"
            >
              <td className="p-2 text-gray-700 max-w-[120px] truncate">
                {H.Autor || "—"}
              </td>
              <td className="p-2 text-gray-700 max-w-[150px] truncate">
                {H.Libro || "—"}
              </td>
              <td className="p-2 text-gray-500">
                {H.Pagina || "—"}
              </td>
              <td className="p-2 text-gray-600 max-w-[300px] truncate">
                {H.Texto}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
