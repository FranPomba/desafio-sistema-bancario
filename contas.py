from cliente import Cliente
from transacao import Historico, datetime


class Conta:
    def __init__(self, cliente, numero, saldo=0.0, agencia="0001"):
        self._saldo = saldo
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
    def nova_conta(cls, cliente: Cliente, numero):
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
            f"operacao realizada com sucesso!!! \n Saldo após o saque R${self._saldo}"
        )
        return True

    def depositar(self, valor):
        if valor < 0:
            print("Operação Invalida! Valor de deposito tem de ser maior que 0")
            return False
        self._saldo += valor
        print(
            f"operacao realizada com sucesso!!! \n Saldo após o deposito R${self._saldo}"
        )
        return True


class ContaCorrente(Conta):
    def __init__(self, saldo, numero, limite=500, limite_saques=3):
        self._limite = limite
        self._limite_saques = limite_saques
        super().__init__(saldo, numero)

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
            if transacao["tipo" == "Saque"]
        ]
        if len(lista_saques) > self.limite_saques:
            print("Operação invalida! limite de saques excedido.")
            return
        if valor > self.limite:
            print("Operação invalida! O valor excede o limite máximo de saques")
            return
        return super().sacar(valor)
