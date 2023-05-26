# Problema de negócio

A Food Zone é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Food Zone, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

Fui contratado como Cientista de Dados para criar soluções de dados e ajudar o novo CEO a identificar os pontos chaves da empresa. Por isso, antes de treinar algoritimos, ele precisa ter os pricipais KPIs estratégicos organizados em uma única ferramenta, para poder consultar a qualquer momento.

Para entender melhor a empresa, tomar melhores decisões estratégicas e alavancar ainda mais o negócio o CEO me solicitou que seja feita uma análise nos dados da empresa e que sejam gerados alguns dashboards, para a partir dessas análises, responder as seguintes perguntas:

## Visão Geral

1. Quantos restaurantes únicos estão registrados?
2. Quantos países estão registrados?
3. Quantas cidades estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?
6. Um mapa, com a posição de cada restaurante.

## Visão Países

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Média de avaliações por restaurante em cada país
4. Preço médio para duas pessos por país

## Visão Cidades

1. Top 10 cidades com mais restaurantes
2. Top 7 cidades com mais restaurantes com nota maior a 4
3. Top 7 cidades com mais restaurantes com nota menos a 2,5
4. Top 10 cidades com maior diversidade de tipos de culinária

## Tipos de Culinária

1. Melhores restaurantes dentro dos principais tipos de culinária
2. Pricipais informações dos melhores restaurantes em todo o mundo
3. As 10 culinárias mais bem avaliadas
4. As 10 culinárias pior avaliadas

# Premissas assumidas para a análise

1. Marketplace foi o modelo de negócio assumido
2. As 3 principais visões de negócio foram:
    1. Visão dos paises
    2. Visão das cidades
    3. Visão dos tipos culinários
3. Os valores são convertidos da moeda local para dolar.

# Estratégia da solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 pricipais visões do modelo de negócio da empres:

### 1. Produto final

- Dashboard interativo com as análises solicitadas pelo CEO

### 2. Ferramentas

- Python
- VS Code
- Streamlit
- Git

# 3. Processo

- Foi feita a coleta dos dados no Kaggle
- Limpeza de valores nulos, erros e outliers
- Exploração inicial do dados
- Planejamento para a resposta das perguntas propostas no problema de negócio
- Responder as perguntas
- Desenvolvimento do dashboard e mapa interativo, integrando graficos com as respostas

### 

# 4. Top 3 Insights de dados

1. Dieferenta da hipótese inicial, os restaurantes mais caros estão em Singapura, não nos EUA
2. Paises onde a média de preço é menor, tendem a ser os com maior número de votos
3. As culinárias com maior número de restaurantes não estão entre as culinárias com a maior nota média.

# 5. Produto final

Painel online, hospedado em um Cloud e disponível para acesso em
qualquer dispositivo conectado à internet.
O painel pode ser acessado através desse link: https://food-zone.streamlit.app/

# 6. Conclusão

O objetivo desse projeto é criar um conjunto de gráficos e tabelas
que exibam essas métricas da melhor forma possível para o CEO.

Da visão da Empresa, podemos concluir que o maior número de restaurantes e usuários está na Ásia.

# 7. Próximos passos

- Criar novos filtros, para detalhar ainda mais a análise.
- Adiconar visões de negócios regionais
