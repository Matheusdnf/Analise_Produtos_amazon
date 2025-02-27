import pandas as pd
from sqlalchemy import create_engine, text
from google.cloud import storage
import os
import psycopg2
import sqlite3

# Configurações do banco
DB_USER = "matheus"
DB_PASSWORD = "matheus1700"
DB_NAME = "Produtos_amazon"
DB_HOST = "127.0.0.1"  # Proxy está rodando localmente
db_port= "3306"


df = pd.read_csv("amazon_normalizado.csv")

# Criando a engine de conexão
try:
    # Criar engine do SQLAlchemy
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{db_port}/{DB_NAME}")

    # Criar conexão e inserir usuário
    with engine.connect() as connection:
        #connection.execute()
        # Seleciona colunas da tabela user
        users = df[['user_id', 'user_name']].drop_duplicates()

        # Debug: Verificar tamanho dos valores de user_id
        # for user_id in users['user_id']:
        #     print(f"id repetido: ",user_id, len(str(user_id)))  # Converte para string caso tenha valores numéricos

        # Inserção dos dados na tabela "user"
        users.to_sql("user", con=engine, if_exists="append", index=False, method="multi")
        products = df[['product_id', 'product_name', 'category', 'discounted_price', 
               'actual_price', 'discount_percentage', 'rating', 
               'about_product', 'img_link', 'product_link']].drop_duplicates()
        products.to_sql("product", con=engine, if_exists="append", index=False, method="multi")
        reviews = df[['review_id', 'review_title', 'review_content', 'user_id', 'product_id']]
        reviews.to_sql("review", con=engine, if_exists="append", index=False, method="multi")
        connection.commit()
        print("Usuário inserido com sucesso!")

except Exception as e:
    print(f"Erro ao inserir usuário: {e}")

finally:
    engine.dispose()