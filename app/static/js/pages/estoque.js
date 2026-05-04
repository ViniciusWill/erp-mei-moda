import { TabelaBuscavel } from "../ui/tabela-buscavel.js";

const tabelaEstoque = new TabelaBuscavel(
    "tabelaEstoque",
    "campoBusca",
    "filtroStatus",
    "contadorVisiveis",
    500,
    "estoque:filtros"
);

tabelaEstoque.inicializar();
