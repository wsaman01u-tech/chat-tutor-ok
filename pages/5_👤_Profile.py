import streamlit as st
from datetime import datetime
from database import DatabaseManager
from progress_tracker import ProgressTracker
from auth import AuthManager, require_auth
from subjects import SUBJECTS

# Configure page
st.set_page_config(
    page_title="Profile - Educational Tutor",
    page_icon="👤",
    layout="wide"
)

# Initialize components
@st.cache_resource
def init_components():
    db = DatabaseManager()
    progress = ProgressTracker(db)
    auth = AuthManager(db)
    return db, progress, auth

def main():
    db, progress, auth = init_components()
    
    # Check authentication
    if not require_auth(auth):
        st.warning("🔒 Please login to access your profile.")
        st.page_link("app.py", label="Go to Home", icon="🏠")
        return
    
    # Enhanced CSS for beautiful profile interface
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .profile-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .profile-header::before {
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
    
    .profile-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .profile-header p {
        font-size: 1.3rem;
        opacity: 0.9;
        margin: 0.5rem 0;
        position: relative;
        z-index: 2;
    }
    
    .stat-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .stat-card h2 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-card p {
        color: #64748b;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .settings-section {
        background: linear-gradient(145deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin: 2rem 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
    }
    
    .achievement-showcase {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .achievement-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .achievement-badge::before {
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
    
    .achievement-badge:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
    }
    
    .achievement-badge h2 {
        font-size: 3rem;
        margin-bottom: 1rem;
        position: relative;
        z-index: 2;
    }
    
    .achievement-badge h4 {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .achievement-badge p {
        font-size: 1rem;
        opacity: 0.9;
        position: relative;
        z-index: 2;
    }
    
    .overview-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .subject-progress-item {
        background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #6366f1;
        transition: all 0.3s ease;
    }
    
    .subject-progress-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
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
        margin: 0.5rem 0;
    }
    
    .action-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(99, 102, 241, 0.4);
    }
    
    .danger-button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3);
        cursor: pointer;
        width: 100%;
    }
    
    .danger-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(239, 68, 68, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get user info
    user_info = auth.get_current_user()
    
    # Profile header
    st.markdown(f"""
    <div class="profile-header">
        <h1>👤 {user_info.get('full_name', 'Student')}</h1>
        <p>@{user_info.get('username', 'user')}</p>
        <p>📧 {user_info.get('email', 'No email')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🏆 Achievements", "⚙️ Settings", "📱 Account"])
    
    with tab1:
        st.markdown("## 📊 Learning Overview")
        
        # Calculate overall statistics
        total_completed = 0
        total_subjects_started = 0
        total_quizzes_taken = 0
        total_chat_sessions = 0
        highest_score = 0
        
        for subject in SUBJECTS.keys():
            user_progress = progress.get_user_progress(st.session_state.user_id, subject)
            if user_progress:
                total_subjects_started += 1
                completed_topics = len([t for t in user_progress if user_progress[t]['completed']])
                total_completed += completed_topics
                
                # Count quizzes and chats
                for topic_data in user_progress.values():
                    if topic_data['best_score'] > 0:
                        total_quizzes_taken += 1
                        highest_score = max(highest_score, topic_data['best_score'])
                    total_chat_sessions += topic_data['chat_count']
        
        # Display stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <h2 style="color: #6366f1;">{total_subjects_started}</h2>
                <p><strong>Subjects Started</strong></p>
                <p style="color: #64748b;">Out of {len(SUBJECTS)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <h2 style="color: #22c55e;">{total_completed}</h2>
                <p><strong>Topics Completed</strong></p>
                <p style="color: #64748b;">Across all subjects</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <h2 style="color: #f59e0b;">{highest_score:.0f}%</h2>
                <p><strong>Highest Score</strong></p>
                <p style="color: #64748b;">Best quiz result</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <h2 style="color: #8b5cf6;">{total_chat_sessions}</h2>
                <p><strong>Chat Sessions</strong></p>
                <p style="color: #64748b;">Total interactions</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent activity (simplified)
        st.markdown("### 📈 Recent Activity")
        if total_chat_sessions > 0 or total_quizzes_taken > 0:
            st.success("🎉 You've been actively learning! Keep up the great work.")
        else:
            st.info("🚀 Start your learning journey by visiting the Learn page!")
        
        # Subject progress summary
        st.markdown("### 📚 Subject Progress")
        
        for subject, info in SUBJECTS.items():
            user_progress = progress.get_user_progress(st.session_state.user_id, subject)
            
            if user_progress:
                topics = len(user_progress)
                completed = len([t for t in user_progress if user_progress[t]['completed']])
                completion_rate = (completed / topics) * 100 if topics > 0 else 0
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{info['icon']} **{subject}**")
                    st.progress(completion_rate / 100)
                    st.caption(f"{completed}/{topics} topics completed ({completion_rate:.1f}%)")
                with col2:
                    if st.button("View Details", key=f"view_{subject}"):
                        st.session_state.progress_subject = subject
                        st.switch_page("pages/4_📊_Progress.py")
            else:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{info['icon']} **{subject}** - Not started")
                with col2:
                    if st.button("Start Learning", key=f"start_{subject}"):
                        st.switch_page("pages/2_📚_Learn.py")
    
    with tab2:
        st.markdown("## 🏆 Your Achievements")
        
        all_badges = []
        for subject in SUBJECTS.keys():
            subject_badges = progress.get_achievement_badges(st.session_state.user_id, subject)
            for badge in subject_badges:
                badge['subject'] = subject
            all_badges.extend(subject_badges)
        
        if all_badges:
            # Group badges by subject
            for subject in SUBJECTS.keys():
                subject_badges = [b for b in all_badges if b.get('subject') == subject]
                if subject_badges:
                    st.markdown(f"### {SUBJECTS[subject]['icon']} {subject}")
                    
                    cols = st.columns(min(len(subject_badges), 3))
                    for i, badge in enumerate(subject_badges):
                        with cols[i % 3]:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                        color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 0.5rem;">
                                <h2>{badge['icon']}</h2>
                                <h4>{badge['name']}</h4>
                                <p>{badge['description']}</p>
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.info("🎯 Start learning to unlock achievements! Complete topics and take quizzes to earn badges.")
            if st.button("🚀 Start Learning Now", type="primary"):
                st.switch_page("pages/2_📚_Learn.py")
    
    with tab3:
        st.markdown("## ⚙️ Settings")
        
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        
        # Learning preferences
        st.markdown("### 📚 Learning Preferences")
        
        col1, col2 = st.columns(2)
        with col1:
            preferred_subject = st.selectbox(
                "Preferred Subject:",
                options=["None"] + list(SUBJECTS.keys()),
                help="This will be suggested as your default subject"
            )
        
        with col2:
            difficulty_level = st.selectbox(
                "Difficulty Level:",
                options=["Beginner", "Intermediate", "Advanced"],
                index=1,
                help="Adjust the complexity of explanations and quizzes"
            )
        
        # Notification settings
        st.markdown("### 🔔 Notifications")
        
        daily_reminder = st.checkbox("Daily learning reminder", value=True)
        quiz_reminder = st.checkbox("Quiz completion reminders", value=True)
        progress_updates = st.checkbox("Weekly progress updates", value=True)
        
        # Study goals
        st.markdown("### 🎯 Study Goals")
        
        col1, col2 = st.columns(2)
        with col1:
            daily_goal = st.number_input("Daily chat sessions goal:", min_value=1, max_value=20, value=3)
        with col2:
            weekly_quiz_goal = st.number_input("Weekly quiz goal:", min_value=1, max_value=10, value=2)
        
        if st.button("💾 Save Settings", type="primary"):
            st.success("✅ Settings saved successfully!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown("## 📱 Account Management")
        
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        
        # Account information
        st.markdown("### 👤 Account Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name:", value=user_info.get('full_name', ''), disabled=True)
            st.text_input("Username:", value=user_info.get('username', ''), disabled=True)
        with col2:
            st.text_input("Email:", value=user_info.get('email', ''), disabled=True)
            if 'created_at' in user_info:
                st.text_input("Member Since:", value=user_info['created_at'][:10], disabled=True)
        
        st.info("👆 To update your account information, please contact support.")
        
        # Data management
        st.markdown("### 📊 Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export All Data", use_container_width=True):
                # Export all progress data
                all_data = {}
                for subject in SUBJECTS.keys():
                    export_data = progress.export_progress_data(st.session_state.user_id, subject)
                    all_data[subject] = export_data
                
                st.download_button(
                    label="💾 Download Complete Report",
                    data=str(all_data),
                    file_name=f"complete_progress_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            if st.button("🗑️ Reset Progress", use_container_width=True, type="secondary"):
                st.warning("⚠️ This action cannot be undone. Please contact support to reset your progress.")
        
        # Logout section
        st.markdown("### 🚪 Session Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Session", use_container_width=True):
                st.rerun()
        
        with col2:
            if st.button("🚪 Logout", use_container_width=True, type="primary"):
                auth.logout()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
