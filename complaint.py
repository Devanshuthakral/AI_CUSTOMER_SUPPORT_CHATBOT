from db import get_connection


# =====================================
# Submit Complaint
# =====================================

def submit_complaint(customer_id, complaint):

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:

        query = """
        INSERT INTO complaints(customer_id, complaint, status)
        VALUES(%s, %s, %s)
        """

        cursor.execute(query, (customer_id, complaint, "Pending"))

        conn.commit()

        return True

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        cursor.close()
        conn.close()


# =====================================
# Get All Complaints of User
# =====================================

def get_complaints(customer_id):

    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    try:

        query = """
        SELECT complaint_id,
               complaint,
               status,
               created_at
        FROM complaints
        WHERE customer_id = %s
        ORDER BY created_at DESC
        """

        cursor.execute(query, (customer_id,))

        complaints = cursor.fetchall()

        return complaints

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        conn.close()


# =====================================
# Update Complaint Status
# (Admin Feature)
# =====================================

def update_complaint_status(complaint_id, status):

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:

        query = """
        UPDATE complaints
        SET status = %s
        WHERE complaint_id = %s
        """

        cursor.execute(query, (status, complaint_id))

        conn.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        cursor.close()
        conn.close()


# =====================================
# Delete Complaint (Optional Admin Feature)
# =====================================

def delete_complaint(complaint_id):

    conn = get_connection()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:

        query = """
        DELETE FROM complaints
        WHERE complaint_id = %s
        """

        cursor.execute(query, (complaint_id,))

        conn.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        cursor.close()
        conn.close()


# =====================================
# Get All Complaints (Admin Feature)
# =====================================

def get_all_complaints():

    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    try:

        query = """
        SELECT complaint_id,
               customer_id,
               complaint,
               status,
               created_at
        FROM complaints
        ORDER BY created_at DESC
        """

        cursor.execute(query)

        complaints = cursor.fetchall()

        return complaints

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        conn.close()