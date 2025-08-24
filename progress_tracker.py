from datetime import datetime, timedelta
import json

class ProgressTracker:
    def __init__(self, database_manager):
        self.db = database_manager
    
    def get_user_progress(self, user_id, subject):
        """Get comprehensive user progress for a subject"""
        return self.db.get_user_progress(user_id, subject)
    
    def get_topic_progress(self, user_id, subject, topic):
        """Get progress for a specific topic"""
        return self.db.get_topic_progress(user_id, subject, topic)
    
    def update_chat_progress(self, user_id, subject, topic):
        """Update progress based on chat activity"""
        current_progress = self.db.get_topic_progress(user_id, subject, topic)
        new_chat_count = current_progress['chat_count'] + 1
        
        self.db.update_progress(
            user_id, subject, topic,
            chat_count=new_chat_count
        )
        
        # Save chat session record
        self.db.save_chat_session(user_id, subject, topic, 1)
    
    def update_quiz_progress(self, user_id, subject, topic, score):
        """Update progress based on quiz performance"""
        current_progress = self.db.get_topic_progress(user_id, subject, topic)
        
        # Update best score if this is better
        new_best_score = max(current_progress['best_score'], score)
        
        # Mark as completed if score is >= 80%
        completed = score >= 80 or current_progress['completed']
        
        self.db.update_progress(
            user_id, subject, topic,
            best_score=new_best_score,
            completed=completed
        )
        
        # Save quiz attempt
        self.db.save_quiz_attempt(user_id, subject, topic, score, {}, {})
    
    def get_learning_recommendations(self, user_id, subject):
        """Generate learning recommendations based on progress"""
        user_progress = self.get_user_progress(user_id, subject)
        
        if not user_progress:
            return ["Start with the first topic to begin your learning journey!"]
        
        recommendations = []
        
        # Find topics that need attention
        low_score_topics = []
        incomplete_topics = []
        zero_chat_topics = []
        
        for topic, progress in user_progress.items():
            if not progress['completed']:
                incomplete_topics.append(topic)
            
            if progress['best_score'] > 0 and progress['best_score'] < 70:
                low_score_topics.append((topic, progress['best_score']))
            
            if progress['chat_count'] == 0:
                zero_chat_topics.append(topic)
        
        # Generate specific recommendations
        if low_score_topics:
            low_score_topics.sort(key=lambda x: x[1])  # Sort by score
            worst_topic = low_score_topics[0]
            recommendations.append(
                f"Review '{worst_topic[0]}' - your quiz score of {worst_topic[1]:.1f}% suggests you need more practice with this topic."
            )
        
        if zero_chat_topics and len(zero_chat_topics) <= 3:
            recommendations.append(
                f"Start learning: {', '.join(zero_chat_topics[:2])} - you haven't explored these topics yet."
            )
        
        if incomplete_topics:
            recommendations.append(
                f"Focus on completing: {incomplete_topics[0]} - aim for a quiz score of 80% or higher."
            )
        
        # Positive reinforcement
        completed_topics = [t for t in user_progress if user_progress[t]['completed']]
        if completed_topics:
            recommendations.append(
                f"Great job completing {len(completed_topics)} topic(s)! Consider exploring advanced concepts or helping others."
            )
        
        # Study habits recommendations
        total_chats = sum([user_progress[t]['chat_count'] for t in user_progress])
        if total_chats < 5:
            recommendations.append(
                "Try using the chat tutor more often - asking questions helps reinforce learning."
            )
        
        return recommendations if recommendations else ["You're doing great! Keep up the excellent work!"]
    
    def get_learning_streak(self, user_id):
        """Calculate the user's learning streak (days with activity)"""
        # Simple implementation based on recent activity
        try:
            conn = self.db.db.connect() if hasattr(self.db, 'db') else self.db
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(DISTINCT DATE(timestamp)) as active_days
                FROM progress 
                WHERE user_id = ? AND timestamp >= datetime('now', '-7 days')
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else 1
        except:
            # Fallback to a reasonable default
            return 1
    
    def get_achievement_badges(self, user_id, subject):
        """Calculate achievement badges based on progress"""
        user_progress = self.get_user_progress(user_id, subject)
        badges = []
        
        if not user_progress:
            return badges
        
        # Calculate metrics
        completed_topics = [t for t in user_progress if user_progress[t]['completed']]
        quiz_scores = [user_progress[t]['best_score'] for t in user_progress if user_progress[t]['best_score'] > 0]
        total_chats = sum([user_progress[t]['chat_count'] for t in user_progress])
        
        # Award badges
        if len(completed_topics) >= 1:
            badges.append({"name": "First Steps", "icon": "🎯", "description": "Completed your first topic"})
        
        if len(completed_topics) >= 3:
            badges.append({"name": "Getting Started", "icon": "🚀", "description": "Completed 3 topics"})
        
        if len(completed_topics) >= 5:
            badges.append({"name": "Dedicated Learner", "icon": "📚", "description": "Completed 5 topics"})
        
        if quiz_scores and max(quiz_scores) >= 90:
            badges.append({"name": "Quiz Master", "icon": "🏆", "description": "Scored 90% or higher on a quiz"})
        
        if quiz_scores and all(score >= 80 for score in quiz_scores):
            badges.append({"name": "Consistent Performer", "icon": "⭐", "description": "All quiz scores above 80%"})
        
        if total_chats >= 20:
            badges.append({"name": "Curious Mind", "icon": "🤔", "description": "Asked 20+ questions in chat"})
        
        return badges
    
    def export_progress_data(self, user_id, subject):
        """Export user progress data for analysis"""
        user_progress = self.get_user_progress(user_id, subject)
        quiz_history = self.db.get_quiz_history(user_id, subject)
        
        export_data = {
            "user_id": user_id,
            "subject": subject,
            "export_date": datetime.now().isoformat(),
            "progress_summary": user_progress,
            "quiz_history": quiz_history,
            "achievements": self.get_achievement_badges(user_id, subject)
        }
        
        return export_data
    
    def get_study_suggestions(self, user_id, subject):
        """Get AI-powered study suggestions based on progress patterns"""
        user_progress = self.get_user_progress(user_id, subject)
        
        if not user_progress:
            return ["Begin with the fundamentals and work your way up systematically."]
        
        suggestions = []
        
        # Analyze patterns
        completed_count = len([t for t in user_progress if user_progress[t]['completed']])
        total_count = len(user_progress)
        completion_rate = completed_count / total_count if total_count > 0 else 0
        
        avg_score = 0
        quiz_taken_count = 0
        for topic, progress in user_progress.items():
            if progress['best_score'] > 0:
                avg_score += progress['best_score']
                quiz_taken_count += 1
        
        if quiz_taken_count > 0:
            avg_score = avg_score / quiz_taken_count
        
        # Generate suggestions based on patterns
        if completion_rate < 0.3:
            suggestions.append("Focus on completing topics systematically rather than jumping around.")
        
        if avg_score < 70 and quiz_taken_count > 0:
            suggestions.append("Spend more time with the chat tutor before taking quizzes to build stronger understanding.")
        
        if avg_score > 85:
            suggestions.append("You're performing excellently! Consider exploring advanced topics or teaching others.")
        
        # Study timing suggestions
        active_topics = [t for t in user_progress if user_progress[t]['chat_count'] > 0 and not user_progress[t]['completed']]
        if len(active_topics) > 3:
            suggestions.append("Consider focusing on fewer topics at once for deeper understanding.")
        
        return suggestions if suggestions else ["Keep up the great work! Your learning approach is effective."]
