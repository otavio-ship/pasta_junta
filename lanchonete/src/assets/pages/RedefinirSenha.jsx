import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import styles from "../styles/RedefinirSenha.module.css";
import apiService from "../../services/api";
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";

function RedefinirSenha() {
    const navigate = useNavigate();
    const location = useLocation();
    const [novaSenha, setNovaSenha] = useState("");
    const [confirmarSenha, setConfirmarSenha] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const codigo = location.state?.codigo || "";

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!novaSenha || !confirmarSenha) {
            setError("Por favor, preencha todos os campos");
            return;
        }

        if (novaSenha !== confirmarSenha) {
            setError("As senhas não coincidem");
            return;
        }

        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/;
        if (!passwordRegex.test(novaSenha)) {
            setError("A senha deve ter pelo menos 8 caracteres, incluindo letra maiúscula, letra minúscula e número");
            return;
        }

        setLoading(true);
        setError("");
        setSuccess("");

        try {
            const data = await apiService.resetPassword(codigo, novaSenha, confirmarSenha);

            if (data.success !== false) {
                setSuccess(data.mensagem || "Senha alterada com sucesso!");
                setTimeout(() => {
                    navigate("/");
                }, 2000);
            } else {
                setError(data.erro || "Erro ao redefinir senha");
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
                <h2>Redefinir Senha</h2>

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
                        <label>Nova Senha:</label>
                        <input
                            type="password"
                            placeholder="Digite sua nova senha"
                            value={novaSenha}
                            onChange={(e) => setNovaSenha(e.target.value)}
                            required
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label>Confirmar Senha:</label>
                        <input
                            type="password"
                            placeholder="Confirme sua nova senha"
                            value={confirmarSenha}
                            onChange={(e) => setConfirmarSenha(e.target.value)}
                            required
                        />
                    </div>

                    <button type="submit" disabled={loading}>
                        {loading ? "Redefinindo..." : "Redefinir Senha"}
                    </button>
                </form>
            </div>

            <Footer />
        </div>
    );
}

export default RedefinirSenha;