function filtrarTabela() {
    const busca  = document.getElementById('campoBusca').value.toLowerCase();
    const status = document.getElementById('filtroStatus').value;
    const linhas = document.querySelectorAll('#tabelaContas tbody tr[data-status]');
    let visiveis = 0;
 
    linhas.forEach(tr => {
        const okBusca = tr.textContent.toLowerCase().includes(busca);
        const okSts   = !status || tr.dataset.status === status;
 
        if (okBusca && okSts) {
            tr.classList.remove('linha-oculta');
            visiveis++;
        } else {
            tr.classList.add('linha-oculta');
        }
    });
 
    document.getElementById('contadorVisiveis').textContent = visiveis;
}