import pandas as pd
from sqlalchemy import create_engine

# Configurações do banco
DB_USER = "matheus"
DB_PASSWORD = "matheus1700"
DB_NAME = "Produtos_amazon"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"

# Criando a engine de conexão
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Ler os novos dados
df = pd.read_csv("amazon_normalizado.csv")

# Função para buscar IDs já cadastrados no banco
def get_existing_ids(table_name, id_column):
    query = f"SELECT {id_column} FROM {table_name}"
    return set(pd.read_sql(query, con=engine)[id_column].astype(str))

# Buscar IDs existentes
existing_user_ids = get_existing_ids("user", "user_id")
existing_product_ids = get_existing_ids("product", "product_id")
existing_review_ids = get_existing_ids("review", "review_id")

# Filtrar apenas os novos registros
new_users = df[['user_id', 'user_name']].drop_duplicates()
new_users = new_users[~new_users['user_id'].astype(str).isin(existing_user_ids)]

new_products = df[['product_id', 'product_name', 'category', 'discounted_price', 
                   'actual_price', 'discount_percentage', 'rating', 
                   'about_product', 'img_link', 'product_link']].drop_duplicates()
new_products = new_products[~new_products['product_id'].astype(str).isin(existing_product_ids)]

new_reviews = df[['review_id', 'review_title', 'review_content', 'user_id', 'product_id']].drop_duplicates()
new_reviews = new_reviews[~new_reviews['review_id'].astype(str).isin(existing_review_ids)]

# Verificar se há novos dados
if new_users.empty and new_products.empty and new_reviews.empty:
    print("⚠ Nenhum dado novo a ser inserido no banco.")
else:
    # Inserir apenas os novos registros no banco
    with engine.connect() as connection:
        if not new_users.empty:
            new_users.to_sql("user", con=engine, if_exists="append", index=False, method="multi")
        if not new_products.empty:
            new_products.to_sql("product", con=engine, if_exists="append", index=False, method="multi")
        if not new_reviews.empty:
            new_reviews.to_sql("review", con=engine, if_exists="append", index=False, method="multi")

    print("✅ Novos dados adicionados ao banco!")

# Fechar conexão
engine.dispose()



# SELECT 
#     p.product_id,
#     p.product_name,
#     COUNT(r.product_id) AS total_compras
# FROM review r
# JOIN product p ON r.product_id = p.product_id
# GROUP BY p.product_id, p.product_name
# ORDER BY total_compras DESC;
