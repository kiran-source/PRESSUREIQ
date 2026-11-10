"""Execution script for Expected Outcome training, evaluation, and PAVA generation."""

import json
import logging
from pathlib import Path
import pandas as pd

from src.config import PROCESSED_DATA_DIR, DOCS_DIR
from src.models.expected_outcomes import (
    ExpectedOutcomeEngine,
    prepare_datasets
)
from src.models.pressure_value import (
    compute_pressure_adjusted_value,
    aggregate_innings_batting_pava,
    aggregate_spell_bowling_pava
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("PRESSUREIQ.TrainExpectedOutcomes")

FEATURES_PARQUET = PROCESSED_DATA_DIR / "features_deliveries.parquet"
DELIVERIES_PAVA_PARQUET = PROCESSED_DATA_DIR / "deliveries_with_pava.parquet"
BATTER_INNINGS_PAVA_PARQUET = PROCESSED_DATA_DIR / "batter_innings_pava.parquet"
BOWLER_SPELL_PAVA_PARQUET = PROCESSED_DATA_DIR / "bowler_spell_pava.parquet"
BENCHMARK_REPORT = DOCS_DIR / "MODEL_BENCHMARK_REPORT.json"


def main():
    logger.info(f"Loading feature dataset from {FEATURES_PARQUET}...")
    df = pd.read_parquet(FEATURES_PARQUET)
    
    # 1. Chronological Train / Val / Test Split
    train_df, val_df, test_df = prepare_datasets(df)
    
    # 2. Train and benchmark models
    engine = ExpectedOutcomeEngine()
    engine.train_and_benchmark(train_df, val_df)
    engine.save()
    
    # Save benchmark report
    with open(BENCHMARK_REPORT, "w", encoding="utf-8") as f:
        json.dump(engine.benchmark_results, f, indent=2)
    logger.info(f"Benchmark results saved to {BENCHMARK_REPORT}")
    
    # 3. Compute expected outcomes on entire dataset
    logger.info("Computing expected outcome predictions across entire dataset...")
    exp_out = engine.predict_expected_outcomes(df)
    
    # 4. Compute delivery-level Pressure-Adjusted Value Added (PAVA)
    logger.info("Calculating delivery-level PAVA...")
    pava_deliveries = compute_pressure_adjusted_value(df, exp_out)
    
    logger.info(f"Writing {DELIVERIES_PAVA_PARQUET}...")
    pava_deliveries.to_parquet(DELIVERIES_PAVA_PARQUET, index=False)
    
    # 5. Aggregate to innings and spell level
    logger.info("Aggregating innings-level batting PAVA...")
    bat_innings = aggregate_innings_batting_pava(pava_deliveries)
    bat_innings.to_parquet(BATTER_INNINGS_PAVA_PARQUET, index=False)
    
    logger.info("Aggregating spell-level bowling PAVA...")
    bowl_spells = aggregate_spell_bowling_pava(pava_deliveries)
    bowl_spells.to_parquet(BOWLER_SPELL_PAVA_PARQUET, index=False)
    
    logger.info("Phase 4 & 5 processing completed successfully!")


if __name__ == "__main__":
    main()

