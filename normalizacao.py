import pandas as pd

# 🔹 Carregar o dataset limpo
file_path = "amazon_clean.csv"
df = pd.read_csv(file_path)

# 🔹 Função para limpar strings (remoção de espaços extras e caracteres indesejados)
def clean_text(text):
    if isinstance(text, str):
        return " ".join(text.strip().split())  # Remove espaços extras
    return text

# 🔹 Aplicar limpeza de texto nas colunas relevantes
text_columns = ["product_name", "category", "about_product", "review_title", "review_content"]
for col in text_columns:
    df[col] = df[col].apply(clean_text)

# 🔹 Remover símbolos de moeda e converter preços para float
df["discounted_price"] = df["discounted_price"].astype(str).str.replace(r"[₹,]", "", regex=True).astype(float)
df["actual_price"] = df["actual_price"].astype(str).str.replace(r"[₹,]", "", regex=True).astype(float)
df["review_content"] = df["review_content"].astype(str).str.replace(r"[₹,]", "", regex=True)

# 🔹 Converter desconto para número
df["discount_percentage"] = df["discount_percentage"].astype(str).str.replace("%", "").astype(float)

# 🔹 Corrigir valores numéricos inconsistentes
df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)  # Converte para número e preenche NaN com 0
df["rating_count"] = df["rating_count"].astype(str).str.replace(",", "")

# 🔹 Tratar valores ausentes (NaN) preenchendo com "NULL"
df.fillna("NULL", inplace=True)


# 🔹 Salvar o dataset padronizado
standardized_file_path = "amazon_normalizado.csv"
df.to_csv(standardized_file_path, index=False)

print(f"✅ Padronização concluída! Arquivo salvo como {standardized_file_path}")
