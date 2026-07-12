from groq import Groq
from dotenv import load_dotenv
import os
from db import get_connection

# ==================================
# Load Environment Variables
# ==================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==================================
# Generate AI Response
# ==================================

def generate_response(user_question):

    prompt = f"""
You are a professional AI Customer Support Assistant.

Rules:
- Answer politely.
- Keep answers short and clear.
- Help customers with:
  • Refund
  • Delivery
  • Payment
  • Return Policy
  • Warranty
  • Order Status
- If you don't know the answer, politely ask the customer to contact support.

Customer Question:
{user_question}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional AI Customer Support Assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"


# ==================================
# Save Chat
# ==================================

def save_chat(customer_id, question, answer):

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    try:

        query = """
        INSERT INTO chat_history(customer_id, question, answer)
        VALUES(%s, %s, %s)
        """

        cursor.execute(query, (customer_id, question, answer))

        conn.commit()

    except Exception as e:
        print("Database Error:", e)

    finally:
        cursor.close()
        conn.close()


# ==================================
# Chat with AI
# ==================================

def chat(customer_id, question):

    answer = generate_response(question)

    save_chat(customer_id, question, answer)

    return answer


# ==================================
# Get Chat History
# ==================================

def get_chat_history(customer_id):

    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    try:

        query = """
        SELECT question, answer, chat_date
        FROM chat_history
        WHERE customer_id=%s
        ORDER BY chat_date DESC
        """

        cursor.execute(query, (customer_id,))

        return cursor.fetchall()

    except Exception as e:
        print("Database Error:", e)
        return []

    finally:
        cursor.close()
        conn.close()


# ==================================
# Delete Chat History
# ==================================

def delete_chat_history(customer_id):

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:

        query = """
        DELETE FROM chat_history
        WHERE customer_id=%s
        """

        cursor.execute(query, (customer_id,))

        conn.commit()

        return True

    except Exception as e:
        print("Database Error:", e)
        return False

    finally:
        cursor.close()
        conn.close()


# ==================================
# Testing
# ==================================

if __name__ == "__main__":

    customer_id = 1

    question = "What is your refund policy?"

    response = chat(customer_id, question)

    print(response)