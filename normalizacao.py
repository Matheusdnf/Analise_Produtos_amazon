import pandas as pd

# 🔹 Carregar o dataset original
file_path = "amazon_clean.csv"
df = pd.read_csv(file_path, dtype=str)  # Carregar tudo como string

# 🔹 Função para limpar strings
def clean_text(text):
    if isinstance(text, str):
        return " ".join(text.strip().split()) if text.strip() else "NULL"  # Substituir vazio por "NULL"
    return "NULL"

# 🔹 Aplicar limpeza de texto nas colunas relevantes
text_columns = ["review_title", "review_content", "product_name", "category", "about_product"]
for col in text_columns:
    df[col] = df[col].apply(clean_text)

# 🔹 Remover símbolos de moeda e converter preços corretamente
df["discounted_price"] = df["discounted_price"].str.replace(r"[₹,]", "", regex=True).astype(float)
df["actual_price"] = df["actual_price"].str.replace(r"[₹,]", "", regex=True).astype(float)
df["discount_percentage"] = df["discount_percentage"].str.replace("%", "").astype(float)
df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)

# 🔹 Remover linhas com IDs nulos antes de dividir listas
df.dropna(subset=["user_id", "review_id", "product_id"], inplace=True)

df["user_id"] = df["user_id"].str.split(",")
df["user_name"] = df["user_name"].str.split(",")
df["review_id"] = df["review_id"].str.split(",")
df["review_title"] = df["review_title"].str.split(",")
df["review_content"] = df["review_content"].str.split(",")

# 🔹 Garantir que todas as listas tenham o mesmo tamanho antes da explosão
def pad_list(lst, length):
    return lst + ["NULL"] * (length - len(lst))

max_len = df.apply(lambda row: max(len(row["user_id"]), len(row["user_name"]), len(row["review_id"]), len(row["review_title"]), len(row["review_content"])), axis=1)

df["user_id"] = df.apply(lambda row: pad_list(row["user_id"], max_len[row.name]), axis=1)
df["user_name"] = df.apply(lambda row: pad_list(row["user_name"], max_len[row.name]), axis=1)
df["review_id"] = df.apply(lambda row: pad_list(row["review_id"], max_len[row.name]), axis=1)
df["review_title"] = df.apply(lambda row: pad_list(row["review_title"], max_len[row.name]), axis=1)
df["review_content"] = df.apply(lambda row: pad_list(row["review_content"], max_len[row.name]), axis=1)

# 🔹 Explodir as colunas corretamente
df = df.explode(["user_id", "user_name", "review_id", "review_title", "review_content"]).reset_index(drop=True)

# 🔹 Remover novamente linhas com IDs nulos após explosão
df.replace("", "NULL", inplace=True)
df.fillna("NULL", inplace=True)
df = df[(df["user_id"] != "NULL") & (df["review_id"] != "NULL") & (df["product_id"] != "NULL")]

# 🔹 Criar tabelas normalizadas
users = df[["user_id", "user_name"]].drop_duplicates(subset=["user_id"])
reviews = df[["review_id", "review_title", "review_content", "user_id", "product_id"]].drop_duplicates()
products = df[["product_id", "product_name", "category", "discounted_price", "actual_price", "discount_percentage", "rating", "about_product", "img_link", "product_link"]].drop_duplicates()

# 🔹 Unir as tabelas mantendo a integridade referencial
final_df = reviews.merge(users, on="user_id", how="left").merge(products, on="product_id", how="left")

# 🔹 Substituir valores ausentes por "NULL"
final_df.replace("", "NULL", inplace=True)
final_df.fillna("NULL", inplace=True)

# 🔹 Verificação final antes de salvar
print(f"🔍 Total de usuários: {len(users)}")
print(f"🔍 Total de reviews: {len(reviews)}")
print(f"🔍 Total de produtos: {len(products)}")

# 🔹 Salvar os dados normalizados em um único arquivo CSV
final_df.to_csv("amazon_final_normalized.csv", index=False)

print("✅ Normalização concluída! Arquivo salvo: amazon_final_normalized.csv")
