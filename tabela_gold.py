import pandas as pd
import os

print("⏳ Carregando as tabelas para estruturar a Camada Gold...")
# 1. LER OS ARQUIVOS DAS CAMADAS ANTERIORES
df_silver_estab = pd.read_csv("data/tb_silver_estabelecimentos.csv")
df_bronze_transacoes = pd.read_csv("data/tb_transacoes.csv")

# ==============================================================================
# 2. CRUZAMENTO DOS DADOS (JOIN)
# ==============================================================================
print("🔗 Cruzando dados de geolocalização com faturamento de VR...")
# Unifica as informações de localização e concorrência com o faturamento real do restaurante
df_gold = pd.merge(df_silver_estab, df_bronze_transacoes, on="estab_id", how="inner")

# ==============================================================================
# 3. ENGENHARIA DE FEATURES AVANÇADA (Visão de Mercado)
# ==============================================================================
print("📊 Calculando métricas de benchmark por categoria...")

# Vamos calcular o faturamento médio de cada categoria (ex: média de todas as pizzarias)
# Isso ajuda o modelo de ML a entender o patamar financeiro de cada tipo de negócio
media_por_categoria = df_gold.groupby("categoria")["volume_faturamento_vr"].mean().reset_index()
media_por_categoria.rename(columns={"volume_faturamento_vr": "faturamento_medio_categoria"}, inplace=True)

# Cruza essa métrica de volta na tabela Gold
df_gold = pd.merge(df_gold, media_por_categoria, on="categoria", how="left")

# ==============================================================================
# 4. SALVANDO A TABELA GOLD FINAL
# ==============================================================================
# Filtrando e ordenando as colunas para o modelo de Machine Learning do Dia 4
colunas_finais = [
    "estab_id", "cnpj", "nome", "categoria", 
    "latitude", "longitude", "qtd_concorrentes_1km", 
    "faturamento_medio_categoria", "volume_faturamento_vr"
]

df_gold = df_gold[colunas_finais]

# Salva o arquivo final pronto para o modelo
df_gold.to_csv("data/tb_gold_analytics.csv", index=False)

print("✅ Dia 3 concluído com sucesso! Tabela Gold gerada e pronta para o Machine Learning.")
print("\n--- Estrutura Final da Tabela Gold (Pronta para o Modelo) ---")
print(df_gold[['nome', 'categoria', 'qtd_concorrentes_1km', 'faturamento_medio_categoria', 'volume_faturamento_vr']].head(5))