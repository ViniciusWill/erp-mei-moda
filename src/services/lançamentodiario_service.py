import pandas as pd
from src.services.compras_service import Lançarcomprasnoestoque
from src.services.vendas_service import Lançarvendasnoestoque
from src.factories.dataframe_factory import Dataframesvenda, Dataframescompra, DataframesEstoque


def lancaropdia(dados):
    novoprod = []
    contasapagar = []
    vendad = []
    vendasareceber = []
    vendanaorealizada = []
    caixa = dados["Caixa"]
    estoque = dados["Estoque"]
    ComprasTotal = dados["Compras"]
    VendasTotal = dados["Vendas"]
    nomearq = dados["nomearq"]
    valoreb = dados["A Receber"]
    valorpag = dados["A Pagar"]
    clientes = dados["Clientes"]

    print('Verificando produtos que estão no estoque..')
    for _,linha in caixa.iterrows():
        produto = linha["Nome do produto"]
        Tamanho = linha["Tamanho"]
        qnt = linha["Quantidade"]
        valoruni = linha["Valor unitario compra"]
        operacao = linha["Operação"]
        data = linha["Data"]
        sexo = linha["Sexo"]
        Participante = linha["Participante"]  

        ##  cria dataframes para registrar as compras, vendas, contas a pagar e contas a receber
        NovaVenda = Dataframesvenda(Participante, produto, Tamanho, sexo, qnt, valoruni, data)
        NovaCompra = Dataframescompra(produto, Tamanho, sexo, qnt, valoruni, data)
        NovalinhaEstoque = DataframesEstoque(produto, Tamanho, qnt, valoruni) 

        if operacao == "Compra":
            ComprasTotal, estoque, valorpag, novoprod, contasapagar = Lançarcomprasnoestoque(linha, estoque, ComprasTotal, NovaCompra, NovalinhaEstoque, valorpag,  novoprod, contasapagar )
        elif operacao == "Venda":
            VendasTotal, estoque, valoreb, clientes, vendasareceber, vendanaorealizada = Lançarvendasnoestoque(VendasTotal, linha, estoque, valoreb, clientes, NovaVenda, vendad, vendasareceber, vendanaorealizada)
        else:
               print(f"Foi encontrado uma operação invalida, verifique as operações lançadas no caixa! Operação: {operacao}!")

    dados_atualizados = {
        "Caixa": caixa,
        "Compras": ComprasTotal,
        "Vendas": VendasTotal,
        "Estoque": estoque,
        "A Receber": valoreb,
        "A Pagar": valorpag,
        "Clientes": clientes,}
    return dados_atualizados, nomearq, novoprod, vendad, vendanaorealizada
