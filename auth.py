import bcrypt
import re
from db import get_connection

# ===============================
# Email & Password Validation
# ===============================

def is_valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email)

def is_valid_password(password):
    if len(password) < 8: return False
    if not re.search(r"[A-Z]", password): return False
    if not re.search(r"[a-z]", password): return False
    if not re.search(r"\d", password): return False
    return True

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


# ==========================================
# Register User (🔄 Role Field Added)
# ==========================================

def register_user(name, email, password, role='user'):
    """
    By default role 'user' rahega. 
    Admin banane ke liye explicitly role='admin' pass karna hoga.
    """
    # Validation for role values to prevent malicious input
    if role not in ['user', 'admin']:
        return False, "Invalid role specified."

    if not is_valid_email(email):
        return False, "Invalid Email Address"

    if not is_valid_password(password):
        return False, "Password must contain 8 characters, uppercase, lowercase and number."

    conn = get_connection()
    if conn is None:
        return False, "Database Connection Failed"

    cursor = conn.cursor()
    try:
        # Check existing email
        cursor.execute("SELECT * FROM customers WHERE email=%s", (email,))
        if cursor.fetchone():
            return False, "Email already registered."

        # 🔐 Password Hash
        hashed_password = hash_password(password)

        # Insert user with explicit role
        cursor.execute(
            """
            INSERT INTO customers(name, email, password, role)
            VALUES(%s, %s, %s, %s)
            """,
            (name, email, hashed_password, role)
        )
        conn.commit()
        return True, "Registration Successful"

    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


# ===============================
# Login User
# ===============================

def login_user(email, password):
    conn = get_connection()
    if conn is None: return None

    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT customer_id, name, email, password, role FROM customers WHERE email=%s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            del user['password'] # Security: password remove kiya
            return user # Isme user['role'] mil jayega frontend par check karne ke liye
        
        return None
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        cursor.close()
        conn.close()


# ==========================================
# 👑 ADMIN ONLY FUNCTIONS (New Features ✨)
# ==========================================

def admin_view_all_users(admin_id):
    """
    Admin saare customers/users ki details dekh sakta hai.
    Safety ke liye pehle verify karega ki requester sach me Admin hai ya nahi.
    """
    conn = get_connection()
    if conn is None: return None

    cursor = conn.cursor(dictionary=True)
    try:
        # 1. Security Check: Verify if the person requesting is actually an admin
        cursor.execute("SELECT role FROM customers WHERE customer_id=%s", (admin_id,))
        admin_check = cursor.fetchone()
        
        if not admin_check or admin_check['role'] != 'admin':
            print("Access Denied: Only admins can view user details.")
            return None

        # 2. Fetch all users details (excluding sensitive passwords)
        query = "SELECT customer_id, name, email, role FROM customers"
        cursor.execute(query)
        users_list = cursor.fetchall()
        return users_list

    except Exception as e:
        print("Error fetching users:", e)
        return None
    finally:
        cursor.close()
        conn.close()


def admin_delete_user(admin_id, user_id_to_delete):
    """Admin kisi bhi user ko portal se delete kar sakta hai"""
    conn = get_connection()
    if conn is None: return False, "Database connection failed."

    cursor = conn.cursor()
    try:
        # Security Check
        cursor.execute("SELECT role FROM customers WHERE customer_id=%s", (admin_id,))
        admin_check = cursor.fetchone()
        
        if not admin_check or admin_check[0] != 'admin':
            return False, "Access Denied."

        # Delete Action
        cursor.execute("DELETE FROM customers WHERE customer_id=%s", (user_id_to_delete,))
        conn.commit()
        return True, "User deleted successfully."

    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


# ==========================================
# Update Password via Forgot Password
# ==========================================

def update_password_by_email(email, new_password):
    if not is_valid_password(new_password):
        return False, "Password must contain 8 characters, uppercase, lowercase and number."

    conn = get_connection()
    if conn is None: return False, "Database Connection Failed"

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT customer_id FROM customers WHERE email=%s", (email,))
        if not cursor.fetchone():
            return False, "Email not found in our database."

        hashed_password = hash_password(new_password)
        cursor.execute("UPDATE customers SET password=%s WHERE email=%s", (hashed_password, email))
        conn.commit()
        return True, "Password updated successfully!"
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()