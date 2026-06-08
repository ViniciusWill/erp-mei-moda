import { onReady } from "../core/dom.js";
import { AbasPersistentes } from "../ui/abas-persistentes.js";
import { ModalConfirmacao } from "../ui/modal-confirmacao.js";
import { TabelaBuscavel } from "../ui/tabela-buscavel.js";

const tabelaVendas = new TabelaBuscavel(
    "tabelaVendas",
    "buscaVendas",
    null,
    null,
    500,
    "relatorios:vendas:filtros"
);
const tabelaCompras = new TabelaBuscavel(
    "tabelaCompras",
    "buscaCompras",
    null,
    null,
    500,
    "relatorios:compras:filtros"
);
const modal = new ModalConfirmacao();
const abasRelatorios = new AbasPersistentes({
    botoesSeletor: ".aba-btn[data-aba]",
    painelPrefixo: "aba-",
    storageKey: "relatorios:aba-ativa",
});

tabelaVendas.inicializar();
tabelaCompras.inicializar();
abasRelatorios.inicializar();

onReady(() => {
    document.querySelectorAll(".btn-excluir-venda").forEach((botao) => {
        botao.addEventListener("click", () => {
            modal.submeterPost({
                action: `/relatorios/venda/${botao.dataset.id}`,
                titulo: "Excluir venda",
                mensagem: `Deseja excluir a venda #${botao.dataset.id}?`,
            });
        });
    });

    document.querySelectorAll(".btn-excluir-compra").forEach((botao) => {
        botao.addEventListener("click", () => {
            modal.submeterPost({
                action: `/relatorios/compra/${botao.dataset.id}`,
                titulo: "Excluir compra",
                mensagem: `Deseja excluir a compra #${botao.dataset.id}?`,
            });
        });
    });
});
