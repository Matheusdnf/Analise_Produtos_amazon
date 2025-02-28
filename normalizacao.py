import pandas as pd

# 🔹 Carregar o dataset original
file_path = "amazon_normalizado.csv"
df = pd.read_csv(file_path)

# 🔹 Função para limpar strings (remoção de espaços extras e caracteres indesejados)
def clean_text(text):
    if isinstance(text, str):
        return " ".join(text.strip().split())  # Remove espaços extras
    return text

# 🔹 Aplicar limpeza de texto nas colunas relevantes
text_columns = ["review_title", "review_content", "product_name", "category", "about_product"]
for col in text_columns:
    df[col] = df[col].apply(clean_text)

# 🔹 Remover símbolos de moeda e converter preços para float
df["discounted_price"] = df["discounted_price"].astype(str).str.replace(r"[₹,]", "", regex=True).astype(float)
df["actual_price"] = df["actual_price"].astype(str).str.replace(r"[₹,]", "", regex=True).astype(float)
df["discount_percentage"] = df["discount_percentage"].astype(str).str.replace("%", "").astype(float)
df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)

# 🔹 Separar os valores das colunas "user_id", "user_name", "review_id", "review_title" e "review_content"
df["user_id"] = df["user_id"].astype(str).str.split(",")
df["user_name"] = df["user_name"].astype(str).str.split(",")
df["review_id"] = df["review_id"].astype(str).str.split(",")
df["review_title"] = df["review_title"].astype(str).str.split(",")
df["review_content"] = df["review_content"].astype(str).str.split(",")

# 🔹 Garantir que user_id e user_name tenham a mesma quantidade de elementos
max_len = df[["user_id", "user_name"]].applymap(len).max(axis=1)  # Maior quantidade de elementos

df["user_id"] = df["user_id"].apply(lambda x: x + ["NULL"] * (max_len.max() - len(x)))
df["user_name"] = df["user_name"].apply(lambda x: x + ["NULL"] * (max_len.max() - len(x)))

# 🔹 Explodir as colunas corretamente
df = df.explode(["user_id", "user_name"]).reset_index(drop=True)

# 🔹 Garantir que review_id, review_title e review_content correspondam aos user_id
max_review_len = df[["review_id", "review_title", "review_content"]].applymap(len).max(axis=1)

df["review_id"] = df["review_id"].apply(lambda x: x + ["NULL"] * (max_review_len.max() - len(x)))
df["review_title"] = df["review_title"].apply(lambda x: x + ["NULL"] * (max_review_len.max() - len(x)))
df["review_content"] = df["review_content"].apply(lambda x: x + ["NULL"] * (max_review_len.max() - len(x)))

df = df.explode(["review_id", "review_title", "review_content"]).reset_index(drop=True)

# 🔹 Separar os produtos corretamente
products = df[["product_id", "product_name", "category", "discounted_price", "actual_price", "discount_percentage", "rating", "about_product", "img_link", "product_link"]].drop_duplicates()

# 🔹 Separar as avaliações corretamente
reviews = df[["review_id", "review_title", "review_content", "user_id", "product_id"]].drop_duplicates()

# 🔹 Separar os usuários corretamente
users = df[["user_id", "user_name"]].drop_duplicates()

# 🔹 Mesclar os dados normalizados
final_df = reviews.merge(users, on="user_id", how="left").merge(products, on="product_id", how="left")

# 🔹 Salvar os dados normalizados em um único arquivo CSV
final_df.to_csv("amazon_final_normalized.csv", index=False)

print("✅ Normalização concluída! Arquivo salvo: amazon_final_normalized.csv")
