import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";
import styles from "../styles/DashboardUsuario.module.css";

function DashboardUsuario() {
    const [usuarios, setUsuarios] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetch("http://localhost:5000/usuarios")
            .then(res => res.json())
            .then(data => setUsuarios(data));
    }, []);

    async function excluirUsuario(id) {
        await fetch(`http://localhost:5000/excluir_usuario/${id}`, { method: "DELETE" });
        setUsuarios(usuarios.filter(u => u.id !== id));
    }

    return (
        <div className={styles.container}>
            <Header />
            
            <div className={styles.main}>
                <h1 className={styles.greeting}>Olá, Admin!</h1>
                
                <h2 className={styles.sectionTitle}>Usuários</h2>
                
                <button className={styles.registerBtn} onClick={() => navigate("/CadastroUsuario")}>
                    Cadastrar Usuário
                </button>
                
                <div className={styles.usersContainer}>
                    {usuarios.map(u => (
                        <div key={u.id} className={styles.userCard}>
                            <img 
                                src={`http://localhost:5000/uploads/usuarios/perfil_${u.id}.jpg`} 
                                alt={u.nome}
                                onError={(e) => { e.target.src = "https://via.placeholder.com/80"; }}
                            />
                            <h3>{u.nome}</h3>
                            <div className={styles.actions}>
                                <button className={styles.editBtn}>Editar</button>
                                <button className={styles.deleteBtn} onClick={() => excluirUsuario(u.id)}>Excluir</button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            
            <Footer />
        </div>
    );
}

export default DashboardUsuario;