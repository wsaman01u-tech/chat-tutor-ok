import streamlit as st
import plotly.express as px
from datetime import datetime
from database import DatabaseManager
from auth import AuthManager
from subjects import SUBJECTS, get_all_subjects

# Configure page
st.set_page_config(
    page_title="Home - Educational Tutor",
    page_icon="🏠",
    layout="wide"
)

# Initialize components
@st.cache_resource
def init_components():
    db = DatabaseManager()
    auth = AuthManager(db)
    return db, auth

def init_session_state():
    """Initialize session state"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = "login"

def main():
    db, auth = init_components()
    init_session_state()
    
    # Enhanced CSS for beautiful modern design
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3);
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
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.5; }
        50% { transform: scale(1.1) rotate(180deg); opacity: 0.8; }
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .main-header p {
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.9;
        position: relative;
        z-index: 2;
    }
    
    .feature-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        margin-bottom: 2rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899, #f59e0b);
    }
    
    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0,0,0,0.2);
    }
    
    .feature-card h4 {
        color: #1e293b;
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.4rem;
    }
    
    .feature-card p {
        color: #64748b;
        line-height: 1.8;
        font-weight: 400;
        font-size: 1rem;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stats-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        animation: rotate 8s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
    }
    
    .stats-card h3 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .stats-card p {
        font-size: 1rem;
        font-weight: 500;
        opacity: 0.9;
        position: relative;
        z-index: 2;
    }
    
    .subject-showcase {
        background: linear-gradient(145deg, #f1f5f9 0%, #e2e8f0 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin: 3rem 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
    }
    
    .subject-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
        margin: 1rem 0;
    }
    
    .subject-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        border-color: #6366f1;
    }
    
    .subject-card h2 {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .subject-card h4 {
        color: #1e293b;
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    .subject-card p {
        color: #64748b;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .quick-actions {
        margin-top: 3rem;
    }
    
    .action-button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        border: none;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
        cursor: pointer;
        width: 100%;
    }
    
    .action-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(99, 102, 241, 0.4);
    }
    
    .section-title {
        text-align: center;
        color: #1e293b;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 3rem 0 2rem 0;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        border-radius: 2px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if not auth.is_authenticated():
        # Show login/signup page
        st.markdown('<div class="main-header"><h1>🎓 Educational Chat Tutor</h1><p>Your AI-powered learning companion</p></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.auth_mode == "login":
                auth.show_login_form()
            else:
                auth.show_signup_form()
        
        # Features showcase
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
        
        # Subjects overview
        st.markdown('<div class="subject-showcase">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">📚 Available Subjects</h3>', unsafe_allow_html=True)
        cols = st.columns(len(SUBJECTS))
        
        for i, (subject, info) in enumerate(SUBJECTS.items()):
            with cols[i]:
                st.markdown(f"""
                <div class="subject-card">
                    <h2>{info['icon']}</h2>
                    <h4>{subject}</h4>
                    <p>{info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Show dashboard for authenticated users
        user_info = auth.get_current_user()
        
        st.markdown(f'<div class="main-header"><h1>Welcome back, {user_info.get("full_name", user_info.get("username", "Student"))}! 🎓</h1><p>Ready to continue your learning journey?</p></div>', unsafe_allow_html=True)
        
        # Quick stats
        from progress_tracker import ProgressTracker
        progress = ProgressTracker(db)
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate overall stats
        total_completed = 0
        total_subjects = len(SUBJECTS)
        avg_score = 0
        total_chats = 0
        
        for subject in SUBJECTS.keys():
            user_progress = progress.get_user_progress(st.session_state.user_id, subject)
            if user_progress:
                completed_topics = len([t for t in user_progress if user_progress[t]['completed']])
                total_completed += completed_topics
                
                quiz_scores = [user_progress[t]['best_score'] for t in user_progress if user_progress[t]['best_score'] > 0]
                if quiz_scores:
                    avg_score += sum(quiz_scores) / len(quiz_scores)
                
                total_chats += sum([user_progress[t]['chat_count'] for t in user_progress])
        
        avg_score = avg_score / total_subjects if total_subjects > 0 else 0
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{total_completed}</h3>
                <p>Topics Completed</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{avg_score:.1f}%</h3>
                <p>Average Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{total_chats}</h3>
                <p>Chat Sessions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{total_subjects}</h3>
                <p>Subjects Available</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick actions
        st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">🚀 Quick Actions</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💬 Start Learning", use_container_width=True, type="primary", key="start_learning"):
                st.switch_page("pages/2_📚_Learn.py")
        
        with col2:
            if st.button("📝 Take Quiz", use_container_width=True, key="take_quiz"):
                st.switch_page("pages/3_📝_Quiz.py")
        
        with col3:
            if st.button("📊 View Progress", use_container_width=True, key="view_progress"):
                st.switch_page("pages/4_📊_Progress.py")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recent activity (simplified for now)
        st.markdown("### 📈 Your Learning Journey")
        st.info("Start learning to see your recent activity here!")

if __name__ == "__main__":
    main()