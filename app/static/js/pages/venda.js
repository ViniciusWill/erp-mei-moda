import { onReady } from "../core/dom.js";

function mostrarFormVenda() {
    const passoPergunta = document.getElementById("passo-pergunta");
    const passoForm = document.getElementById("passo-form");

    if (!passoPergunta || !passoForm) return;

    passoPergunta.style.display = "none";
    passoForm.style.display = "block";
}

function voltarPerguntaVenda() {
    const passoPergunta = document.getElementById("passo-pergunta");
    const passoForm = document.getElementById("passo-form");

    if (!passoPergunta || !passoForm) return;

    passoForm.style.display = "none";
    passoPergunta.style.display = "flex";
}

onReady(() => {
    const container = document.getElementById("Vendas");
    const mostrarFormBotao = document.querySelector(".js-mostrar-form-venda");
    const voltarPerguntaBotao = document.querySelector(".js-voltar-pergunta-venda");

    if (mostrarFormBotao) {
        mostrarFormBotao.addEventListener("click", mostrarFormVenda);
    }

    if (voltarPerguntaBotao) {
        voltarPerguntaBotao.addEventListener("click", voltarPerguntaVenda);
    }

    if (container?.dataset.produtoSelecionado) {
        mostrarFormVenda();
    }
});
