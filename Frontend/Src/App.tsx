import { Routes, Route } from "react-router-dom";
import { Pagina_Landing } from "@/Paginas/Pagina_Landing";
import { Pagina_Login } from "@/Paginas/Pagina_Login";

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Pagina_Landing />} />
      <Route path="/login" element={<Pagina_Login />} />
    </Routes>
  );
}
