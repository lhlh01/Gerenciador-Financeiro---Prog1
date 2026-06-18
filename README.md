Gerenciador Financeiro Pessoal

Integrante:

Luana Maria Carvalho da Silva Hildever

Descrição do Projeto

Sistema para registrar receitas e despesas pessoais via terminal. O usuário pode lançar movimentações com data, categoria, valor e descrição. O programa calcula o saldo, emite alertas quando o orçamento de uma categoria é estourado, e gera um relatório dos gastos por categoria. Os dados são salvos em arquivo CSV.

Instruções de Execução

Pré-requisitos: Python 3 instalado na máquina.

1. Faça o download ou clone este repositório
2. Abra o terminal na pasta do projeto
3. Execute o comando: "python gerenciador_financeiro.py"
4. Use o menu numérico para navegar pelas opções

O arquivo "transacoes.csv" será criado automaticamente na primeira execução, caso ele não exista.

Bibliotecas Utilizadas:
csv: serve para a leitura e escrita do arquivo de transações
os: serve para verificar se o arquivo csv já existe
datetime: serve para obter a data atual e também filtrar as transações por mês

Obs: Como todas são bibliotecas padrão do Python, nenhuma instalação adicional é necessária.

Funcionalidades

- Adicionar receitas e despesas com data, categoria, valor e descrição
- Alerta automático ao estourar o orçamento mensal de uma categoria
- Listar e remover transações registradas
- Relatório geral com total de receitas, despesas e saldo
- Dados salvos em "transacoes.csv" 

Divisão de Responsabilidade

A integrante Luana Maria Carvalho da Silva Hildever (eu), desenvolveu o projeto por completo (estrutura do código, leitura/escrita em CSV, lógica de orçamento, relatório e etc)

Obs: Os valores incluidos no financeiro são meramente ilustrativos, servindo apenas para exemplificar o funcionamento do gerenciador.
