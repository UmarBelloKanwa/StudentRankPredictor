from fastapi.testclient import TestClient
from api.main import app  # Import your FastAPI app (make sure the app is correctly imported)
import json

client = TestClient(app)

# Load student performance data from submission_data.json
with open("data/submission_data.json", "r") as file:
    submission_data = json.load(file)

# Test for the "/analyze-performance" endpoint
def test_analyze_performance():
    response = client.get("/analyze-performance")
    
    assert response.status_code == 200  # Assert the response code is 200 OK
    data = response.json()
    print("Analyze performance", data)  # Add logging
    # Check if the key data exists
    assert "total_accuracy" in data
    assert "total_score" in data
    assert "total_quizzes" in data

# Test for the "/generate-insights" endpoint
def test_generate_insights():
    response = client.get("/generate-insights")
    
    assert response.status_code == 200
    data = response.json()
    print("Generate insight", data)
    assert "Overall Performance" in data
    assert "Weak Areas" in data
    assert "Improvement Trends" in data

# Test for the "/predict-rank" endpoint
def test_predict_rank():
    response = client.post("/predict-rank", json=submission_data)
    
    assert response.status_code == 200
    data = response.json()
    print("predict rank", data)

    # Check if the predicted rank key is in the response
    assert "predicted_rank" in data

# Test for the "/predict-college" endpoint
def test_predict_college():
    predicted_rank = 250  # Example rank for predicting college
    response = client.post("/predict-college", json={"predicted_rank": predicted_rank})
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")
    assert response.status_code == 200
    data = response.json()
    print("predict college", data)
    # Check if the college prediction is returned correctly
    assert "predicted_college" in data

test_analyze_performance()
test_generate_insights()
test_predict_rank()
test_predict_college()