/**
 * Hook para manejar selección de filas en
 * tabla tipo explorador de archivos.
 * Soporta: click individual, Shift (rango),
 * Ctrl (toggle).
 */

import { useState, useCallback } from "react";

export function Usar_Seleccion_Tabla(
  Total_Items: number
) {
  const [Seleccionados, Set_Seleccionados] = useState<Set<number>>(
    new Set()
  );
  const [Ultimo_Click, Set_Ultimo_Click] = useState<number | null>(null);

  const Manejar_Click = useCallback(
    (Indice: number, Evento: React.MouseEvent) => {
      Set_Seleccionados((Prev) => {
        const Nuevo = new Set(Prev);

        if (Evento.shiftKey && Ultimo_Click !== null) {
          // Selección de rango con Shift.
          const Inicio = Math.min(Ultimo_Click, Indice);
          const Fin = Math.max(Ultimo_Click, Indice);
          for (let I = Inicio; I <= Fin; I++) {
            Nuevo.add(I);
          }
        } else if (Evento.ctrlKey || Evento.metaKey) {
          // Toggle individual con Ctrl/Cmd.
          if (Nuevo.has(Indice)) {
            Nuevo.delete(Indice);
          } else {
            Nuevo.add(Indice);
          }
        } else {
          // Click simple: selección única.
          Nuevo.clear();
          Nuevo.add(Indice);
        }

        return Nuevo;
      });

      Set_Ultimo_Click(Indice);
    },
    [Ultimo_Click]
  );

  const Manejar_Checkbox = useCallback(
    (Indice: number) => {
      Set_Seleccionados((Prev) => {
        const Nuevo = new Set(Prev);
        if (Nuevo.has(Indice)) {
          Nuevo.delete(Indice);
        } else {
          Nuevo.add(Indice);
        }
        return Nuevo;
      });
    },
    []
  );

  const Seleccionar_Todos = useCallback(() => {
    const Nuevo = new Set<number>();
    for (let I = 0; I < Total_Items; I++) {
      Nuevo.add(I);
    }
    Set_Seleccionados(Nuevo);
  }, [Total_Items]);

  const Deseleccionar_Todos = useCallback(() => {
    Set_Seleccionados(new Set());
  }, []);

  return {
    Seleccionados,
    Manejar_Click,
    Manejar_Checkbox,
    Seleccionar_Todos,
    Deseleccionar_Todos,
    Cantidad_Seleccionados: Seleccionados.size,
  };
}
