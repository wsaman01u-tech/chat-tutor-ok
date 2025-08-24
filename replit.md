# Education Tutor System

## Overview

This is an AI-powered educational tutoring application that provides personalized learning experiences across multiple academic subjects including Calculus, Programming, Physics, Chemistry, and Statistics. The system combines interactive tutoring through OpenAI's GPT-4o model with quiz generation capabilities, progress tracking, and comprehensive learning analytics. Students can engage in conversational learning sessions on specific topics and take assessments to measure their understanding and progress.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Application Structure
The application follows a modular architecture with clear separation of concerns across five main components:

**Database Layer (`database.py`)**
- Uses SQLite for local data persistence with a lightweight, file-based approach
- Implements three core tables: users, progress, and quiz_attempts
- Provides comprehensive tracking of user activity, learning progress, and assessment history
- Chosen for simplicity and zero-configuration deployment requirements

**Subject Management (`subjects.py`)**
- Centralizes subject and topic definitions in a structured dictionary format
- Supports five core academic subjects with predefined topic hierarchies
- Includes metadata for UI presentation (icons, colors, descriptions)
- Enables easy expansion to additional subjects without code changes

**AI Tutoring Engine (`tutor_engine.py`)**
- Integrates OpenAI GPT-4o for conversational tutoring experiences
- Maintains conversation context for coherent multi-turn interactions
- Implements adaptive teaching strategies with step-by-step explanations
- Uses system prompts to ensure consistent, educational-focused responses

**Quiz Generation System (`quiz_engine.py`)**
- Leverages OpenAI for dynamic assessment creation
- Generates structured multiple-choice questions with varying difficulty levels
- Provides automatic validation and sanitization of generated content
- Returns standardized JSON format for consistent UI integration

**Progress Analytics (`progress_tracker.py`)**
- Tracks both chat-based learning activities and quiz performance
- Implements completion criteria (80% quiz score threshold)
- Maintains historical records for learning analytics
- Provides foundation for recommendation engine development

### Data Flow Architecture
The system implements a layered data flow:
1. User interactions captured through chat/quiz interfaces
2. AI engines process requests with subject/topic context
3. Progress tracker updates learning metrics
4. Database manager persists all activity data
5. Analytics inform future learning recommendations

### Design Principles
- **Modularity**: Each component has single responsibility and clear interfaces
- **Extensibility**: Easy addition of new subjects, topics, and assessment types
- **Offline Capability**: SQLite enables local operation without external database dependencies
- **AI-First**: OpenAI integration provides intelligent content generation and personalized responses

## External Dependencies

**OpenAI API Integration**
- Primary dependency for AI-powered tutoring and quiz generation
- Uses GPT-4o model for optimal educational content quality
- Requires API key configuration for operation
- Implements structured prompting for consistent educational responses

**SQLite Database**
- Embedded database solution for local data persistence
- No external database server required
- Supports full CRUD operations for user progress tracking
- Provides ACID compliance for data integrity

**Python Standard Libraries**
- json: API response parsing and data serialization
- datetime: Timestamp management and progress tracking
- os: Environment variable access for API configuration
- sqlite3: Database connectivity and query execution

**Development Environment**
- Designed for Replit deployment with minimal configuration
- Environment variable support for secure API key management
- No additional infrastructure requirements beyond Python runtime