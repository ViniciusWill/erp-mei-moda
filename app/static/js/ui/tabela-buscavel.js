import { debounce } from "../core/debounce.js";
import { onReady } from "../core/dom.js";
import { PreferenciasLocais } from "../core/storage.js";

export class TabelaBuscavel {
    constructor(tabelaId, campoBuscaId, filtroStatusId = null, contadorId = null, debounceDelay = 500, storageKey = null) {
        this.tabelaId = tabelaId;
        this.campoBuscaId = campoBuscaId;
        this.filtroStatusId = filtroStatusId;
        this.contadorId = contadorId;
        this.debounceDelay = debounceDelay;
        this.storageKey = storageKey || `tabela:${tabelaId}`;
        this.preferencias = new PreferenciasLocais();
        this.filtrarComDebounce = debounce(() => this.filtrar(), this.debounceDelay);
    }

    _carregarElementos() {
        this.tabela = document.getElementById(this.tabelaId);
        this.campoBusca = document.getElementById(this.campoBuscaId);
        this.filtroStatus = this.filtroStatusId
            ? document.getElementById(this.filtroStatusId)
            : null;
        this.contador = this.contadorId
            ? document.getElementById(this.contadorId)
            : null;

        return Boolean(this.tabela && this.campoBusca);
    }

    _restaurarPreferencias() {
        const preferencias = this.preferencias.ler(this.storageKey, {});

        if (preferencias.busca && this.campoBusca) {
            this.campoBusca.value = preferencias.busca;
        }

        if (preferencias.status && this.filtroStatus) {
            this.filtroStatus.value = preferencias.status;
        }
    }

    _salvarPreferencias() {
        this.preferencias.salvar(this.storageKey, {
            busca: this.campoBusca?.value || "",
            status: this.filtroStatus?.value || "",
        });
    }

    filtrar() {
        if (!this.campoBusca || !this.tabela) return;

        const busca = this.campoBusca.value.toLowerCase();
        const status = this.filtroStatus ? this.filtroStatus.value : "";
        const linhas = this.tabela.querySelectorAll("tbody tr");
        let visiveis = 0;

        linhas.forEach((linha) => {
            const okBusca = linha.textContent.toLowerCase().includes(busca);
            const okStatus = !status || linha.dataset.status === status;
            const visivel = okBusca && okStatus;

            linha.classList.toggle("linha-oculta", !visivel);
            if (visivel) visiveis++;
        });

        if (this.contador) this.contador.textContent = visiveis;
        this._salvarPreferencias();
    }

    inicializar() {
        onReady(() => {
            if (!this._carregarElementos()) return;

            this._restaurarPreferencias();
            this.campoBusca.addEventListener("input", this.filtrarComDebounce);

            if (this.filtroStatus) {
                this.filtroStatus.addEventListener("change", () => this.filtrar());
            }

            this.filtrar();
        });
    }
}
