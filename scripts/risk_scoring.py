"""
Function to calculate thhe overall risk score, combining the predicted risk scores for
injury, psychological distress, and asthma/respiratory issues.
"""
import pandas as pd

# TODO: Revisar contra resultados de distribución
MID_THRESHOLD = 0.33
HIGH_THRESHOLD = 0.66

def normalize_binary_risk(probability: float, mid_threshold: float = MID_THRESHOLD, high_threshold: float = HIGH_THRESHOLD) -> str:
    if probability >= high_threshold:
        return "high"
    elif probability >= mid_threshold:
        return "medium"
    else:
        return "low"

def normalize_ordinal_risk(ordinal_class: int) -> str:
    if int(ordinal_class) == 2:
        return "high"
    elif int(ordinal_class) == 1:
        return "medium"
    else:
        return "low"

def calculate_risk_score(proba_lesion: float, class_malestar_psicologico: float, proba_respiratorio: float, 
    mid_threshold: float = MID_THRESHOLD, high_threshold: float = HIGH_THRESHOLD) -> dict:
    """
    Calculate the overall risk score based on individual risk scores.

    Parameters:
    - proba_lesion: Probability of injury (float)
    - class_malestar_psicologico: Class representing psychological discomfort (int)
    - proba_respiratorio: Probability of respiratory issues (float)
    - mid_threshold: Threshold for medium risk (float)
    - high_threshold: Threshold for high risk (float)

    Returns:
    - dict containing:
        - risk_score: Overall risk score (str)
        - risk_score_lesion: Risk score for injury (str)
        - risk_score_malestar_psicologico: Risk score for psychological discomfort (str)
        - risk_score_respiratorio: Risk score for respiratory issues (str)
    """
    domains = {
        "lesion": normalize_binary_risk(proba_lesion, mid_threshold, high_threshold),
        "malestar_psicologico": normalize_ordinal_risk(class_malestar_psicologico),
        "respiratorio": normalize_binary_risk(proba_respiratorio, mid_threshold, high_threshold)
    }
    if "high" in domains.values():
        risk_score = "high"
    elif "medium" in domains.values():
        risk_score = "medium"
    else:
        risk_score = "low"

    return {
        "risk_score": risk_score,
        # "risk_score_numeric": 0, # TODO: Implement numeric risk score calculation if needed
        "risk_score_lesion": domains["lesion"],
        "risk_score_malestar_psicologico": domains["malestar_psicologico"],
        "risk_score_respiratorio": domains["respiratorio"]
    }

def calculate_batch_risk_score(df_predictions, mid_threshold: float = MID_THRESHOLD, 
    high_threshold: float = HIGH_THRESHOLD) -> pd.DataFrame:
    """
    Calculate the overall risk score for a batch of predictions.

    Parameters:
    - df_predictions: DataFrame containing individual risk scores with columns:
        - 'proba_lesion'
        - 'class_malestar_psicologico'
        - 'proba_respiratorio'
    - mid_threshold: Threshold for medium risk (float)
    - high_threshold: Threshold for high risk (float)

    Returns:
    - risk_scores: DataFrame containing the overall risk scores for each prediction
    """
    results = df_predictions.apply(
        lambda row: calculate_risk_score(
            row['proba_lesion'],
            row['class_malestar_psicologico'],
            row['proba_respiratorio'],
            mid_threshold,
            high_threshold
        ),
        axis=1
    )

    return pd.DataFrame(
        {
            "risk_score": results.map(lambda r: r["risk_score"]),
            "risk_score_lesion": results.map(lambda r: r["risk_score_lesion"]),
            "risk_score_malestar_psicologico": results.map(lambda r: r["risk_score_malestar_psicologico"]),
            "risk_score_respiratorio": results.map(lambda r: r["risk_score_respiratorio"])
        }
    )