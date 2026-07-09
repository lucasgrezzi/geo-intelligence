import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

print("⏳ Carregando a Camada Gold e iniciando a esteira de Machine Learning...")
# 1. LER A TABELA GOLD
df_gold = pd.read_csv("data/tb_gold_analytics.csv")

# ==============================================================================
# 2. PRÉ-PROCESSAMENTO (Tratamento de Variáveis Categóricas)
# ==============================================================================
# O modelo não aceita texto ("Pizzaria", "Japonês"). Precisamos transformar em colunas numéricas (0 ou 1)
df_processado = pd.get_dummies(df_gold, columns=["categoria"], drop_first=False)

# Identifica quais são as novas colunas geradas pela categoria
colunas_categoria = [col for col in df_processado.columns if "categoria_" in col]

# Definição das variáveis preditoras (X) e a variável que queremos prever (y)
features = ["latitude", "longitude", "qtd_concorrentes_1km", "faturamento_medio_categoria"] + colunas_categoria
target = "volume_faturamento_vr"

X = df_processado[features]
y = df_processado[target]

# ==============================================================================
# 3. DIVISÃO EM TREINO E TESTE & TREINAMENTO DO MODELO
# ==============================================================================
print("🧠 Treinando o modelo de Regressão (Random Forest)...")

# Separamos 20% dos dados para testar se o modelo aprendeu bem e não apenas decorou
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Instancia e treina o algoritmo
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# ==============================================================================
# 4. AVALIAÇÃO DO MODELO & GERAÇÃO DAS PREVISÕES
# ==============================================================================
# Faz as previsões no conjunto de teste para validação
y_pred_test = modelo.predict(X_test)

mae = mean_absolute_error(y_test, y_pred_test)
r2 = r2_score(y_test, y_pred_test)

print(f"\n📊 Métricas de Validação do Modelo:")
print(f"   -> Erro Médio Absoluto (MAE): R$ {mae:.2f}")
print(f"   -> Coeficiente de Determinação (R²): {r2:.2f}")

# Agora, fazemos a previsão para a base INTEIRA para gerar o "Faturamento Potencial"
df_gold["faturamento_previsto_modelo"] = modelo.predict(X)

# ==============================================================================
# 5. SALVANDO OS RESULTADOS PREVISTOS
# ==============================================================================
# Salva o arquivo com as previsões acopladas
df_gold.to_csv("data/tb_gold_com_previsoes.csv", index=False)

print("\n✅ Dia 4 concluído com sucesso! Modelo treinado e previsões geradas.")
print("Dados salvos em 'data/tb_gold_com_previsoes.csv'")