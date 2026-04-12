function excluir(id, nome) {
    if (!confirm('Deseja excluir o participante "' + nome + '"?')) return;
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/participantes/' + id;
    document.body.appendChild(form);
    form.submit();
}