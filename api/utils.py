import json
import numpy as np

def json_files(*args: str):
    names = list(args)
    for name in names:
        try:
            with open(f"data/{name}.json", "r") as file:
                yield json.load(file)
        except:
            yield None


def train_rank_predictor(data):
    # Prepare training data (X = features, y = target)
    X = np.array([[entry.score, entry.accuracy, entry.mistakes_corrected, entry.final_score] for entry in data])
    y = np.array([entry.better_than for entry in data])  # Rank (target)

    # Add a column of ones to X for the intercept term
    X = np.c_[np.ones(X.shape[0]), X]

    # Compute the normal equation using Pseudo-Inverse
    theta = np.linalg.pinv(X.T @ X) @ X.T @ y  # Use pinv instead of inv
    return theta
