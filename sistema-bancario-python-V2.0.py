import random

# Função para criar um novo usuário
def criar_usuario(nome, data_nascimento, cpf, endereco, usuarios):
    cpf = cpf.replace(".", "").replace("-", "")  # Remove caracteres não numéricos
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("Usuário já cadastrado com esse CPF.")
        return None
    usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    }
    usuarios.append(usuario)
    print(f"Usuário {nome} cadastrado com sucesso!")
    return usuario

# Função para criar uma nova conta corrente
def criar_conta_corrente(usuario, contas):
    numero_conta = len(contas) + 1
    conta = {
        'agencia': '0001',
        'numero': numero_conta,
        'usuario': usuario
    }
    contas.append(conta)
    print(f"Conta corrente número {numero_conta} criada com sucesso para o usuário {usuario['nome']}!")

# Função de depósito
def depositar(saldo, valor, extrato):
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    return saldo, extrato

# Função de saque
def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente. 😢")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite. 💸")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido. 🚫")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato, numero_saques

# Função de extrato
def extrato(saldo, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Função para calcular bônus
def bonus(saldo):
    if saldo >= 1000:
        valor_bonus = random.uniform(10, 50)
        print(f"\nParabéns! Você ganhou um bônus de R$ {valor_bonus:.2f} por ter mais de R$1000 na conta!")
        return valor_bonus
    return 0

# Listas para armazenar usuários e contas
usuarios = []
contas = []

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[c] Consultar Saldo
[r] Reiniciar Conta
[n] Novo Usuário
[b] Nova Conta Corrente
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            saldo, extrato = depositar(saldo, valor, extrato)
            saldo += bonus(saldo)  # Aplicando o bônus
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato, numero_saques = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES)

    elif opcao == "e":
        extrato(saldo, extrato=extrato)

    elif opcao == "c":
        print(f"\nSeu saldo atual é de: R$ {saldo:.2f}")

    elif opcao == "r":
        confirmar = input("Tem certeza que deseja reiniciar a conta? [s/n]: ")
        if confirmar == "s":
            saldo = 0
            extrato = ""
            numero_saques = 0
            print("Conta reiniciada com sucesso!")
        else:
            print("Reinicialização cancelada.")

    elif opcao == "n":
        nome = input("Informe o nome do usuário: ")
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        cpf = input("Informe o CPF (apenas números): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        criar_usuario(nome, data_nascimento, cpf, endereco, usuarios)

    elif opcao == "b":
        cpf = input("Informe o CPF do usuário para criar a conta (apenas números): ")
        usuario = next((u for u in usuarios if u['cpf'] == cpf), None)
        if usuario:
            criar_conta_corrente(usuario, contas)
        else:
            print("Usuário não encontrado.")

    elif opcao == "q":
        print("Saindo... Volte sempre! 👋")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
