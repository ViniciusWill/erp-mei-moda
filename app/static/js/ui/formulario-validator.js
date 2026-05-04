export class FormularioValidator {
    constructor(formulario) {
        this.formulario = formulario;
    }

    inicializar() {
        this.formulario.setAttribute("novalidate", "novalidate");
        this.formulario.addEventListener("submit", (event) => this._aoEnviar(event));

        this._campos().forEach((campo) => {
            campo.addEventListener("input", () => this._limparErro(campo));
            campo.addEventListener("change", () => this._limparErro(campo));
        });
    }

    _campos() {
        return Array.from(this.formulario.querySelectorAll("input, select, textarea"));
    }

    _aoEnviar(event) {
        const campoInvalido = this._campos().find((campo) => !this._validarCampo(campo));

        if (!campoInvalido) return;

        event.preventDefault();
        campoInvalido.focus();
    }

    _validarCampo(campo) {
        this._limparErro(campo);

        if (campo.validity.valid) return true;

        this._mostrarErro(campo, this._mensagem(campo));
        return false;
    }

    _mensagem(campo) {
        if (campo.validity.valueMissing) return "Preencha este campo.";
        if (campo.validity.tooShort) return `Informe pelo menos ${campo.minLength} caracteres.`;
        if (campo.validity.tooLong) return `Informe no maximo ${campo.maxLength} caracteres.`;
        if (campo.validity.rangeUnderflow) return `Informe um valor maior ou igual a ${campo.min}.`;
        if (campo.validity.patternMismatch) return campo.title || "Formato invalido.";
        return "Revise este campo.";
    }

    _mostrarErro(campo, mensagem) {
        campo.classList.add("campo-invalido");

        const erro = document.createElement("span");
        erro.className = "campo-erro";
        erro.textContent = mensagem;
        campo.insertAdjacentElement("afterend", erro);
    }

    _limparErro(campo) {
        campo.classList.remove("campo-invalido");
        const erro = campo.nextElementSibling?.classList.contains("campo-erro")
            ? campo.nextElementSibling
            : null;
        if (erro) erro.remove();
    }

    static inicializarTodos(seletor = ".formulario") {
        document.querySelectorAll(seletor).forEach((formulario) => {
            new FormularioValidator(formulario).inicializar();
        });
    }
}
