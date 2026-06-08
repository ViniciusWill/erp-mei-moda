import { TabelaBuscavel } from "../ui/tabela-buscavel.js";

const tabelaContasPagar = new TabelaBuscavel(
    "tabelaContas",
    "campoBusca",
    "filtroStatus",
    "contadorVisiveis",
    500,
    "contas-pagar:filtros"
);

tabelaContasPagar.inicializar();
