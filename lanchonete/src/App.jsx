import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./assets/pages/Login.jsx";
import EsqueciSenha from "./assets/pages/EsqueciSenha.jsx";
import Codigo from "./assets/pages/Codigo.jsx";
import RedefinirSenha from "./assets/pages/RedefinirSenha.jsx";
import DashboardUsuario from "./assets/pages/DashboardUsuario.jsx";
import CadastroUsuario from "./assets/pages/CadastroUsuario.jsx";
import ConfirmarCodigo from "./assets/pages/ConfirmarCodigo.jsx";
import "./App.css";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/EsqueciSenha" element={<EsqueciSenha />} />
                <Route path="/Codigo" element={<Codigo />} />
                <Route path="/RedefinirSenha" element={<RedefinirSenha />} />
                <Route path="/dashboard-usuario" element={<DashboardUsuario />} />
                <Route path="/CadastroUsuario" element={<CadastroUsuario />} />
                <Route path="/confirmar-codigo" element={<ConfirmarCodigo />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;