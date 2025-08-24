import os
import json
from google import genai
from google.genai import types
import random

class QuizEngine:
    def __init__(self):
        # Using Google Gemini AI for quiz generation
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.5-pro"
    
    def generate_quiz(self, subject, topic, num_questions=5):
        """Generate a quiz for the specified topic"""
        try:
            prompt = f"""Create a {num_questions}-question multiple choice quiz about {topic} in {subject}.
            
            Requirements:
            - Each question should test understanding of key concepts
            - Provide 4 multiple choice options (A, B, C, D)
            - Mix difficulty levels (easy, medium, hard)
            - Include clear, unambiguous questions
            - Make sure there's only one clearly correct answer per question
            
            Return the quiz in the following JSON format:
            {{
                "title": "Quiz title",
                "questions": [
                    {{
                        "question": "Question text",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": 0,
                        "explanation": "Brief explanation of the correct answer",
                        "difficulty": "easy|medium|hard"
                    }}
                ]
            }}
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            content = response.text or '{}'
            quiz_data = json.loads(content)
            
            # Validate and sanitize the quiz data
            if not self._validate_quiz_data(quiz_data):
                return self._generate_fallback_quiz(subject, topic)
            
            return quiz_data
            
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return self._generate_fallback_quiz(subject, topic)
    
    def _validate_quiz_data(self, quiz_data):
        """Validate the structure of quiz data"""
        try:
            required_fields = ['title', 'questions']
            if not all(field in quiz_data for field in required_fields):
                return False
            
            questions = quiz_data['questions']
            if not isinstance(questions, list) or len(questions) == 0:
                return False
            
            for question in questions:
                required_q_fields = ['question', 'options', 'correct_answer']
                if not all(field in question for field in required_q_fields):
                    return False
                
                if not isinstance(question['options'], list) or len(question['options']) != 4:
                    return False
                
                if not isinstance(question['correct_answer'], int) or question['correct_answer'] not in range(4):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def _generate_fallback_quiz(self, subject, topic):
        """Generate a basic fallback quiz if AI generation fails"""
        return {
            "title": f"{topic} Quiz",
            "questions": [
                {
                    "question": f"Which of the following is a key concept in {topic}?",
                    "options": [
                        "Concept A",
                        "Concept B", 
                        "Concept C",
                        "All of the above"
                    ],
                    "correct_answer": 3,
                    "explanation": "This is a basic question about key concepts.",
                    "difficulty": "easy"
                }
            ]
        }
    
    def calculate_score(self, quiz_data, user_answers):
        """Calculate the quiz score based on user answers"""
        if not quiz_data or 'questions' not in quiz_data:
            return 0
        
        questions = quiz_data['questions']
        correct_answers = 0
        total_questions = len(questions)
        
        for i, question in enumerate(questions):
            if i in user_answers and user_answers[i] == question['correct_answer']:
                correct_answers += 1
        
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        return round(score, 1)
    
    def get_detailed_results(self, quiz_data, user_answers):
        """Get detailed results showing correct/incorrect answers"""
        if not quiz_data or 'questions' not in quiz_data:
            return []
        
        results = []
        questions = quiz_data['questions']
        
        for i, question in enumerate(questions):
            user_answer = user_answers.get(i, -1)
            correct_answer = question['correct_answer']
            is_correct = user_answer == correct_answer
            
            result = {
                'question_num': i + 1,
                'question': question['question'],
                'user_answer': question['options'][user_answer] if user_answer >= 0 else "Not answered",
                'correct_answer': question['options'][correct_answer],
                'is_correct': is_correct,
                'explanation': question.get('explanation', ''),
                'difficulty': question.get('difficulty', 'medium')
            }
            
            results.append(result)
        
        return results
    
    def get_recommendations(self, subject, topic, score):
        """Get personalized learning recommendations based on quiz performance"""
        try:
            if score >= 90:
                performance = "excellent"
            elif score >= 80:
                performance = "good"
            elif score >= 60:
                performance = "fair"
            else:
                performance = "needs_improvement"
            
            prompt = f"""A student just completed a quiz on {topic} in {subject} with a score of {score}% (performance level: {performance}).
            
            Provide personalized learning recommendations including:
            1. Feedback on their performance
            2. Specific areas to focus on for improvement
            3. Study strategies tailored to this topic
            4. Next steps in their learning journey
            5. Encouragement and motivation
            
            Keep the response concise but actionable."""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text or "Unable to generate recommendations at the moment."
            
        except Exception as e:
            # Fallback recommendations based on score
            if score >= 80:
                return "🎉 Great job! You've demonstrated a solid understanding of this topic. Consider exploring more advanced concepts or helping others learn this material."
            elif score >= 60:
                return "👍 Good effort! Review the areas where you had difficulty and try some practice problems to strengthen your understanding."
            else:
                return "📚 Keep studying! Focus on the fundamental concepts and don't hesitate to ask questions. Consider reviewing the material again and taking practice quizzes."
    
    def analyze_performance_trends(self, quiz_history):
        """Analyze performance trends across multiple quiz attempts"""
        if not quiz_history or len(quiz_history) < 2:
            return "Take more quizzes to see your performance trends!"
        
        scores = [attempt['score'] for attempt in quiz_history]
        latest_score = scores[0]  # Most recent
        previous_score = scores[1]
        
        if latest_score > previous_score:
            trend = "improving"
        elif latest_score < previous_score:
            trend = "declining"
        else:
            trend = "stable"
        
        avg_score = sum(scores) / len(scores)
        
        analysis = f"📈 **Performance Analysis:**\n"
        analysis += f"- Latest Score: {latest_score}%\n"
        analysis += f"- Average Score: {avg_score:.1f}%\n"
        analysis += f"- Trend: {trend.title()}\n"
        
        if trend == "improving":
            analysis += "🎉 You're making great progress! Keep up the excellent work."
        elif trend == "declining":
            analysis += "📚 Consider reviewing the material and identifying areas that need more focus."
        else:
            analysis += "✅ Your performance is consistent. Try challenging yourself with harder topics."
        
        return analysis
