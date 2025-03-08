from datetime import datetime
from abc import ABC, abstractmethod


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

    @property
    @abstractmethod
    def valor(self):
        pass


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y  %H:%M:%S"),
            }
        )


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao = conta.depositar(self.valor)
        if transacao:
            conta.historico.adicionar_transacao(self)
        return transacao


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao = conta.sacar(self._valor)
        if transacao:
            conta.historico.adicionar_transacao(self)
        return transacao


class Conta:
    def __init__(self, cliente, numero, saldo=0.0, agencia="0001"):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def historico(self):
        return self._historico

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def numero(self):
        return self._numero

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    def sacar(self, valor):
        if valor < 0:
            print("Operacao Invalida! Valor de saque tem de maior que 0")
            return False
        if self._saldo < valor:
            print("Operação Invalida! Saldo insuficiente")
            return False
        self._saldo -= valor
        print(
            f"operacao realizada com sucesso!!! \n Saldo após o saque R$ {self._saldo:.2f}"
        )
        return True

    def depositar(self, valor):
        if valor < 0:
            print("Operação Invalida! Valor de deposito tem de ser maior que 0")
            return False
        self._saldo += valor
        print(
            f"operacao realizada com sucesso!!! \n Saldo após o deposito R$ {self._saldo:.2f}"
        )
        return True


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        self._limite = limite
        self._limite_saques = limite_saques
        super().__init__(cliente, numero)

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    def __str__(self):
        return f"""
              \tAgencia Nº: {self.agencia}
              \tConta Nº: {self.numero}
              \tNome do titular: {self.cliente.nome}
              \tEndereço: {self.cliente.endereco}
              """

    def sacar(self, valor):
        lista_saques = [
            transacao
            for transacao in self.historico.transacoes
            if transacao["tipo"] == "Saque"
        ]
        if len(lista_saques) > self.limite_saques:
            print("Operação invalida! limite de saques excedido.")
            return
        if valor > self.limite:
            print("Operação invalida! O valor excede o limite máximo de saques")
            return
        return super().sacar(valor)


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        super().__init__(endereco)

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf

    @property
    def data_nascimento(self):
        return self._data_nascimento


menu_bancario = """
        ================== Bemvindo ao menu Bancario =================
        Selecione uma das opcoes
        [1] - Deposito
        [2] - Saque
        [3] - Consultar Extrato
        [4] - Cadastrar Cliente
        [5] - Criar Conta Corrente
        [6] - Listar Contas
        [0] - Sair
        =>
    """

def main():
    contas = []
    clientes = []
    opcao = ""
    while opcao != "0":
        print(menu_bancario)
        opcao = input()
        if opcao == "1":
            deposito(clientes)
        if opcao == "2":
            saque(clientes)
        if opcao == "3":
            extrato(clientes)
        if opcao == "4":
            cadastrar_cliente(clientes)
        if opcao == "5":
            criar_conta_corrente(clientes, contas)
        if opcao == "6":
            listar_contas(contas)
        if opcao == "0":
            print("Fechando o sistema...")

def deposito(clientes):
    print("\n==================Deposito======================")
    cpf = input("Digite o cpf do cliente: ")
    cliente = buscar_cliente(clientes, cpf)
    if cliente:
        valor = float(input("Digite o valor do deposito: "))
        deposito = Deposito(valor)
        conta = buscar_conta_corrente(cliente)
        if conta:
            if deposito.registrar(conta):
                print("operacao realizada com sucesso")
                return
            return
        return
    print("cliente não encontrado")
    
def saque(clientes):
    print("\n====================Saque====================")
    cpf = input("Digite o cpf do cliente: ")
    cliente = buscar_cliente(clientes, cpf)
    if cliente:
        valor = float(input("Digite o valor do saque: "))
        saque = Saque(valor)
        conta = buscar_conta_corrente(cliente)
        if conta:
            if saque.registrar(conta):
                print("Operação realizada com sucesso")
                return
            return
        return
    print("cliente não encontrado")

def extrato(clientes):
    print("\n================ EXTRATO ================")
    cpf = input("Digite o cpf do Cliente: ")
    cliente = buscar_cliente(clientes, cpf)
    if cliente:
        conta = buscar_conta_corrente(cliente)
        if conta:
            print(f"\n Nome: {cliente.nome}")
            if len(conta.historico.transacoes) == 0:
                print("Não Foram realizadas nenhuma transação")
                return
            for transacao in conta.historico.transacoes:
                print(transacao)
            print(f"Saldo atual: R$ {conta.saldo}:.2f")
            return
        return
    print("Nenhum cliente encontado")
 
def criar_conta_corrente(clientes, contas):
    print("\n================ Criar Conta Corrente ================")
    cpf = input("Digite o cpf do Cliente: ")
    cliente = buscar_cliente(clientes, cpf)
    if cliente:
        numero = len(contas) + 1
        conta = ContaCorrente(cliente, numero)
        cliente.adicionar_conta(conta)
        contas.append(conta)
        print(f"Conta de {cliente.nome} criado com sucesso")
        return
    print("cliente não encontrado")
    
def cadastrar_cliente(clientes):
    print("\n ================Cadastrar Novo Cliente======================")
    cpf = input("Digite o cpf do cliente: ")
    
    if buscar_cliente(clientes, cpf) is None:
        nome = input("Digite o nome do cliente: ")
        data_nascimento = input("Digite a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Digite o endereço: ")
        cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
        clientes.append(cliente)
        print(f"Cliente {cliente.nome} cadastrado com sucesso")
        return
    print(f"cliente com cpf: {cpf} já cadastrado no sistema")
    
def listar_contas(contas):
    for conta in contas:
        print(f"""
              \tAgencia Nº: {conta.agencia}
              \tConta Nº: {conta.numero}
              \tNome do titular: {conta.cliente.nome}
              \tEndereço: {conta.cliente.endereco}
              """)
    
def buscar_cliente(clientes, cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def buscar_conta_corrente(cliente):
    if not cliente.contas:
        print("cliente não possui nenhuma conta")
        return None
    if len(cliente.contas) != 1:
        numero = int(input("Digite o numero de conta do cliente: "))
        for conta in cliente.contas:
            if conta.numero == numero:
                return conta
        print(f"não existe nenuma conta com o numero: {numero} pertecente ao cliente {cliente.nome}")
        return None
    return cliente.contas[0]

main()