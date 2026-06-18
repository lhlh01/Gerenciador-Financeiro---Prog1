# Gerenciador Financeiro Pessoal

## Integrantes

- Luana Maria Carvalho da Silva Hildever

## Descrição do Projeto

Sistema para registrar receitas e despesas pessoais via terminal. O usuário pode lançar movimentações com data, categoria, valor e descrição. O programa calcula o saldo, emite alertas quando o orçamento de uma categoria é estourado, e gera um relatório com gráfico ASCII dos gastos por categoria. Os dados são salvos em arquivo CSV para persistência entre sessões.

## Instruções de Execução

**Pré-requisitos:** Python 3 instalado na máquina.

1. Faça o download ou clone este repositório
2. Abra o terminal na pasta do projeto
3. Execute o comando:
   ```
   python gerenciador_financeiro.py
   ```
4. Use o menu numérico para navegar pelas opções

> O arquivo `transacoes.csv` será criado automaticamente na primeira execução, caso não exista.

## Bibliotecas Utilizadas

| Biblioteca | Uso |
|---|---|
| `csv` | Leitura e escrita do arquivo de transações |
| `os` | Verificar se o arquivo CSV já existe |
| `datetime` | Obter a data atual e filtrar transações por mês |

Todas são bibliotecas padrão do Python — nenhuma instalação adicional é necessária.

## Funcionalidades

- Adicionar receitas e despesas com data, categoria, valor e descrição
- Alerta automático ao estourar o orçamento mensal de uma categoria
- Listar e remover transações registradas
- Relatório geral com total de receitas, despesas, saldo e gráfico ASCII por categoria
- Dados salvos em `transacoes.csv` para persistência

## Divisão de Responsabilidades

| Integrante | Responsabilidades |
|---|---|
| Luana Maria Carvalho da Silva Hildever | Desenvolvimento completo do projeto: estrutura do código, leitura/escrita em CSV, lógica de orçamento, relatório e gráfico ASCII |
