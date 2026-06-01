import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import styles from "../styles/Login.module.css";
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";

function Login() {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function fazerLogin(e) {
        e.preventDefault();

        setLoading(true);
        setError("");

        try {
            const response = await fetch("http://localhost:5000/login_usuario", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    senha: senha
                })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("token", data.token);
                navigate("/dashboard-usuario");
            } else {
                setError(data.erro || "Falha no login");
            }

        } catch (err) {
            console.error(err);
            setError("Erro ao conectar com o servidor");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.pageContainer}>
            <Header />

            <div className={styles.container}>
                <form onSubmit={fazerLogin} className={styles.formBox}>
                    <h2>Login</h2>

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

                    <div className={styles.inputGroup}>
                        <label>Senha:</label>

                        <input
                            type="password"
                            placeholder="Digite sua senha"
                            value={senha}
                            onChange={(e) => setSenha(e.target.value)}
                            required
                        />
                    </div>

                    {error && (
                        <p className={styles.error}>
                            {error}
                        </p>
                    )}

                    <button type="submit" disabled={loading}>
                        {loading ? "Entrando..." : "Entrar"}
                    </button>

                    <Link to="/EsqueciSenha" className={styles.esqueceu}>
                        Esqueceu sua senha?
                    </Link>
                </form>
            </div>

            <Footer />
        </div>
    );
}

export default Login;