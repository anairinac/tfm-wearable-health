"""
"""

import pandas as pd
import os
import pickle
import xgboost as XGBoost
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer

X_TRAIN_PATH = "../data/processed/X_train.parquet"
Y_TRAIN_PATH = "../data/processed/y_train.parquet"
random_seed = 42


numeric_features = ['AGEP_A',
 'SLPHOURS_A',
 'MODMIN_A',
 'VIGMIN_A',
 'MODFREQW_A',
 'VIGFREQW_A',
 'STRFREQW_A',
 'HEIGHT_CM',
 'MODMIN_WEEKLY',
 'VIGMIN_WEEKLY']

categorical_features =  ['ANXEV_A',
 'DEPEV_A',
 'ASEV_A',
 'SEX_A',
 'BMICAT_A',
 'CANT_MODFREQW_A',
 'CANT_VIGFREQW_A',
 'CANT_STRFREQW_A',
 'MOD_LEVEL',
 'VIG_LEVEL']

# Separamos las variables por tipo de transformer a usar: cat, ord, num standard o num outlier
vars_dur_semanal = ['MODMIN_WEEKLY', 'VIGMIN_WEEKLY']
num_std_features, num_outlier_features = [f for f in numeric_features if f not in vars_dur_semanal], vars_dur_semanal
cat_std_features = [f for f in categorical_features if f not in ['MOD_LEVEL', 'VIG_LEVEL']]
cat_ordinal_features = [f for f in categorical_features if f in ['MOD_LEVEL', 'VIG_LEVEL']]
ord_categories = ['sin', 'insuficiente', 'minimo', 'supera']

PREPROCESS = {
    "numeric_transformer": Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ]),

    "robust_transformer": Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', RobustScaler())
    ]),
    "categorical_transformer": Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value=-1)),
        ('encoder', OneHotEncoder(drop='if_binary', handle_unknown='ignore'))
    ]),
    "ordinal_transformer": Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OrdinalEncoder(categories=[ord_categories, ord_categories]))
    ])
}

targets = [
    {
        "name": "y_lesion_deportiva",
        "model": XGBoost.XGBClassifier,
        "params": {
            "colsample_bytree": 1.0,
            "learning_rate": 0.005,
            "max_depth": 3,
            "n_estimators": 100,
            "scale_pos_weight": 1,
            "subsample": 0.3
        }
    },
    {
        "name": "y_malestar_psicologico",
        "model": RandomForestClassifier,
        "params": {
            "max_depth": 16,
            "n_estimators": 300,
            "min_samples_leaf": 3,
            "max_features": 9,
            "criterion": "gini",
            "class_weight": "balanced"
        }
    },
    {
        "name": "y_respiratorio",
        "model": XGBoost.XGBClassifier,
        "params": {
            "colsample_bytree": 0.8,
            "learning_rate": 0.01,
            "max_depth": 3,
            "n_estimators": 300,
            "scale_pos_weight": 1,
            "subsample": 0.2
        }
    }
]

def train_best_model(target_name, preprocessor, X_train, y_train):
    target = next(t for t in targets if t["name"] == target_name)
    model = target["model"](
        **target["params"],
        random_state=random_seed
    )
    notna_mask = y_train[target_name].notna()
    pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("model", model)
    ])
    pipeline.fit(X_train.loc[notna_mask], y_train.loc[notna_mask, target_name])
    return pipeline

def main():
    X_train = pd.read_parquet(X_TRAIN_PATH)
    y_train = pd.read_parquet(Y_TRAIN_PATH)

    preprocessor = ColumnTransformer([
        ('num', PREPROCESS["numeric_transformer"], num_std_features), # numeric
        ('num_outlier', PREPROCESS["robust_transformer"], num_outlier_features), # num outliers in activity duration features
        ('cat', PREPROCESS["categorical_transformer"], cat_std_features), # categoric
        ('ord', PREPROCESS["ordinal_transformer"], cat_ordinal_features) # ordinal cat
    ])

    for target in targets:
        pipeline = train_best_model(target["name"], preprocessor, X_train, y_train)
        os.makedirs("models", exist_ok=True)
        with open(f"models/{target['name']}_pipeline.pkl", "wb") as model_file:
            pickle.dump(pipeline, model_file)
        print(f"{target['name']} serialized in models/{target['name']}_pipeline.pkl")

if __name__ == "__main__":
    main()