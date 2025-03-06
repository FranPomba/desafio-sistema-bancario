from abc import ABC, abstractmethod
from contas import Conta
from datetime import datetime

class Transacao(ABC):
    
    
    @abstractmethod
    def registrar(self, conta: Conta):
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
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y  %H:%M:%s")  
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