import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";
import styles from "../styles/Cadastro.module.css";

function Cadastro() {
    const navigate = useNavigate();
    const [nome, setNome] = useState("");
    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");
    const [tipo, setTipo] = useState("garcom");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setError("");
        setSuccess("");

        try {
            const response = await fetch("http://localhost:5000/criar_usuario", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ nome, email, senha, tipo })
            });

            const data = await response.json();

            if (response.ok) {
                setSuccess("Usuário cadastrado com sucesso! Verifique o e-mail.");
                setTimeout(() => navigate("/"), 2000);
            } else {
                setError(data.erro || "Erro ao cadastrar usuário");
            }
        } catch (err) {
            setError("Erro de conexão com o servidor");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.pageContainer}>
            <Header />

            <div className={styles.box}>
                <h2>Cadastrar Usuário</h2>

                {error && <p className={styles.error}>{error}</p>}
                {success && <p className={styles.success}>{success}</p>}

                <form onSubmit={handleSubmit}>
                    <div className={styles.inputGroup}>
                        <label>Nome:</label>
                        <input
                            type="text"
                            placeholder="Digite o nome"
                            value={nome}
                            onChange={(e) => setNome(e.target.value)}
                            required
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label>Email:</label>
                        <input
                            type="email"
                            placeholder="Digite o email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label>Senha:</label>
                        <input
                            type="password"
                            placeholder="Digite a senha"
                            value={senha}
                            onChange={(e) => setSenha(e.target.value)}
                            required
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label>Tipo:</label>
                        <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
                            <option value="admin">Admin</option>
                            <option value="garcom">Garçom</option>
                        </select>
                    </div>

                    <button type="submit" disabled={loading}>
                        {loading ? "Cadastrando..." : "Cadastrar"}
                    </button>
                </form>
            </div>

            <Footer />
        </div>
    );
}

export default Cadastro;