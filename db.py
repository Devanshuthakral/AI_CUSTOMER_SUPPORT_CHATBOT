import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===========================
# Database Connection
# ===========================

def get_connection():
    """Create and return MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("❌ Database Connection Error:", e)
        return None

# ===========================
# Execute INSERT / UPDATE / DELETE
# ===========================

def execute_query(query, values=None):
    """
    Run non-SELECT queries like INSERT, UPDATE, DELETE.
    Ensures connection is closed properly.
    """
    connection = get_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        connection.commit()
        return True
    except Error as e:
        print("❌ Query Execution Error:", e)
        return False
    finally:
        cursor.close()
        connection.close()  # Connection leak fix kiya ✅

# ===========================
# Execute SELECT Queries (New ✨)
# ===========================

def fetch_query(query, values=None, fetch_one=False):
    """
    Run SELECT queries and return data.
    dictionary=True use kiya hai taaki output tuple ki jagah dict {'id': 1, 'name': 'Pooja'} mile.
    """
    connection = get_connection()
    if connection is None:
        return None

    # dictionary=True se readable format me data milega
    cursor = connection.cursor(dictionary=True)
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        if fetch_one:
            return cursor.fetchone()  # Ek single user ya record ke liye (e.g., Login/Forgot Password)
        return cursor.fetchall()       # Saare records ke liye (e.g., History/Complaints list)
        
    except Error as e:
        print("❌ Fetch Query Error:", e)
        return None
    finally:
        cursor.close()
        connection.close()  # Connection securely closed ✅ 