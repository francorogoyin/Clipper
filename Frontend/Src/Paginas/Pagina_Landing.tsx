import { Link } from "react-router-dom";

export function Pagina_Landing() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-white">
      <h1 className="text-5xl font-bold mb-4">
        Highlighter
      </h1>
      <p className="text-xl text-gray-600 mb-8 max-w-md text-center">
        Procesá tus resaltados de libros digitales
        y exportalos a cualquier formato.
      </p>
      <Link
        to="/login"
        className="bg-black text-white px-8 py-3 rounded-lg text-lg hover:bg-gray-800 transition"
      >
        Empezar
      </Link>
    </main>
  );
}
