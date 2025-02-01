from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from api.controller import router  # Import the controller module
from api.service import analyze_performance, generate_insights, visualize_performance
from api.utils import json_files
from api.models import SubmissionData
import json

app = FastAPI()
templates = Jinja2Templates(directory=".")

# Include the router with the controller's endpoints
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    # Load data for current quiz, historical data, and submission data
    current_quiz_data, historical_data, submission_data = json_files("current_quiz_data", "historical_data", "submission_data")

    # Convert historical data to list of SubmissionData objects
    historical_submissions = [SubmissionData(**data) for data in historical_data]

    # Analyze user performance based on historical submissions
    analysis_data = analyze_performance(historical_submissions)
    insights = generate_insights(analysis_data)
    visualize_performance(analysis_data)  # Call the visualization function here
    
    # Convert analysis data and insights to JSON strings and escape them
    analysis_data_json = json.dumps(analysis_data).replace("</", "<\\/")
    insights_json = json.dumps(insights).replace("</", "<\\/")

    return templates.TemplateResponse("index.html", {"request": request, "analysis_data": analysis_data_json, "insights": insights_json})