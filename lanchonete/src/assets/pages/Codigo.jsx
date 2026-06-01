import { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "../styles/Codigo.module.css";
import apiService from "../../services/api";
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";

function Codigo() {
    const navigate = useNavigate();
    const [codigo, setCodigo] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!codigo) {
            setError("Por favor, informe o código");
            return;
        }

        const { success } = await apiService.verifyCode(codigo);

        if (!success) {
            setError("Código deve conter 6 dígitos");
            return;
        }

        navigate("/RedefinirSenha", { state: { codigo } });
    };

    return (
        <div className={styles.pageContainer}>
            <Header />

            <div className={styles.box}>
                <h2>Verificar Código</h2>

                {error && (
                    <p className={styles.error}>
                        {error}
                    </p>
                )}

                <form onSubmit={handleSubmit}>
                    <div className={styles.inputGroup}>
                        <label>Código:</label>
                        <input
                            type="text"
                            placeholder="Digite o código de 6 dígitos"
                            value={codigo}
                            onChange={(e) => setCodigo(e.target.value)}
                            maxLength="6"
                            required
                        />
                    </div>

                    <button type="submit">Verificar Código</button>
                </form>
            </div>

            <Footer />
        </div>
    );
}

export default Codigo;