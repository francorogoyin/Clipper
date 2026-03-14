/**
 * Paso 1 del Pipeline: P_Start.
 * Subir archivo, elegir formato, configurar
 * estilos y partición.
 */

import { useState, useCallback } from "react";
import { Usar_Store_Pipeline } from "@/Stores/Store_Pipeline";
import { Api_Upload } from "@/Lib/Api_Cliente";

const Formatos_Salida = [
  "pdf", "docx", "doc", "odt", "csv",
  "xlsx", "xls", "txt", "notion", "obsidian",
];

const Formatos_Con_Estilo = [
  "pdf", "docx", "doc", "odt",
];

const Criterios_Particion = [
  "Author", "Book", "Year", "Month", "Day",
];

interface Respuesta_Upload {
  Id_Archivo: string;
  Cantidad_Highlights: number;
  Highlights: Array<{
    Id_Highlight: string;
    Texto: string;
    Autor: string | null;
    Libro: string | null;
    Pagina: string | null;
    Tipo_Semantico: string;
  }>;
}

export function Paso_P_Start() {
  const Store = Usar_Store_Pipeline();

  const [Archivo, Set_Archivo] = useState<File | null>(null);
  const [Cargando, Set_Cargando] = useState(false);
  const [Error_Msg, Set_Error] = useState<string | null>(null);
  const [Separar, Set_Separar] = useState(false);

  const Formato_Soporta_Estilo = Formatos_Con_Estilo.includes(
    Store.Formato_Salida
  );

  const Manejar_Drop = useCallback(
    (Evento: React.DragEvent) => {
      Evento.preventDefault();
      const Archivos = Evento.dataTransfer.files;
      if (Archivos.length > 0) {
        Set_Archivo(Archivos[0]);
        Set_Error(null);
      }
    },
    []
  );

  const Manejar_Seleccion = useCallback(
    (Evento: React.ChangeEvent<HTMLInputElement>) => {
      const Archivos = Evento.target.files;
      if (Archivos && Archivos.length > 0) {
        Set_Archivo(Archivos[0]);
        Set_Error(null);
      }
    },
    []
  );

  const Manejar_Get_Highlights = async () => {
    if (!Archivo) {
      Set_Error("Seleccioná un archivo primero.");
      return;
    }

    Set_Cargando(true);
    Set_Error(null);

    try {
      const Resultado = await Api_Upload<Respuesta_Upload>(
        "/files/upload",
        Archivo
      );

      Store.Establecer_Archivo(Resultado.Id_Archivo);
      Store.Establecer_Highlights(Resultado.Highlights);

      if (!Store.Nombre_Archivo_Salida) {
        const Nombre_Base = Archivo.name.replace(
          /\.[^.]+$/, ""
        );
        Store.Establecer_Nombre(Nombre_Base);
      }

      // Avanzar al siguiente paso.
      if (Store.Usar_P_Display_Defecto) {
        if (Store.Usar_P_Processing_Defecto) {
          Store.Establecer_Paso(
            Store.Formato_Salida === "notion" ? 4 : 5
          );
        } else {
          Store.Establecer_Paso(3);
        }
      } else {
        Store.Establecer_Paso(2);
      }
    } catch (Err) {
      Set_Error(
        Err instanceof Error
          ? Err.message
          : "Error al subir el archivo."
      );
    } finally {
      Set_Cargando(false);
    }
  };

  return (
    <div className="max-w-2xl">
      <h2 className="text-2xl font-bold mb-6">
        Subí tu archivo
      </h2>

      {/* Zona de drop. */}
      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={Manejar_Drop}
        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6 hover:border-gray-400 transition cursor-pointer"
        onClick={() =>
          document.getElementById("Input_Archivo")?.click()
        }
      >
        <input
          id="Input_Archivo"
          type="file"
          accept=".txt,.docx"
          onChange={Manejar_Seleccion}
          className="hidden"
        />
        {Archivo ? (
          <p className="text-gray-700">
            {Archivo.name} ({(Archivo.size / 1024).toFixed(0)} KB)
          </p>
        ) : (
          <p className="text-gray-400">
            Arrastrá tu archivo .txt o .docx acá,
            o hacé click para seleccionar.
          </p>
        )}
      </div>

      {/* Error. */}
      {Error_Msg && (
        <div className="bg-red-50 text-red-700 p-3 rounded-md mb-4 text-sm">
          {Error_Msg}
        </div>
      )}

      {/* Formato de salida. */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">
          Formato de salida
        </label>
        <select
          value={Store.Formato_Salida}
          onChange={(e) => Store.Establecer_Formato(e.target.value)}
          className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
        >
          {Formatos_Salida.map((F) => (
            <option key={F} value={F}>
              {F.toUpperCase()}
            </option>
          ))}
        </select>
      </div>

      {/* Partición. */}
      <div className="mb-4">
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={Separar}
            onChange={(e) => {
              Set_Separar(e.target.checked);
              if (!e.target.checked) {
                Store.Establecer_Particion(null);
              }
            }}
          />
          Guardar en archivos separados
        </label>
        {Separar && (
          <select
            value={Store.Criterio_Particion || ""}
            onChange={(e) =>
              Store.Establecer_Particion(e.target.value)
            }
            className="mt-2 w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
          >
            <option value="">Elegir criterio</option>
            {Criterios_Particion.map((C) => (
              <option key={C} value={C}>{C}</option>
            ))}
          </select>
        )}
      </div>

      {/* Estilo de Block (condicional). */}
      {Formato_Soporta_Estilo && (
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">
            Estilo de Block
          </label>
          <div className="grid grid-cols-3 gap-2">
            {[1, 2, 3, 4, 5, 6].map((N) => {
              const Nombres = [
                "", "Clásico", "Cita", "Tarjeta",
                "Minimalista", "Numerado", "Destacado",
              ];
              return (
                <button
                  key={N}
                  onClick={() => Store.Establecer_Estilo(N)}
                  className={`p-2 text-xs rounded-md border ${
                    Store.Estilo_Block === N
                      ? "border-black bg-gray-100"
                      : "border-gray-200 hover:border-gray-300"
                  }`}
                >
                  {Nombres[N]}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Nombre del archivo. */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">
          Nombre del archivo de salida
        </label>
        <input
          type="text"
          value={Store.Nombre_Archivo_Salida}
          onChange={(e) =>
            Store.Establecer_Nombre(e.target.value)
          }
          placeholder="Mi archivo"
          className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
        />
      </div>

      {/* Checkboxes defaults. */}
      <div className="mb-6 flex flex-col gap-2">
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={Store.Usar_P_Display_Defecto}
            onChange={(e) =>
              Store.Establecer_Display_Defecto(e.target.checked)
            }
          />
          Usar configuración de P_Display por defecto
        </label>
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={Store.Usar_P_Processing_Defecto}
            onChange={(e) =>
              Store.Establecer_Processing_Defecto(e.target.checked)
            }
          />
          Usar configuración de P_Processing por defecto
        </label>
      </div>

      {/* Botón principal. */}
      <button
        onClick={Manejar_Get_Highlights}
        disabled={!Archivo || Cargando}
        className="w-full bg-black text-white py-3 rounded-lg text-sm font-medium hover:bg-gray-800 transition disabled:bg-gray-300 disabled:cursor-not-allowed"
      >
        {Cargando ? "Procesando..." : "Get Highlights"}
      </button>
    </div>
  );
}
