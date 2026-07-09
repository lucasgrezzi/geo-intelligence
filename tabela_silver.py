import pandas as pd
import numpy as np

# ==============================================================================
# 1. LEITURA DOS DADOS (Camada Bronze Local)
# ==============================================================================
print("⏳ Carregando os dados do Dia 1...")
df_estabelecimentos = pd.read_csv("data/tb_estabelecimentos.csv")
df_transacoes = pd.read_csv("data/tb_transacoes.csv")

# ==============================================================================
# 2. FUNÇÃO HAVERSINE (Cálculo de Distância Geográfica)
# ==============================================================================
def calcular_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula a distância em quilômetros entre dois pontos na Terra
    usando as coordenadas de latitude e longitude.
    """
    # Raio da Terra em quilômetros
    R = 6371.0
    
    # Convertendo graus para radianos
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Diferenças das coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Fórmula de Haversine
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return R * c

# ==============================================================================
# 3. MAPEANDO A CONCORRÊNCIA NO RAIO DE 1 KM
# ==============================================================================
print("🛰️ Calculando a densidade de concorrentes por raio (1 km)...")

contagem_concorrentes = []

# Loop par a par (compara cada restaurante com todos os outros)
for index_foco, row_foco in df_estabelecimentos.iterrows():
    concorrentes_no_raio = 0
    
    for index_comp, row_comp in df_estabelecimentos.iterrows():
        # Não comparar o restaurante com ele mesmo
        if row_foco['estab_id'] == row_comp['estab_id']:
            continue
            
        # Regra de Negócio: Só é concorrente se for da MESMA categoria
        if row_foco['categoria'] == row_comp['categoria']:
            # Calcula a distância entre o restaurante foco e o restaurante comparado
            distancia = calcular_haversine(
                row_foco['latitude'], row_foco['longitude'],
                row_comp['latitude'], row_comp['longitude']
            )
            
            # Se estiver dentro do raio de 1 km, conta como concorrente
            if distancia <= 1.0:
                concorrentes_no_raio += 1
                
    contagem_concorrentes.append({
        "estab_id": row_foco['estab_id'],
        "qtd_concorrentes_1km": concorrentes_no_raio
    })

# Transforma a lista de resultados em um DataFrame
df_recursos_geograficos = pd.DataFrame(contagem_concorrentes)

# ==============================================================================
# 4. SALVANDO NA CAMADA SILVER (Dados Processados)
# ==============================================================================
# Junta a contagem de concorrentes de volta na tabela original de estabelecimentos
df_silver_estabelecimentos = pd.merge(df_estabelecimentos, df_recursos_geograficos, on="estab_id", how="left")

# Salva o resultado na nova camada do nosso "Data Lake" local
df_silver_estabelecimentos.to_csv("data/tb_silver_estabelecimentos.csv", index=False)

print("✅ Dia 2 concluído com sucesso! Tabela Silver gerada.")
print("\n--- Amostra dos dados com a nova Feature Geográfica ---")
print(df_silver_estabelecimentos[['estab_id', 'nome', 'categoria', 'qtd_concorrentes_1km']].head(5))