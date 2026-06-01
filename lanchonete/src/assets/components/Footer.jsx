import styles from "../styles/Footer.module.css";

export function Footer() {
    return (
        <footer className={styles.footer}>
            <div className={styles.logo}>
                <img src="/logo.png" alt="Logo" />
            </div>
            <div className={styles.info}>
                <p>R: Salvador, nº233</p>
                <p>mestredohamburguer@vendas.com.br</p>
            </div>
        </footer>
    );
}

export default Footer;