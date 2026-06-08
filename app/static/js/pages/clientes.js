import { onReady } from "../core/dom.js";
import { ModalConfirmacao } from "../ui/modal-confirmacao.js";
import { TabelaBuscavel } from "../ui/tabela-buscavel.js";

const tabelaClientes = new TabelaBuscavel(
    "tabelaClientes",
    "campoBusca",
    null,
    null,
    500,
    "clientes:filtros"
);

tabelaClientes.inicializar();
const modal = new ModalConfirmacao();

onReady(() => {
    document.querySelectorAll(".btn-excluir-cliente").forEach((botao) => {
        botao.addEventListener("click", () => {
            modal.submeterPost({
                action: `/clientes/${botao.dataset.id}`,
                titulo: "Excluir cliente",
                mensagem: `Deseja excluir o cliente "${botao.dataset.nome}"?`,
            });
        });
    });
});
