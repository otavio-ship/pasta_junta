import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";
import styles from "../styles/ConfirmarCodigo.module.css";

function ConfirmarCodigo() {
    const navigate = useNavigate();
    const location = useLocation();
    const [codigo, setCodigo] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const email = location.state?.email || "";

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setError("");

        try {
            const response = await fetch("http://localhost:5000/confirmar_codigo", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, codigo })
            });

            const data = await response.json();

            if (response.ok) {
                navigate("/");
            } else {
                setError(data.erro || "Código inválido");
            }
        } catch (err) {
            setError("Erro de conexão com o servidor");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.container}>
            <Header />
            
            <div className={styles.main}>
                <div className={styles.box}>
                    <h2>Confirmar Código</h2>
                    <p>Digite o código enviado para o seu email</p>
                    
                    {error && <p className={styles.error}>{error}</p>}
                    
                    <form onSubmit={handleSubmit}>
                        <div className={styles.inputGroup}>
                            <label>Código:</label>
                            <input
                                type="text"
                                placeholder="Digite o código"
                                value={codigo}
                                onChange={(e) => setCodigo(e.target.value)}
                                required
                            />
                        </div>
                        
                        <button type="submit" disabled={loading}>
                            {loading ? "Confirmando..." : "Confirmar"}
                        </button>
                    </form>
                </div>
            </div>
            
            <Footer />
        </div>
    );
}

export default ConfirmarCodigo;