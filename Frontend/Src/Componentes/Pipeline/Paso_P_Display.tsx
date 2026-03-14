/**
 * Paso 2 del Pipeline: P_Display.
 * Tabla paginada de highlights con operaciones
 * de ordenar, agrupar, combinar, dividir, eliminar.
 */

import { useState, useMemo } from "react";
import { Usar_Store_Pipeline } from "@/Stores/Store_Pipeline";
import { Usar_Seleccion_Tabla } from "@/Hooks/Usar_Seleccion_Tabla";

const Items_Por_Pagina = 20;

type Criterio_Orden = "autor" | "libro" | "fecha" | "original";
type Criterio_Agrupacion =
  | "ninguno" | "autor" | "libro" | "mes" | "anio";

export function Paso_P_Display() {
  const Store = Usar_Store_Pipeline();
  const Highlights = Store.Highlights;

  const [Pagina, Set_Pagina] = useState(1);
  const [Orden, Set_Orden] = useState<Criterio_Orden>("original");
  const [Agrupacion, Set_Agrupacion] =
    useState<Criterio_Agrupacion>("ninguno");

  // Ordenar highlights.
  const Highlights_Ordenados = useMemo(() => {
    const Copia = [...Highlights];
    switch (Orden) {
      case "autor":
        return Copia.sort((A, B) =>
          (A.Autor || "").localeCompare(B.Autor || "")
        );
      case "libro":
        return Copia.sort((A, B) =>
          (A.Libro || "").localeCompare(B.Libro || "")
        );
      case "fecha":
        return Copia.reverse();
      default:
        return Copia;
    }
  }, [Highlights, Orden]);

  // Paginar.
  const Total_Paginas = Math.ceil(
    Highlights_Ordenados.length / Items_Por_Pagina
  );
  const Highlights_Pagina = Highlights_Ordenados.slice(
    (Pagina - 1) * Items_Por_Pagina,
    Pagina * Items_Por_Pagina
  );

  const {
    Seleccionados,
    Manejar_Click,
    Manejar_Checkbox,
    Cantidad_Seleccionados,
    Deseleccionar_Todos,
  } = Usar_Seleccion_Tabla(Highlights_Pagina.length);

  const Manejar_Eliminar = () => {
    if (Cantidad_Seleccionados === 0) return;

    const Ids_A_Eliminar = new Set(
      [...Seleccionados].map(
        (I) => Highlights_Pagina[I]?.Id_Highlight
      )
    );

    Store.Establecer_Highlights(
      Highlights.filter(
        (H) => !Ids_A_Eliminar.has(H.Id_Highlight)
      )
    );

    Deseleccionar_Todos();
  };

  const Manejar_Proceder = () => {
    if (Store.Usar_P_Processing_Defecto) {
      Store.Establecer_Paso(
        Store.Formato_Salida === "notion" ? 4 : 5
      );
    } else {
      Store.Establecer_Paso(3);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">
        Bloques
      </h2>

      {/* Barra de herramientas. */}
      <div className="flex gap-3 mb-4 flex-wrap">
        <select
          value={Orden}
          onChange={(e) => {
            Set_Orden(e.target.value as Criterio_Orden);
            Set_Pagina(1);
          }}
          className="border border-gray-300 rounded-md px-3 py-1.5 text-sm"
        >
          <option value="original">Orden original</option>
          <option value="autor">Por autor</option>
          <option value="libro">Por libro</option>
          <option value="fecha">Por fecha</option>
        </select>

        <select
          value={Agrupacion}
          onChange={(e) =>
            Set_Agrupacion(
              e.target.value as Criterio_Agrupacion
            )
          }
          className="border border-gray-300 rounded-md px-3 py-1.5 text-sm"
        >
          <option value="ninguno">Sin agrupar</option>
          <option value="autor">Agrupar por autor</option>
          <option value="libro">Agrupar por libro</option>
          <option value="mes">Agrupar por mes</option>
          <option value="anio">Agrupar por año</option>
        </select>

        {Cantidad_Seleccionados > 0 && (
          <>
            <button
              onClick={Manejar_Eliminar}
              className="bg-red-50 text-red-700 px-3 py-1.5 rounded-md text-sm hover:bg-red-100"
            >
              Eliminar ({Cantidad_Seleccionados})
            </button>
            <button
              onClick={Deseleccionar_Todos}
              className="text-sm text-gray-500 hover:underline"
            >
              Deseleccionar
            </button>
          </>
        )}
      </div>

      {/* Tabla. */}
      <div className="border border-gray-200 rounded-lg overflow-hidden mb-4">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="w-8 p-2"></th>
              <th className="text-left p-2">Autor</th>
              <th className="text-left p-2">Libro</th>
              <th className="text-left p-2 w-16">Pág.</th>
              <th className="text-left p-2">Highlight</th>
            </tr>
          </thead>
          <tbody>
            {Highlights_Pagina.map((H, Indice) => (
              <tr
                key={H.Id_Highlight}
                onClick={(e) => Manejar_Click(Indice, e)}
                className={`border-t border-gray-100 cursor-pointer ${
                  Seleccionados.has(Indice)
                    ? "bg-blue-50"
                    : "hover:bg-gray-50"
                }`}
              >
                <td className="p-2 text-center">
                  <input
                    type="checkbox"
                    checked={Seleccionados.has(Indice)}
                    onChange={() => Manejar_Checkbox(Indice)}
                    onClick={(e) => e.stopPropagation()}
                  />
                </td>
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

      {/* Paginación. */}
      <div className="flex items-center justify-between mb-6">
        <span className="text-sm text-gray-500">
          {Highlights.length} highlights
        </span>
        <div className="flex gap-2">
          <button
            onClick={() => Set_Pagina((P) => Math.max(1, P - 1))}
            disabled={Pagina === 1}
            className="px-3 py-1 text-sm border border-gray-300 rounded-md disabled:opacity-30"
          >
            Anterior
          </button>
          <span className="px-3 py-1 text-sm">
            {Pagina} / {Total_Paginas}
          </span>
          <button
            onClick={() =>
              Set_Pagina((P) => Math.min(Total_Paginas, P + 1))
            }
            disabled={Pagina === Total_Paginas}
            className="px-3 py-1 text-sm border border-gray-300 rounded-md disabled:opacity-30"
          >
            Siguiente
          </button>
        </div>
      </div>

      {/* Botón proceder. */}
      <button
        onClick={Manejar_Proceder}
        className="w-full bg-black text-white py-3 rounded-lg text-sm font-medium hover:bg-gray-800 transition"
      >
        Proceder con el orden final
      </button>
    </div>
  );
}
