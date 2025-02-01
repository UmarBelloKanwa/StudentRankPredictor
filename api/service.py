from api.models import SubmissionData, colleges
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import os

# Function for analyzing student performance
def analyze_performance(user_data: List[SubmissionData]):
    # Initialize variables for tracking performance
    total_accuracy = 0
    total_score = 0
    total_final_score = 0
    total_negative_score = 0
    total_rank = 0
    total_mistakes_corrected = 0
    total_quizzes = 0
    topic_performance = {}
    accuracy_trends = []
    
    # Loop through each submission in the user data
    for submission in user_data:
        total_quizzes += 1
        accuracy_numeric = submission.accuracy
        total_accuracy += accuracy_numeric
        
        # Add to overall scores
        total_score += submission.score
        total_final_score += submission.final_score
        total_negative_score += submission.negative_score
        total_rank += submission.better_than
        total_mistakes_corrected += submission.mistakes_corrected

        # Track performance by topic
        topic = submission.quiz.topic  # Assuming 'quiz' is an object with a 'topic' attribute
        if topic:
            if topic not in topic_performance:
                topic_performance[topic] = {'correct': 0, 'total': 0, 'mistakes': 0}
            topic_performance[topic]['correct'] += submission.correct_answers
            topic_performance[topic]['total'] += submission.total_questions
            topic_performance[topic]['mistakes'] += submission.incorrect_answers
        
        # Track accuracy trends over time
        accuracy_trends.append(accuracy_numeric)
    
    return {
        'total_accuracy': total_accuracy,
        'total_score': total_score,
        'total_final_score': total_final_score,
        'total_negative_score': total_negative_score,
        'total_rank': total_rank,
        'total_mistakes_corrected': total_mistakes_corrected,
        'total_quizzes': total_quizzes,
        'topic_performance': topic_performance,
        'accuracy_trends': accuracy_trends
    }

# Function to generate insights from the analysis
def generate_insights(analysis_data):
    # Calculate averages and other insights
    average_accuracy = analysis_data['total_accuracy'] / analysis_data['total_quizzes'] if analysis_data['total_quizzes'] > 0 else 0
    average_score = analysis_data['total_score'] / analysis_data['total_quizzes'] if analysis_data['total_quizzes'] > 0 else 0
    average_final_score = analysis_data['total_final_score'] / analysis_data['total_quizzes'] if analysis_data['total_quizzes'] > 0 else 0
    average_negative_score = analysis_data['total_negative_score'] / analysis_data['total_quizzes'] if analysis_data['total_quizzes'] > 0 else 0
    average_rank = analysis_data['total_rank'] / analysis_data['total_quizzes'] if analysis_data['total_quizzes'] > 0 else 0
    average_mistakes_corrected = analysis_data['total_mistakes_corrected'] / analysis_data['total_quizzes'] if analysis_data['total_quizzes'] > 0 else 0

    weak_areas = {}
    for topic, performance in analysis_data['topic_performance'].items():
        topic_accuracy = performance['correct'] / performance['total'] if performance['total'] > 0 else 0
        if topic_accuracy < 0.5:
            weak_areas[topic] = {
                'correct_answers': performance['correct'],
                'total_questions': performance['total'],
                'accuracy': topic_accuracy,
                'mistakes': performance['mistakes']
            }

    improvement_trend = "Improved" if analysis_data['accuracy_trends'][-1] > analysis_data['accuracy_trends'][0] else "No Significant Change"

    return {
        'Overall Performance': {
            'Average Accuracy': f"{average_accuracy * 100:.2f}%",
            'Average Score': average_score,
            'Average Final Score': average_final_score,
            'Average Negative Score': average_negative_score,
            'Average Rank': average_rank,
            'Average Mistakes Corrected': average_mistakes_corrected
        },
        'Weak Areas': weak_areas,
        'Improvement Trends': improvement_trend
    }

# Rank prediction function
def predict_rank(features, theta):
    features = np.array([1] + list(features))  # Adding intercept term
    return features @ theta

# College prediction based on rank
def predict_college(predicted_rank: float):
    for college, rank_range in colleges.items():
        if rank_range["rank_lower"] <= predicted_rank <= rank_range["rank_upper"]:
            return college
    
    return "No college found"

# Function to visualize performance analysis
def visualize_performance(analysis_data):
    # Plot accuracy trends
    plt.figure(figsize=(10, 5))
    plt.plot(analysis_data['accuracy_trends'], marker='o')
    plt.title('Accuracy Trends Over Time')
    plt.xlabel('Quiz Number')
    plt.ylabel('Accuracy')
    plt.grid(True)
    plt.savefig(os.path.join(os.getcwd(), 'accuracy_trends.png'))
    plt.close()

    # Plot topic performance
    topics = list(analysis_data['topic_performance'].keys())
    correct_answers = [analysis_data['topic_performance'][topic]['correct'] for topic in topics]
    total_questions = [analysis_data['topic_performance'][topic]['total'] for topic in topics]

    x = np.arange(len(topics))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width/2, correct_answers, width, label='Correct Answers')
    rects2 = ax.bar(x + width/2, total_questions, width, label='Total Questions')

    ax.set_xlabel('Topics')
    ax.set_ylabel('Number of Questions')
    ax.set_title('Performance by Topic')
    ax.set_xticks(x)
    ax.set_xticklabels(topics, rotation=45, ha='right')
    ax.legend()

    fig.tight_layout()
    plt.savefig(os.path.join(os.getcwd(), 'topic_performance.png'))
    plt.close()