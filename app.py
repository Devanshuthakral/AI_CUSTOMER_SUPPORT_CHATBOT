import streamlit as st
from auth import register_user, login_user, update_password_by_email  # Updated import ✅
from chatbot import chat
from history import get_chat_history
from complaint import submit_complaint, get_complaints

# New Imports for Admin and OTP functionalities 🚀
from admin import admin_dashboard  
from otp import generate_otp
from mail import send_otp

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Customer Support Chatbot",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Session State Initialization
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "customer_id" not in st.session_state:
    st.session_state.customer_id = None

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "user_role" not in st.session_state:
    st.session_state.user_role = "user"  # Default role user rahega

if "page" not in st.session_state:
    st.session_state.page = "Login"

# Forgot Password State Trackers
if "reset_email" not in st.session_state:
    st.session_state.reset_email = ""
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None
if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

# -----------------------------
# Sidebar Navigation Control
# -----------------------------
st.sidebar.title("🤖 AI Customer Support")

if st.session_state.logged_in:
    # 👨‍💻 If logged in as ADMIN
    if st.session_state.user_role == "admin":
        choice = st.sidebar.radio(
            "Admin Menu",
            [
                "Admin Dashboard",
                "Logout"
            ]
        )
    # 👤 If logged in as USER
    else:
        choice = st.sidebar.radio(
            "Menu",
            [
                "Chat",
                "Chat History",
                "Complaints",
                "Logout"
            ]
        )
else:
    choice = st.sidebar.radio(
        "Menu",
        [
            "Login",
            "Register",
            "Forgot Password"
        ]
    )

# =====================================================
# REGISTER PAGE (🔄 Updated: Role Dropdown Added)
# =====================================================
if choice == "Register":
    st.title("📝 Create Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    # ✨ Naya Dropdown: User type select karne ke liye
    role_choice = st.selectbox("Select Role / Account Type", ["User", "Admin"])
    # Backend format me convert karne ke liye lowercase kiya ('user' or 'admin')
    selected_role = role_choice.lower() 

    if st.button("Register"):
        if name.strip() == "" or email.strip() == "" or password.strip() == "":
            st.warning("Please fill all the fields.")
        else:
            # 🔄 Ab selected_role parameter bhi ja rha hai backend verification me
            success, message = register_user(name, email, password, role=selected_role)
            if success:
                st.success(message)
            else:
                st.error(message)

# =====================================================
# LOGIN PAGE
# =====================================================
elif choice == "Login":
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.customer_id = user["customer_id"]
            st.session_state.customer_name = user["name"]
            st.session_state.user_role = user.get("role", "user") 

            st.success(f"Welcome {user['name']} ({st.session_state.user_role.upper()})")
            st.rerun()
        else:
            st.error("Invalid Email or Password")

# =====================================================
# FORGOT PASSWORD PAGE
# =====================================================
elif choice == "Forgot Password":
    st.title("🔑 Forgot Password using OTP")

    # STEP 1: Enter Email and Send OTP
    if not st.session_state.generated_otp and not st.session_state.otp_verified:
        reset_email = st.text_input("Enter Registered Email Address")
        if st.button("Send Verification OTP"):
            if reset_email.strip() == "":
                st.warning("Please enter your email.")
            else:
                otp_code = generate_otp()
                st.session_state.reset_email = reset_email
                st.session_state.generated_otp = otp_code
                
                if send_otp(reset_email, otp_code):
                    st.success(f"📦 A secure 6-digit OTP has been sent to {reset_email}")
                    st.rerun()
                else:
                    st.error("Failed to send OTP email. Please check your SMTP configuration.")

    # STEP 2: Verify OTP
    elif st.session_state.generated_otp and not st.session_state.otp_verified:
        st.info(f"OTP verification running for: {st.session_state.reset_email}")
        entered_otp = st.text_input("Enter 6-Digit OTP", max_chars=6)
        
        if st.button("Verify OTP"):
            if entered_otp == st.session_state.generated_otp:
                st.session_state.otp_verified = True
                st.success("✅ OTP Verified Successfully! Now you can reset your password.")
                st.rerun()
            else:
                st.error("❌ Invalid OTP. Please check the code sent to your email.")
        
        if st.button("Resend/Cancel"):
            st.session_state.generated_otp = None
            st.rerun()

    # STEP 3: Create New Password
    elif st.session_state.otp_verified:
        st.subheader("🛠️ Set New Password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        if st.button("Update Password"):
            if new_password != confirm_password:
                st.error("Passwords do not match!")
            else:
                success, message = update_password_by_email(st.session_state.reset_email, new_password)
                
                if success:
                    st.success(f"🎉 {message} You can now log in.")
                    st.session_state.generated_otp = None
                    st.session_state.otp_verified = False
                    st.session_state.reset_email = ""
                    st.rerun()
                else:
                    st.error(message)

# =====================================================
# ADMIN PORTAL DASHBOARD
# =====================================================
elif choice == "Admin Dashboard" and st.session_state.user_role == "admin":
    # 👑 Yahan aapka imported admin_dashboard dashboard load hoga aur dashboard
    # me current admin ka naam pass hoga.
    admin_dashboard(st.session_state.customer_name)

# =====================================================
# CHAT PAGE
# =====================================================
elif choice == "Chat" and st.session_state.user_role == "user":
    st.title("🤖 AI Customer Support Chatbot")
    st.write(f"Welcome **{st.session_state.customer_name}** 👋")

    question = st.text_area("Ask your question")

    if st.button("Send"):
        if question.strip() == "":
            st.warning("Please enter your question.")
        else:
            answer = chat(st.session_state.customer_id, question)
            st.subheader("AI Response")
            st.success(answer)

# =====================================================
# CHAT HISTORY
# =====================================================
elif choice == "Chat History" and st.session_state.user_role == "user":
    st.title("📜 Chat History")
    history = get_chat_history(st.session_state.customer_id)

    if not history or len(history) == 0:
        st.info("No Chat History Available.")
    else:
        for chat_data in history:
            with st.chat_message("user", avatar="👤"):
                st.markdown(chat_data["question"])

            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(chat_data["answer"])

            st.caption(f"📅 {chat_data['chat_date']}")
            st.divider()

# =====================================================
# COMPLAINT PAGE
# =====================================================
elif choice == "Complaints" and st.session_state.user_role == "user":
    st.title("📝 Register Complaint")
    complaint = st.text_area("Describe your complaint")

    if st.button("Submit Complaint"):
        if complaint.strip() == "":
            st.warning("Please enter your complaint.")
        else:
            submit_complaint(st.session_state.customer_id, complaint)
            st.success("Complaint Submitted Successfully.")

    st.markdown("---")
    st.subheader("Your Complaints")
    complaints = get_complaints(st.session_state.customer_id)

    if not complaints or len(complaints) == 0:
        st.info("No Complaints Found.")
    else:
        for item in complaints:
            st.markdown("---")
            st.write("📌 Complaint")
            st.write(item["complaint"])
            st.write("📍 Status")
            st.info(item["status"])
            st.caption(str(item["created_at"]))

# =====================================================
# LOGOUT
# =====================================================
elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.customer_id = None
    st.session_state.customer_name = ""
    st.session_state.user_role = "user"
    
    st.session_state.generated_otp = None
    st.session_state.otp_verified = False
    st.session_state.reset_email = ""

    st.success("Logged out successfully.")
    st.rerun()

# =====================================================
# FOOTER & SIDEBAR INFO
# =====================================================
st.sidebar.markdown("---")
if st.session_state.logged_in:
    st.sidebar.success(f"Logged in as: {st.session_state.customer_name} ({st.session_state.user_role.upper()})")

st.sidebar.markdown("---")
st.sidebar.markdown("## 🤖 AI Customer Support Assistant")
st.sidebar.write("**Version:** 2.0")

st.sidebar.markdown("### ⚙️ Tech Stack")
st.sidebar.markdown("""
- 🐍 Python
- 🎨 Streamlit
- 🗄️ MySQL
- 🚀 Groq API
- 🧠 Llama 3.3 70B
""")
 
st.sidebar.markdown("---")
st.sidebar.caption("Developed with using Streamlit & Python")