import pandas as pd

#  Carregar o dataset
file_path = "amazon.csv"  
df = pd.read_csv(file_path)

# Remover valores de ids que estejam repetidos mantendo apenas o primeiro encontrado
df = df.drop_duplicates(subset=["product_id"], keep="first")  # Mantém apenas um produto único
df = df.drop_duplicates(subset=["user_id"], keep="first")  # Mantém apenas um usuário único
df = df.drop_duplicates(subset=["review_id"], keep="first")  # Mantém apenas um usuário único

# Salvar em um arquivo
df.to_csv("amazon_clean.csv", index=False)

print("Remoção de duplicadas realizadas com sucesso.")
