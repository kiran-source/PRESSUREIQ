import pandas as pd

df = pd.read_parquet('data/processed/deliveries_with_pava.parquet')

top_bats = [
    'Ruturaj Gaikwad', 'Rohit Sharma', 'Fakhar Zaman', 'Suryakumar Yadav',
    'Romario Shepherd', 'Naman Dhir', 'Phil Salt', 'Jitesh Sharma',
    'Nicholas Pooran', 'Jos Buttler'
]

print("=== BATTERS PHASE & MATCHUP BREAKDOWN ===")
for b in top_bats:
    sub = df[df['striker_name'] == b]
    pp = sub[sub['balls_remaining_before'] > 84]
    mid = sub[(sub['balls_remaining_before'] >= 36) & (sub['balls_remaining_before'] <= 84)]
    death = sub[sub['balls_remaining_before'] < 36]
    
    sr_pp = pp['batter_runs'].sum() / max(len(pp), 1) * 100
    sr_mid = mid['batter_runs'].sum() / max(len(mid), 1) * 100
    sr_death = death['batter_runs'].sum() / max(len(death), 1) * 100
    
    # Pace vs spin
    pace = sub[sub['bowling_type'].str.contains('Fast|medium|pace', case=False, na=False)]
    spin = sub[sub['bowling_type'].str.contains('spin|orthodox|chinaman|break', case=False, na=False)]
    
    sr_pace = pace['batter_runs'].sum() / max(len(pace), 1) * 100
    sr_spin = spin['batter_runs'].sum() / max(len(spin), 1) * 100
    
    print(f"{b}:")
    print(f"  PP Balls={len(pp)} (SR={sr_pp:.1f}), Mid Balls={len(mid)} (SR={sr_mid:.1f}), Death Balls={len(death)} (SR={sr_death:.1f})")
    print(f"  vs Pace Balls={len(pace)} (SR={sr_pace:.1f}), vs Spin Balls={len(spin)} (SR={sr_spin:.1f})")

top_bowls = [
    'Liam Dawson', 'Haris Rauf', 'Abbas Afridi', 'Nathan Ellis',
    'Sufiyan Muqeem', 'Matheesha Pathirana', 'Nasum Ahmed', 'Ishant Sharma',
    'Shoriful Islam', 'Tim Southee'
]

print("\n=== BOWLERS PHASE & ECONOMY BREAKDOWN ===")
for bw in top_bowls:
    sub = df[df['bowler_name'] == bw]
    pp = sub[sub['balls_remaining_before'] > 84]
    mid = sub[(sub['balls_remaining_before'] >= 36) & (sub['balls_remaining_before'] <= 84)]
    death = sub[sub['balls_remaining_before'] < 36]
    
    econ_pp = pp['bowler_runs_conceded'].sum() / max(pp['is_legal_ball'].sum(), 1) * 6.0
    econ_mid = mid['bowler_runs_conceded'].sum() / max(mid['is_legal_ball'].sum(), 1) * 6.0
    econ_death = death['bowler_runs_conceded'].sum() / max(death['is_legal_ball'].sum(), 1) * 6.0
    
    wkts_pp = pp['is_bowler_wicket'].sum()
    wkts_mid = mid['is_bowler_wicket'].sum()
    wkts_death = death['is_bowler_wicket'].sum()
    
    print(f"{bw}:")
    print(f"  PP: {pp['is_legal_ball'].sum()} legal balls, {wkts_pp} wkts, Econ={econ_pp:.2f}")
    print(f"  Mid: {mid['is_legal_ball'].sum()} legal balls, {wkts_mid} wkts, Econ={econ_mid:.2f}")
    print(f"  Death: {death['is_legal_ball'].sum()} legal balls, {wkts_death} wkts, Econ={econ_death:.2f}")

