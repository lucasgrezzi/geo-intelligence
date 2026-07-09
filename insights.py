import pandas as pd

print("⏳ Carregando as previsões do modelo para gerar os leads comerciais...")
# 1. LER OS DADOS COM AS PREVISÕES DO DIA 4
df_previsoes = pd.read_csv("data/tb_gold_com_previsoes.csv")

# ==============================================================================
# 2. CÁLCULO DO GAP DE VENDAS (O RESIDUAL DE NEGÓCIO)
# ==============================================================================
# Oportunidade = Faturamento Real - Faturamento Previsto pelo Modelo
# Valores muito negativos indicam estabelecimentos subperformando drasticamente
df_previsoes["gap_faturamento"] = df_previsoes["volume_faturamento_vr"] - df_previsoes["faturamento_previsto_modelo"]

# Criamos também o Market Share estimado dele dentro do raio de 1km para dar mais argumento de vendas
faturamento_total_raio = df_previsoes["volume_faturamento_vr"].sum() # Simbolizando o bolo total da região
df_previsoes["market_share_estimado_porcento"] = round((df_previsoes["volume_faturamento_vr"] / faturamento_total_raio) * 100, 2)

# ==============================================================================
# 3. FILTRANDO OS TOP 5 LEADS PARA O TIME COMERCIAL (HUNTING / CROSS-SELLING)
# ==============================================================================
# Ordenamos do pior faturamento em relação ao potencial para o melhor faturamento
df_oportunidades = df_previsoes.sort_values(by="gap_faturamento", ascending=True)

# Selecionamos os top 5 que estão mais "comendo poeira" do mercado local
top_5_leads = df_oportunidades.head(5).copy()

# Transformamos o gap em um valor positivo absoluto apenas para exibição comercial
top_5_leads["faturamento_perdido"] = top_5_leads["gap_faturamento"].abs()

# ==============================================================================
# 4. SALVANDO A LISTA DE LEADS (Camada de Entrega / Output de Negócio)
# ==============================================================================
colunas_comerciais = [
    "estab_id", "nome", "categoria", "qtd_concorrentes_1km", 
    "volume_faturamento_vr", "faturamento_previsto_modelo", 
    "faturamento_perdido", "market_share_estimado_porcento"
]

df_leads_finais = top_5_leads[colunas_comerciais]
df_leads_finais.to_csv("data/tb_leads_comerciais_paulista.csv", index=False)

print("✅ Dia 5 concluído com sucesso! Lista de oportunidades gerada.")
print("\n🎯 --- TOP 5 RESTAURANTES PARA O TIME DE VENDAS ATACAR ---")
print("Estes estabelecimentos faturam MENOS do que o potencial do seu raio comercial indicou:")
print("-" * 90)

for idx, row in df_leads_finais.iterrows():
    print(f"Restaurante: {row['nome']} ({row['categoria']})")
    print(f"   -> Concorrentes diretos no raio: {row['qtd_concorrentes_1km']}")
    print(f"   -> Market Share na região: {row['market_share_estimado_porcento']}%")
    print(f"   -> Faturamento Real de VR: R$ {row['volume_faturamento_vr']:.2f}")
    print(f"   -> Quanto deveria faturar (Modelo): R$ {row['faturamento_previsto_modelo']:.2f}")
    print(f"   ⚠️ DINHEIRO DEIXADO NA MESA (Oportunidade): R$ {row['faturamento_perdido']:.2f}")
    print("-" * 90)