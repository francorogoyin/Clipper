/**
 * Store de Zustand para el estado del wizard
 * del pipeline. Persiste datos entre pasos.
 */

import { create } from "zustand";

interface Highlight_Data {
  Id_Highlight: string;
  Texto: string;
  Autor: string | null;
  Libro: string | null;
  Pagina: string | null;
  Tipo_Semantico: string;
}

interface Estado_Pipeline {
  Paso_Actual: number;
  Id_Archivo: string | null;
  Formato_Salida: string;
  Highlights: Highlight_Data[];
  Nombre_Archivo_Salida: string;
  Usar_P_Display_Defecto: boolean;
  Usar_P_Processing_Defecto: boolean;
  Estilo_Block: number;
  Criterio_Particion: string | null;

  Establecer_Paso: (Paso: number) => void;
  Establecer_Archivo: (Id: string) => void;
  Establecer_Formato: (Formato: string) => void;
  Establecer_Highlights: (H: Highlight_Data[]) => void;
  Establecer_Nombre: (Nombre: string) => void;
  Establecer_Display_Defecto: (V: boolean) => void;
  Establecer_Processing_Defecto: (V: boolean) => void;
  Establecer_Estilo: (E: number) => void;
  Establecer_Particion: (C: string | null) => void;
  Resetear: () => void;
}

const Estado_Inicial = {
  Paso_Actual: 1,
  Id_Archivo: null,
  Formato_Salida: "pdf",
  Highlights: [],
  Nombre_Archivo_Salida: "",
  Usar_P_Display_Defecto: false,
  Usar_P_Processing_Defecto: false,
  Estilo_Block: 1,
  Criterio_Particion: null,
};

export const Usar_Store_Pipeline = create<Estado_Pipeline>(
  (set) => ({
    ...Estado_Inicial,

    Establecer_Paso: (Paso) =>
      set({ Paso_Actual: Paso }),

    Establecer_Archivo: (Id) =>
      set({ Id_Archivo: Id }),

    Establecer_Formato: (Formato) =>
      set({ Formato_Salida: Formato }),

    Establecer_Highlights: (H) =>
      set({ Highlights: H }),

    Establecer_Nombre: (Nombre) =>
      set({ Nombre_Archivo_Salida: Nombre }),

    Establecer_Display_Defecto: (V) =>
      set({ Usar_P_Display_Defecto: V }),

    Establecer_Processing_Defecto: (V) =>
      set({ Usar_P_Processing_Defecto: V }),

    Establecer_Estilo: (E) =>
      set({ Estilo_Block: E }),

    Establecer_Particion: (C) =>
      set({ Criterio_Particion: C }),

    Resetear: () => set(Estado_Inicial),
  })
);
