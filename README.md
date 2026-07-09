```markdown
# 🛰️ Inteligência Geográfica de Vendas & Propensão de Faturamento VR

Este projeto desenvolve um pipeline de dados e um modelo preditivo de Machine Learning voltado para o setor de **Benefícios Corporativos (Vale-Refeição)**. O objetivo principal é identificar estabelecimentos credenciados que estão performando abaixo do potencial de sua região, gerando leads qualificados com argumentos consultivos para o time de vendas (*Hunting* e *Cross-selling*).

---

## 💼 O Desafio de Negócio

Em redes de benefícios (como Vale-Refeição), expandir ou manter a rede credenciada de forma cega gera ineficiência. Um restaurante parceiro pode estar transacionando muito menos do que o potencial geográfico do seu quarteirão sugere. 

A solução criada utiliza **Inteligência Espacial** e **Modelagem Preditiva** para calcular o "faturamento justo" de um estabelecimento com base em sua localização, concorrência e categoria. Ao comparar o faturamento real com o previsto pelo modelo, mapeamos o **Residual (Gap de Vendas)**, revelando quais parceiros estão deixando dinheiro na mesa e precisam de intervenção comercial (cupons, destaque no app, revisão de taxas ou combos).

---

## 🏗️ Arquitetura do Pipeline (Medalhão Local)

O projeto foi estruturado seguindo as boas práticas de engenharia de dados, dividindo as responsabilidades de processamento em camadas modulares:

```text
PROJ_DADOS/
│
├── data/                                 # Nosso "Data Lake" Local
│   ├── tb_estabelecimentos.csv           # Dados brutos de localização (Bronze)
│   ├── tb_transacoes.csv                 # Volume de faturamento bruto de VR (Bronze)
│   ├── tb_silver_estabelecimentos.csv    # Engenharia de Recursos Geográficos (Silver)
│   ├── tb_gold_analytics.csv             # Dados unificados e agregados (Gold)
│   ├── tb_gold_com_previsoes.csv         # Outputs da tabela Gold pós-Machine Learning
│   └── tb_leads_comerciais_paulista.csv  # Camada de entrega com os insights finais de negócio
│
├── createdata.py                         # Dia 1: Ingestão e simulação de dados de mercado
├── tabela_silver.py                      # Dia 2: Geoprocessamento e cálculo de raio (Haversine)
├── tabela_gold.py                        # Dia 3: Agregações, joins e benchmarks de categoria
├── modelo.py                             # Dia 4: Treinamento e validação do modelo de ML
└── insights.py                           # Dia 5: Geração de gaps de faturamento e leads comerciais

```

---

## 🛠️ Tecnologias Utilizadas

* **Python 3** como linguagem central do projeto.
* **Pandas** para manipulação de DataFrames e estruturação das camadas do pipeline.
* **NumPy** para operações matemáticas de alta performance.
* **Scikit-Learn** para pipeline de Machine Learning (tratamento categórico com *One-Hot Encoding*, divisão treino/teste e modelagem).
* **RandomForestRegressor** como algoritmo de regressão para estimar os faturamentos potenciais.

---

## 📈 Detalhes Técnico e Mapeamento por Etapas

### 1. Ingestão & Regras de Domínio (`createdata.py`)

Geração de dados sintéticos localizados na região da Avenida Paulista (São Paulo/SP). Os dados foram calibrados utilizando regras de domínio reais de mercado, indexando patamares financeiros lógicos para categorias distintas de culinária (ex: culinária Japonesa com ticket e faturamento base mais altos que Cafeterias), adicionando ruído natural de mercado.

### 2. Engenharia de Recursos Geográficos (`tabela_silver.py`)

Implementação da **Fórmula de Haversine** em Python para calcular a distância par a par considerando a curvatura da Terra. O script mapeia, de forma automatizada, a densidade competitiva de cada estabelecimento, gerando a feature `qtd_concorrentes_1km` apenas para concorrentes da mesma categoria.

### 3. Consolidação de Negócio (`tabela_gold.py`)

Realiza os cruzamentos (*joins*) entre dados espaciais e financeiros. Adiciona uma feature de benchmark setorial: o faturamento médio da categoria na região, servindo como uma linha de base crucial para o aprendizado do modelo.

### 4. Modelagem Preditiva com Machine Learning (`modelo.py`)

O modelo foi treinado separando 20% dos dados para validação em teste cego. O algoritmo alcançou métricas de alta performance para dados tabulares:

* **Coeficiente de Determinação ($R^2$): 0.85** (O modelo explica 85% da variabilidade do faturamento local).
* **Erro Médio Absoluto (MAE): R$ 5.437,05** (Margem de erro média das previsões de faturamento).

### 5. Geração de Valor Comercial (`insights.py`)

Etapa final que transforma predições em receita. Calcula o `gap_faturamento` ($Real - Previsto$). O script isola os estabelecimentos com maiores resíduos negativos, calculando o *Market Share* regional e gerando um relatório pronto de **Top 5 Oportunidades** para o time comercial agir imediatamente.

```

```