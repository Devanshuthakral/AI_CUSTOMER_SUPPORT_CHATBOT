from db import get_connection


# ==================================
# Get Complete Chat History
# ==================================

def get_chat_history(customer_id):

    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        SELECT chat_id, question, answer, chat_date
        FROM chat_history
        WHERE customer_id=%s
        ORDER BY chat_date DESC
        """

        cursor.execute(query, (customer_id,))
        history = cursor.fetchall()

        return history

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        conn.close()


# ==================================
# Search Chat History
# ==================================

def search_chat(customer_id, keyword):

    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        SELECT chat_id, question, answer, chat_date
        FROM chat_history
        WHERE customer_id=%s
        AND (question LIKE %s OR answer LIKE %s)
        ORDER BY chat_date DESC
        """

        search = "%" + keyword + "%"

        cursor.execute(query, (customer_id, search, search))

        result = cursor.fetchall()

        return result

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        conn.close()