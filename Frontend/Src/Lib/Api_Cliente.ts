/**
 * Cliente HTTP para comunicarse con el backend.
 * Todas las requests van con credentials para
 * enviar la cookie httpOnly.
 */

const BASE_URL = "/api";

interface Opciones_Fetch {
  Metodo?: string;
  Cuerpo?: unknown;
  Params?: Record<string, string>;
}

export async function Api_Fetch<T>(
  Ruta: string,
  Opciones: Opciones_Fetch = {}
): Promise<T> {
  const { Metodo = "GET", Cuerpo, Params } = Opciones;

  let Url = `${BASE_URL}${Ruta}`;

  if (Params) {
    const Query = new URLSearchParams(Params);
    Url += `?${Query.toString()}`;
  }

  const Config: RequestInit = {
    method: Metodo,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (Cuerpo) {
    Config.body = JSON.stringify(Cuerpo);
  }

  const Respuesta = await fetch(Url, Config);

  if (!Respuesta.ok) {
    const Error_Data = await Respuesta.json().catch(
      () => ({ Detalle: "Error desconocido" })
    );
    throw new Error(
      Error_Data.detail || Error_Data.Detalle || `Error ${Respuesta.status}`
    );
  }

  return Respuesta.json();
}

export async function Api_Upload<T>(
  Ruta: string,
  Archivo: File
): Promise<T> {
  const Form_Data = new FormData();
  Form_Data.append("Archivo", Archivo);

  const Respuesta = await fetch(`${BASE_URL}${Ruta}`, {
    method: "POST",
    credentials: "include",
    body: Form_Data,
  });

  if (!Respuesta.ok) {
    const Error_Data = await Respuesta.json().catch(
      () => ({ Detalle: "Error desconocido" })
    );
    throw new Error(
      Error_Data.detail || Error_Data.Detalle || `Error ${Respuesta.status}`
    );
  }

  return Respuesta.json();
}
