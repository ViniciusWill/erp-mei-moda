function excluir(id, nome) {
    if (!confirm('Deseja excluir o cliente "' + nome + '"?')) return;
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/clientes/' + id;
    document.body.appendChild(form);
    form.submit();
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".btn-excluir-cliente").forEach((botao) => {
        botao.addEventListener("click", () => {
            excluir(botao.dataset.id, botao.dataset.nome);
        });
    });
});
