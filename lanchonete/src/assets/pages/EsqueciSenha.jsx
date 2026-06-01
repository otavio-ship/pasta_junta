import { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "../styles/EsqueciSenha.module.css";
import apiService from "../../services/api";
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";

function EsqueciSenha() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!email) {
            setError("Por favor, informe seu email");
            return;
        }

        setLoading(true);
        setError("");
        setSuccess("");

        try {
            const data = await apiService.forgotPassword(email);

            if (data.success !== false) {
                setSuccess(data.mensagem || "Se o email estiver cadastrado, você receberá um código");
                setTimeout(() => {
                    navigate("/Codigo");
                }, 2000);
            } else {
                setError(data.erro || "Erro ao solicitar recuperação");
            }
        } catch (err) {
            console.error(err);
            setError("Erro ao conectar com o servidor");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.pageContainer}>
            <Header />

            <div className={styles.box}>
                <h2>Recuperar Senha</h2>

                {error && (
                    <p className={styles.error}>
                        {error}
                    </p>
                )}

                {success && (
                    <p className={styles.success}>
                        {success}
                    </p>
                )}

                <form onSubmit={handleSubmit}>
                    <div className={styles.inputGroup}>
                        <label>Email:</label>
                        <input
                            type="email"
                            placeholder="Digite seu email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    <button type="submit" disabled={loading}>
                        {loading ? "Enviando..." : "Enviar Código"}
                    </button>
                </form>
            </div>

            <Footer />
        </div>
    );
}

export default EsqueciSenha;