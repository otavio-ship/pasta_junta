import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";
import styles from "../styles/CadastroUsuario.module.css";

function CadastroUsuario() {
    const navigate = useNavigate();
    const [nome, setNome] = useState("");
    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");
    const [tipo, setTipo] = useState("garcom");
    const [foto, setFoto] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setError("");

        const formData = new FormData();
        formData.append("nome", nome);
        formData.append("email", email);
        formData.append("senha", senha);
        formData.append("tipo", tipo);
        if (foto) {
            formData.append("foto", foto);
        }

        try {
            const response = await fetch("http://localhost:5000/criar_usuario", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                navigate("/confirmar-codigo", { state: { email } });
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

                    <div className={styles.inputGroup}>
                        <label>Foto:</label>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={(e) => setFoto(e.target.files[0])}
                        />
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

export default CadastroUsuario;