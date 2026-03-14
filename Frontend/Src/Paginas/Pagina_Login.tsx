export function Pagina_Login() {
  const Manejar_Login_Google = () => {
    window.location.href = "/api/auth/google/login";
  };

  const Manejar_Login_Notion = () => {
    window.location.href = "/api/auth/notion/login";
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-white">
      <h1 className="text-3xl font-bold mb-8">
        Iniciar sesión
      </h1>
      <div className="flex flex-col gap-4 w-72">
        <button
          onClick={Manejar_Login_Google}
          className="bg-white border border-gray-300 text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-50 transition"
        >
          Continuar con Google
        </button>
        <button
          onClick={Manejar_Login_Notion}
          className="bg-black text-white px-6 py-3 rounded-lg hover:bg-gray-800 transition"
        >
          Continuar con Notion
        </button>
      </div>
    </main>
  );
}
