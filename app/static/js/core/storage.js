export class PreferenciasLocais {
    constructor(prefixo = "erpMeiModa") {
        this.prefixo = prefixo;
    }

    _chave(chave) {
        return `${this.prefixo}:${chave}`;
    }

    salvar(chave, valor) {
        localStorage.setItem(this._chave(chave), JSON.stringify(valor));
    }

    ler(chave, valorPadrao = null) {
        const valor = localStorage.getItem(this._chave(chave));
        if (valor === null) return valorPadrao;

        try {
            return JSON.parse(valor);
        } catch {
            return valorPadrao;
        }
    }
}
