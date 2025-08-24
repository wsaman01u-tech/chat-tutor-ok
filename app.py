import streamlit as st
from database import DatabaseManager
from auth import AuthManager

# Configure the main page
st.set_page_config(
    page_title="Educational Chat Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def init_components():
    db = DatabaseManager()
    auth = AuthManager(db)
    return db, auth

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = "login"

def main():
    db, auth = init_components()
    init_session_state()
    
    # Enhanced CSS for beautiful styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    .feature-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .feature-card h4 {
        color: #1e293b;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    .feature-card p {
        color: #64748b;
        line-height: 1.6;
        font-weight: 400;
    }
    
    .auth-container {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    }
    
    .features-section {
        margin-top: 4rem;
    }
    
    .features-section h3 {
        text-align: center;
        color: #1e293b;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 3rem;
        position: relative;
    }
    
    .features-section h3::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        border-radius: 2px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if user is authenticated
    if not auth.is_authenticated():
        # Show login/signup page
        st.markdown('<div class="main-header"><h1>🎓 Educational Chat Tutor</h1><p>Your AI-powered learning companion</p></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            if st.session_state.auth_mode == "login":
                auth.show_login_form()
            else:
                auth.show_signup_form()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show features for non-authenticated users
        st.markdown('<div class="features-section">', unsafe_allow_html=True)
        st.markdown("### ✨ Why Choose Our Educational Tutor?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>🤖 AI-Powered Tutoring</h4>
                <p>Get personalized explanations and step-by-step guidance from our advanced AI tutor.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>📝 Smart Quizzes</h4>
                <p>Take adaptive quizzes that adjust to your learning level and track your progress.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h4>📊 Progress Analytics</h4>
                <p>Monitor your learning journey with detailed analytics and performance insights.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # User is authenticated, redirect to home page
        st.switch_page("pages/1_Home")

if __name__ == "__main__":
    main()
