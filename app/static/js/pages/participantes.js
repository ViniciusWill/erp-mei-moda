import { onReady } from "../core/dom.js";
import { ModalConfirmacao } from "../ui/modal-confirmacao.js";
import { TabelaBuscavel } from "../ui/tabela-buscavel.js";

const modal = new ModalConfirmacao();
const tabelaParticipantes = new TabelaBuscavel(
    "tabelaParticipantes",
    "campoBusca",
    null,
    null,
    500,
    "participantes:filtros"
);

tabelaParticipantes.inicializar();

onReady(() => {
    document.querySelectorAll(".btn-excluir-participante").forEach((botao) => {
        botao.addEventListener("click", () => {
            modal.submeterPost({
                action: `/participantes/${botao.dataset.id}`,
                titulo: "Excluir participante",
                mensagem: `Deseja excluir o participante "${botao.dataset.nome}"?`,
            });
        });
    });
});
