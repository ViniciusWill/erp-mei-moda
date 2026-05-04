import { onReady } from "../core/dom.js";
import { PreferenciasLocais } from "../core/storage.js";

export class AbasPersistentes {
    constructor({ botoesSeletor, painelPrefixo, classeAtiva = "ativa", storageKey }) {
        this.botoesSeletor = botoesSeletor;
        this.painelPrefixo = painelPrefixo;
        this.classeAtiva = classeAtiva;
        this.storageKey = storageKey;
        this.preferencias = new PreferenciasLocais();
    }

    ativar(nomeAba, botaoAtivo = null) {
        document.querySelectorAll(this.botoesSeletor).forEach((botao) => {
            botao.classList.toggle(this.classeAtiva, botao === botaoAtivo || botao.dataset.aba === nomeAba);
        });

        document.querySelectorAll(`[id^="${this.painelPrefixo}"]`).forEach((painel) => {
            painel.classList.remove(this.classeAtiva);
        });

        const painel = document.getElementById(`${this.painelPrefixo}${nomeAba}`);
        if (painel) painel.classList.add(this.classeAtiva);
        this.preferencias.salvar(this.storageKey, nomeAba);
    }

    inicializar() {
        onReady(() => {
            const botoes = document.querySelectorAll(this.botoesSeletor);
            botoes.forEach((botao) => {
                botao.addEventListener("click", () => this.ativar(botao.dataset.aba, botao));
            });

            const abaSalva = this.preferencias.ler(this.storageKey);
            if (abaSalva) this.ativar(abaSalva);
        });
    }
}
