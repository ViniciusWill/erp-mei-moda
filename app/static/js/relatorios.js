function trocarAbaRelatorios(nomeAba, botaoAtivo) {
    document.querySelectorAll(".aba-painel").forEach((painel) => {
        painel.classList.remove("ativa");
    });

    document.querySelectorAll(".aba-btn").forEach((botao) => {
        botao.classList.remove("ativa");
    });

    const painelAlvo = document.getElementById(`aba-${nomeAba}`);
    if (painelAlvo) {
        painelAlvo.classList.add("ativa");
    }

    botaoAtivo.classList.add("ativa");
}

function filtrarTabelaRelatorios(tabelaId, termo) {
    const linhas = document.querySelectorAll(`#${tabelaId} tbody tr`);
    const busca = termo.toLowerCase();

    linhas.forEach((linha) => {
        const visivel = linha.textContent.toLowerCase().includes(busca);
        linha.classList.toggle("linha-oculta", !visivel);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".aba-btn[data-aba]").forEach((botao) => {
        botao.addEventListener("click", () => {
            trocarAbaRelatorios(botao.dataset.aba, botao);
        });
    });

    document.querySelectorAll(".relatorios-busca[data-tabela-alvo]").forEach((campo) => {
        campo.addEventListener("input", () => {
            filtrarTabelaRelatorios(campo.dataset.tabelaAlvo, campo.value);
        });
    });
});

function excluirVenda(id) {
    if (!confirm('Deseja excluir a venda #' + id + '?')) return;
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/relatorios/venda/' + id;
    document.body.appendChild(form);
    form.submit();
}

function excluirCompra(id) {
    if (!confirm('Deseja excluir a compra #' + id + '?')) return;
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/relatorios/compra/' + id;
    document.body.appendChild(form);
    form.submit();
}