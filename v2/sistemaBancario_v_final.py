from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

# ==========================
# HISTÓRICO
# ==========================
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

# ==========================
# CONTA
# ==========================
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            print(f"Saque de R${valor:.2f} realizado com sucesso!")
            return True
        else:
            print("Operação falhou! Saldo insuficiente ou valor inválido.")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
            return True
        else:
            print("Operação falhou! Valor inválido.")
            return False

# ==========================
# CONTA CORRENTE
# ==========================
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0

    def sacar(self, valor):
        excedeu_limite = valor > self._limite
        excedeu_saques = self._saques_realizados >= self._limite_saques

        if excedeu_limite:
            print("Operação falhou! Valor excede o limite.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques atingido.")
        elif super().sacar(valor):
            self._saques_realizados += 1
            return True
        return False

# ==========================
# INTERFACE TRANSAÇÃO
# ==========================
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

# ==========================
# DEPÓSITO
# ==========================
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)

# ==========================
# SAQUE
# ==========================
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)

# ==========================
# CLIENTE
# ==========================
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    @property
    def contas(self):
        return self._contas

# ==========================
# PESSOA FÍSICA
# ==========================
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf

# ==========================
# FUNÇÕES AUXILIARES DO MENU
# ==========================
def menu():
    opcoes = """\n
    ================ MENU ================
    [1] Depósito
    [2] Saque
    [3] Extrato
    [4] Nova Conta
    [5] Listar Contas
    [6] Novo Usuário
    [0] Sair
    -> """
    return input(textwrap.dedent(opcoes))

def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for t in transacoes:
            print(f"{t['tipo']}: R${t['valor']:.2f} em {t['data']}")
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(f"Agência: {conta.agencia} | Conta: {conta.numero} | Titular: {conta.cliente.nome}")

def selecionar_conta(contas):
    if not contas:
        print("Nenhuma conta disponível.")
        return None
    for i, conta in enumerate(contas):
        print(f"[{i}] Agência: {conta.agencia} | Conta: {conta.numero} | Titular: {conta.cliente.nome}")
    try:
        indice = int(input("Escolha o número da conta desejada: "))
        if 0 <= indice < len(contas):
            return contas[indice]
        else:
            print("Conta inválida.")
    except ValueError:
        print("Entrada inválida.")
    return None

# ==========================
# PROGRAMA PRINCIPAL
# ==========================
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            conta = selecionar_conta(contas)
            if conta:
                valor = float(input("Valor do depósito: R$ "))
                transacao = Deposito(valor)
                conta.cliente.realizar_transacao(conta, transacao)

        elif opcao == "2":
            conta = selecionar_conta(contas)
            if conta:
                valor = float(input("Valor do saque: R$ "))
                transacao = Saque(valor)
                conta.cliente.realizar_transacao(conta, transacao)

        elif opcao == "3":
            conta = selecionar_conta(contas)
            if conta:
                exibir_extrato(conta)

        elif opcao == "4":
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if cliente:
                numero_conta = len(contas) + 1
                conta = ContaCorrente.nova_conta(cliente, numero_conta)
                cliente.adicionar_conta(conta)
                contas.append(conta)
                print("Conta criada com sucesso!")
            else:
                print("Cliente não encontrado.")

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "6":
            nome = input("Nome completo: ")
            cpf = input("CPF: ")
            data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
            endereco = input("Endereço: ")
            cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
            clientes.append(cliente)
            print("Cliente criado com sucesso!")

        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")

main()
