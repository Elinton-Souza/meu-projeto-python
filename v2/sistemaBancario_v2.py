import textwrap

def menu():
    menu = """\n
    ================ MENU ================ 
    [1]Depósito 
    [2]Saque 
    [3]Extrato 
    [4]Nova conta
    [5]Listar contas
    [6]Novo Usuário
    [0]Sair
 -> """
    return input(textwrap.dedent(menu))

def depositar(conta, valor):
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito: R${valor:.2f}\n"
        print(f"Depósito de R${valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

def sacar(conta, valor, limite, limite_saques):
    excedeu_saldo = valor > conta["saldo"]
    excedeu_limite = valor > limite
    excedeu_saques = conta["numero_saques"] >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Saldo insuficiente.")
    elif excedeu_limite:
        print("Operação falhou! Valor excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques atingido.")
    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R${valor:.2f}\n"
        conta["numero_saques"] += 1
        print(f"Saque de R${valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! Valor inválido.")

def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
    print(f"\nSaldo: R$ {conta['saldo']:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com esse CPF.")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    
    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        conta = {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "extrato": "",
            "numero_saques": 0,
        }
        print(f"Conta criada com sucesso para o usuário {usuario['nome']}!")
        return conta
    
    print("Usuário não encontrado. Conta não criada.")
    return None

def listar_contas(contas):
    for conta in contas:
        linha = f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} |  Usuário: {conta['usuario']['nome']}"
        print("=" * 100)
        print(textwrap.dedent(linha))

def selecionar_conta(contas):
    if not contas:
        print("Nenhuma conta disponível.")
        return None
    
    for i, conta in enumerate(contas):
        print(f"[{i}] Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}")

    try:
        indice = int(input("Escolha o número da conta desejada: "))
        if 0 <= indice < len(contas):
            return contas[indice]
        else:
            print("Conta inválida.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    limite = 500
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            conta = selecionar_conta(contas)
            if conta:
                try:
                    valor = float(input("Informe o valor do depósito: R$ "))
                    depositar(conta, valor)
                except ValueError:
                    print("Valor inválido. Use apenas números e ponto para decimal.")
            else:
                print("Nenhuma conta selecionada.")

        elif opcao == "2":
            conta = selecionar_conta(contas)
            if conta:
                try:
                    valor = float(input("Informe o valor do saque: R$ "))
                    sacar(conta, valor, limite, LIMITE_SAQUES)
                except ValueError:
                    print("Valor inválido. Use apenas números e ponto para decimal.")
            else:
                print("Nenhuma conta selecionada.")

        elif opcao == "3":
            conta = selecionar_conta(contas)
            if conta:
                exibir_extrato(conta)
            else:
                print("Nenhuma conta selecionada.")

        elif opcao == "4":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "6":
            criar_usuario(usuarios)

        elif opcao == "0":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

main()
