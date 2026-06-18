# Projeto de Programação 1 - Gerenciador Financeiro Pessoal - Luana Maria Carvalho da Silva Hildever

import csv  # biblioteca para ler e escrever arquivos CSV
import os # biblioteca para verificar se arquivos existem no computador
from datetime import datetime # importa so a parte de data e hora da biblioteca

ARQUIVO = "transacoes.csv"  # nome do arquivo onde os dados ficam salvos

# dicionario com o limite de gasto mensal de cada categoria
ORCAMENTOS = {   
    "Alimentacao": 500.00,
    "Transporte": 300.00,
    "Lazer": 200.00,
    "Contas": 1000.00
}

# esse bloco cria o arquivo CSV caso ele ainda nao exista.
# ele usa os.path.exists() para verificar se o arquivo ja foi criado antes.
# se nao existir, abre o arquivo no modo escrita e usa csv.writer()
# para escrever a primeira linha com os nomes das colunas (cabecalho)

# verifica se o arquivo ainda nao existe
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f: # cria o arquivo
        escritor = csv.writer(f)  # prepara para escrever no formato CSV
        escritor.writerow(["data", "categoria", "valor", "descricao"])  # escreve o cabecalho

# essa funcao le o arquivo CSV e retorna todas as despesas em uma lista.
# ela abre o arquivo no modo leitura, usa csv.reader() para percorrer
# cada linha e vai guardando elas numa lista com append()
# o next() pula o cabecalho para nao incluir ele nos dados
# no final retorna a lista completa para quem chamou a funcao

# funcao que le as transacoes
def ler_transacoes():
    lista = [] # lista vazia que vai guardar todas as transacoes
    with open(ARQUIVO, "r", encoding="utf-8") as f: # abre o arquivo para leitura
        leitor = csv.reader(f)  # prepara para ler o arquivo CSV linha por linha
        next(leitor)  # pula a primeira linha porque ela e o cabecalho
        for linha in leitor: # percorre cada linha do arquivo
            lista.append(linha) # adiciona a linha na lista
    return lista # retorna a lista com todas as transacoes


# essa funcao recebe uma lista de despesas e salva ela no arquivo CSV.
# ela abre o arquivo no modo escrita, o que apaga tudo que tinha antes,
# reescreve o cabecalho e depois usa um for para escrever
# cada despesa da lista no arquivo linha por linha
def salvar_transacoes(lista):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:   # abre o arquivo para escrita, apagando o conteudo anterior
        escritor = csv.writer(f)  # prepara para escrever no formato CSV
        escritor.writerow(["data", "categoria", "valor", "descricao"]) # reescreve o cabecalho
        for linha in lista: # percorre cada transacao da lista
            escritor.writerow(linha) # escreve a transacao no arquivo


# essa funcao e responsavel por registrar uma nova despesa.
# ela pede ao usuario a categoria, o valor, a descricao e a data.
# usa try/except para evitar que o programa trave se o usuario
# digitar um valor invalido. antes de salvar, verifica se o gasto
# vai estourar o orcamento da categoria no mes atual somando
# todas as despesas da mesma categoria com um for.
# so salva a despesa se o usuario confirmar com "s"
def adicionar_despesa():
    print("\n--- Nova Despesa ---")

    print("Categorias:", ", ".join(ORCAMENTOS.keys()))  # mostra as categorias disponiveis
    categoria = input("Categoria: ").strip().capitalize() # pega a categoria e coloca a primeira letra maiuscula

    valor_str = input("Valor (R$): ").strip() # pega o valor digitado como texto
    try:
        valor = float(valor_str) # tenta converter o texto para numero decimal
    except:
        print("Valor invalido!") # se nao conseguir converter, avisa o usuario
        return # encerra a funcao sem salvar nada

    descricao = input("Descricao: ").strip() # pega a descricao da despesa
    data = input("Data (AAAA-MM-DD) ou Enter para hoje: ").strip() # pega a data
    if data == "":  # se o usuario nao digitou nada
        data = datetime.now().strftime("%Y-%m-%d") # usa a data de hoje automaticamente

    # so verifica o orcamento se a categoria existir no dicionario
    if categoria in ORCAMENTOS:
        mes_atual = datetime.now().strftime("%Y-%m")  # pega o mes atual no formato AAAA-MM
        total_gasto = 0.0 # começa o total zerado
        for linha in ler_transacoes(): # percorre todas as transacoes salvas
            if linha[1] == categoria and linha[0].startswith(mes_atual):  # filtra pela categoria e mes atual
                total_gasto = total_gasto + float(linha[2])  # soma o valor da despesa encontrada

        limite = ORCAMENTOS[categoria] # pega o limite do dicionario para essa categoria
        if total_gasto + valor > limite: # verifica se vai passar do limite
            print("\n[ALERTA] Este gasto vai estourar o orcamento de " + categoria + "!")
            print("Limite: R$ " + str(limite) + " | Ja gasto: R$ " + str(round(total_gasto, 2)))

    confirmar = input("\nConfirmar? (s/n): ").strip().lower() # pede confirmacao antes de salvar
    if confirmar == "s": # so salva se o usuario confirmar
        lista = ler_transacoes() # le as transacoes que ja existem no arquivo
        lista.append([data, categoria, str(valor), descricao]) # adiciona a nova despesa na lista
        salvar_transacoes(lista) # salva a lista atualizada no arquivo
        print("Despesa salva com sucesso!")


# essa funcao lista todas as despesas salvas e permite deletar uma delas.
# ela le as despesas com ler_transacoes() e usa um while para imprimir
# cada uma com seu numero na frente. depois pergunta se o usuario quer
# deletar alguma. se sim, usa pop() para remover da lista pelo indice
# e salva a lista atualizada no arquivo. usa try/except para evitar
# erro caso o usuario digite algo que nao seja numero
def listar_e_deletar():
    lista = ler_transacoes() # le todas as despesas do arquivo

    if len(lista) == 0: # verifica se a lista esta vazia
        print("\nNenhuma despesa encontrada.")
        return # encerra a funcao se nao tiver nada para mostrar

    print("\n--- Lista de Despesas ---")
    i = 0 # comeca o contador do while em zero
    while i < len(lista): # repete enquanto nao chegar no fim da lista
        linha = lista[i]  # pega a despesa na posicao i
        print("[" + str(i) + "] " + linha[0] + " | " + linha[1] + " | R$ " + linha[2] + " | " + linha[3]) # imprime a despesa
        i = i + 1 # avanca para a proxima posicao

    opcao = input("\nDigite o numero para deletar ou 'n' para voltar: ").strip()
    if opcao != "n":  # so tenta deletar se o usuario nao digitou 'n'
        try:
            idx = int(opcao) # converte a opcao para numero inteiro
            if idx >= 0 and idx < len(lista): # verifica se o numero existe na lista
                removida = lista.pop(idx) # remove a despesa da lista e guarda ela na variavel
                salvar_transacoes(lista) # salva a lista atualizada no arquivo
                print("Despesa removida: " + removida[3]) # mostra o nome da despesa removida
            else:
                print("Indice invalido.") # avisa se o numero nao existe na lista
        except:
            print("Opcao invalida.") # avisa se o usuario digitou algo que nao e numero


# essa funcao gera um relatorio com o resumo financeiro do usuario.
# ela percorre todas as despesas com um for, somando o total gasto
# e agrupando os valores por categoria num dicionario.
# depois soma todos os limites do dicionario ORCAMENTOS para calcular
# o orcamento total e subtrai as despesas para obter o saldo restante.
# por fim, desenha um grafico de barras em ASCII onde o tamanho de cada
# barra e proporcional ao maior gasto entre as categorias, usando
# o operador * para repetir o caractere "=" e formar a barra
def gerar_relatorio():
    lista = ler_transacoes()  # le todas as despesas do arquivo

    total_despesas = 0.0 # variavel para somar todas as despesas
    gastos_por_cat = {} # dicionario para guardar o total gasto em cada categoria

    for linha in lista: # percorre cada despesa
        total_despesas = total_despesas + float(linha[2]) # soma o valor no total geral
        cat = linha[1]  # pega o nome da categoria dessa despesa
        if cat not in gastos_por_cat:  # se a categoria ainda nao esta no dicionario
            gastos_por_cat[cat] = 0.0 # cria ela com valor zero
        gastos_por_cat[cat] = gastos_por_cat[cat] + float(linha[2]) # soma o valor na categoria

    # soma todos os limites do dicionario para ter o orcamento total
    total_orcamento = 0.0
    for cat in ORCAMENTOS:  # percorre cada categoria do dicionario de orcamentos
        total_orcamento = total_orcamento + ORCAMENTOS[cat]  # soma o limite de cada categoria

    saldo = total_orcamento - total_despesas # calcula quanto ainda sobra do orcamento

    print("\n======================================")
    print("       RELATORIO FINANCEIRO GERAL     ")
    print("======================================")
    print("Orcamento Total: R$ " + str(round(total_orcamento, 2))) # mostra o orcamento total
    print("Total Despesas : R$ " + str(round(total_despesas, 2)))  # mostra o total gasto
    print("Saldo Restante : R$ " + str(round(saldo, 2)))  # mostra quanto ainda sobra
    print("======================================")

    if len(gastos_por_cat) > 0: # so mostra o grafico se tiver pelo menos uma despesa
        print("\nGrafico de Gastos por Categoria:")
        maior = 0.0 # variavel para guardar o maior gasto entre as categorias
        for cat in gastos_por_cat: # percorre o dicionario para achar o maior valor
            if gastos_por_cat[cat] > maior: # se o valor dessa categoria for maior que o atual maior
                maior = gastos_por_cat[cat] # atualiza o maior

        # percorre de novo para desenhar as barras
        for cat in gastos_por_cat:
            valor_cat = gastos_por_cat[cat] # pega o total gasto nessa categoria
            if maior > 0:
                tamanho = int((valor_cat / maior) * 20)  # calcula quantos "=" a barra vai ter (maximo 20
            else:
                tamanho = 0
            barra = "=" * tamanho # cria a barra repetindo o caractere "="
            print(cat + " | " + barra + " R$ " + str(round(valor_cat, 2))) # imprime a barra

    print("======================================")

# esse bloco e o menu principal do programa. ele usa um while True para
# ficar mostrando as opcoes repetidamente ate o usuario escolher sair.
# usa if/elif/else para identificar qual opcao foi digitada e chamar
# a funcao correspondente. o break na opcao 4 encerra o loop e finaliza
# o programa
if not os.path.exists(ARQUIVO):  # verifica de novo se o arquivo existe antes de comecar o menu
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f: # cria o arquivo se nao existir
        escritor = csv.writer(f)
        escritor.writerow(["data", "categoria", "valor", "descricao"])  # escreve o cabecalho

while True: # loop infinito que so para quando o usuario escolher sair
    print("\n=== GERENCIADOR FINANCEIRO PESSOAL ===")
    print("1. Adicionar Despesa")
    print("2. Ver / Remover Despesas")
    print("3. Relatorio e Grafico de Gastos")
    print("4. Sair")

    opcao = input("Escolha uma opcao: ").strip()  # pega a opcao digitada e remove espacos

    if opcao == "1":
        adicionar_despesa()  # chama a funcao de adicionar despesa
    elif opcao == "2":
        listar_e_deletar() # chama a funcao de listar e deletar
    elif opcao == "3":
        gerar_relatorio() # chama a funcao de gerar relatorio
    elif opcao == "4":
        print("\nAte logo!")
        break # encerra o loop e finaliza o programa
    else:
        print("Opcao invalida! Tente novamente.") # avisa se a opcao nao existe
