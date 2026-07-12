import streamlit as st
from auth import admin_view_all_users, admin_delete_user
from db import get_connection

def get_all_complaints():
    """Database se saari complaints nikalne ke liye"""
    conn = get_connection()
    if conn is None: return []
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT c.complaint_id, cust.name as customer_name, cust.email, c.complaint, c.status, c.created_at 
        FROM complaints c 
        JOIN customers cust ON c.customer_id = cust.customer_id
        ORDER BY c.created_at DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("Error fetching complaints:", e)
        return []
    finally:
        cursor.close()
        conn.close()

def update_complaint_status(complaint_id, status):
    """Complaint ko Resolve karne ke liye"""
    conn = get_connection()
    if conn is None: return False
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE complaints SET status=%s WHERE complaint_id=%s", (status, complaint_id))
        conn.commit()
        return True
    except Exception as e:
        print("Error updating status:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def delete_complaint_db(complaint_id):
    """Complaint delete karne ke liye"""
    conn = get_connection()
    if conn is None: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM complaints WHERE complaint_id=%s", (complaint_id,))
        conn.commit()
        return True
    except Exception as e:
        print("Error deleting complaint:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def get_user_chat_history(customer_id):
    """Kisi specific user ki chat history fetch karne ke liye"""
    conn = get_connection()
    if conn is None: return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT question, answer, chat_date FROM history WHERE customer_id=%s ORDER BY chat_date DESC", (customer_id,))
        return cursor.fetchall()
    except Exception as e:
        print("Error fetching user chat:", e)
        return []
    finally:
        cursor.close()
        conn.close()

# ==========================================
# 👑 MAIN ADMIN DASHBOARD UI
# ==========================================
def admin_dashboard(admin_name):
    st.title(f"👨‍💻 Welcome to Admin Portal: {admin_name}")
    st.write("Manage users, complaints, and view chat logs dynamically from this panel.")
    
    # 📑 UI Tabs banane ke liye taaki terminal jaise bar-bar option na chunna pade
    tab1, tab2, tab3 = st.tabs(["👤 View & Manage Users", "📝 User Complaints", "💬 User Chat Histories"])

    # 🛑 Pehle session state se admin_id nikal lete hain verification ke liye
    admin_id = st.session_state.get("customer_id")

    # ------------------------------------------
    # TAB 1: VIEW & MANAGE USERS
    # ------------------------------------------
    with tab1:
        st.subheader("👥 All Registered Users")
        users = admin_view_all_users(admin_id)
        
        if not users:
            st.info("No users found or access denied.")
        else:
            # Table format me user list dikhane ke liye
            st.table(users)
            
            st.markdown("---")
            st.subheader("🗑️ Delete a User Account")
            user_to_delete = st.selectbox(
                "Select user to remove permanently", 
                options=[u['customer_id'] for u in users if u['role'] != 'admin'],
                format_func=lambda x: next((f"{u['name']} ({u['email']})" for u in users if u['customer_id'] == x), str(x))
            )
            
            if st.button("Delete User Account", type="primary"):
                success, msg = admin_delete_user(admin_id, user_to_delete)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    # ------------------------------------------
    # TAB 2: VIEW & MANAGE COMPLAINTS
    # ------------------------------------------
    with tab2:
        st.subheader("📋 Active Complaints Portal")
        complaints = get_all_complaints()
        
        if not complaints:
            st.info("No complaints registered yet.")
        else:
            for c in complaints:
                with st.expander(f"📌 {c['customer_name']} - Status: {c['status'].upper()} (ID: {c['complaint_id']})"):
                    st.write(f"**Email:** {c['email']}")
                    st.write(f"**Complaint Description:** {c['complaint']}")
                    st.caption(f"Filed on: {c['created_at']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if c['status'].lower() != 'resolved':
                            if st.button(f"Mark Resolved #{c['complaint_id']}", key=f"res_{c['complaint_id']}"):
                                if update_complaint_status(c['complaint_id'], 'resolved'):
                                    st.success("Status Updated!")
                                    st.rerun()
                    with col2:
                        if st.button(f"Delete Complaint #{c['complaint_id']}", key=f"del_{c['complaint_id']}", type="primary"):
                            if delete_complaint_db(c['complaint_id']):
                                st.success("Complaint Removed!")
                                st.rerun()

    # ------------------------------------------
    # TAB 3: CHAT HISTORY AUDIT
    # ------------------------------------------
    with tab3:
        st.subheader("💬 Audit User Interactions with AI")
        users_for_chat = admin_view_all_users(admin_id)
        
        if users_for_chat:
            selected_user = st.selectbox(
                "Select a customer to inspect their chat history:",
                options=[u['customer_id'] for u in users_for_chat if u['role'] == 'user'],
                format_func=lambda x: next((f"{u['name']} ({u['email']})" for u in users_for_chat if u['customer_id'] == x), str(x))
            )
            
            if selected_user:
                history = get_user_chat_history(selected_user)
                if not history:
                    st.info("This user hasn't talked to the bot yet.")
                else:
                    for ch in history:
                        st.markdown(f"**🧑 User:** {ch['question']}")
                        st.markdown(f"**🤖 AI Response:** {ch['answer']}")
                        st.caption(f"Time: {ch['chat_date']}")
                        st.divider()