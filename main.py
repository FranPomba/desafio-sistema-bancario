menu_bancario = """
        ================== Bemvindo ao menu Bancario =================
        Selecione uma das opcoes
        [1] - Deposito
        [2] - Saque
        [3] - Consultar Extrato
        [0] - Sair
        =>
    """
saldo = 0
LIMITE_SAQUE = 3
numero_saque = 0
limite_diario = 500
operacoes = ""
opcao = ""

def opcao_menu(opcao):
    valor = 0
    if opcao == "1":
        valor = int(input("Digite o valor do deposito: "))
        deposito(valor)
    elif opcao == "2":
        valor = int(input("Digite o valor do saque: "))
        saque(valor)
    elif opcao == "3":
        extrato()
    elif opcao == "0":
        print("Terminando o programa...")
    else:
        print("Operacao Invalida!!! Por favor selecione uma opcao valida.")


def deposito(valor):
    global saldo, operacoes
    
    if valor < 0:
        print("Operacao Invalida!!!. Não é possivel realizar deposito de valor negativo")
        return
    saldo += valor
    operacoes += f"Deposito no valor: R$ {valor} \n"
    print(f"operacao realizada com sucesso!!! \n Saldo após o deposito R$ {saldo}")


def saque(valor):
    global saldo, operacoes, numero_saque, limite_diario
    
    if valor < 0:
        print("Operacao Invalida!!!. valor de saque tem de maior que 0")
        return
    if numero_saque == LIMITE_SAQUE:
        print("Operacao Invalida!!!. Excedeu o limite de saques")
        return
    if valor > limite_diario:
        print("Operacao Invalida!!!. Valor de saque excede o limite diario")
        return
    if valor > saldo:
        print(f"Operacao Invalida!!!. O valor de saque excede o seu saldo atual R$ {saldo}")
        return

    saldo -= valor
    operacoes += f"Saque no valor de R${valor}\n"
    numero_saque += 1
    limite_diario -= valor
    print(f"operacao realizada com sucesso!!! \n Saldo após o saque R${saldo}")

def extrato():
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not operacoes else operacoes)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


while opcao != "0":
    print(menu_bancario)
    opcao = input()
    opcao_menu(opcao)
