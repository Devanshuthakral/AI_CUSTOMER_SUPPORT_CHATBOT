import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            ssl_ca="certs/isrgrootx1.pem"
        )

        print("✅ Connected Successfully")
        return conn

    except Exception as e:
        print(e)