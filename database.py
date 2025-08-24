import sqlite3
import json
from datetime import datetime
import os
import hashlib
import uuid

class DatabaseManager:
    def __init__(self, db_path="education_tutor.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                subject TEXT,
                topic TEXT,
                completed BOOLEAN DEFAULT FALSE,
                best_score REAL DEFAULT 0,
                chat_count INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Quiz attempts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                subject TEXT,
                topic TEXT,
                score REAL,
                questions_data TEXT,
                answers_data TEXT,
                attempt_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Chat sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                subject TEXT,
                topic TEXT,
                message_count INTEGER DEFAULT 0,
                session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def ensure_user_exists(self, user_id):
        """Ensure user exists in database (legacy support)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        if not cursor.fetchone():
            # Create a legacy user for backward compatibility
            cursor.execute(
                'INSERT OR IGNORE INTO users (user_id, username, email, password_hash) VALUES (?, ?, ?, ?)',
                (user_id, f'guest_{user_id[:8]}', f'{user_id}@guest.local', 'legacy')
            )
        
        conn.commit()
        conn.close()
    
    def get_user_progress(self, user_id, subject):
        """Get user progress for a specific subject"""
        self.ensure_user_exists(user_id)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT topic, completed, best_score, chat_count
            FROM progress
            WHERE user_id = ? AND subject = ?
        ''', (user_id, subject))
        
        results = cursor.fetchall()
        conn.close()
        
        progress = {}
        for topic, completed, best_score, chat_count in results:
            progress[topic] = {
                'completed': bool(completed),
                'best_score': best_score,
                'chat_count': chat_count
            }
        
        return progress
    
    def get_topic_progress(self, user_id, subject, topic):
        """Get progress for a specific topic"""
        self.ensure_user_exists(user_id)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT completed, best_score, chat_count
            FROM progress
            WHERE user_id = ? AND subject = ? AND topic = ?
        ''', (user_id, subject, topic))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            completed, best_score, chat_count = result
            return {
                'completed': bool(completed),
                'best_score': best_score,
                'chat_count': chat_count
            }
        else:
            return {
                'completed': False,
                'best_score': 0,
                'chat_count': 0
            }
    
    def update_progress(self, user_id, subject, topic, **kwargs):
        """Update progress for a specific topic"""
        self.ensure_user_exists(user_id)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if progress record exists
        cursor.execute('''
            SELECT id FROM progress
            WHERE user_id = ? AND subject = ? AND topic = ?
        ''', (user_id, subject, topic))
        
        if cursor.fetchone():
            # Update existing record
            set_clauses = []
            values = []
            
            for key, value in kwargs.items():
                if key in ['completed', 'best_score', 'chat_count']:
                    set_clauses.append(f'{key} = ?')
                    values.append(value)
            
            if set_clauses:
                set_clauses.append('last_updated = CURRENT_TIMESTAMP')
                values.extend([user_id, subject, topic])
                
                cursor.execute(f'''
                    UPDATE progress
                    SET {', '.join(set_clauses)}
                    WHERE user_id = ? AND subject = ? AND topic = ?
                ''', values)
        else:
            # Insert new record
            cursor.execute('''
                INSERT INTO progress (user_id, subject, topic, completed, best_score, chat_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id, subject, topic,
                kwargs.get('completed', False),
                kwargs.get('best_score', 0),
                kwargs.get('chat_count', 0)
            ))
        
        conn.commit()
        conn.close()
    
    def save_quiz_attempt(self, user_id, subject, topic, score, questions_data, answers_data):
        """Save a quiz attempt"""
        self.ensure_user_exists(user_id)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO quiz_attempts (user_id, subject, topic, score, questions_data, answers_data)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id, subject, topic, score,
            json.dumps(questions_data),
            json.dumps(answers_data)
        ))
        
        conn.commit()
        conn.close()
    
    def save_chat_session(self, user_id, subject, topic, message_count):
        """Save a chat session"""
        self.ensure_user_exists(user_id)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_sessions (user_id, subject, topic, message_count)
            VALUES (?, ?, ?, ?)
        ''', (user_id, subject, topic, message_count))
        
        conn.commit()
        conn.close()
    
    def get_quiz_history(self, user_id, subject, topic=None):
        """Get quiz history for a user"""
        self.ensure_user_exists(user_id)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if topic:
            cursor.execute('''
                SELECT score, attempt_date
                FROM quiz_attempts
                WHERE user_id = ? AND subject = ? AND topic = ?
                ORDER BY attempt_date DESC
            ''', (user_id, subject, topic))
        else:
            cursor.execute('''
                SELECT topic, score, attempt_date
                FROM quiz_attempts
                WHERE user_id = ? AND subject = ?
                ORDER BY attempt_date DESC
            ''', (user_id, subject))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def create_user(self, username, email, password, full_name=None):
        """Create a new user account"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Generate user ID and hash password
            user_id = str(uuid.uuid4())
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO users (user_id, username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, email, password_hash, full_name))
            
            conn.commit()
            conn.close()
            return user_id
            
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('''
            SELECT user_id, username, email, full_name
            FROM users
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'user_id': result[0],
                'username': result[1],
                'email': result[2],
                'full_name': result[3]
            }
        return None
    
    def get_user_by_username(self, username):
        """Get user info by username"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, email, full_name, created_at
            FROM users
            WHERE username = ?
        ''', (username,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'user_id': result[0],
                'username': result[1],
                'email': result[2],
                'full_name': result[3],
                'created_at': result[4]
            }
        return None
