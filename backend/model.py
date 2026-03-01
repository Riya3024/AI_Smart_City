import numpy as np
from sklearn.linear_model import LinearRegression

def train_model():
    X = np.array([[100], [200], [300], [400], [500]])
    y = np.array([30, 45, 65, 85, 110])
    model = LinearRegression()
    model.fit(X, y)
    return model

model = train_model()

def predict_congestion(students):
    return float(model.predict([[students]])[0])