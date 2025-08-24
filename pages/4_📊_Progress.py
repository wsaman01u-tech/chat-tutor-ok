import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from database import DatabaseManager
from progress_tracker import ProgressTracker
from auth import AuthManager, require_auth
from subjects import SUBJECTS, get_subject_topics

# Configure page
st.set_page_config(
    page_title="Progress - Educational Tutor",
    page_icon="📊",
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
        st.warning("🔒 Please login to access your progress.")
        st.page_link("app.py", label="Go to Home", icon="🏠")
        return
    
    # Enhanced CSS for beautiful progress dashboard
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .progress-header {
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
    
    .progress-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    .progress-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .metric-card {
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
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .metric-card h2 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card p {
        color: #64748b;
        font-weight: 600;
        font-size: 1.1rem;
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
    
    .progress-section {
        background: linear-gradient(145deg, #f1f5f9 0%, #e2e8f0 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin: 3rem 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
    }
    
    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .subject-selector {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .recommendations-section {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border-left: 6px solid #22c55e;
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
    
    # Enhanced Header
    user_info = auth.get_current_user()
    st.markdown(f"""
    <div class="progress-header">
        <h1>📊 {user_info.get('full_name', user_info.get('username', 'Your'))} Progress</h1>
        <p>Track your learning journey and celebrate your achievements</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Subject selector
    st.markdown('<div class="subject-selector">', unsafe_allow_html=True)
    selected_subject = st.selectbox(
        "📚 Select Subject to View Progress:",
        options=list(SUBJECTS.keys()),
        key="progress_subject"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if selected_subject:
        # Get user progress for selected subject
        user_progress = progress.get_user_progress(st.session_state.user_id, selected_subject)
        
        if not user_progress:
            st.info(f"📚 You haven't started learning {selected_subject} yet. Go to the Learn page to begin!")
            if st.button("🚀 Start Learning", type="primary"):
                st.switch_page("pages/2_📚_Learn.py")
            return
        
        # Overall metrics
        topics = get_subject_topics(selected_subject)
        completed_topics = len([t for t in user_progress if user_progress[t]['completed']])
        total_topics = len(topics)
        completion_rate = (completed_topics / total_topics) * 100 if total_topics > 0 else 0
        
        # Calculate average scores
        quiz_scores = [user_progress[t]['best_score'] for t in user_progress if user_progress[t]['best_score'] > 0]
        avg_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0
        total_chats = sum([user_progress[t]['chat_count'] for t in user_progress])
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h2 style="color: #6366f1;">{completed_topics}/{total_topics}</h2>
                <p><strong>Topics Completed</strong></p>
                <p style="color: #22c55e;">{completion_rate:.1f}% Complete</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h2 style="color: #8b5cf6;">{avg_score:.1f}%</h2>
                <p><strong>Average Quiz Score</strong></p>
                <p style="color: #64748b;">Across {len(quiz_scores)} quizzes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h2 style="color: #06b6d4;">{total_chats}</h2>
                <p><strong>Chat Sessions</strong></p>
                <p style="color: #64748b;">Total interactions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            streak_days = progress.get_learning_streak(st.session_state.user_id)
            st.markdown(f"""
            <div class="metric-card">
                <h2 style="color: #f59e0b;">{streak_days}</h2>
                <p><strong>Learning Streak</strong></p>
                <p style="color: #64748b;">Days active</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Progress visualization
        st.markdown('<div class="progress-section">', unsafe_allow_html=True)
        st.markdown("## 📈 Progress Visualization")
        
        # Create progress DataFrame
        progress_data = []
        for topic in topics:
            topic_data = user_progress.get(topic, {'completed': False, 'best_score': 0, 'chat_count': 0})
            progress_data.append({
                'Topic': topic,
                'Completed': topic_data['completed'],
                'Best Score': topic_data['best_score'],
                'Chat Sessions': topic_data['chat_count'],
                'Status': 'Completed' if topic_data['completed'] else 'In Progress'
            })
        
        df = pd.DataFrame(progress_data)
        
        # Two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Quiz scores bar chart
            fig1 = px.bar(
                df,
                x='Topic',
                y='Best Score',
                color='Status',
                title='Quiz Scores by Topic',
                color_discrete_map={'Completed': '#22c55e', 'In Progress': '#94a3b8'},
                height=400
            )
            fig1.update_layout(xaxis_tickangle=-45, showlegend=True)
            fig1.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Chat activity chart
            fig2 = px.bar(
                df,
                x='Topic',
                y='Chat Sessions',
                title='Learning Activity by Topic',
                color_discrete_sequence=['#6366f1'],
                height=400
            )
            fig2.update_layout(xaxis_tickangle=-45)
            fig2.update_traces(texttemplate='%{y}', textposition='outside')
            st.plotly_chart(fig2, use_container_width=True)
        
        # Radar chart for overall performance
        if len(quiz_scores) > 0:
            radar_data = []
            radar_categories = []
            
            for topic in topics[:6]:  # Show first 6 topics in radar
                if topic in user_progress and user_progress[topic]['best_score'] > 0:
                    radar_data.append(user_progress[topic]['best_score'])
                    radar_categories.append(topic[:15] + '...' if len(topic) > 15 else topic)
            
            if radar_data:
                fig3 = go.Figure()
                fig3.add_trace(go.Scatterpolar(
                    r=radar_data,
                    theta=radar_categories,
                    fill='toself',
                    name='Your Performance',
                    line_color='#6366f1'
                ))
                
                fig3.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    showlegend=True,
                    title="Performance Radar Chart",
                    height=400
                )
                st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed progress table
        st.markdown("## 📋 Detailed Progress")
        
        # Format the dataframe for display
        display_df = df.copy()
        display_df['Progress'] = display_df.apply(
            lambda row: f"✅ {row['Best Score']:.1f}%" if row['Completed'] 
            else f"🔄 {row['Best Score']:.1f}%" if row['Best Score'] > 0 
            else "📚 Not started", axis=1
        )
        
        st.dataframe(
            display_df[['Topic', 'Progress', 'Chat Sessions']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Topic": st.column_config.TextColumn("📖 Topic"),
                "Progress": st.column_config.TextColumn("📊 Progress"),
                "Chat Sessions": st.column_config.NumberColumn("💬 Sessions")
            }
        )
        
        # Achievements section
        st.markdown("## 🏆 Achievements")
        
        badges = progress.get_achievement_badges(st.session_state.user_id, selected_subject)
        
        if badges:
            cols = st.columns(min(len(badges), 4))
            for i, badge in enumerate(badges):
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="achievement-badge">
                        <h2>{badge['icon']}</h2>
                        <h4>{badge['name']}</h4>
                        <p>{badge['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("🎯 Keep learning to unlock achievements!")
        
        # Learning recommendations
        st.markdown("## 💡 Learning Recommendations")
        
        recommendations = progress.get_learning_recommendations(st.session_state.user_id, selected_subject)
        
        for i, rec in enumerate(recommendations):
            if i == 0:
                st.success(f"🎯 {rec}")
            else:
                st.info(f"📚 {rec}")
        
        # Study suggestions
        suggestions = progress.get_study_suggestions(st.session_state.user_id, selected_subject)
        
        if suggestions:
            st.markdown("### 📖 Study Tips")
            for suggestion in suggestions:
                st.write(f"• {suggestion}")
        
        # Quick actions
        st.markdown("---")
        st.markdown("## 🚀 Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💬 Continue Learning", use_container_width=True, type="primary"):
                st.switch_page("pages/2_📚_Learn.py")
        
        with col2:
            if st.button("📝 Take a Quiz", use_container_width=True):
                st.switch_page("pages/3_📝_Quiz.py")
        
        with col3:
            # Export progress
            if st.button("📥 Export Progress", use_container_width=True):
                export_data = progress.export_progress_data(st.session_state.user_id, selected_subject)
                st.download_button(
                    label="💾 Download Report",
                    data=str(export_data),
                    file_name=f"progress_{selected_subject}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()
