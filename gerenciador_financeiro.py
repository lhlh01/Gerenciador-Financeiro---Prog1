# Projeto de Programação 1 - Gerenciador Financeiro Pessoal - Luana Maria Carvalho da Silva Hildever

import csv # o csv serve para ler e escrever arquivos no formato CSV (planilha de texto).
import os # o "os" serve para interagir com o sistema operacional, como verificar se um arquivo já existe no computador
from datetime import datetime # "datetime" serve para pegar a data e hora atual do sistema.


ARQUIVO = "transacoes.csv"

ORCAMENTOS = {
    "Alimentacao": 500.00,
    "Transporte": 300.00,
    "Lazer": 200.00,
    "Contas": 1000.00
}



if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["data", "categoria", "valor", "descricao"])


def ler_transacoes():
    lista = []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        leitor = csv.reader(f)
        next(leitor)
        for linha in leitor:
            lista.append(linha)
    return lista


def salvar_transacoes(lista):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["data", "categoria", "valor", "descricao"])
        for linha in lista:
            escritor.writerow(linha)

def adicionar_despesa():
    print("\n--- Nova Despesa ---")

    print("Categorias:", ", ".join(ORCAMENTOS.keys()))
    categoria = input("Categoria: ").strip().capitalize()

    valor_str = input("Valor (R$): ").strip()
    try:
        valor = float(valor_str)
    except:
        print("Valor invalido!")
        return

    descricao = input("Descricao: ").strip()
    data = input("Data (AAAA-MM-DD) ou Enter para hoje: ").strip()
    if data == "":
        data = datetime.now().strftime("%Y-%m-%d")

    # verifica o orcamento se a categoria existir no dicionario
    if categoria in ORCAMENTOS:
        mes_atual = datetime.now().strftime("%Y-%m")
        total_gasto = 0.0
        for linha in ler_transacoes():
            if linha[1] == categoria and linha[0].startswith(mes_atual):
                total_gasto = total_gasto + float(linha[2])

        limite = ORCAMENTOS[categoria]
        if total_gasto + valor > limite:
            print("\n[ALERTA] Este gasto vai estourar o orcamento de " + categoria + "!")
            print("Limite: R$ " + str(limite) + " | Ja gasto: R$ " + str(round(total_gasto, 2)))

    confirmar = input("\nConfirmar? (s/n): ").strip().lower()
    if confirmar == "s":
        lista = ler_transacoes()
        lista.append([data, categoria, str(valor), descricao])
        salvar_transacoes(lista)
        print("Despesa salva com sucesso!")

def listar_e_deletar():
    lista = ler_transacoes()

    if len(lista) == 0:
        print("\nNenhuma despesa encontrada.")
        return

    print("\n--- Lista de Despesas ---")
    i = 0
    while i < len(lista):
        linha = lista[i]
        print("[" + str(i) + "] " + linha[0] + " | " + linha[1] + " | R$ " + linha[2] + " | " + linha[3])
        i = i + 1

    opcao = input("\nDigite o numero para deletar ou 'n' para voltar: ").strip()
    if opcao != "n":
        try:
            idx = int(opcao)
            if idx >= 0 and idx < len(lista):
                removida = lista.pop(idx)
                salvar_transacoes(lista)
                print("Despesa removida: " + removida[3])
            else:
                print("Indice invalido.")
        except:
            print("Opcao invalida.")


def gerar_relatorio():
    lista = ler_transacoes()

    total_despesas = 0.0
    gastos_por_cat = {}

    for linha in lista:
        total_despesas = total_despesas + float(linha[2])
        cat = linha[1]
        if cat not in gastos_por_cat:
            gastos_por_cat[cat] = 0.0
        gastos_por_cat[cat] = gastos_por_cat[cat] + float(linha[2])

    # soma todos os limites do dicionario para ter o orcamento total
    total_orcamento = 0.0
    for cat in ORCAMENTOS:
        total_orcamento = total_orcamento + ORCAMENTOS[cat]

    saldo = total_orcamento - total_despesas

    print("\n======================================")
    print("       RELATORIO FINANCEIRO GERAL     ")
    print("======================================")
    print("Orcamento Total: R$ " + str(round(total_orcamento, 2)))
    print("Total Despesas : R$ " + str(round(total_despesas, 2)))
    print("Saldo Restante : R$ " + str(round(saldo, 2)))
    print("======================================")

    if len(gastos_por_cat) > 0:
        print("\nGrafico de Gastos por Categoria:")
        maior = 0.0
        for cat in gastos_por_cat:
            if gastos_por_cat[cat] > maior:
                maior = gastos_por_cat[cat]

        for cat in gastos_por_cat:
            valor_cat = gastos_por_cat[cat]
            if maior > 0:
                tamanho = int((valor_cat / maior) * 20)
            else:
                tamanho = 0
            barra = "=" * tamanho
            print(cat + " | " + barra + " R$ " + str(round(valor_cat, 2)))

    print("======================================")


if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["data", "categoria", "valor", "descricao"])

while True:
    print("\n=== GERENCIADOR FINANCEIRO PESSOAL ===")
    print("1. Adicionar Despesa")
    print("2. Ver / Remover Despesas")
    print("3. Relatorio e Grafico de Gastos")
    print("4. Sair")

    opcao = input("Escolha uma opcao: ").strip()

    if opcao == "1":
        adicionar_despesa()
    elif opcao == "2":
        listar_e_deletar()
    elif opcao == "3":
        gerar_relatorio()
    elif opcao == "4":
        print("\nAte logo!")
        break
    else:
        print("Opcao invalida! Tente novamente.")
