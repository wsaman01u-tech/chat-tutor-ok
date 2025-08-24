import os
import json
from google import genai
from google.genai import types

class TutorEngine:
    def __init__(self):
        # Using Google Gemini AI for educational content generation
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.5-flash"
    
    def generate_response(self, subject, topic, question, chat_history=None):
        """Generate a tutoring response based on the question and context"""
        try:
            # Build context from chat history
            context = ""
            if chat_history:
                context = "\n".join([
                    f"{'Student' if msg['role'] == 'user' else 'Tutor'}: {msg['content']}"
                    for msg in chat_history[-5:]  # Last 5 messages for context
                ])
            
            # Create the tutoring prompt
            system_prompt = f"""You are an expert educational tutor specializing in {subject}. 
            You are currently helping a student learn about {topic}.
            
            Your teaching style should be:
            - Patient and encouraging
            - Use step-by-step explanations
            - Provide examples when helpful
            - Ask guiding questions to help student think
            - Adapt to the student's level of understanding
            - Be concise but thorough
            
            Previous conversation context:
            {context}
            """
            
            user_prompt = f"""Student's question about {topic}: {question}
            
            Please provide a helpful tutoring response that guides the student's learning."""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(role="user", parts=[types.Part(text=f"{system_prompt}\n\n{user_prompt}")])
                ]
            )
            
            return response.text or "I apologize, but I'm having trouble processing your question right now."
            
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your question right now. Please try again or rephrase your question. Error: {str(e)}"
    
    def get_learning_tips(self, subject, topic):
        """Generate learning tips for a specific topic"""
        try:
            prompt = f"""As an expert {subject} tutor, provide 3-5 specific learning tips for studying {topic}. 
            Focus on effective study strategies, common pitfalls to avoid, and practical advice for mastering this topic.
            
            Format your response as a helpful guide with actionable tips."""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return "🎯 **Learning Tips for " + topic + ":**\n\n" + (response.text or "Unable to generate learning tips at the moment.")
            
        except Exception as e:
            return f"Unable to generate learning tips at the moment. Please try again later. Error: {str(e)}"
    
    def generate_practice_problem(self, subject, topic):
        """Generate a practice problem for the topic"""
        try:
            prompt = f"""Create a practice problem for {subject} - {topic} that would help a student understand the key concepts.
            
            Include:
            1. A clear problem statement
            2. Any necessary context or given information
            3. What the student should find or solve
            
            Make it educational and appropriately challenging. Don't include the solution - the student should work through it."""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            content = response.text or "Unable to generate practice problem at this time."
            return "📝 **Practice Problem:**\n\n" + content + "\n\n*Try to solve this step by step, and feel free to ask for hints if you get stuck!*"
            
        except Exception as e:
            return f"Unable to generate a practice problem at the moment. Please try again later. Error: {str(e)}"
    
    def explain_concept(self, subject, topic):
        """Provide a clear explanation of the topic concept"""
        try:
            prompt = f"""Provide a clear, comprehensive explanation of {topic} in {subject}.
            
            Structure your explanation with:
            1. What it is (definition)
            2. Why it's important
            3. How it works or key principles
            4. A simple example if applicable
            5. Connection to other related concepts
            
            Make it accessible but thorough, suitable for someone learning this topic."""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return "🔍 **Concept Explanation: " + topic + "**\n\n" + (response.text or "Unable to provide concept explanation at the moment.")
            
        except Exception as e:
            return f"Unable to provide concept explanation at the moment. Please try again later. Error: {str(e)}"
    
    def get_study_recommendations(self, subject, topic, performance_data):
        """Get personalized study recommendations based on performance"""
        try:
            prompt = f"""Based on a student's performance in {subject} - {topic}, provide personalized study recommendations.
            
            Performance data: {performance_data}
            
            Provide specific, actionable recommendations for:
            1. Areas to focus on
            2. Study strategies
            3. Next steps for improvement
            4. Resources or practice suggestions
            
            Be encouraging and constructive."""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text or "Unable to generate recommendations at the moment."
            
        except Exception as e:
            return f"Unable to generate recommendations at the moment. Please try again later. Error: {str(e)}"
