"""
Subject and topic definitions for the educational tutor
"""

SUBJECTS = {
    "Calculus": {
        "description": "Mathematical analysis involving limits, derivatives, and integrals",
        "icon": "📐",
        "color": "#007bff"
    },
    "Programming": {
        "description": "Computer programming concepts and languages",
        "icon": "💻", 
        "color": "#28a745"
    },
    "Physics": {
        "description": "Physical sciences covering mechanics, thermodynamics, and more",
        "icon": "⚛️",
        "color": "#ffc107"
    },
    "Chemistry": {
        "description": "Chemical reactions, molecular structure, and laboratory techniques",
        "icon": "🧪",
        "color": "#dc3545"
    },
    "Statistics": {
        "description": "Data analysis, probability, and statistical inference",
        "icon": "📊",
        "color": "#6f42c1"
    }
}

SUBJECT_TOPICS = {
    "Calculus": [
        "Limits and Continuity",
        "Derivatives and Differentiation",
        "Applications of Derivatives",
        "Integration Techniques",
        "Definite Integrals",
        "Applications of Integration",
        "Differential Equations",
        "Sequences and Series",
        "Multivariable Calculus",
        "Vector Calculus"
    ],
    "Programming": [
        "Variables and Data Types",
        "Control Structures",
        "Functions and Methods",
        "Object-Oriented Programming",
        "Data Structures",
        "Algorithms and Complexity",
        "File Input/Output",
        "Error Handling",
        "Testing and Debugging",
        "Software Design Patterns"
    ],
    "Physics": [
        "Kinematics and Motion",
        "Forces and Newton's Laws",
        "Energy and Work",
        "Momentum and Collisions",
        "Rotational Motion",
        "Waves and Oscillations",
        "Thermodynamics",
        "Electricity and Magnetism",
        "Optics and Light",
        "Modern Physics"
    ],
    "Chemistry": [
        "Atomic Structure",
        "Chemical Bonding",
        "Stoichiometry",
        "Chemical Reactions",
        "Acids and Bases",
        "Thermochemistry",
        "Chemical Equilibrium",
        "Electrochemistry",
        "Organic Chemistry Basics",
        "Laboratory Techniques"
    ],
    "Statistics": [
        "Descriptive Statistics",
        "Probability Theory",
        "Random Variables",
        "Sampling Distributions",
        "Hypothesis Testing",
        "Confidence Intervals",
        "Correlation and Regression",
        "ANOVA and T-Tests",
        "Non-parametric Tests",
        "Experimental Design"
    ]
}

def get_subject_topics(subject):
    """Get the list of topics for a given subject"""
    return SUBJECT_TOPICS.get(subject, [])

def get_subject_info(subject):
    """Get detailed information about a subject"""
    return SUBJECTS.get(subject, {})

def get_all_subjects():
    """Get all available subjects"""
    return list(SUBJECTS.keys())

def get_topic_prerequisites(subject, topic):
    """Get suggested prerequisites for a topic (simplified implementation)"""
    topics = get_subject_topics(subject)
    if topic not in topics:
        return []
    
    topic_index = topics.index(topic)
    # Return previous topics as prerequisites
    return topics[:topic_index]

def get_next_suggested_topics(subject, completed_topics):
    """Get suggested next topics based on completed topics"""
    all_topics = get_subject_topics(subject)
    
    # Simple logic: suggest the next topic in sequence
    for i, topic in enumerate(all_topics):
        if topic not in completed_topics:
            return [topic]
    
    # If all topics completed, suggest review or advanced topics
    return ["Review all topics", "Explore advanced concepts"]

def validate_subject_topic(subject, topic):
    """Validate that a topic exists for the given subject"""
    return subject in SUBJECTS and topic in get_subject_topics(subject)

# Topic difficulty levels (for future enhancement)
TOPIC_DIFFICULTY = {
    "Calculus": {
        "Limits and Continuity": "Beginner",
        "Derivatives and Differentiation": "Beginner", 
        "Applications of Derivatives": "Intermediate",
        "Integration Techniques": "Intermediate",
        "Definite Integrals": "Intermediate",
        "Applications of Integration": "Intermediate",
        "Differential Equations": "Advanced",
        "Sequences and Series": "Advanced",
        "Multivariable Calculus": "Advanced",
        "Vector Calculus": "Advanced"
    },
    "Programming": {
        "Variables and Data Types": "Beginner",
        "Control Structures": "Beginner",
        "Functions and Methods": "Beginner",
        "Object-Oriented Programming": "Intermediate",
        "Data Structures": "Intermediate", 
        "Algorithms and Complexity": "Intermediate",
        "File Input/Output": "Intermediate",
        "Error Handling": "Intermediate",
        "Testing and Debugging": "Advanced",
        "Software Design Patterns": "Advanced"
    }
    # Add more subjects as needed
}

def get_topic_difficulty(subject, topic):
    """Get the difficulty level of a topic"""
    return TOPIC_DIFFICULTY.get(subject, {}).get(topic, "Intermediate")
