"""
Lambda function que recibe datos de un usuario y retorna 
la predicción de riesgo para las variables objetivo
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

pipeline_lesion = load_pipeline("y_lesion_deportiva")
pipeline_malestar_psicologico = load_pipeline("y_malestar_psicologico")
pipeline_respiratorio = load_pipeline("y_respiratorio")

def handler(event, context):
    try:
        body = json.loads(event.get("body") or {})
    except json.JSONDecodeError:
        return build_response(400, {"error": "Invalid JSON body on request"})

    try:
        features = build_features(body)
    except KeyError as e:
        return build_response(400, {"error": f"Missing field: {e}"})

    X = pd.DataFrame([features])
    proba_lesion_deportiva = pipeline_lesion.predict_proba(X)[0][1]
    clase_malestar_psicologico = pipeline_malestar_psicologico.predict(X)[0]
    proba_respiratorio = pipeline_respiratorio.predict_proba(X)[0][1]

    result = calculate_risk_score(proba_lesion_deportiva, clase_malestar_psicologico, proba_respiratorio)

    return build_response(200, result)

def build_response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }