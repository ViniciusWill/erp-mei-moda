import pandas as pd



def Dataframescompra(Nome, Tam, Sexo, Qnt, Valor, Data):
    NovaCompra = pd.DataFrame([{"Nome do produto": Nome, 
                                    "Tamanho": Tam,
                                    "Sexo": Sexo,
                                    "Quantidade": Qnt,
                                    "Valor unitario compra": Valor,
                                    "Data da compra": Data
                                    }])
    return NovaCompra


def DataframesEstoque(Nome, Tam, Qnt, Valor):
    NovalinhaEstoque = pd.DataFrame([[Nome, Tam, Qnt, Valor]],
                    columns=["Nome do produto", "Tamanho", "Quantidade", "Valor unitario compra"])      
    return NovalinhaEstoque   


def Dataframesvenda(Part, Nome, Tam, Sexo, Qnt, Valor, Data):
    NovaVenda = pd.DataFrame([{ "Cliente": Part,
                                           "Nome do produto": Nome,
                                           "Tamanho": Tam,  
                                           "Sexo": Sexo,
                                           "Quantidade": Qnt,
                                           "Valor unitario venda": Valor,
                                            "Data": Data
                                             }])  
    return NovaVenda