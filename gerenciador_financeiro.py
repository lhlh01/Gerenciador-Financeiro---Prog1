import csv
import os
from datetime import datetime

ARQUIVO = "transacoes.csv"

ORCAMENTOS = {
    "Alimentacao": 500.00,
    "Transporte": 300.00,
    "Lazer": 200.00,
    "Contas": 1000.00
}

# Garante que o arquivo exista com cabecalho
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["data", "tipo", "categoria", "valor", "descricao"])


def ler_transacoes():
    lista = []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        leitor = csv.reader(f)
        next(leitor)  # pula o cabecalho
        for linha in leitor:
            lista.append(linha)
    return lista


def salvar_transacoes(lista):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["data", "tipo", "categoria", "valor", "descricao"])
        for linha in lista:
            escritor.writerow(linha)


def adicionar_movimentacao():
    print("\n--- Nova Movimentacao ---")

    tipo_op = input("Tipo (1 - Receita / 2 - Despesa): ").strip()
    if tipo_op == "1":
        tipo = "Receita"
    else:
        tipo = "Despesa"

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

    # Verifica orcamento se for despesa
    if tipo == "Despesa" and categoria in ORCAMENTOS:
        mes_atual = datetime.now().strftime("%Y-%m")
        total_gasto = 0.0
        for linha in ler_transacoes():
            if linha[1] == "Despesa" and linha[2] == categoria and linha[0].startswith(mes_atual):
                total_gasto = total_gasto + float(linha[3])

        limite = ORCAMENTOS[categoria]
        if total_gasto + valor > limite:
            print("\n[ALERTA] Este gasto vai estourar o orcamento de " + categoria + "!")
            print("Limite: R$ " + str(limite) + " | Ja gasto: R$ " + str(round(total_gasto, 2)))

    confirmar = input("\nConfirmar? (s/n): ").strip().lower()
    if confirmar == "s":
        lista = ler_transacoes()
        lista.append([data, tipo, categoria, str(valor), descricao])
        salvar_transacoes(lista)
        print("Movimentacao salva com sucesso!")


def listar_e_deletar():
    lista = ler_transacoes()

    if len(lista) == 0:
        print("\nNenhuma transacao encontrada.")
        return

    print("\n--- Lista de Transacoes ---")
    i = 0
    while i < len(lista):
        linha = lista[i]
        print("[" + str(i) + "] " + linha[0] + " | " + linha[1] + " | " + linha[2] + " | R$ " + linha[3] + " | " + linha[4])
        i = i + 1

    opcao = input("\nDigite o numero para deletar ou 'n' para voltar: ").strip()
    if opcao != "n":
        try:
            idx = int(opcao)
            if idx >= 0 and idx < len(lista):
                removida = lista.pop(idx)
                salvar_transacoes(lista)
                print("Transacao removida: " + removida[4])
            else:
                print("Indice invalido.")
        except:
            print("Opcao invalida.")


def gerar_relatorio():
    lista = ler_transacoes()

    total_receitas = 0.0
    total_despesas = 0.0
    gastos_por_cat = {}

    for linha in lista:
        if linha[1] == "Receita":
            total_receitas = total_receitas + float(linha[3])
        else:
            total_despesas = total_despesas + float(linha[3])
            cat = linha[2]
            if cat not in gastos_por_cat:
                gastos_por_cat[cat] = 0.0
            gastos_por_cat[cat] = gastos_por_cat[cat] + float(linha[3])

    saldo = total_receitas - total_despesas

    print("\n======================================")
    print("       RELATORIO FINANCEIRO GERAL     ")
    print("======================================")
    print("Total Receitas: R$ " + str(round(total_receitas, 2)))
    print("Total Despesas: R$ " + str(round(total_despesas, 2)))
    print("Saldo Atual   : R$ " + str(round(saldo, 2)))
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


# --- Menu principal ---
# Garante que o arquivo exista ao iniciar
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["data", "tipo", "categoria", "valor", "descricao"])

while True:
    print("\n=== GERENCIADOR FINANCEIRO PESSOAL ===")
    print("1. Adicionar Movimentacao")
    print("2. Ver / Remover Movimentacoes")
    print("3. Relatorio e Grafico de Gastos")
    print("4. Sair")

    opcao = input("Escolha uma opcao: ").strip()

    if opcao == "1":
        adicionar_movimentacao()
    elif opcao == "2":
        listar_e_deletar()
    elif opcao == "3":
        gerar_relatorio()
    elif opcao == "4":
        print("\nAte logo! Mantenha suas financas sob controle.")
        break
    else:
        print("Opcao invalida! Tente novamente.")
