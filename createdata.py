import os
import random
import pandas as pd

# Coordenadas centrais da Av. Paulista para balizar nossa geolocalização
LAT_CENTRO = -23.5614
LON_CENTRO = -46.6559

categorias = ["Self-Service", "Pizzaria", "Hamburgueria", "Japonês", "Cafeteria"]
nomes_restaurantes = ["Sabor do Ponto", "Bella Pizza", "Burger Master", "Sushi Zen", "Café Vintage", 
                      "Tempero da Villa", "Fornaria Paulista", "Artisan Burger", "Sakura Premium", "Grão Gourmet"]

dados_estabelecimentos = []

# 1. Gerando 50 estabelecimentos espalhados num raio próximo da Paulista
random.seed(42) 
for i in range(1, 51):
    estab_id = f"ESTAB_{i:03d}"
    cnpj = f"{random.randint(10000000, 99999999)}0001{random.randint(10, 99)}"
    nome = f"{random.choice(nomes_restaurantes)} {random.randint(1, 5)}"
    categoria = random.choice(categorias)
    
    # Pequena variação geográfica para simular ruas paralelas e travessas
    lat = LAT_CENTRO + random.uniform(-0.015, 0.015)
    lon = LON_CENTRO + random.uniform(-0.015, 0.015)
    
    dados_estabelecimentos.append({
        "estab_id": estab_id, 
        "cnpj": cnpj, 
        "nome": nome, 
        "categoria": categoria, 
        "latitude": lat, 
        "longitude": lon
    })

df_estabelecimentos = pd.DataFrame(dados_estabelecimentos)

# 2. Gerando dados de transações com uma lógica de negócio real para o modelo aprender
dados_transacoes = []
for estab in dados_estabelecimentos:
    estab_id = estab["estab_id"]
    categoria = estab["categoria"]
    
    # Criamos um faturamento base fixo por categoria de restaurante
    base_faturamento = {
        "Japonês": 65000.0,
        "Pizzaria": 45000.0,
        "Hamburgueria": 40000.0,
        "Self-Service": 30000.0,
        "Cafeteria": 15000.0
    }
    
    faturamento_base = base_faturamento[categoria]
    
    # Adicionamos um ruído de mercado aleatório (uma variação natural de até 15%)
    ruido = random.uniform(-0.15, 0.15)
    volume_vr = round(faturamento_base * (1 + ruido), 2)
    
    dados_transacoes.append({
        "estab_id": estab_id, 
        "volume_faturamento_vr": volume_vr
    })

# CORREÇÃO: Transformando a lista de transações em DataFrame do Pandas
df_transacoes = pd.DataFrame(dados_transacoes)

# ==============================================================================
# 3. SALVANDO LOCALMENTE (Pasta data/)
# ==============================================================================
os.makedirs("data", exist_ok=True)

# Salva em formato CSV (simples, rápido e leve)
df_estabelecimentos.to_csv("data/tb_estabelecimentos.csv", index=False)
df_transacoes.to_csv("data/tb_transacoes.csv", index=False)

print("✅ Dia 1 concluído com Pandas com sucesso!")
print("Os arquivos foram salvos na pasta 'data/'")

# Exibe a prévia dos dados na tela para conferência
print("\n--- Prévia dos Estabelecimentos ---")
print(df_estabelecimentos.head(3))

print("\n--- Prévia das Transações (Lógica de Negócio Corrigida) ---")
print(df_transacoes.head(3))