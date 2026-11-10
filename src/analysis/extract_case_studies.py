"""Extract real clutch match moments for Top 10 Batters and Bowlers."""

import duckdb
import pandas as pd
from src.config import PROCESSED_DATA_DIR

con = duckdb.connect()
deliv_p = (PROCESSED_DATA_DIR / 'deliveries_with_pava.parquet').as_posix()
con.execute(f"CREATE VIEW d AS SELECT * FROM read_parquet('{deliv_p}')")

top_batters = [
    'Romario Shepherd', 'Ruturaj Gaikwad', 'Naman Dhir', 'Fakhar Zaman',
    'Rohit Sharma', 'Darwish Rasooli', 'Mohammad Nabi', 'Jason Holder',
    'Nicholas Pooran', 'Curtis Campher'
]
top_bowlers = [
    'Nathan Ellis', 'Liam Dawson', 'Abbas Afridi', 'Sufiyan Muqeem',
    'Harpreet Brar', 'Haris Rauf', 'Lungi Ngidi', 'Shoriful Islam',
    'Matheesha Pathirana', 'Nasum Ahmed'
]

print("=== TOP CLUTCH INNINGS FOR TOP BATTERS (HIGH BPI >= 45) ===")
batter_dossiers = []
for b in top_batters:
    q = f"""
        SELECT match_date, comp_category, innings, COUNT(*) as balls, SUM(batter_runs) as runs,
               ROUND(AVG(bpi), 1) as avg_bpi, ROUND(SUM(pava_bat), 1) as total_pava
        FROM d
        WHERE striker_name = '{b}'
        GROUP BY match_date, comp_category, innings
        HAVING AVG(bpi) >= 45
        ORDER BY total_pava DESC
        LIMIT 1
    """
    res = con.execute(q).df()
    if len(res) > 0:
        r = res.iloc[0]
        line = f"- **{b}**: Scored **{int(r['runs'])} runs off {int(r['balls'])} balls** (Average BPI: {r['avg_bpi']}, PAVA: +{r['total_pava']} runs) in {r['comp_category']} on {r['match_date']}."
        print(line)
        batter_dossiers.append(line)

print("\n=== TOP CLUTCH SPELLS FOR TOP BOWLERS (HIGH BoPI >= 45) ===")
bowler_dossiers = []
for b in top_bowlers:
    q = f"""
        SELECT match_date, comp_category, innings, COUNT(*) as balls, SUM(bowler_runs_conceded) as runs_conceded,
               SUM(is_bowler_wicket::INT) as wickets, ROUND(AVG(bopi), 1) as avg_bopi, ROUND(SUM(pava_bowl), 1) as total_pava
        FROM d
        WHERE bowler_name = '{b}'
        GROUP BY match_date, comp_category, innings
        HAVING AVG(bopi) >= 45
        ORDER BY total_pava DESC
        LIMIT 1
    """
    res = con.execute(q).df()
    if len(res) > 0:
        r = res.iloc[0]
        line = f"- **{b}**: Took **{int(r['wickets'])} wickets for {int(r['runs_conceded'])} runs in {int(r['balls'])} balls** (Average BoPI: {r['avg_bopi']}, PAVA: +{r['total_pava']} runs) in {r['comp_category']} on {r['match_date']}."
        print(line)
        bowler_dossiers.append(line)
