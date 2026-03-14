/**
 * Paso 3 del Pipeline: P_Processing.
 * Checkboxes de procesamiento de texto con
 * preview en tiempo real.
 */

import { useState, useEffect, useRef } from "react";
import { Usar_Store_Pipeline } from "@/Stores/Store_Pipeline";
import { Api_Fetch } from "@/Lib/Api_Cliente";

interface Config_Processing {
  Primera_Letra_Mayuscula: boolean;
  Borrar_Caracteres: boolean;
  Caracteres_A_Borrar: string;
  Primer_Caracter_Letra_Mayus: boolean;
  Agregar_Signos_Faltantes: boolean;
}

const Config_Default: Config_Processing = {
  Primera_Letra_Mayuscula: true,
  Borrar_Caracteres: false,
  Caracteres_A_Borrar: "",
  Primer_Caracter_Letra_Mayus: true,
  Agregar_Signos_Faltantes: true,
};

export function Paso_P_Processing() {
  const Store = Usar_Store_Pipeline();

  const [Config, Set_Config] = useState<Config_Processing>(
    Config_Default
  );
  const [Preview, Set_Preview] = useState<string>("");
  const Timer_Ref = useRef<ReturnType<typeof setTimeout>>();

  // Texto de ejemplo para preview.
  const Texto_Ejemplo = Store.Highlights[0]?.Texto || "Texto de ejemplo.";

  // Preview en tiempo real con debounce 300ms.
  useEffect(() => {
    if (Timer_Ref.current) {
      clearTimeout(Timer_Ref.current);
    }

    Timer_Ref.current = setTimeout(async () => {
      try {
        const Resultado = await Api_Fetch<{
          Texto_Procesado: string;
        }>("/processing/preview", {
          Metodo: "POST",
          Cuerpo: {
            Texto: Texto_Ejemplo,
            ...Config,
          },
        });
        Set_Preview(Resultado.Texto_Procesado);
      } catch {
        Set_Preview(Texto_Ejemplo);
      }
    }, 300);

    return () => {
      if (Timer_Ref.current) {
        clearTimeout(Timer_Ref.current);
      }
    };
  }, [Config, Texto_Ejemplo]);

  const Manejar_Aceptar = () => {
    Store.Establecer_Paso(
      Store.Formato_Salida === "notion" ? 4 : 5
    );
  };

  return (
    <div className="max-w-2xl">
      <h2 className="text-2xl font-bold mb-6">
        Procesamiento de texto
      </h2>

      {/* Preview en tiempo real. */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
        <p className="text-xs text-gray-400 mb-2">
          Vista previa
        </p>
        <p className="text-sm text-gray-800">
          {Preview || Texto_Ejemplo}
        </p>
      </div>

      {/* Checkboxes. */}
      <div className="space-y-4 mb-8">
        <label className="flex items-center gap-3">
          <input
            type="checkbox"
            checked={Config.Primera_Letra_Mayuscula}
            onChange={(e) =>
              Set_Config({
                ...Config,
                Primera_Letra_Mayuscula: e.target.checked,
              })
            }
          />
          <span className="text-sm">
            Cambiar primera letra a mayúscula
          </span>
        </label>

        <label className="flex items-center gap-3">
          <input
            type="checkbox"
            checked={Config.Primer_Caracter_Letra_Mayus}
            onChange={(e) =>
              Set_Config({
                ...Config,
                Primer_Caracter_Letra_Mayus: e.target.checked,
              })
            }
          />
          <span className="text-sm">
            Cambiar primer carácter "Letra" a mayúscula
          </span>
        </label>

        <label className="flex items-center gap-3">
          <input
            type="checkbox"
            checked={Config.Agregar_Signos_Faltantes}
            onChange={(e) =>
              Set_Config({
                ...Config,
                Agregar_Signos_Faltantes: e.target.checked,
              })
            }
          />
          <span className="text-sm">
            Agregar signos faltantes (', ", «, (, ¿, ¡)
          </span>
        </label>

        <div>
          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={Config.Borrar_Caracteres}
              onChange={(e) =>
                Set_Config({
                  ...Config,
                  Borrar_Caracteres: e.target.checked,
                })
              }
            />
            <span className="text-sm">
              Borrar caracteres específicos
            </span>
          </label>
          {Config.Borrar_Caracteres && (
            <input
              type="text"
              value={Config.Caracteres_A_Borrar}
              onChange={(e) =>
                Set_Config({
                  ...Config,
                  Caracteres_A_Borrar: e.target.value,
                })
              }
              placeholder="Caracteres a borrar"
              className="mt-2 ml-8 border border-gray-300 rounded-md px-3 py-1.5 text-sm w-48"
            />
          )}
        </div>
      </div>

      {/* Acciones. */}
      <div className="flex gap-3">
        <button
          onClick={() => Store.Establecer_Paso(2)}
          className="px-6 py-3 border border-gray-300 rounded-lg text-sm hover:bg-gray-50 transition"
        >
          Volver
        </button>
        <button
          onClick={Manejar_Aceptar}
          className="flex-1 bg-black text-white py-3 rounded-lg text-sm font-medium hover:bg-gray-800 transition"
        >
          Acepto el procesamiento
        </button>
      </div>
    </div>
  );
}
