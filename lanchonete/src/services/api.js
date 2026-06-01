const API_BASE_URL = "http://localhost:5000";

const apiService = {
    async login(email, senha) {
        const response = await fetch(`${API_BASE_URL}/login_usuario`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, senha })
        });
        return await response.json();
    },

    async forgotPassword(email) {
        const response = await fetch(`${API_BASE_URL}/solicitar_recuperacao`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email })
        });
        return await response.json();
    },

    async verifyCode(codigo) {
        return { success: /^\d{6}$/.test(codigo) };
    },

    async resetPassword(codigo, novaSenha, confirmarSenha) {
        const response = await fetch(`${API_BASE_URL}/redefinir_senha`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ codigo, nova_senha: novaSenha, confirmar_senha: confirmarSenha })
        });
        return await response.json();
    }
};

export default apiService;