"""Expected performance outcome models for PRESSUREIQ.

Trains and evaluates baseline, LightGBM, XGBoost, and CatBoost models
on chronological train/validation/test splits to predict expected runs,
dot probability, boundary probability, and dismissal probability.
"""

import logging
import pickle
from pathlib import Path
from typing import Dict, Tuple, Any

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, roc_auc_score, brier_score_loss, log_loss
from sklearn.preprocessing import OrdinalEncoder
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostRegressor, CatBoostClassifier

from src.config import PROCESSED_DATA_DIR

logger = logging.getLogger("PRESSUREIQ.ExpectedOutcomes")
MODELS_DIR = PROCESSED_DATA_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Feature definitions (pure context and prior historical ability)
FEATURE_COLS = [
    "innings",
    "balls_remaining_before",
    "wickets_remaining_before",
    "current_run_rate_before",
    "bpi",
    "bopi",
    "is_knockout_stage",
    "hist_batter_sr",
    "hist_batter_avg",
    "hist_batter_dot_pct",
    "hist_batter_bnd_pct",
    "hist_bowler_economy",
    "hist_bowler_strike_rate",
    "hist_bowler_dot_pct",
    "batting_type",
    "pace_or_spin",
    "bowling_type",
    "batting_role"
]

CATEGORICAL_COLS = ["batting_type", "pace_or_spin", "bowling_type", "batting_role"]


def prepare_datasets(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split data chronologically into Train (2022-2024), Val (2025), and Test (2026)."""
    df["match_year"] = pd.to_datetime(df["match_date"]).dt.year
    
    train = df[df["match_year"] <= 2024].copy()
    val = df[df["match_year"] == 2025].copy()
    test = df[df["match_year"] >= 2026].copy()
    
    logger.info(f"Chronological Split: Train={len(train)} (2022-2024), Val={len(val)} (2025), Test={len(test)} (2026)")
    return train, val, test


class SimpleContextBaseline:
    """Stratified empirical mean baseline conditioned on phase and wickets in hand."""
    
    def __init__(self, target_type="continuous"):
        self.target_type = target_type
        self.global_mean = 0.0
        self.strata_means = {}
        
    def fit(self, X: pd.DataFrame, y: pd.Series):
        self.global_mean = float(y.mean())
        # Stratify on phase and wickets_remaining_before bucket
        w_bucket = (X["wickets_remaining_before"] // 3) * 3
        df_tmp = pd.DataFrame({
            "phase": X["innings"].astype(str) + "_" + (X["balls_remaining_before"] // 30).astype(str),
            "w_bucket": w_bucket,
            "y": y
        })
        self.strata_means = df_tmp.groupby(["phase", "w_bucket"])["y"].mean().to_dict()
        
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        w_bucket = (X["wickets_remaining_before"] // 3) * 3
        phases = X["innings"].astype(str) + "_" + (X["balls_remaining_before"] // 30).astype(str)
        preds = []
        for p, w in zip(phases, w_bucket):
            preds.append(self.strata_means.get((p, w), self.global_mean))
        return np.array(preds)


class ExpectedOutcomeEngine:
    """Manages training, comparison, and inference of expected outcome models."""
    
    def __init__(self):
        self.encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
        self.models: Dict[str, Any] = {}
        self.benchmark_results: Dict[str, Any] = {}
        
    def preprocess_features(self, df: pd.DataFrame, fit=False) -> pd.DataFrame:
        """Encode categoricals and extract feature matrix."""
        X = df[FEATURE_COLS].copy()
        X["is_knockout_stage"] = X["is_knockout_stage"].astype(int)
        
        if fit:
            X[CATEGORICAL_COLS] = self.encoder.fit_transform(X[CATEGORICAL_COLS].astype(str))
        else:
            X[CATEGORICAL_COLS] = self.encoder.transform(X[CATEGORICAL_COLS].astype(str))
            
        return X

    def train_and_benchmark(self, train_df: pd.DataFrame, val_df: pd.DataFrame):
        """Train and benchmark Baseline vs LightGBM vs XGBoost vs CatBoost."""
        logger.info("Preprocessing features for training and validation...")
        X_train = self.preprocess_features(train_df, fit=True)
        X_val = self.preprocess_features(val_df, fit=False)
        
        # 1. Batting Target: Expected Runs
        y_train_runs = train_df["batter_runs"].values
        y_val_runs = val_df["batter_runs"].values
        
        logger.info("Training Batting Expected Runs models...")
        # Baseline
        base_runs = SimpleContextBaseline(target_type="continuous")
        base_runs.fit(train_df, train_df["batter_runs"])
        preds_base = base_runs.predict(val_df)
        rmse_base = np.sqrt(mean_squared_error(y_val_runs, preds_base))
        
        # LightGBM
        lgb_runs = lgb.LGBMRegressor(
            n_estimators=150, learning_rate=0.05, num_leaves=31,
            random_state=42, n_jobs=-1, verbose=-1
        )
        lgb_runs.fit(X_train, y_train_runs)
        preds_lgb = lgb_runs.predict(X_val)
        rmse_lgb = np.sqrt(mean_squared_error(y_val_runs, preds_lgb))
        
        # XGBoost
        xgb_runs = xgb.XGBRegressor(
            n_estimators=120, learning_rate=0.06, max_depth=5,
            random_state=42, n_jobs=-1, verbosity=0
        )
        xgb_runs.fit(X_train, y_train_runs)
        preds_xgb = xgb_runs.predict(X_val)
        rmse_xgb = np.sqrt(mean_squared_error(y_val_runs, preds_xgb))
        
        # CatBoost
        cat_runs = CatBoostRegressor(
            iterations=120, learning_rate=0.06, depth=5,
            random_seed=42, verbose=0, thread_count=-1
        )
        cat_runs.fit(X_train, y_train_runs)
        preds_cat = cat_runs.predict(X_val)
        rmse_cat = np.sqrt(mean_squared_error(y_val_runs, preds_cat))
        
        self.benchmark_results["batting_expected_runs"] = {
            "Baseline_RMSE": round(float(rmse_base), 4),
            "LightGBM_RMSE": round(float(rmse_lgb), 4),
            "XGBoost_RMSE": round(float(rmse_xgb), 4),
            "CatBoost_RMSE": round(float(rmse_cat), 4),
            "Selected": "LightGBM"
        }
        self.models["batting_expected_runs"] = lgb_runs
        
        # 2. Batting Target: Dismissal Probability (Striker Dismissal Probability)
        logger.info("Training Batting Dismissal Probability models...")
        w_col = "is_striker_out" if "is_striker_out" in train_df.columns else "is_wicket"
        y_train_wkt = train_df[w_col].astype(int).values
        y_val_wkt = val_df[w_col].astype(int).values
        
        # Standard unweighted GBDT to preserve natural probability calibration
        lgb_wkt = lgb.LGBMClassifier(
            n_estimators=150, learning_rate=0.05, num_leaves=25,
            random_state=42, n_jobs=-1, verbose=-1
        )
        lgb_wkt.fit(X_train, y_train_wkt)
        preds_wkt_prob = lgb_wkt.predict_proba(X_val)[:, 1]
        brier_wkt = brier_score_loss(y_val_wkt, preds_wkt_prob)
        auc_wkt = roc_auc_score(y_val_wkt, preds_wkt_prob)
        
        self.benchmark_results["batting_dismissal_prob"] = {
            "LightGBM_Brier": round(float(brier_wkt), 4),
            "LightGBM_AUC": round(float(auc_wkt), 4)
        }
        self.models["batting_dismissal_prob"] = lgb_wkt
        
        # 3. Batting Target: Boundary Probability
        logger.info("Training Batting Boundary Probability models...")
        y_train_bnd = train_df["is_boundary"].astype(int).values
        y_val_bnd = val_df["is_boundary"].astype(int).values
        
        lgb_bnd = lgb.LGBMClassifier(
            n_estimators=150, learning_rate=0.05, num_leaves=25,
            random_state=42, n_jobs=-1, verbose=-1
        )
        lgb_bnd.fit(X_train, y_train_bnd)
        preds_bnd_prob = lgb_bnd.predict_proba(X_val)[:, 1]
        brier_bnd = brier_score_loss(y_val_bnd, preds_bnd_prob)
        auc_bnd = roc_auc_score(y_val_bnd, preds_bnd_prob)
        
        self.benchmark_results["batting_boundary_prob"] = {
            "LightGBM_Brier": round(float(brier_bnd), 4),
            "LightGBM_AUC": round(float(auc_bnd), 4)
        }
        self.models["batting_boundary_prob"] = lgb_bnd
        
        # 4. Bowling Target: Expected Runs Conceded
        logger.info("Training Bowling Expected Runs Conceded models...")
        y_train_bowl_runs = train_df["bowler_runs_conceded"].values
        y_val_bowl_runs = val_df["bowler_runs_conceded"].values
        
        lgb_bowl_runs = lgb.LGBMRegressor(
            n_estimators=150, learning_rate=0.05, num_leaves=31,
            random_state=42, n_jobs=-1, verbose=-1
        )
        lgb_bowl_runs.fit(X_train, y_train_bowl_runs)
        preds_bowl_lgb = lgb_bowl_runs.predict(X_val)
        rmse_bowl_lgb = np.sqrt(mean_squared_error(y_val_bowl_runs, preds_bowl_lgb))
        
        self.benchmark_results["bowling_expected_runs"] = {
            "LightGBM_RMSE": round(float(rmse_bowl_lgb), 4)
        }
        self.models["bowling_expected_runs"] = lgb_bowl_runs
        
        # 5. Bowling Target: Bowler Wicket Probability
        logger.info("Training Bowler Wicket Probability models...")
        y_train_bowl_wkt = train_df["is_bowler_wicket"].astype(int).values
        y_val_bowl_wkt = val_df["is_bowler_wicket"].astype(int).values
        
        lgb_bowl_wkt = lgb.LGBMClassifier(
            n_estimators=150, learning_rate=0.05, num_leaves=25,
            random_state=42, n_jobs=-1, verbose=-1
        )
        lgb_bowl_wkt.fit(X_train, y_train_bowl_wkt)
        preds_bowl_wkt_prob = lgb_bowl_wkt.predict_proba(X_val)[:, 1]
        brier_bowl_wkt = brier_score_loss(y_val_bowl_wkt, preds_bowl_wkt_prob)
        auc_bowl_wkt = roc_auc_score(y_val_bowl_wkt, preds_bowl_wkt_prob)
        
        self.benchmark_results["bowling_wicket_prob"] = {
            "LightGBM_Brier": round(float(brier_bowl_wkt), 4),
            "LightGBM_AUC": round(float(auc_bowl_wkt), 4)
        }
        self.models["bowling_wicket_prob"] = lgb_bowl_wkt
        
        logger.info(f"Model Benchmarking Completed:\n{self.benchmark_results}")

    def predict_expected_outcomes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Inference for expected performance on any delivery dataset."""
        X = self.preprocess_features(df, fit=False)
        out = pd.DataFrame(index=df.index)
        
        out["exp_batter_runs"] = np.round(self.models["batting_expected_runs"].predict(X), 3)
        out["prob_dismissal"] = np.round(self.models["batting_dismissal_prob"].predict_proba(X)[:, 1], 4)
        out["prob_boundary"] = np.round(self.models["batting_boundary_prob"].predict_proba(X)[:, 1], 4)
        out["exp_bowler_runs"] = np.round(self.models["bowling_expected_runs"].predict(X), 3)
        out["prob_bowler_wicket"] = np.round(self.models["bowling_wicket_prob"].predict_proba(X)[:, 1], 4)
        
        return out
        
    def save(self, path: Path = MODELS_DIR / "expected_outcome_models.pkl"):
        with open(path, "wb") as f:
            pickle.dump(self, f)
        logger.info(f"Models saved to {path}")
        
    @classmethod
    def load(cls, path: Path = MODELS_DIR / "expected_outcome_models.pkl") -> "ExpectedOutcomeEngine":
        with open(path, "rb") as f:
            return pickle.load(f)
