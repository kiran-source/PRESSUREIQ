import sys
import os
sys.path.insert(0, os.path.abspath("."))
import pandas as pd
import numpy as np

features_path = "data/processed/features_deliveries.parquet"
df = pd.read_parquet(features_path)

print(f"Total deliveries: {len(df):,}")
print(f"Date range: {df['match_date'].min()} to {df['match_date'].max()}")

# 1. Check for same-date matches per player
striker_dates = df.groupby(["striker_id", "match_date"])["match_id"].nunique()
multi_match_strikers = striker_dates[striker_dates > 1]
print(f"\nStrikers with > 1 match on the same date: {len(multi_match_strikers)}")
if len(multi_match_strikers) > 0:
    print(multi_match_strikers.head(10))

bowler_dates = df.groupby(["bowler_id", "match_date"])["match_id"].nunique()
multi_match_bowlers = bowler_dates[bowler_dates > 1]
print(f"Bowlers with > 1 match on the same date: {len(multi_match_bowlers)}")
if len(multi_match_bowlers) > 0:
    print(multi_match_bowlers.head(10))

# 2. Check chronological splits
# In src/config.py or train_models.py, what are the splits?
df["year"] = pd.to_datetime(df["match_date"]).dt.year
print("\nDeliveries by year:")
print(df["year"].value_counts().sort_index())

print("\nMatches by year:")
print(df.groupby("year")["match_id"].nunique())

# Check match isolation: does any match_id appear in multiple years?
match_years = df.groupby("match_id")["year"].nunique()
print(f"\nMatches spanning multiple years: {(match_years > 1).sum()}")

# Check train/val/test assignment in modeling
from src.config import TRAIN_END_DATE, VAL_END_DATE
print(f"\nConfigured split dates: TRAIN_END_DATE={TRAIN_END_DATE}, VAL_END_DATE={VAL_END_DATE}")

train_matches = set(df[df["match_date"] <= TRAIN_END_DATE]["match_id"].unique())
val_matches = set(df[(df["match_date"] > TRAIN_END_DATE) & (df["match_date"] <= VAL_END_DATE)]["match_id"].unique())
test_matches = set(df[df["match_date"] > VAL_END_DATE]["match_id"].unique())

print(f"Train matches: {len(train_matches)} ({len(df[df['match_id'].isin(train_matches)]):,} balls)")
print(f"Val matches: {len(val_matches)} ({len(df[df['match_id'].isin(val_matches)]):,} balls)")
print(f"Test matches: {len(test_matches)} ({len(df[df['match_id'].isin(test_matches)]):,} balls)")

# Overlap checks
print(f"Train & Val match intersection: {len(train_matches & val_matches)}")
print(f"Train & Test match intersection: {len(train_matches & test_matches)}")
print(f"Val & Test match intersection: {len(val_matches & test_matches)}")
