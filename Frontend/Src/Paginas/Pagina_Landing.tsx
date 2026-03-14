/**
 * Landing page: hero, features, pricing, CTA.
 */

import { Link } from "react-router-dom";

const Caracteristicas = [
  {
    Titulo: "Subí tu archivo",
    Descripcion:
      "Importá tu My Clippings.txt de Kindle o un DOCX con marcas de formato.",
  },
  {
    Titulo: "Organizá tus highlights",
    Descripcion:
      "Ordená, agrupá, combiná y editá tus resaltados con un wizard intuitivo.",
  },
  {
    Titulo: "Exportá a cualquier formato",
    Descripcion:
      "PDF, DOCX, XLSX, Notion, Obsidian y más. Con 6 estilos visuales.",
  },
  {
    Titulo: "Guardá en tu cuenta",
    Descripcion:
      "Tus highlights se guardan para que vuelvas a editarlos y re-exportar.",
  },
];

export function Pagina_Landing() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero. */}
      <header className="flex flex-col items-center justify-center py-24 px-4">
        <h1 className="text-6xl font-bold mb-4 text-center">
          Highlighter
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-lg text-center">
          Procesá tus resaltados de libros digitales
          y exportalos al formato que quieras.
        </p>
        <Link
          to="/login"
          className="bg-black text-white px-8 py-3 rounded-lg text-lg hover:bg-gray-800 transition"
        >
          Empezar gratis
        </Link>
      </header>

      {/* Features. */}
      <section className="max-w-4xl mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {Caracteristicas.map((C) => (
            <div key={C.Titulo} className="p-6 rounded-lg border border-gray-100">
              <h3 className="font-semibold text-lg mb-2">
                {C.Titulo}
              </h3>
              <p className="text-gray-600 text-sm">
                {C.Descripcion}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Pricing. */}
      <section className="max-w-2xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-8">
          Precios
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Free. */}
          <div className="p-6 rounded-lg border border-gray-200">
            <h3 className="font-semibold text-lg mb-2">Free</h3>
            <p className="text-3xl font-bold mb-4">$0</p>
            <ul className="text-sm text-gray-600 space-y-2">
              <li>Hasta 50 highlights</li>
              <li>Todos los formatos</li>
              <li>6 estilos de Block</li>
            </ul>
          </div>

          {/* Premium. */}
          <div className="p-6 rounded-lg border-2 border-black">
            <h3 className="font-semibold text-lg mb-2">Premium</h3>
            <p className="text-3xl font-bold mb-4">
              Próximamente
            </p>
            <ul className="text-sm text-gray-600 space-y-2">
              <li>Highlights ilimitados</li>
              <li>Todos los formatos</li>
              <li>Soporte prioritario</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Footer. */}
      <footer className="text-center py-8 text-sm text-gray-400">
        Highlighter — 2026
      </footer>
    </div>
  );
}
