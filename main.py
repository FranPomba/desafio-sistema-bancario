menu_bancario = """
        ================== Bemvindo ao menu Bancario =================
        Selecione uma das opcoes
        [1] - Deposito
        [2] - Saque
        [3] - Consultar Extrato
        [4] - Criar Usuário
        [5] - Criar Conta Corrente
        [6] - Listar Contas
        [0] - Sair
        =>
    """

LIMITE_SAQUE = 3
AGENCIA = "0001"
usuarios = []
contas_corrente = []

def menu():
    saldo = 0
    numero_saque = 0
    limite_diario = 500
    operacoes = ""
    opcao = ""

    while opcao != "0":
        print(menu_bancario)
        opcao = input("")
        if opcao == "1":
            valor = float(input("Digite o valor do deposito: "))
            saldo, operacoes = deposito(saldo, valor, operacoes)
        elif opcao == "2":
            valor = float(input("Digite o valor do saque: "))
            saldo, operacoes, numero_saque = saque(saldo=saldo, valor=valor, operacoes=operacoes, numero_saque=numero_saque, limite_diario=limite_diario)
        elif opcao == "3":
            extrato(saldo, operacoes=operacoes)
        elif opcao == "4":
            criar_usuario(usuarios)
        elif opcao == "5":
            criar_conta_corrente(contas_corrente, usuarios)
        elif opcao == "6":
            listar_contas(contas_corrente)
        elif opcao == "0":
            print("Terminando o programa...")
        else:
            print("Operacao Invalida!!! Por favor selecione uma opcao valida.")


def deposito(saldo, valor, operacoes, /):    
    if valor < 0:
        print("Operacao Invalida!!!. Não é possivel realizar deposito de valor negativo")
        return saldo, operacoes
    saldo += valor
    operacoes += f"Deposito no valor: R$ {valor:.2f} \n"
    print(f"operacao realizada com sucesso!!! \n Saldo após o deposito R$ {saldo:.2f}")
    return saldo, operacoes


def saque(*, saldo, valor, operacoes, numero_saque, limite_diario):
    if valor < 0:
        print("Operacao Invalida!!!. valor de saque tem de maior que 0")
        return saldo, operacoes, numero_saque
    if numero_saque == LIMITE_SAQUE:
        print("Operacao Invalida!!!. Excedeu o limite de saques")
        return saldo, operacoes, numero_saque
    if valor > limite_diario:
        print("Operacao Invalida!!!. Valor de saque excede o limite diario")
        return saldo, operacoes, numero_saque
    if valor > saldo:
        print(f"Operacao Invalida!!!. O valor de saque excede o seu saldo atual R$ {saldo:.2f}")
        return saldo, operacoes, numero_saque

    saldo -= valor
    operacoes += f"Saque no valor de R${valor:.2f}\n"
    numero_saque += 1
    print(f"operacao realizada com sucesso!!! \n Saldo após o saque R${saldo}")
    return saldo, operacoes, numero_saque

def extrato(saldo, / , * , operacoes):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not operacoes else operacoes)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios:list):
    print("\n================ Criar Usuário ================")
    cpf = input("Digite o cpf (apenas  numero): ")
    if buscar_usuario(cpf, usuarios) == None:
        nome =  input("Digite o nome: ")
        data_nascimento = input("Digite a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Digite o indereço: ")
        usuarios.append({"nome": nome, "cpf": cpf, 
                         "data_nascimento": data_nascimento,
                         "endereco": endereco})
        print(f"Usuário {nome} cadastrado com sucesso")
    else:
        print(f"usuário com cpf: {cpf} já cadastrado no sistema")

def buscar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if cpf == usuario["cpf"]:
            return usuario
    return None

def criar_conta_corrente(contas_corrente, usuarios):
    print("\n================ Criar Conta Corrente ================")
    cpf = input("Digite o cpf: ")
    usuario =  buscar_usuario(cpf, usuarios)
    if usuario != None:
        numero_conta = len(contas_corrente) + 1
        contas_corrente.append({"agencia": AGENCIA,
                                      "numero_conta": numero_conta,
                                      "usuario": usuario})
        print(f"Conta de {usuario["nome"]} criada com sucesso")
        return
    print(f"cpf não encontrado no sistema. por favor cadastre o usuário")

def listar_contas(contas_corrente):
    print("\n================ Lista de Contas Correntes ================")
    if len(contas_corrente) == 0:
        print("não existe nenhuma conta cadastrada no momento")
        return
    for conta in contas_corrente:
        print(f"""
              \tAgencia Nº: {conta["agencia"]}
              \tConta Nº: {conta["numero_conta"]}
              \tNome do titular: {conta["usuario"]["nome"]}
              \tEndereço: {conta["usuario"]["endereco"]}
              """)
        print("=========================================================")    

menu()
