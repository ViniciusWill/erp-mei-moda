export class Toast {
    constructor(containerId = "toast-container") {
        this.containerId = containerId;
        this.container = null;
    }

    _container() {
        if (this.container) return this.container;

        this.container = document.getElementById(this.containerId);
        if (!this.container) {
            this.container = document.createElement("div");
            this.container.id = this.containerId;
            this.container.className = "toast-container";
            document.body.appendChild(this.container);
        }

        return this.container;
    }

    mostrar(mensagem, tipo = "success", duracao = 3500) {
        const item = document.createElement("div");
        item.className = `toast toast--${tipo}`;
        item.textContent = mensagem;
        this._container().appendChild(item);

        window.setTimeout(() => item.classList.add("toast--saindo"), duracao);
        window.setTimeout(() => item.remove(), duracao + 250);
    }

    static exibirFlashMessages() {
        const toast = new Toast();

        document.querySelectorAll(".flash-container .alerta").forEach((alerta) => {
            const tipo = alerta.classList.contains("alerta-error") ? "error" : "success";
            toast.mostrar(alerta.textContent.trim(), tipo);
            alerta.remove();
        });
    }
}
