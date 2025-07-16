nome = input("Digite seu nome: ")
print(f"Olá, {nome}! Bem-vindo ao sistema bancário.\n")

menu = ('''Escolha a opção desejada: 
[1]Depósito 
[2]Saque 
[3]Extrato 
[0]Sair: ''')

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: R$ "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R${valor:.2f}\n"
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "2":
        if numero_saques >= LIMITE_SAQUES:
            print("Operação falhou! Número máximo de saques atingido.")
        else:
            valor = float(input("Informe o valor do saque: R$ "))
            if valor > limite:
                print("Operação falhou! O valor do saque excede o limite.")
            elif valor > saldo:
                print("Operação falhou! Saldo insuficiente.")
            elif valor > 0:
                saldo -= valor
                extrato += f"Saque:   R${valor:.2f}\n"
                numero_saques += 1
                print(f"Saque de R${valor:.2f} realizado com sucesso!")
            else:
                print("Operação falhou! O valor informado é inválido.")

    elif opcao == "3":
        print("\n========== EXTRATO ==========")
        print(extrato if extrato else "Não foram realizadas movimentações.")
        print(f"\nSaldo atual: R${saldo:.2f}")
        print("=============================")

    elif opcao == "0":
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida. Tente novamente.")