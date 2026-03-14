/**
 * Store de Zustand para el estado de
 * autenticación del usuario.
 */

import { create } from "zustand";
import { Api_Fetch } from "@/Lib/Api_Cliente";

interface Datos_Usuario {
  Id: string;
  Email: string;
  Nickname: string | null;
  Avatar_Url: string | null;
  Tipo_Suscripcion: string;
}

interface Estado_Auth {
  Usuario: Datos_Usuario | null;
  Cargando: boolean;
  Autenticado: boolean;

  Verificar_Sesion: () => Promise<void>;
  Cerrar_Sesion: () => Promise<void>;
}

export const Usar_Store_Auth = create<Estado_Auth>(
  (set) => ({
    Usuario: null,
    Cargando: true,
    Autenticado: false,

    Verificar_Sesion: async () => {
      try {
        const Datos = await Api_Fetch<Datos_Usuario>(
          "/auth/me"
        );
        set({
          Usuario: Datos,
          Autenticado: true,
          Cargando: false,
        });
      } catch {
        set({
          Usuario: null,
          Autenticado: false,
          Cargando: false,
        });
      }
    },

    Cerrar_Sesion: async () => {
      await Api_Fetch("/auth/logout", { Metodo: "POST" });
      set({
        Usuario: null,
        Autenticado: false,
      });
    },
  })
);
