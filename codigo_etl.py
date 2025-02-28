import pandas as pd
from sqlalchemy import create_engine

# Configurações do banco
DB_USER = "matheus"  #Inserir o nome do usuário do banco de dados 
DB_PASSWORD = "matheus1700"  #inserir senha do usuário
DB_NAME = "Produtos_amazon" #nome do banco criado
DB_HOST = "127.0.0.1" #host escolhido para rodar, o que eu utilizei foi um local
DB_PORT = "3306" #porta local disponível no computador

# Estabelecendo conexão com o banco
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Leitura do Arquivo que CSV que será inserido no banco de dados
df = pd.read_csv("amazon_final_normalized.csv")

# Remover entradas com IDs nulos
df = df.dropna(subset=["user_id", "product_id", "review_id"])

# Buscar IDs já cadastrados no banco
def get_existing_ids(table_name, id_column):
    query = f"SELECT {id_column} FROM {table_name}"
    return set(pd.read_sql(query, con=engine)[id_column].astype(str))

# Buscar IDs existentes no banco
existing_user_ids = get_existing_ids("user", "user_id")
existing_product_ids = get_existing_ids("product", "product_id")
existing_review_ids = get_existing_ids("review", "review_id")

# Remover duplicatas dentro do próprio dataset antes da inserção
df = df.drop_duplicates(subset=["user_id", "product_id", "review_id"])

# Filtrar apenas usuários novos
new_users = df[['user_id', 'user_name']].drop_duplicates(subset=['user_id'])
new_users = new_users[~new_users['user_id'].astype(str).isin(existing_user_ids)]

# Filtrar apenas produtos novos
new_products = df[['product_id', 'product_name', 'category', 'discounted_price', 
                   'actual_price', 'discount_percentage', 'rating', 
                   'about_product', 'img_link', 'product_link']].drop_duplicates(subset=['product_id'])
new_products = new_products[~new_products['product_id'].astype(str).isin(existing_product_ids)]

# Inserir novos usuários e produtos 
with engine.connect() as connection:
    if not new_users.empty:
        new_users.to_sql("user", con=engine, if_exists="append", index=False, method="multi")
    if not new_products.empty:
        new_products.to_sql("product", con=engine, if_exists="append", index=False, method="multi")

# Atualizar IDs existentes no banco **após inserção**
existing_user_ids.update(new_users["user_id"].astype(str).tolist())
existing_product_ids.update(new_products["product_id"].astype(str).tolist())

# Filtrar reviews válidas (removendo duplicatas e garantindo FK válidas)
new_reviews = df[['review_id', 'review_title', 'review_content', 'user_id', 'product_id']]
new_reviews = new_reviews.drop_duplicates(subset=['review_id'])
new_reviews = new_reviews[~new_reviews['review_id'].astype(str).isin(existing_review_ids)]

# Garantir que user_id e product_id existem antes de inserir review
new_reviews = new_reviews[new_reviews['user_id'].astype(str).isin(existing_user_ids)]
new_reviews = new_reviews[new_reviews['product_id'].astype(str).isin(existing_product_ids)]

# Inserir apenas novas reviews
if not new_reviews.empty:
    with engine.connect() as connection:
        new_reviews.to_sql("review", con=engine, if_exists="append", index=False, method="multi")

print("Novos dados adicionados ao banco")

# Finalizar conexão com o banco
engine.dispose()
