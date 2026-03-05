import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.vendas_service import VendasService
from services.compras_service import CompraService
from services.estoque_service import EstoqueService
from services.clientes_service import ClienteService
from services.participantes_service import ParticipanteService


def menu_principal():
    venda_service = VendasService()
    compra_service = CompraService()
    estoque_service = EstoqueService()
    cliente_service = ClienteService()
    participante_service = ParticipanteService()


    while True:
        print("\n" + "="*30)
        print("   SISTEMA DE GESTÃO - LOJA")
        print("="*30)
        print("1. Registrar Nova Compra")
        print("2. Registrar Nova Venda")
        print("3. Cadastrar Novo Cliente")
        print("4. Cadastrar Novo Participante")
        print("4. Ver Estoque (Em breve)")
        print("0. Sair")
        print("-" * 30)

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("\n⚠️ ERRO: Digite apenas números para escolher a opção!")
            continue

        if opcao == 1:
            try:
                print("\n" + "-"*30)
                opcao_produto = int(input("O Produto já está no estoque? (1. Sim / 2. Não): "))
                
                f_id = int(input("ID do fornecedor: "))
                
                if opcao_produto == 1:
                    estoque_id = int(input("ID Produto (Estoque): "))
                    qtd = int(input("Quantidade adquirida: "))
                    compra_service.lançamento_compra(fornecedor_id=f_id, estoque_id=estoque_id, quantidade=qtd)
                else:
                    nome_produto = input("Nome do produto: ") 
                    tamanho = input("Tamanho: ")
                    qtd = int(input("Quantidade: "))
                    valor_compra = float(input("Valor unitário: "))
                    
                    id_novo = estoque_service.registrar_produto_estoque(
                        nome_produto=nome_produto, tamanho=tamanho, 
                        quantidade=qtd, valor_compra=valor_compra
                    )
                    compra_service.lançamento_compra(fornecedor_id=f_id, estoque_id=id_novo, quantidade=qtd)
                
                print("✅ Compra registrada com sucesso!")
            except ValueError as e:
                print(f"\n⚠️ ERRO DE VALIDAÇÃO: Verifique se digitou números corretamente.")
            except Exception as e:
                print(f"\n❌ ERRO INESPERADO: {e}")

        elif opcao == 2:
            try:
                print("\n--- REGISTRAR VENDA ---")
                c_id = int(input("ID do Cliente/Participante: "))
                p_id = int(input("ID do Produto: "))
                qtd = int(input("Quantidade: "))
                preco = float(input("Preço Unitário: "))

                venda_service.realizar_venda(
                    cliente_id=c_id, estoque_id=p_id, 
                    quantidade_desejada=qtd, valor_unitario=preco
                )
                print("✅ Venda realizada!")
            except Exception as e:
                print(f"\n❌ ERRO NA VENDA: {e}")

        elif opcao == 3:
            try:
                print("\n--- REGISTRAR CLIENTE ---")
                nome_cliente = input("Nome (Obrigatório): ")
                info = input("Deseja inserir info adicionais? (S/N): ").upper()
                
                if info == 'S':
                    cpf = input("CPF: ")
                    email = input("E-mail: ")
                    tel = input("Telefone: ")
                else:
                    cliente_service.LançamentoClienteCamposObrigatorios(nome=nome_cliente)
                print("✅ Cliente cadastrado!")
            except Exception as e:
                print(f"\n❌ ERRO AO CADASTRAR CLIENTE: {e}")
        
        elif opcao == 4:
            try:
                print("\n--- REGISTRAR PARTICIPANTE ---")
                nome_participante = input("Nome (Obrigatorio): ")
                info = input("Deseja inserir infor adicionais? (S/N): ").upper()
                
                if info == 'S':
                    cpf = input("CPF: ")
                    email = input("E-mail: ")
                    tel = input("Telefone: ")
                else:
                    participante_service.LançamentoParticipanteCampoObrigatorio(nome_participante)
                print("✅ Participante cadastrado!")

            except Exception as e:
                print(f"\n❌ ERRO AO CADASTRAR PARTICIPANTE: {e}")
                    
        elif opcao == 0:
            print("Encerrando sistema... Até logo!")
            break
        else:
            print("Opção inválida!")
if __name__ == "__main__":
    menu_principal()


