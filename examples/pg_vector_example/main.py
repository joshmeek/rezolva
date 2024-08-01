import os
import psycopg2
from pgvector.psycopg2 import register_vector
from dotenv import load_dotenv

load_dotenv()

HOST="localhost"
USER="vectoruser"
PASSWORD=os.getenv("POSTGRES_PASSWORD")
DBNAME="vectordb"

conn = psycopg2.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    dbname=DBNAME,
    port=5432,
)

register_vector(conn)

cursor = conn.cursor()

## change to fit existing schema in `vector_based_example.py`
cursor.execute(
    """
CREATE TABLE articles (
    article_id INT PRIMARY KEY NOT NULL
    ,article_text varchar(10000)
    ,embedding vector(1536)
);
"""
)

conn.commit()