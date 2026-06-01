import styles from "../styles/Header.module.css";

export function Header() {
    return (
        <header className={styles.header}>
            <div className={styles.logo}>
                <img src="/logo.png" alt="Logo Mestre do Hambúrguer" />
            </div>
        </header>
    );
}

export default Header;