"""Script to build final competition deliverables for PRESSUREIQ.

Generates:
1. data/processed/final_competition_batter_top10.csv
2. data/processed/final_competition_bowler_top10.csv
3. data/processed/player_evidence_dossier.csv (30 players: 20 top + 10 near misses)
4. data/processed/emerging_talent_watchlist.csv
"""

import os
import numpy as np
import pandas as pd

def main():
    print("Building final competition deliverables...")
    os.makedirs("data/processed", exist_ok=True)
    
    # 1. Load canonical Model A rankings
    fb = pd.read_csv("data/processed/final_batter_rankings.csv")
    fw = pd.read_csv("data/processed/final_bowler_rankings.csv")
    
    # Verify exact top 10
    b_top10 = fb.head(10).copy()
    w_top10 = fw.head(10).copy()
    
    # Add strategic franchise context without changing statistical reliability
    # Canonical player IDs & audited 2026 squad / Nov 5 trade / policy statuses
    strat_b = {
        6059: ("Opposition Benchmark (CSK 2026 / Pending 2027 Verification)", "Tactical planning benchmark; high-tempo powerplay anchor (2027 CSK list pending Nov 17)"),
        126: ("Opposition Benchmark (MI 2026 / Pending 2027 Verification)", "Clutch powerplay pace exploitation; game-tempo control (2027 MI list pending Nov 17)"),
        2921: ("Global Benchmark (Pakistan / Policy Review)", "High-leverage left-hand boundary striker (IPL ineligible under BCCI geopolitical policy)"),
        1699: ("Opposition Benchmark (MI 2026 / Pending 2027 Verification)", "360-degree middle-overs spin/pace destroyer (2027 MI list pending Nov 17)"),
        6726: ("Watchlist Asset (RCB 2026 / Pending 2027 Verification)", "Seam-bowling power finisher fit for #7 if released by RCB on Nov 17"),
        37052: ("Watchlist Asset (MI 2026 / Pending 2027 Verification)", "Young dynamic Indian top/middle-order clutch climber (2027 MI list pending Nov 17)"),
        5553: ("Watchlist Asset (RCB 2026 / Pending 2027 Verification)", "High-tempo powerplay wicketkeeper-batter (2027 RCB list pending Nov 17)"),
        3916: ("Watchlist Asset (RCB 2026 / Pending 2027 Verification)", "Indian middle-order keeper-finisher (2027 RCB list pending Nov 17)"),
        3125: ("Opposition Benchmark (LSG 2026 / Pending 2027 Verification)", "World-class spin destructor and boundary anchor (2027 LSG list pending Nov 17)"),
        813: ("Opposition Asset (GT 2026 / Pending 2027 Verification)", "Former RR opener now in GT squad; proven high-pressure chase master (2027 list pending Nov 17)"),
    }

    strat_w = {
        722: ("Watchlist Overseas Option (Uncontracted / Pending 2027)", "Economical orthodox left-arm spinner and lower-order bat"),
        7364: ("Global Benchmark (Pakistan / Policy Review)", "Express pace reverse-swing yorker benchmark (IPL ineligible under BCCI geopolitical policy)"),
        7699: ("Global Benchmark (Pakistan / Policy Review)", "Back-of-hand slower ball and change-of-pace weapon (IPL ineligible under BCCI geopolitical policy)"),
        7920: ("Unavailable — Confirmed Trade (SRH Pre-2027 Trade)", "Traded CSK -> SRH (5 Nov 2026); death-yorker benchmark (unattainable in auction)"),
        34485: ("Global Benchmark (Pakistan / Policy Review)", "Unorthodox left-arm wrist spinner (IPL ineligible under BCCI geopolitical policy)"),
        8661: ("Opposition Asset (KKR 2026 / Pending 2027 Verification)", "Slingy express death-overs executioner (acquired by KKR for IPL 2026; Nov 17 pending)"),
        4658: ("Watchlist Overseas Option (Bangladesh / Uncontracted)", "Powerplay defensive finger spinner"),
        28: ("Watchlist Domestic Depth (GT 2026 / Pending 2027 Verification)", "Veteran Indian hit-the-deck seam experience (2027 GT list pending Nov 17)"),
        7344: ("Watchlist Overseas Option (Bangladesh / Uncontracted)", "Left-arm swing and death executioner"),
        278: ("Watchlist Veteran Option (New Zealand / Uncontracted)", "Experienced change-of-pace death bowler"),
    }

    missing_b = [int(pid) for pid in b_top10["player_id"] if int(pid) not in strat_b]
    missing_w = [int(pid) for pid in w_top10["player_id"] if int(pid) not in strat_w]
    assert not missing_b, f"Missing canonical batter IDs in strat_b: {missing_b}"
    assert not missing_w, f"Missing canonical bowler IDs in strat_w: {missing_w}"
    
    b_top10["strategic_category"] = b_top10["player_id"].map(lambda x: strat_b.get(x, ("Target", "Key player"))[0])
    b_top10["rr_strategic_utility"] = b_top10["player_id"].map(lambda x: strat_b.get(x, ("Target", "Key player"))[1])
    
    w_top10["strategic_category"] = w_top10["player_id"].map(lambda x: strat_w.get(x, ("Target", "Key player"))[0])
    w_top10["rr_strategic_utility"] = w_top10["player_id"].map(lambda x: strat_w.get(x, ("Target", "Key player"))[1])
    
    # Export final competition top 10
    b_top10.to_csv("data/processed/final_competition_batter_top10.csv", index=False)
    w_top10.to_csv("data/processed/final_competition_bowler_top10.csv", index=False)
    print("Saved final_competition_batter_top10.csv and final_competition_bowler_top10.csv")
    
    # 2. Build 30-Player Evidence Dossier (10 Batters + 5 Near Misses, 10 Bowlers + 5 Near Misses)
    b_dossier = fb.head(15).copy()
    b_dossier["discipline"] = "Batting"
    b_dossier["selection_status"] = b_dossier["rank"].apply(lambda r: "Selected (Top 10)" if r <= 10 else "Near Miss (Rank 11-15)")
    
    w_dossier = fw.head(15).copy()
    w_dossier["discipline"] = "Bowling"
    w_dossier["selection_status"] = w_dossier["rank"].apply(lambda r: "Selected (Top 10)" if r <= 10 else "Near Miss (Rank 11-15)")
    
    # Unify columns for dossier
    dossier_rows = []
    for _, row in b_dossier.iterrows():
        dossier_rows.append({
            "rank": row["rank"],
            "player_id": row["player_id"],
            "player_name": row["player_name"],
            "discipline": "Batting",
            "role": row["role"],
            "selection_status": row["selection_status"],
            "reliability_score": row["reliability_score"],
            "matches": row["matches"],
            "hp_balls": row["hp_balls"],
            "total_balls": row["total_balls"],
            "prc_archetype": row["prc_archetype"],
            "prc_slope": row["prc_slope"],
            "boot_ci_lower_95": row["boot_score_ci_lower_95"],
            "boot_ci_upper_95": row["boot_score_ci_upper_95"],
            "top10_inclusion_prob": row["top10_inclusion_prob"],
            "key_strength": "High-pressure boundary strike rate & PAVA value-add",
            "main_limitation": "Sample size in extreme leverage" if row["hp_balls"] < 100 else "High variance across match clusters",
            "rr_strategic_role": strat_b.get(row["player_id"], ("Target / Competitor", "Middle-order depth / benchmark"))[1]
        })
        
    for _, row in w_dossier.iterrows():
        dossier_rows.append({
            "rank": row["rank"],
            "player_id": row["player_id"],
            "player_name": row["player_name"],
            "discipline": "Bowling",
            "role": row["bowling_type"],
            "selection_status": row["selection_status"],
            "reliability_score": row["reliability_score"],
            "matches": row["matches"],
            "hp_balls": row["hp_balls"],
            "total_balls": row["legal_balls"],
            "prc_archetype": row["prc_archetype"],
            "prc_slope": row["prc_slope"],
            "boot_ci_lower_95": row["boot_score_ci_lower_95"],
            "boot_ci_upper_95": row["boot_score_ci_upper_95"],
            "top10_inclusion_prob": row["top10_inclusion_prob"],
            "key_strength": "Dot-ball pressure creation & death-overs run suppression",
            "main_limitation": "Sample size in death overs" if row["hp_balls"] < 100 else "Boundary concession on mis-executed lengths",
            "rr_strategic_role": strat_w.get(row["player_id"], ("Target / Competitor", "Bowling depth / benchmark"))[1]
        })
        
    dossier_df = pd.DataFrame(dossier_rows)
    dossier_df.to_csv("data/processed/player_evidence_dossier.csv", index=False)
    print("Saved player_evidence_dossier.csv (30 players)")
    
    # 3. Build Dedicated Emerging Talent Watchlist with canonical IDs & dataset-verified metrics
    d_pava = pd.read_parquet(
        "data/processed/deliveries_with_pava.parquet",
        columns=["striker_id", "bowler_id", "is_batter_ball", "is_legal_ball", "batter_runs", "bpi", "bopi"],
    )
    bat_by_id = fb.set_index("player_id")
    bowl_by_id = fw.set_index("player_id")

    def _bat_stats(pid: int) -> tuple[int, int, float]:
        sub = d_pava[(d_pava["striker_id"] == pid) & (d_pava["is_batter_ball"] == 1)]
        balls = int(len(sub))
        hp = int((sub["bpi"] >= 50.0).sum())
        sr = round(float(sub["batter_runs"].sum()) * 100.0 / balls, 1) if balls > 0 else 0.0
        return balls, hp, sr

    def _bowl_stats(pid: int) -> tuple[int, int, int]:
        all_d = d_pava[d_pava["bowler_id"] == pid]
        legal = all_d[all_d["is_legal_ball"] == 1]
        return int(len(legal)), int(len(all_d)), int((legal["bopi"] >= 50.0).sum())

    sv_b, sv_hp, sv_sr = _bat_stats(50284)
    vp_leg, _vp_all, vp_hp = _bowl_stats(48557)

    emerging_data = [
        {
            "player_name": "Vaibhav Sooryavanshi",
            "player_id": 50284,
            "age": 14,
            "nationality": "India",
            "category": "Tier C: High-Potential (Insufficient HP Exposure)",
            "role": "Top-Order Left-Hand Batter",
            "franchise": "Rajasthan Royals (IPL 2026 / Pending 2027 Verification)",
            "total_balls_dataset": sv_b,
            "hp_balls_dataset": sv_hp,
            "dataset_strike_rate": sv_sr,
            "pressure_reliability_score": f"Unqualified ({sv_hp}/30 HP balls)",
            "tactical_assessment": f"Generational prodigy ({sv_sr:.1f} SR over {sv_b} balls); fearless aggressive strokeplay in powerplays with {sv_hp} BPI>=50 deliveries.",
            "recommendation_for_rr": "Back long-term developmental trajectory within RR squad; groom in high-pressure match simulations."
        },
        {
            "player_name": "Vignesh Puthur",
            "player_id": 48557,
            "age": 22,
            "nationality": "India",
            "category": "Tier C: High-Potential (Insufficient Career Exposure)",
            "role": "Slow Left-Arm Wrist/Orthodox Spinner",
            "franchise": "Rajasthan Royals (IPL 2026 Auction Signing / Pending 2027 Verification)",
            "total_balls_dataset": vp_leg,
            "hp_balls_dataset": vp_hp,
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": f"Unqualified ({vp_leg}/400 legal balls)",
            "tactical_assessment": f"Uncapped Kerala spinner acquired by RR at Dec 2025 auction ({vp_leg} legal balls, {vp_hp} BoPI>=50 balls).",
            "recommendation_for_rr": "Develop as high-upside domestic spin depth for Jaipur home conditions."
        },
        {
            "player_name": "Naman Dhir",
            "player_id": 37052,
            "age": 24,
            "nationality": "India",
            "category": f"Tier A: Proven Pressure Performer (Selected #{int(bat_by_id.loc[37052, 'rank'])})",
            "role": "Top/Middle-Order Batter & Off-Break Bowler",
            "franchise": "Mumbai Indians (IPL 2026 / Pending 2027 Verification)",
            "total_balls_dataset": int(bat_by_id.loc[37052, "total_balls"]),
            "hp_balls_dataset": int(bat_by_id.loc[37052, "hp_balls"]),
            "dataset_strike_rate": round(float(bat_by_id.loc[37052, "career_sr"]), 1),
            "pressure_reliability_score": f"{bat_by_id.loc[37052, 'reliability_score']:.2f} (Rank #{int(bat_by_id.loc[37052, 'rank'])} Batter)",
            "tactical_assessment": f"Breakout young Indian batter (SR {bat_by_id.loc[37052, 'career_sr']:.1f}, slope {bat_by_id.loc[37052, 'prc_slope']:+.4f} {bat_by_id.loc[37052, 'prc_archetype']}).",
            "recommendation_for_rr": "Watchlist target if released by MI on Nov 17, 2026; provides versatile top-order/middle tempo."
        },
        {
            "player_name": "Prince Yadav",
            "player_id": 58246,
            "age": 23,
            "nationality": "India",
            "category": f"Tier B: Emerging Pressure Performer (Rank #{int(bowl_by_id.loc[58246, 'rank'])} Bowler)",
            "role": "Right-Arm Fast Bowler",
            "franchise": "Lucknow Super Giants (IPL 2026 / Pending 2027 Verification)",
            "total_balls_dataset": int(bowl_by_id.loc[58246, "legal_balls"]),
            "hp_balls_dataset": int(bowl_by_id.loc[58246, "hp_balls"]),
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": f"{bowl_by_id.loc[58246, 'reliability_score']:.2f} (Rank #{int(bowl_by_id.loc[58246, 'rank'])} Bowler)",
            "tactical_assessment": "Domestic pace discovery with strong high-pressure resilience across nearly 300 BoPI>=50 balls.",
            "recommendation_for_rr": "Monitor Nov 17 LSG retention decision as domestic fast-bowling depth candidate."
        },
        {
            "player_name": "Rasikh Salam",
            "player_id": 7327,
            "age": 24,
            "nationality": "India",
            "category": f"Tier B: Emerging Pressure Performer (Rank #{int(bowl_by_id.loc[7327, 'rank'])} Bowler)",
            "role": "Right-Arm Medium-Fast Bowler",
            "franchise": "Royal Challengers Bengaluru / Domestic India",
            "total_balls_dataset": int(bowl_by_id.loc[7327, "legal_balls"]),
            "hp_balls_dataset": int(bowl_by_id.loc[7327, "hp_balls"]),
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": f"{bowl_by_id.loc[7327, 'reliability_score']:.2f} (Rank #{int(bowl_by_id.loc[7327, 'rank'])} Bowler)",
            "tactical_assessment": "Skilful death executor with slower-ball and yorker variations across IPL and India A fixtures.",
            "recommendation_for_rr": "Domestic middle/death pace option pending official Nov 17 retention lists."
        },
        {
            "player_name": "Allah Ghazanfar",
            "player_id": 32862,
            "age": 18,
            "nationality": "Afghanistan",
            "category": f"Tier B: Emerging Pressure Performer (Rank #{int(bowl_by_id.loc[32862, 'rank'])} Bowler)",
            "role": "Right-Arm Mystery Off-Break Spinner",
            "franchise": "Afghanistan / Franchise Pool",
            "total_balls_dataset": int(bowl_by_id.loc[32862, "legal_balls"]),
            "hp_balls_dataset": int(bowl_by_id.loc[32862, "hp_balls"]),
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": f"{bowl_by_id.loc[32862, 'reliability_score']:.2f} (Rank #{int(bowl_by_id.loc[32862, 'rank'])} Bowler)",
            "tactical_assessment": "Teenage mystery spinner holding positive execution surplus across 212 high-pressure legal balls.",
            "recommendation_for_rr": "High-upside overseas mystery spin watchlist candidate for Jaipur surfaces."
        },
        {
            "player_name": "Abbas Afridi",
            "player_id": 7699,
            "age": 23,
            "nationality": "Pakistan",
            "category": f"Tier A: Proven Pressure Performer (Rank #{int(bowl_by_id.loc[7699, 'rank'])} Bowler)",
            "role": "Right-Arm Medium-Fast Seamer",
            "franchise": "Pakistan (Policy/Eligibility Review)",
            "total_balls_dataset": int(bowl_by_id.loc[7699, "legal_balls"]),
            "hp_balls_dataset": int(bowl_by_id.loc[7699, "hp_balls"]),
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": f"{bowl_by_id.loc[7699, 'reliability_score']:.2f} (Rank #{int(bowl_by_id.loc[7699, 'rank'])} Bowler)",
            "tactical_assessment": "Change-of-pace death bowler under extreme leverage; serves strictly as an analytical benchmark.",
            "recommendation_for_rr": "Global analytical benchmark only (BCCI geopolitical stance precludes IPL participation since 2008)."
        },
        {
            "player_name": "Sufiyan Muqeem",
            "player_id": 34485,
            "age": 24,
            "nationality": "Pakistan",
            "category": f"Tier A: Proven Pressure Performer (Rank #{int(bowl_by_id.loc[34485, 'rank'])} Bowler)",
            "role": "Left-Arm Wrist Spinner (Chinaman)",
            "franchise": "Pakistan (Policy/Eligibility Review)",
            "total_balls_dataset": int(bowl_by_id.loc[34485, "legal_balls"]),
            "hp_balls_dataset": int(bowl_by_id.loc[34485, "hp_balls"]),
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": f"{bowl_by_id.loc[34485, 'reliability_score']:.2f} (Rank #{int(bowl_by_id.loc[34485, 'rank'])} Bowler)",
            "tactical_assessment": "Left-arm wrist spin with sub-6.00 economy under high BoPI; serves strictly as an analytical benchmark.",
            "recommendation_for_rr": "Global analytical benchmark only (BCCI geopolitical stance precludes IPL participation since 2008)."
        },
        {
            "player_name": "Harpreet Brar",
            "player_id": 7325,
            "age": 29,
            "nationality": "India",
            "category": f"Tier B: Emerging/Established Pressure Asset (Rank #{int(bowl_by_id.loc[7325, 'rank'])} Bowler)",
            "role": "Slow Left-Arm Orthodox Spinner",
            "franchise": "Punjab Kings (IPL 2026 / Pending 2027 Verification)",
            "total_balls_dataset": int(bowl_by_id.loc[7325, "legal_balls"]),
            "hp_balls_dataset": int(bowl_by_id.loc[7325, "hp_balls"]),
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": f"{bowl_by_id.loc[7325, 'reliability_score']:.2f} (Rank #{int(bowl_by_id.loc[7325, 'rank'])} Bowler)",
            "tactical_assessment": "Clutch Climber SLA spinner firing flat, tight lengths against right-hand power hitters.",
            "recommendation_for_rr": "Monitor PBKS Nov 17 list as domestic SLA squeeze target for SMS Stadium."
        },
        {
            "player_name": "Rinku Singh",
            "player_id": 4708,
            "age": 27,
            "nationality": "India",
            "category": f"Tier A: Proven Pressure Performer (Rank #{int(bat_by_id.loc[4708, 'rank'])} Batter)",
            "role": "Left-Hand Middle-Order Finisher",
            "franchise": "Kolkata Knight Riders (IPL 2026 / Pending 2027 Verification)",
            "total_balls_dataset": int(bat_by_id.loc[4708, "total_balls"]),
            "hp_balls_dataset": int(bat_by_id.loc[4708, "hp_balls"]),
            "dataset_strike_rate": round(float(bat_by_id.loc[4708, "career_sr"]), 1),
            "pressure_reliability_score": f"{bat_by_id.loc[4708, 'reliability_score']:.2f} (Rank #{int(bat_by_id.loc[4708, 'rank'])} Batter)",
            "tactical_assessment": "Elite domestic finisher missing Model A top-10 by 0.08 points across 418 HP balls.",
            "recommendation_for_rr": "Tactical case study / watchlist asset depending on KKR Nov 17 retention announcement."
        }
    ]
    
    em_df = pd.DataFrame(emerging_data)
    em_df.to_csv("data/processed/emerging_talent_watchlist.csv", index=False)
    print("Saved emerging_talent_watchlist.csv (10 detailed profiles)")

if __name__ == "__main__":
    main()

