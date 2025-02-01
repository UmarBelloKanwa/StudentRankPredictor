from fastapi import APIRouter, HTTPException, FastAPI
from typing import List
from api.service import analyze_performance, generate_insights, predict_rank, predict_college, visualize_performance
from api.utils import train_rank_predictor
from api.models import SubmissionData, Quiz
from api.utils import json_files

router = APIRouter()
app = FastAPI()

# Load data for current quiz, historical data, and submission data
current_quiz_data, historical_data, submission_data = json_files("current_quiz_data", "historical_data", "submission_data")

# Initialize objects
quiz_data: Quiz = Quiz(**current_quiz_data.get("quiz"))
historical_submissions: List[SubmissionData] = [SubmissionData(**data) for data in historical_data]
submitted_data: SubmissionData = SubmissionData(**submission_data)

@app.post("/analyze-performance")
def analyze_performance_endpoint(user_data: List[SubmissionData]):
    analysis_data = analyze_performance(user_data)
    insights = generate_insights(analysis_data)
    visualize_performance(analysis_data)  # Call the visualization function here
    return {"analysis": analysis_data, "insights": insights}

@router.get("/analyze-performance")
def get_performance_analysis():
    try:
        # Analyze user performance based on historical submissions
        analysis_data = analyze_performance(historical_submissions) 
        return analysis_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing performance: {str(e)}")

@router.get("/generate-insights")
def get_performance_insights():
    try:
        # Analyze performance and generate insights
        analysis_data = analyze_performance(historical_submissions)
        insights = generate_insights(analysis_data)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")

@router.post("/predict-rank")
def predict_student_rank(student_performance: SubmissionData):
    try:
        # Train rank predictor model using historical submissions
        theta = train_rank_predictor(historical_submissions)

        # Extract relevant performance data
        features = [
            student_performance.score,
            student_performance.accuracy,
            student_performance.mistakes_corrected,
            student_performance.final_score
        ]
        print("Extracted features", features)

        # Predict rank for the new student
        predicted_rank = predict_rank(features, theta)
        return {"predicted_rank": predicted_rank}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting rank: {str(e)}")

@router.post("/predict-college")
def predict_student_college(predicted_rank: dict):
    try:
        # Predict the college the student may attend based on predicted rank
        rank = predicted_rank.get("predicted_rank")
        predicted_college = predict_college(rank)
        return {"predicted_college": predicted_college}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting college: {str(e)}")
