function excluir(id, nome) {
    if (!confirm('Deseja excluir o participante "' + nome + '"?')) return;
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/participantes/' + id;
    document.body.appendChild(form);
    form.submit();
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".btn-excluir-participante").forEach((botao) => {
        botao.addEventListener("click", () => {
            excluir(botao.dataset.id, botao.dataset.nome);
        });
    });
});
