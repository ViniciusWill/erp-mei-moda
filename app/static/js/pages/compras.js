import { onReady } from "../core/dom.js";

function exibirEtapa(etapa) {
    const passoPerguntaProduto = document.getElementById("passo-pergunta-produto");
    const passoPerguntaFornecedor = document.getElementById("passo-pergunta-fornecedor");
    const passoForm = document.getElementById("passo-form");

    if (!passoPerguntaProduto || !passoPerguntaFornecedor || !passoForm) return;

    passoPerguntaProduto.style.display = etapa === "produto" ? "block" : "none";
    passoPerguntaFornecedor.style.display = etapa === "fornecedor" ? "block" : "none";
    passoForm.style.display = etapa === "formulario" ? "block" : "none";
}

onReady(() => {
    const container = document.getElementById("Compras");
    const avancarProdutoBotao = document.querySelector(".js-mostrar-form-compra");
    const avancarFornecedorBotao = document.querySelector(".js-mostrar-form-fornecedor");

    if (avancarProdutoBotao) {
        avancarProdutoBotao.addEventListener("click", () => exibirEtapa("fornecedor"));
    }

    if (avancarFornecedorBotao) {
        avancarFornecedorBotao.addEventListener("click", () => exibirEtapa("formulario"));
    }

    if (container?.dataset.fornecedorSelecionado) {
        exibirEtapa("formulario");
        return;
    }

    if (container?.dataset.produtoSelecionado) {
        exibirEtapa("fornecedor");
        return;
    }

    exibirEtapa("produto");
});
