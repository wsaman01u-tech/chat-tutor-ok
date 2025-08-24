import streamlit as st
from database import DatabaseManager
from tutor_engine import TutorEngine
from progress_tracker import ProgressTracker
from auth import AuthManager, require_auth
from subjects import SUBJECTS, get_subject_topics

# Configure page
st.set_page_config(
    page_title="Learn - Educational Tutor",
    page_icon="📚",
    layout="wide"
)

# Initialize components
@st.cache_resource
def init_components():
    db = DatabaseManager()
    tutor = TutorEngine()
    progress = ProgressTracker(db)
    auth = AuthManager(db)
    return db, tutor, progress, auth

def init_session_state():
    """Initialize session state variables"""
    if 'current_subject' not in st.session_state:
        st.session_state.current_subject = None
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def main():
    db, tutor, progress, auth = init_components()
    
    # Check authentication
    if not require_auth(auth):
        st.warning("🔒 Please login to access the learning features.")
        st.page_link("app.py", label="Go to Home", icon="🏠")
        return
    
    init_session_state()
    
    # Enhanced CSS for beautiful chat interface
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .chat-message-user {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
        position: relative;
        max-width: 80%;
        margin-left: auto;
    }
    
    .chat-message-user::before {
        content: '';
        position: absolute;
        bottom: 0;
        right: -10px;
        width: 0;
        height: 0;
        border: 10px solid transparent;
        border-left-color: #8b5cf6;
        border-bottom-color: transparent;
        border-right-color: transparent;
    }
    
    .chat-message-assistant {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        color: #1e293b;
        padding: 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 4px solid #6366f1;
        position: relative;
        max-width: 80%;
    }
    
    .chat-message-assistant::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: -10px;
        width: 0;
        height: 0;
        border: 10px solid transparent;
        border-right-color: #f8fafc;
        border-bottom-color: transparent;
        border-left-color: transparent;
    }
    
    .subject-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .subject-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
    }
    
    .subject-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .learning-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    }
    
    .learning-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .quick-action-btn {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
        cursor: pointer;
        width: 100%;
        margin: 0.5rem 0;
    }
    
    .quick-action-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(99, 102, 241, 0.4);
    }
    
    .sidebar-section {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .progress-indicator {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .topic-button {
        background: white;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
        text-align: left;
    }
    
    .topic-button:hover {
        border-color: #6366f1;
        background: #f8fafc;
        transform: translateX(5px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced Header
    st.markdown("""
    <div class="learning-header">
        <h1>📚 Interactive Learning</h1>
        <p>Engage with AI-powered tutoring tailored to your learning pace</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Sidebar for subject and topic selection
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🎯 Learning Options")
        
        # Subject selection
        if st.session_state.current_subject:
            st.success(f"📖 Subject: {st.session_state.current_subject}")
            if st.button("Change Subject"):
                st.session_state.current_subject = None
                st.session_state.current_topic = None
                st.session_state.chat_history = []
                st.rerun()
        else:
            st.markdown("**Select a Subject:**")
            for subject, info in SUBJECTS.items():
                if st.button(f"{info['icon']} {subject}", use_container_width=True):
                    st.session_state.current_subject = subject
                    st.session_state.current_topic = None
                    st.session_state.chat_history = []
                    st.rerun()
        
        # Topic selection
        if st.session_state.current_subject:
            st.divider()
            topics = get_subject_topics(st.session_state.current_subject)
            
            if st.session_state.current_topic:
                st.success(f"📋 Topic: {st.session_state.current_topic}")
                if st.button("Change Topic"):
                    st.session_state.current_topic = None
                    st.session_state.chat_history = []
                    st.rerun()
            else:
                st.markdown("**Select a Topic:**")
                for i, topic in enumerate(topics):
                    if st.button(f"{i+1}. {topic}", use_container_width=True):
                        st.session_state.current_topic = topic
                        st.session_state.chat_history = []
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Progress display
        if st.session_state.current_subject and st.session_state.current_topic:
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            topic_progress = progress.get_topic_progress(
                st.session_state.user_id, 
                st.session_state.current_subject, 
                st.session_state.current_topic
            )
            
            st.markdown("**📈 Your Progress:**")
            if topic_progress['completed']:
                st.markdown('<div class="progress-indicator">✅ Completed!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="progress-indicator" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">🔄 In Progress</div>', unsafe_allow_html=True)
            
            if topic_progress['best_score'] > 0:
                st.metric("Best Quiz Score", f"{topic_progress['best_score']:.1f}%")
            
            st.metric("Chat Sessions", topic_progress['chat_count'])
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    if not st.session_state.current_subject:
        # Subject selection
        st.markdown("## 🎯 Choose Your Subject")
        
        cols = st.columns(2)
        for i, (subject, info) in enumerate(SUBJECTS.items()):
            with cols[i % 2]:
                if st.button(f"{info['icon']} {subject}", key=f"main_{subject}", use_container_width=True):
                    st.session_state.current_subject = subject
                    st.rerun()
                st.caption(info['description'])
    
    elif not st.session_state.current_topic:
        # Topic selection
        st.markdown(f"## 📖 {st.session_state.current_subject} Topics")
        
        topics = get_subject_topics(st.session_state.current_subject)
        
        for i, topic in enumerate(topics):
            if st.button(f"📋 {topic}", key=f"topic_{i}", use_container_width=True):
                st.session_state.current_topic = topic
                st.rerun()
    
    else:
        # Chat interface
        st.markdown(f"## 💬 Learning: {st.session_state.current_topic}")
        st.markdown(f"*Subject: {st.session_state.current_subject}*")
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-message-user"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message-assistant"><strong>Tutor:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        
        # Chat input
        if prompt := st.chat_input("Ask a question about the topic..."):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Generate response
            with st.spinner("🤔 Thinking..."):
                response = tutor.generate_response(
                    subject=st.session_state.current_subject,
                    topic=st.session_state.current_topic,
                    question=prompt,
                    chat_history=st.session_state.chat_history[:-1]
                )
            
            # Add assistant response
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Update progress
            progress.update_chat_progress(
                st.session_state.user_id,
                st.session_state.current_subject,
                st.session_state.current_topic
            )
            
            st.rerun()
        
        # Quick action buttons
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎯 Get Learning Tips"):
                tips = tutor.get_learning_tips(st.session_state.current_subject, st.session_state.current_topic)
                st.session_state.chat_history.append({"role": "assistant", "content": tips})
                progress.update_chat_progress(st.session_state.user_id, st.session_state.current_subject, st.session_state.current_topic)
                st.rerun()
        
        with col2:
            if st.button("📝 Practice Problem"):
                problem = tutor.generate_practice_problem(st.session_state.current_subject, st.session_state.current_topic)
                st.session_state.chat_history.append({"role": "assistant", "content": problem})
                progress.update_chat_progress(st.session_state.user_id, st.session_state.current_subject, st.session_state.current_topic)
                st.rerun()
        
        with col3:
            if st.button("🔍 Explain Concept"):
                explanation = tutor.explain_concept(st.session_state.current_subject, st.session_state.current_topic)
                st.session_state.chat_history.append({"role": "assistant", "content": explanation})
                progress.update_chat_progress(st.session_state.user_id, st.session_state.current_subject, st.session_state.current_topic)
                st.rerun()

if __name__ == "__main__":
    main()
