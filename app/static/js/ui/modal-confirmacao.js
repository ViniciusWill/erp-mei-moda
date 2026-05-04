export class ModalConfirmacao {
    constructor() {
        this.overlay = null;
    }

    _criar() {
        if (this.overlay) return;

        this.overlay = document.createElement("div");
        this.overlay.className = "modal-confirmacao";
        this.overlay.innerHTML = `
            <div class="modal-confirmacao__caixa" role="dialog" aria-modal="true">
                <h2 class="modal-confirmacao__titulo"></h2>
                <p class="modal-confirmacao__mensagem"></p>
                <div class="modal-confirmacao__acoes">
                    <button type="button" class="btn-nao modal-confirmacao__cancelar">Cancelar</button>
                    <button type="button" class="btn-excluir modal-confirmacao__confirmar">Confirmar</button>
                </div>
            </div>
        `;
        document.body.appendChild(this.overlay);
    }

    confirmar({ titulo = "Confirmar acao", mensagem, textoConfirmar = "Confirmar" }) {
        this._criar();

        const tituloEl = this.overlay.querySelector(".modal-confirmacao__titulo");
        const mensagemEl = this.overlay.querySelector(".modal-confirmacao__mensagem");
        const cancelarBtn = this.overlay.querySelector(".modal-confirmacao__cancelar");
        const confirmarBtn = this.overlay.querySelector(".modal-confirmacao__confirmar");

        tituloEl.textContent = titulo;
        mensagemEl.textContent = mensagem;
        confirmarBtn.textContent = textoConfirmar;
        this.overlay.classList.add("modal-confirmacao--ativa");
        confirmarBtn.focus();

        return new Promise((resolve) => {
            const fechar = (resultado) => {
                this.overlay.classList.remove("modal-confirmacao--ativa");
                cancelarBtn.removeEventListener("click", cancelar);
                confirmarBtn.removeEventListener("click", confirmar);
                this.overlay.removeEventListener("click", cliqueFora);
                document.removeEventListener("keydown", tecla);
                resolve(resultado);
            };

            const cancelar = () => fechar(false);
            const confirmar = () => fechar(true);
            const cliqueFora = (event) => {
                if (event.target === this.overlay) fechar(false);
            };
            const tecla = (event) => {
                if (event.key === "Escape") fechar(false);
            };

            cancelarBtn.addEventListener("click", cancelar);
            confirmarBtn.addEventListener("click", confirmar);
            this.overlay.addEventListener("click", cliqueFora);
            document.addEventListener("keydown", tecla);
        });
    }

    async submeterPost({ action, titulo, mensagem, textoConfirmar = "Excluir" }) {
        const confirmado = await this.confirmar({ titulo, mensagem, textoConfirmar });
        if (!confirmado) return;

        const form = document.createElement("form");
        form.method = "POST";
        form.action = action;
        document.body.appendChild(form);
        form.submit();
    }
}
