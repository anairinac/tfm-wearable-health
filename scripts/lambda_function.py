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
# import pickle
import json


def handler(event, context):
    versions = {
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "sklearn": sklearn.__version__,
        "xgboost": xgboost.__version__
    }
    return {
        "statusCode": 200,
        "body": json.dumps({
            "ok": True,
            "versions": versions,
            "event": event
        })
    }