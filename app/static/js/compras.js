function mostrarFormCompra() {
    const passoPergunta = document.getElementById("passo-pergunta");
    const passoForm = document.getElementById("passo-form");

    if (!passoPergunta || !passoForm) return;

    passoPergunta.style.display = "none";
    passoForm.style.display = "block";
}

function voltarPerguntaCompra() {
    const passoPergunta = document.getElementById("passo-pergunta");
    const passoForm = document.getElementById("passo-form");

    if (!passoPergunta || !passoForm) return;

    passoForm.style.display = "none";
    passoPergunta.style.display = "flex";
}

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("Compras");
    const mostrarFormBotao = document.querySelector(".js-mostrar-form-compra");
    const voltarPerguntaBotao = document.querySelector(".js-voltar-pergunta-compra");

    if (mostrarFormBotao) {
        mostrarFormBotao.addEventListener("click", mostrarFormCompra);
    }

    if (voltarPerguntaBotao) {
        voltarPerguntaBotao.addEventListener("click", voltarPerguntaCompra);
    }

    if (container?.dataset.produtoSelecionado) {
        mostrarFormCompra();
    }
});
