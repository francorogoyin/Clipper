/**
 * Paso 4 del Pipeline: P_Notion.
 * Sub-wizard de 4 pasos: conexión, matcheo,
 * posición de paste, formato de N_Block.
 */

import { useState } from "react";
import { Usar_Store_Pipeline } from "@/Stores/Store_Pipeline";
import { Api_Fetch } from "@/Lib/Api_Cliente";

interface N_Match_Item {
  Id_Clipping: string;
  N_Page_Id: string;
  N_Page_Titulo: string;
  Estado: "verde" | "rojo";
}

interface Pagina_Notion {
  Id: string;
  Titulo: string;
  Icono: string;
}

export function Paso_P_Notion() {
  const Store = Usar_Store_Pipeline();

  const [Sub_Paso, Set_Sub_Paso] = useState(1);
  const [Conectado, Set_Conectado] = useState(false);
  const [Matches, Set_Matches] = useState<N_Match_Item[]>([]);
  const [Paginas, Set_Paginas] = useState<Pagina_Notion[]>([]);
  const [Busqueda, Set_Busqueda] = useState("");
  const [Posicion, Set_Posicion] = useState("final");
  const [Tipo_Block, Set_Tipo_Block] = useState("paragraph");
  const [Emoji_Block, Set_Emoji_Block] = useState("");
  const [Cargando, Set_Cargando] = useState(false);

  // Sub-paso 1: Conexión.
  const Verificar_Conexion = async () => {
    Set_Cargando(true);
    try {
      await Api_Fetch("/notion/config");
      Set_Conectado(true);
      Set_Sub_Paso(2);
    } catch {
      window.location.href = "/api/auth/notion/login";
    } finally {
      Set_Cargando(false);
    }
  };

  // Sub-paso 2: Matcheo.
  const Buscar_Paginas = async () => {
    Set_Cargando(true);
    try {
      const Resultado = await Api_Fetch<{
        Paginas: Pagina_Notion[];
      }>("/notion/paginas", {
        Params: Busqueda
          ? { Busqueda: Busqueda }
          : {},
      });
      Set_Paginas(Resultado.Paginas);
    } catch {
      // Silenciar error de búsqueda.
    } finally {
      Set_Cargando(false);
    }
  };

  const Asignar_Match = async (
    Pagina: Pagina_Notion
  ) => {
    const Nuevo_Match: N_Match_Item = {
      Id_Clipping: "pendiente",
      N_Page_Id: Pagina.Id,
      N_Page_Titulo: Pagina.Titulo,
      Estado: "verde",
    };

    Set_Matches((Prev) => [...Prev, Nuevo_Match]);
  };

  const Sub_Paso_Nombres = [
    "",
    "Conexión",
    "Matcheo",
    "Posición",
    "Formato",
  ];

  return (
    <div className="max-w-2xl">
      <h2 className="text-2xl font-bold mb-2">
        Notion
      </h2>

      {/* Barra de sub-pasos. */}
      <div className="flex gap-2 mb-6">
        {[1, 2, 3, 4].map((N) => (
          <div
            key={N}
            className={`flex-1 text-center py-1.5 text-xs rounded-md ${
              N === Sub_Paso
                ? "bg-black text-white"
                : N < Sub_Paso
                ? "bg-gray-200 text-gray-600"
                : "bg-gray-50 text-gray-400"
            }`}
          >
            {Sub_Paso_Nombres[N]}
          </div>
        ))}
      </div>

      {/* Sub-paso 1: Conexión. */}
      {Sub_Paso === 1 && (
        <div className="space-y-4">
          <p className="text-sm text-gray-600">
            Conectá tu cuenta de Notion para exportar
            highlights directamente a tus páginas.
          </p>
          <button
            onClick={Verificar_Conexion}
            disabled={Cargando}
            className="w-full bg-black text-white py-3 rounded-lg text-sm font-medium hover:bg-gray-800 transition"
          >
            {Cargando
              ? "Verificando..."
              : Conectado
              ? "Conectado — Siguiente"
              : "Conectar con Notion"}
          </button>
        </div>
      )}

      {/* Sub-paso 2: Matcheo. */}
      {Sub_Paso === 2 && (
        <div className="space-y-4">
          <p className="text-sm text-gray-600 mb-2">
            Buscá y seleccioná las páginas de Notion
            donde querés pegar tus highlights.
          </p>

          {/* Buscador. */}
          <div className="flex gap-2">
            <input
              type="text"
              value={Busqueda}
              onChange={(e) => Set_Busqueda(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && Buscar_Paginas()}
              placeholder="Buscar páginas..."
              className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
            <button
              onClick={Buscar_Paginas}
              disabled={Cargando}
              className="px-4 py-2 bg-gray-100 rounded-md text-sm hover:bg-gray-200"
            >
              Buscar
            </button>
          </div>

          {/* Lista de páginas. */}
          {Paginas.length > 0 && (
            <div className="border border-gray-200 rounded-lg max-h-60 overflow-y-auto">
              {Paginas.map((P) => (
                <button
                  key={P.Id}
                  onClick={() => Asignar_Match(P)}
                  className="w-full text-left px-4 py-2.5 text-sm hover:bg-gray-50 border-b border-gray-100 last:border-b-0"
                >
                  {P.Icono && <span className="mr-2">{P.Icono}</span>}
                  {P.Titulo || "Sin título"}
                </button>
              ))}
            </div>
          )}

          {/* Matches asignados. */}
          {Matches.length > 0 && (
            <div className="space-y-2">
              <p className="text-xs text-gray-400">
                Matches asignados
              </p>
              {Matches.map((M, I) => (
                <div
                  key={I}
                  className="flex items-center gap-2 p-2 rounded-md bg-green-50 text-sm"
                >
                  <span className="w-2 h-2 rounded-full bg-green-500" />
                  {M.N_Page_Titulo}
                </div>
              ))}
            </div>
          )}

          <button
            onClick={() => Set_Sub_Paso(3)}
            className="w-full bg-black text-white py-3 rounded-lg text-sm font-medium hover:bg-gray-800 transition"
          >
            Siguiente
          </button>
        </div>
      )}

      {/* Sub-paso 3: Posición de paste. */}
      {Sub_Paso === 3 && (
        <div className="space-y-4">
          <p className="text-sm text-gray-600">
            Elegí dónde insertar los highlights
            dentro de cada página.
          </p>

          <div className="space-y-2">
            {["final", "principio", "especifico"].map((P) => (
              <label key={P} className="flex items-center gap-3 p-3 rounded-md border border-gray-200 cursor-pointer hover:bg-gray-50">
                <input
                  type="radio"
                  name="posicion"
                  value={P}
                  checked={Posicion === P}
                  onChange={(e) => Set_Posicion(e.target.value)}
                />
                <span className="text-sm">
                  {P === "final" && "Al final de la página"}
                  {P === "principio" && "Al principio de la página"}
                  {P === "especifico" && "En un bloque específico"}
                </span>
              </label>
            ))}
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => Set_Sub_Paso(2)}
              className="px-6 py-3 border border-gray-300 rounded-lg text-sm hover:bg-gray-50"
            >
              Volver
            </button>
            <button
              onClick={() => Set_Sub_Paso(4)}
              className="flex-1 bg-black text-white py-3 rounded-lg text-sm font-medium hover:bg-gray-800 transition"
            >
              Siguiente
            </button>
          </div>
        </div>
      )}

      {/* Sub-paso 4: Formato del N_Block. */}
      {Sub_Paso === 4 && (
        <div className="space-y-4">
          <p className="text-sm text-gray-600">
            Configurá cómo se ven los highlights
            en Notion.
          </p>

          <div>
            <label className="block text-sm font-medium mb-1">
              Tipo de bloque
            </label>
            <select
              value={Tipo_Block}
              onChange={(e) => Set_Tipo_Block(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
            >
              <option value="paragraph">Párrafo</option>
              <option value="callout">Callout</option>
              <option value="quote">Cita</option>
            </select>
          </div>

          {Tipo_Block === "callout" && (
            <div>
              <label className="block text-sm font-medium mb-1">
                Emoji del callout
              </label>
              <input
                type="text"
                value={Emoji_Block}
                onChange={(e) => Set_Emoji_Block(e.target.value)}
                placeholder="📚"
                className="w-16 border border-gray-300 rounded-md px-3 py-2 text-sm text-center"
                maxLength={2}
              />
            </div>
          )}

          {/* Preview del N_Block. */}
          <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-xs text-gray-400 mb-2">
              Vista previa
            </p>
            <div className={`text-sm ${
              Tipo_Block === "quote"
                ? "border-l-4 border-gray-300 pl-3 italic"
                : Tipo_Block === "callout"
                ? "bg-gray-100 p-3 rounded-md"
                : ""
            }`}>
              {Tipo_Block === "callout" && Emoji_Block && (
                <span className="mr-2">{Emoji_Block}</span>
              )}
              {Store.Highlights[0]?.Texto?.substring(0, 80) || "Texto de ejemplo..."}
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => Set_Sub_Paso(3)}
              className="px-6 py-3 border border-gray-300 rounded-lg text-sm hover:bg-gray-50"
            >
              Volver
            </button>
            <button
              onClick={() => Store.Establecer_Paso(5)}
              className="flex-1 bg-black text-white py-3 rounded-lg text-sm font-medium hover:bg-gray-800 transition"
            >
              Aceptar destinos
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
