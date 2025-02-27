import pandas as pd

# 🔹 Carregar o dataset
file_path = "amazon.csv"  # Certifique-se de que o arquivo está no mesmo diretório do script
df = pd.read_csv(file_path)

# 🔹 Remover duplicatas para garantir IDs únicos
df = df.drop_duplicates(subset=["product_id"], keep="first")  # Mantém apenas um produto único
df = df.drop_duplicates(subset=["user_id"], keep="first")  # Mantém apenas um usuário único

# 🔹 Salvar o novo CSV sem duplicatas
df.to_csv("amazon_clean.csv", index=False)

print("✅ Duplicatas removidas com sucesso! Apenas uma ocorrência por 'product_id', 'user_id' e 'review_id' foi mantida.")
