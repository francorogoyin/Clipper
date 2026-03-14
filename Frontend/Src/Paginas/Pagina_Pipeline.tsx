/**
 * Página del Pipeline: wizard de 5 pasos.
 * Renderiza el paso actual según el store.
 */

import { Usar_Store_Pipeline } from "@/Stores/Store_Pipeline";
import { Paso_P_Start } from "@/Componentes/Pipeline/Paso_P_Start";
import { Paso_P_Display } from "@/Componentes/Pipeline/Paso_P_Display";
import { Paso_P_Processing } from "@/Componentes/Pipeline/Paso_P_Processing";
import { Paso_P_End } from "@/Componentes/Pipeline/Paso_P_End";

const Nombres_Pasos = [
  "Inicio",
  "Bloques",
  "Procesamiento",
  "Notion",
  "Final",
];

export function Pagina_Pipeline() {
  const { Paso_Actual } = Usar_Store_Pipeline();

  return (
    <div>
      {/* Barra de progreso del wizard. */}
      <div className="flex gap-2 mb-8">
        {Nombres_Pasos.map((Nombre, Indice) => (
          <div
            key={Nombre}
            className={`flex-1 text-center py-2 text-sm rounded-md ${
              Indice + 1 === Paso_Actual
                ? "bg-black text-white"
                : Indice + 1 < Paso_Actual
                ? "bg-gray-200 text-gray-600"
                : "bg-gray-50 text-gray-400"
            }`}
          >
            {Indice + 1}. {Nombre}
          </div>
        ))}
      </div>

      {/* Paso actual. */}
      {Paso_Actual === 1 && <Paso_P_Start />}
      {Paso_Actual === 2 && <Paso_P_Display />}
      {Paso_Actual === 3 && <Paso_P_Processing />}
      {Paso_Actual === 4 && (
        <div className="text-gray-500">
          P_Notion — próximamente
        </div>
      )}
      {Paso_Actual === 5 && <Paso_P_End />}
    </div>
  );
}
