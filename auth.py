"""
Authentication module for the Educational Tutor System
"""
import streamlit as st
from database import DatabaseManager

class AuthManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def show_login_form(self):
        """Display login form"""
        st.markdown("### 🔑 Login to Your Account")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                login_clicked = st.form_submit_button("Login", use_container_width=True, type="primary")
            with col2:
                if st.form_submit_button("Sign Up Instead", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.rerun()
        
        if login_clicked:
            if username and password:
                user_info = self.db.authenticate_user(username, password)
                if user_info:
                    st.session_state.authenticated = True
                    st.session_state.user_info = user_info
                    st.session_state.user_id = user_info['user_id']
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.error("Please fill in all fields")
    
    def show_signup_form(self):
        """Display signup form"""
        st.markdown("### 📝 Create Your Account")
        
        with st.form("signup_form"):
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            username = st.text_input("Username", placeholder="Choose a username")
            email = st.text_input("Email", placeholder="Enter your email address")
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            col1, col2 = st.columns(2)
            with col1:
                signup_clicked = st.form_submit_button("Create Account", use_container_width=True, type="primary")
            with col2:
                if st.form_submit_button("Login Instead", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()
        
        if signup_clicked:
            if all([full_name, username, email, password, confirm_password]):
                if password == confirm_password:
                    if len(password) >= 6:
                        user_id = self.db.create_user(username, email, password, full_name)
                        if user_id:
                            st.success("✅ Account created successfully! Please login.")
                            st.session_state.auth_mode = "login"
                            st.rerun()
                        else:
                            st.error("❌ Username or email already exists")
                    else:
                        st.error("Password must be at least 6 characters long")
                else:
                    st.error("Passwords do not match")
            else:
                st.error("Please fill in all fields")
    
    def logout(self):
        """Logout user"""
        for key in ['authenticated', 'user_info', 'user_id', 'current_subject', 'current_topic', 'chat_history']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.authenticated = False
        st.rerun()
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self):
        """Get current user info"""
        return st.session_state.get('user_info', {})

def require_auth(auth_manager):
    """Decorator to require authentication"""
    if not auth_manager.is_authenticated():
        return False
    return True