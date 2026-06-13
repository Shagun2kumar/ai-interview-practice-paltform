import random
from textblob import TextBlob

import random


def generate_questions(role, skills):

    # ================= NON-TECHNICAL =================
    if role == "non-technical":

        hr_questions = [

            # INTRO
            "Tell me about yourself.",
            "Introduce yourself in 2 minutes.",
            "Walk me through your resume.",

            # BACKGROUND
            "Tell me about your school life.",
            "What did you learn from your college experience?",
            "Which subject did you enjoy the most and why?",

            # PERSONALITY
            "What are your strengths and weaknesses?",
            "How do your friends describe you?",
            "What motivates you in life?",

            # THINKING
            "If you could change one thing in the world, what would it be?",
            "Where do you see yourself in 5 years?",
            "What does success mean to you?",

            # BEHAVIORAL
            "Tell me about a challenge you faced and how you handled it.",
            "Describe a situation where you showed leadership.",
            "Tell me about a failure and what you learned.",

            # JOB RELATED
            "Why should we hire you?",
            "Why do you want to join our company?",
            "What makes you different from other candidates?"
        ]

        return random.sample(hr_questions, 6)

    # ================= TECHNICAL =================
    else:

        tech_questions = []

        # Skill-based questions
        for skill in skills:
            tech_questions.append(f"Explain {skill}.")
            tech_questions.append(f"Where have you used {skill} in your projects?")
            tech_questions.append(f"What are the advantages of {skill}?")

        # Core CS questions
        core_questions = [
            "What is OOP and its principles?",
            "Explain difference between array and linked list.",
            "What is database normalization?",
            "What is API and how it works?",
            "Difference between frontend and backend.",
            "What is time complexity?",
            "Explain stack and queue.",
            "What is HTTP and HTTPS?",
            "Difference between SQL and NoSQL.",
            "What is multithreading?"
        ]

        # Mix both
        all_questions = tech_questions + core_questions

        # Shuffle for randomness
        random.shuffle(all_questions)

        return all_questions[:6]

    
def evaluate_answer(q, a):
    blob = TextBlob(a)
    score = int((blob.sentiment.polarity + 1) * 5)

    if score > 7:
        fb = "Excellent answer"
    elif score > 4:
        fb = "Good answer"
    else:
        fb = "Needs improvement"

    return score, fb




