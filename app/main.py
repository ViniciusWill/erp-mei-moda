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
                    nova_compra_id, valor_compra = compra_service.lançamento_compra(
                        fornecedor_id=f_id,
                          estoque_id=estoque_id, 
                          quantidade=qtd)
                else:
                    nome_produto = input("Nome do produto: ") 
                    tamanho = input("Tamanho: ")
                    qtd = int(input("Quantidade: "))
                    valor_compra = float(input("Valor unitário: "))
                    id_novo_produto_estoque = estoque_service.registrar_produto_estoque(
                        nome_produto=nome_produto, tamanho=tamanho, 
                        quantidade=qtd, valor_compra=valor_compra
                    )
                    nova_compra_id, _ = compra_service.lançamento_compra(
                        fornecedor_id=f_id, 
                        estoque_id=id_novo_produto_estoque, 
                        quantidade=qtd
                    )
                print("\n" + "-"*30)
                opcao_tipo_compra = int(input("A compra realizada foi uma compra a vista ou parcelada? (1. A vista / 2. Parcelada.): "))
                if opcao_tipo_compra == 1: 
                    print("✅ Compra a vista registrada com sucesso!")
                if opcao_tipo_compra == 2: 
                    parcelas_compra = int(input("Insira o numero de parcelas em que o produto sera pago: "))
                    compra_service.lançamento_compra_parcelada(compra_id=nova_compra_id, valor_unitario=valor_compra, quantidade=qtd, parcelas=parcelas_compra)
                print("Compra parcelada registrada!")


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

                nova_venda_id = venda_service.realizar_venda(
                    cliente_id=c_id, estoque_id=p_id, 
                    quantidade_desejada=qtd, valor_unitario=preco
                )
                opcao_tipo_venda = int(input("A venda realizada foi uma venda a vista ou parcelada? (1. A vista / 2. Parcelada): "))
                if opcao_tipo_venda == 1:
                    print("✅ Venda a vista cadastrada com sucesso!")
                else: 
                    parcelas_venda = int(input("Insira o numero de parcelas em que o produto sera pago: "))
                    venda_service.lançamento_venda_parcelada(venda_id=nova_venda_id, valor_unitario=preco, quantidade=qtd, parcelas=parcelas_venda)
                print("✅ Venda parcelada cadastrada com sucesso!")
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


