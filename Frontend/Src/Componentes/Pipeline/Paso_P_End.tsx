/**
 * Paso 5 del Pipeline: P_End.
 * Resumen de configuración, botón Finalizar,
 * barra de progreso y descarga.
 */

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Usar_Store_Pipeline } from "@/Stores/Store_Pipeline";

export function Paso_P_End() {
  const Store = Usar_Store_Pipeline();
  const Navigate = useNavigate();

  const [Exportando, Set_Exportando] = useState(false);
  const [Progreso, Set_Progreso] = useState(0);
  const [Completado, Set_Completado] = useState(false);
  const [Error_Msg, Set_Error] = useState<string | null>(null);
  const [Url_Descarga, Set_Url] = useState<string | null>(null);

  const Manejar_Finalizar = async () => {
    Set_Exportando(true);
    Set_Error(null);
    Set_Progreso(10);

    try {
      // Simular progreso mientras se genera.
      const Intervalo = setInterval(() => {
        Set_Progreso((P) => Math.min(P + 15, 85));
      }, 500);

      const Respuesta = await fetch("/api/export/generar", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          Formato: Store.Formato_Salida,
          Config_Estilo: {
            Estilo_Block: Store.Estilo_Block,
          },
        }),
      });

      clearInterval(Intervalo);

      if (!Respuesta.ok) {
        const Datos_Error = await Respuesta.json();
        throw new Error(Datos_Error.detail || "Error al exportar");
      }

      // Crear URL de descarga desde el blob.
      const Blob = await Respuesta.blob();
      const Url = URL.createObjectURL(Blob);

      Set_Url(Url);
      Set_Progreso(100);
      Set_Completado(true);
    } catch (Err) {
      Set_Error(
        Err instanceof Error ? Err.message : "Error desconocido"
      );
    } finally {
      Set_Exportando(false);
    }
  };

  const Manejar_Descarga = () => {
    if (!Url_Descarga) return;

    const Link = document.createElement("a");
    Link.href = Url_Descarga;
    Link.download = `${
      Store.Nombre_Archivo_Salida || "highlights"
    }.${Store.Formato_Salida}`;
    Link.click();
  };

  return (
    <div className="max-w-2xl">
      <h2 className="text-2xl font-bold mb-6">
        {Completado ? "Listo" : "Resumen"}
      </h2>

      {!Completado && (
        <>
          {/* Resumen. */}
          <div className="bg-gray-50 rounded-lg p-6 mb-6 space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-500">Highlights</span>
              <span>{Store.Highlights.length}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Formato</span>
              <span>{Store.Formato_Salida.toUpperCase()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Estilo</span>
              <span>
                {[
                  "", "Clásico", "Cita", "Tarjeta",
                  "Minimalista", "Numerado", "Destacado",
                ][Store.Estilo_Block]}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Archivo</span>
              <span>
                {Store.Nombre_Archivo_Salida || "highlights"}
                .{Store.Formato_Salida}
              </span>
            </div>
          </div>

          {/* Barra de progreso. */}
          {Exportando && (
            <div className="mb-6">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-black h-2 rounded-full transition-all duration-300"
                  style={{ width: `${Progreso}%` }}
                />
              </div>
              <p className="text-xs text-gray-400 mt-1 text-center">
                {Progreso}%
              </p>
            </div>
          )}

          {/* Error. */}
          {Error_Msg && (
            <div className="bg-red-50 text-red-700 p-3 rounded-md mb-4 text-sm">
              {Error_Msg}
            </div>
          )}

          {/* Botones. */}
          <div className="flex gap-3">
            <button
              onClick={() => Store.Establecer_Paso(3)}
              disabled={Exportando}
              className="px-6 py-3 border border-gray-300 rounded-lg text-sm hover:bg-gray-50 transition disabled:opacity-50"
            >
              Volver
            </button>
            <button
              onClick={Manejar_Finalizar}
              disabled={Exportando}
              className="flex-1 bg-black text-white py-3 rounded-lg text-sm font-medium hover:bg-gray-800 transition disabled:bg-gray-300"
            >
              {Exportando ? "Exportando..." : "Finalizar"}
            </button>
          </div>
        </>
      )}

      {Completado && (
        <div className="text-center py-8">
          <div className="text-4xl mb-4">
            &#10003;
          </div>
          <p className="text-lg mb-6">
            Exportación completada
          </p>

          <div className="flex flex-col gap-3 max-w-xs mx-auto">
            <button
              onClick={Manejar_Descarga}
              className="bg-black text-white py-3 rounded-lg text-sm font-medium hover:bg-gray-800 transition"
            >
              Descargar
            </button>
            <button
              onClick={() => Navigate("/biblioteca")}
              className="border border-gray-300 py-3 rounded-lg text-sm hover:bg-gray-50 transition"
            >
              Ir a Biblioteca
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
