import { TabelaBuscavel } from "../ui/tabela-buscavel.js";

const tabelaContasReceber = new TabelaBuscavel(
    "tabelaContas",
    "campoBusca",
    "filtroStatus",
    "contadorVisiveis",
    500,
    "contas-receber:filtros"
);

tabelaContasReceber.inicializar();
