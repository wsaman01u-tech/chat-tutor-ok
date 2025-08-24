import streamlit as st
from database import DatabaseManager
from quiz_engine import QuizEngine
from progress_tracker import ProgressTracker
from auth import AuthManager, require_auth
from subjects import SUBJECTS, get_subject_topics

# Configure page
st.set_page_config(
    page_title="Quiz - Educational Tutor",
    page_icon="📝",
    layout="wide"
)

# Initialize components
@st.cache_resource
def init_components():
    db = DatabaseManager()
    quiz = QuizEngine()
    progress = ProgressTracker(db)
    auth = AuthManager(db)
    return db, quiz, progress, auth

def init_session_state():
    """Initialize session state variables"""
    if 'current_subject' not in st.session_state:
        st.session_state.current_subject = None
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = None
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = None
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = None

def main():
    db, quiz, progress, auth = init_components()
    
    # Check authentication
    if not require_auth(auth):
        st.warning("🔒 Please login to access the quiz features.")
        st.page_link("app.py", label="Go to Home", icon="🏠")
        return
    
    init_session_state()
    
    # Enhanced CSS for stunning quiz interface
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .quiz-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .quiz-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    .quiz-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .quiz-container {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .quiz-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 6px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899, #f59e0b);
    }
    
    .question-card {
        background: linear-gradient(145deg, #ffffff 0%, #f1f5f9 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border-left: 6px solid #6366f1;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .question-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
    }
    
    .question-card h4 {
        color: #1e293b;
        font-weight: 700;
        font-size: 1.4rem;
        margin-bottom: 1rem;
    }
    
    .question-card p {
        color: #475569;
        font-size: 1.1rem;
        line-height: 1.7;
        margin: 0;
    }
    
    .score-display {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        margin: 3rem 0;
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .score-display::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        animation: rotate 10s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .score-display h2 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        position: relative;
        z-index: 2;
    }
    
    .score-display h1 {
        font-size: 4rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .score-display p {
        font-size: 1.2rem;
        opacity: 0.9;
        position: relative;
        z-index: 2;
    }
    
    .quiz-start-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        text-align: center;
        margin: 2rem 0;
        border: 2px solid rgba(99, 102, 241, 0.1);
    }
    
    .quiz-start-card h3 {
        color: #1e293b;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .quiz-progress {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        height: 8px;
        border-radius: 4px;
        margin: 2rem 0;
        box-shadow: 0 2px 10px rgba(99, 102, 241, 0.3);
    }
    
    .subject-selection {
        background: linear-gradient(145deg, #f1f5f9 0%, #e2e8f0 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin: 2rem 0;
    }
    
    .subject-button {
        background: white;
        border: 2px solid #e2e8f0;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    .subject-button:hover {
        border-color: #6366f1;
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .topic-list {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .topic-item {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid #e2e8f0;
    }
    
    .topic-item:hover {
        background: #f8fafc;
        border-color: #6366f1;
        transform: translateX(5px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced Header
    st.markdown("""
    <div class="quiz-header">
        <h1>📝 Quiz Center</h1>
        <p>Test your knowledge with AI-generated personalized quizzes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for subject and topic selection
    with st.sidebar:
        st.markdown("### 🎯 Quiz Options")
        
        # Subject selection
        if st.session_state.current_subject:
            st.success(f"📖 Subject: {st.session_state.current_subject}")
            if st.button("Change Subject"):
                st.session_state.current_subject = None
                st.session_state.current_topic = None
                st.session_state.current_quiz = None
                st.session_state.quiz_answers = {}
                st.session_state.quiz_score = None
                st.rerun()
        else:
            st.markdown("**Select a Subject:**")
            for subject, info in SUBJECTS.items():
                if st.button(f"{info['icon']} {subject}", use_container_width=True):
                    st.session_state.current_subject = subject
                    st.session_state.current_topic = None
                    st.session_state.current_quiz = None
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_score = None
                    st.rerun()
        
        # Topic selection
        if st.session_state.current_subject:
            st.divider()
            topics = get_subject_topics(st.session_state.current_subject)
            
            if st.session_state.current_topic:
                st.success(f"📋 Topic: {st.session_state.current_topic}")
                if st.button("Change Topic"):
                    st.session_state.current_topic = None
                    st.session_state.current_quiz = None
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_score = None
                    st.rerun()
            else:
                st.markdown("**Select a Topic:**")
                for i, topic in enumerate(topics):
                    if st.button(f"{i+1}. {topic}", use_container_width=True):
                        st.session_state.current_topic = topic
                        st.session_state.current_quiz = None
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_score = None
                        st.rerun()
        
        # Quiz progress
        if st.session_state.current_quiz:
            st.divider()
            st.markdown("**📊 Quiz Progress:**")
            progress_value = len(st.session_state.quiz_answers) / len(st.session_state.current_quiz['questions'])
            st.progress(progress_value)
            st.caption(f"{len(st.session_state.quiz_answers)}/{len(st.session_state.current_quiz['questions'])} questions answered")
    
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
            # Show progress for each topic
            topic_progress = progress.get_topic_progress(st.session_state.user_id, st.session_state.current_subject, topic)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"📋 {topic}", key=f"topic_{i}", use_container_width=True):
                    st.session_state.current_topic = topic
                    st.rerun()
            with col2:
                if topic_progress['best_score'] > 0:
                    st.metric("Best", f"{topic_progress['best_score']:.0f}%")
                else:
                    st.caption("Not taken")
    
    else:
        # Quiz interface
        st.markdown(f"## 📝 Quiz: {st.session_state.current_topic}")
        st.markdown(f"*Subject: {st.session_state.current_subject}*")
        
        if st.session_state.current_quiz is None:
            # Start new quiz
            st.markdown("""
            <div class="quiz-start-card">
                <h3>🎯 Ready to test your knowledge?</h3>
                <p>Click the button below to start your personalized quiz!</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
                    with st.spinner("🧠 Generating your personalized quiz..."):
                        st.session_state.current_quiz = quiz.generate_quiz(
                            st.session_state.current_subject,
                            st.session_state.current_topic
                        )
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_score = None
                    st.rerun()
        
        else:
            # Display quiz
            quiz_data = st.session_state.current_quiz
            
            st.markdown(f'<div class="quiz-container"><h3>📋 {quiz_data["title"]}</h3></div>', unsafe_allow_html=True)
            
            # Display questions
            for i, question in enumerate(quiz_data['questions']):
                st.markdown(f'<div class="question-card"><h4>Question {i+1}:</h4><p>{question["question"]}</p></div>', unsafe_allow_html=True)
                
                # Radio buttons for answers
                answer_key = f"q_{i}"
                selected_answer = st.radio(
                    f"Select your answer for question {i+1}:",
                    options=question['options'],
                    key=answer_key,
                    index=st.session_state.quiz_answers.get(i, 0)
                )
                
                st.session_state.quiz_answers[i] = question['options'].index(selected_answer)
                st.divider()
            
            # Submit quiz
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("📊 Submit Quiz", type="primary", disabled=len(st.session_state.quiz_answers) < len(quiz_data['questions'])):
                    score = quiz.calculate_score(quiz_data, st.session_state.quiz_answers)
                    st.session_state.quiz_score = score
                    
                    # Update progress
                    progress.update_quiz_progress(
                        st.session_state.user_id,
                        st.session_state.current_subject,
                        st.session_state.current_topic,
                        score
                    )
                    st.rerun()
            
            with col2:
                if st.button("🔄 Reset Quiz"):
                    st.session_state.current_quiz = None
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_score = None
                    st.rerun()
            
            with col3:
                if st.button("📚 Back to Learning"):
                    st.switch_page("pages/2_📚_Learn.py")
            
            # Display results
            if st.session_state.quiz_score is not None:
                score = st.session_state.quiz_score
                
                st.markdown(f'''
                <div class="score-display">
                    <h2>🎉 Quiz Completed!</h2>
                    <h1>{score:.1f}%</h1>
                    <p>Your score</p>
                </div>
                ''', unsafe_allow_html=True)
                
                if score >= 90:
                    st.balloons()
                    st.success("🏆 Outstanding! You've mastered this topic!")
                elif score >= 80:
                    st.success("🎉 Excellent work! You've completed this topic!")
                elif score >= 60:
                    st.info("👍 Good job! Consider reviewing some concepts for better understanding.")
                else:
                    st.warning("📚 Keep studying! Review the material and try again.")
                
                # Get recommendations
                recommendations = quiz.get_recommendations(
                    st.session_state.current_subject,
                    st.session_state.current_topic,
                    score
                )
                
                if recommendations:
                    st.markdown("### 💡 Personalized Recommendations")
                    st.info(recommendations)

if __name__ == "__main__":
    main()
