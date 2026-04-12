function filtrarTabelaContasReceber() {
    const campoBusca = document.getElementById("campoBusca");
    const filtroStatus = document.getElementById("filtroStatus");
    const contador = document.getElementById("contadorVisiveis");

    if (!campoBusca || !filtroStatus || !contador) {
        return;
    }

    const busca = campoBusca.value.toLowerCase();
    const status = filtroStatus.value;
    const linhas = document.querySelectorAll("#tabelaContas tbody tr[data-status]");
    let visiveis = 0;

    linhas.forEach((linha) => {
        const okBusca = linha.textContent.toLowerCase().includes(busca);
        const okStatus = !status || linha.dataset.status === status;

        if (okBusca && okStatus) {
            linha.classList.remove("linha-oculta");
            visiveis += 1;
        } else {
            linha.classList.add("linha-oculta");
        }
    });

    contador.textContent = visiveis;
}

document.addEventListener("DOMContentLoaded", () => {
    const campoBusca = document.getElementById("campoBusca");
    const filtroStatus = document.getElementById("filtroStatus");

    if (!campoBusca || !filtroStatus || !document.getElementById("tabelaContas")) {
        return;
    }

    campoBusca.addEventListener("input", filtrarTabelaContasReceber);
    filtroStatus.addEventListener("change", filtrarTabelaContasReceber);
});
