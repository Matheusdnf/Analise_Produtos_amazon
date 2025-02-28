## Configuração do Banco de Dados no Google Cloud

### Decisões tomadas

Escolhi uma base de dados da plataforma kaggle sendo ela a da [amazon](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset)

E como ferramentas utilizei:

- **Python** : Realizar a limpeza dos dados e uppar os dados para o banco.
  Execute antes de tudo o script python (instalar_biblioteca.py)
- **Google Cloud**: Para abrigar os dados e o banco em si.
- **Google Bquery** : Para a realização das consultas ao banco.
- **Google Locker** : Criação da dashboard.

### 1. Criação do Banco de Dados

Acesse o link abaixo para criar uma instância do MySQL no Google Cloud:

[Criação do Banco de Dados](https://console.cloud.google.com/sql/choose-instance-engine?hl=pt-br&project=lyrical-edition-452118-a7)

Escolha as preferências desejadas e configure o banco de dados conforme necessário. Após a configuração, o banco estará pronto para uso.

### 2. Upload do Esquema SQL

No repositório do GitHub, há um arquivo denominado `esquema.sql`, que contém a estrutura do banco de dados. Siga os passos abaixo para realizar o upload desse arquivo:

1. Acesse o link para o Google Cloud Storage:
   [Google Cloud Storage](https://console.cloud.google.com/storage/browser?hl=pt-br&project=lyrical-edition-452118-a7)
2. Crie um bucket e associe-o ao banco de dados criado.
3. Envie o arquivo `esquema.sql` para o bucket.
4. Após o upload, importe o esquema para o banco de dados.

Dessa forma, a estrutura do banco será carregada corretamente.

---

## Configuração do Ambiente e APIs Necessárias

Para estabelecer a conexão entre o ambiente local, o Google Cloud e o BigQuery, é necessário ativar as seguintes APIs:

- **BigQuery API**: Permite consultas SQL no BigQuery.
- **Cloud Storage API**: Necessária para armazenar arquivos CSV antes de carregá-los no BigQuery.
- **Cloud SQL Admin API**: Necessária para conectar um banco de dados SQL ao BigQuery.

Ative essas APIs no link:
[Ativar APIs](https://console.cloud.google.com/apis/library?project=lyrical-edition-452118-a7)

---

## Extração dos Dados

Execute o script `remover_duplicatas.py` para gerar um novo arquivo CSV com a remoção de dados duplicados e inconsistências.

---

## Transformação dos Dados

Após a extração, execute o script `normalizacao.py`, responsável por:

- Realizar limpeza e padronização dos dados.
- Corrigir problemas de formatação.
- Converter preços e remover inconsistências.

---

## Conexão com o Banco de Dados no Google Cloud

Para inserir os dados no banco de dados, é necessário estabelecer uma conexão com o **Cloud SQL**. O repositório contém o arquivo `cloud_sql_proxy.exe`, que facilita essa conexão.

### Passos para Conectar ao Banco de Dados:

1. No terminal, execute o seguinte comando:

   ```bash
   ./cloud-sql-proxy --credentials-file PATH_TO_KEY_FILE INSTANCE_CONNECTION_NAME
   ```

   Onde:

   - `PATH_TO_KEY_FILE` é o caminho do arquivo JSON com a chave de conexão.
   - `INSTANCE_CONNECTION_NAME` é o nome da instância criada no banco de dados.

2. Para obter a chave JSON:
   - Acesse: [Gerenciamento de Contas de Serviço](https://console.cloud.google.com/iam-admin/serviceaccounts?project=lyrical-edition-452118-a7)
   - Crie uma conta de serviço e baixe o arquivo JSON correspondente.

Para mais informações, consulte a documentação oficial do Google Cloud:
[Documentação Cloud SQL Proxy](https://cloud.google.com/sql/docs/mysql/connect-auth-proxy?hl=pt-br)

---

## Carga dos Dados no Banco de Dados

Após estabelecer a conexão, execute o script `codigo_etl.py`. Esse script irá:

- Conectar-se ao banco de dados.
- Inserir os dados processados.
- Garantir a integridade dos dados armazenados.

---

## Configuração do BigQuery

Com os dados carregados no banco de dados, acesse o BigQuery pelo link:
[BigQuery Console](https://console.cloud.google.com/bigquery?project=lyrical-edition-452118-a7)

1. No BigQuery, clique em **Adicionar** → **Conexão com Fonte de Dados Externa**.
2. Configure a conexão com as credenciais do banco de dados do Google Cloud.
3. Após a configuração, os dados estarão acessíveis para a realização de consultas SQL.

### Exemplos de Consultas SQL no BigQuery

**Distribuição de preços dos produtos:**

```sql
SELECT
  CASE
    WHEN actual_price < 50 THEN 'Menos de $50'
    WHEN actual_price BETWEEN 50 AND 100 THEN '$50 - $100'
    WHEN actual_price BETWEEN 100 AND 200 THEN '$100 - $200'
    WHEN actual_price BETWEEN 200 AND 500 THEN '$200 - $500'
    ELSE 'Acima de $500'
  END AS price_range,
  COUNT(product_id) AS total_products
FROM product
GROUP BY price_range
ORDER BY total_products DESC;
```

**Produtos com maior desconto:**

```sql
SELECT
  product_name,
  actual_price,
  discounted_price,
  discount_percentage
FROM product
ORDER BY CAST(discount_percentage AS DECIMAL(3,2)) DESC;
```

**Produtos mais vendidos por categoria principal:**

```sql
SELECT
  SUBSTRING_INDEX(category, '|', 1) AS main_category,
  COUNT(*) AS total_products
FROM product
GROUP BY main_category
ORDER BY total_products DESC;
```

**Quantidade total de usuários, produtos e reviews:**

```sql
SELECT
  (SELECT COUNT(*) FROM user) AS total_users,
  (SELECT COUNT(*) FROM product) AS total_products,
  (SELECT COUNT(*) FROM review) AS total_reviews;
```

---

## Criação do Dashboard no Looker Studio

Após configurar o BigQuery, acesse o Looker Studio para criar o dashboard:

[Acessar Looker Studio](https://lookerstudio.google.com/navigation/reporting)

### Passos para Criar o Dashboard:

1. Clique em **Criar** → **Dashboard em Branco**.
2. Adicione os dados do BigQuery.
3. Selecione as tabelas desejadas.
4. Personalize gráficos e métricas para visualização.
