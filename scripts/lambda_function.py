"""
Lambda function que recibe datos de un usuario y retorna 
la predicción de variables objetivo

TODO: Por ahora retorna solo datos de prueba para configurar 
la infraestructura y el pipeline
"""

import numpy as np
import pandas as pd
import sklearn
import xgboost
import pickle
import json
from sklearn.pipeline import Pipeline
from data_cleanup import build_features
from risk_scoring import calculate_risk_score

def load_pipeline(target_name: str) -> Pipeline:
    with open(f"models/{target_name}_pipeline.pkl", "rb") as model_file:
        return pickle.load(model_file)

def handler(event, context):
    versions = {
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "sklearn": sklearn.__version__,
        "xgboost": xgboost.__version__
    }
    return build_response(200, versions)

def build_response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }