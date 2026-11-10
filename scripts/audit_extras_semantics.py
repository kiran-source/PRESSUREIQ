import duckdb
import pandas as pd

raw_bbb = "SupeRR Selector Season 2 _ Problem Statement _ Data Pack/SupeRR Selector Season 2 _ Data Pack/ball_by_ball.csv"
raw_matches = "SupeRR Selector Season 2 _ Problem Statement _ Data Pack/SupeRR Selector Season 2 _ Data Pack/matches.csv"

con = duckdb.connect()

print("\nCheck distinct values of runs, extras1_runs, extras_2_runs for byes and legbyes and others:")
dist_runs = con.execute(f"""
    SELECT extras_type, runs, extras1_runs, extras_2_runs, count(*) as cnt
    FROM read_csv_auto('{raw_bbb}')
    WHERE extras_type IS NOT NULL
    GROUP BY extras_type, runs, extras1_runs, extras_2_runs
    ORDER BY extras_type, cnt DESC
""").fetchdf()
print(dist_runs.to_string())

print("\nLet's inspect matches table columns:")
m_cols = con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{raw_matches}')").fetchdf()
print(m_cols[['column_name', 'column_type']].to_string())

sample_m = con.execute(f"SELECT * FROM read_csv_auto('{raw_matches}') LIMIT 5").fetchdf()
print(sample_m.to_string())
