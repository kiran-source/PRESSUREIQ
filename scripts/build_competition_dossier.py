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
    # Batters Strategic Category
    strat_b = {
        6059: ("Opposition Benchmark (CSK Retained)", "Tactical planning benchmark; high-tempo powerplay anchor"),
        126: ("Opposition Benchmark (MI Retained)", "Clutch powerplay pace exploitation; game-tempo control"),
        2921: ("Global Benchmark (Pakistan)", "High-leverage left-hand boundary striker"),
        6018: ("Opposition Benchmark (MI Retained)", "360-degree middle-overs spin/pace destroyer"),
        6776: ("Prime Acquisition Target (West Indies)", "Priority #7 seam-bowling power finisher for RR"),
        37052: ("Emerging Target / Retention (MI)", "Young dynamic top/middle-order clutch climber"),
        6640: ("High-Value Target (England)", "Fearless powerplay wicketkeeper-batter"),
        6017: ("Prime Domestic Target (India)", "High-intensity Indian finisher and wicketkeeper"),
        5977: ("Opposition Benchmark (LSG Retained)", "World-class spin destructor and boundary anchor"),
        813: ("RR Priority Asset (England)", "Franchise pillar and proven high-pressure chase master")
    }
    
    # Bowlers Strategic Category
    strat_w = {
        722: ("High-Value Target (England)", "Jaipur-squeeze orthodox spinner and lower-order bat"),
        7364: ("Global Benchmark (Pakistan)", "Express pace reverse-swing yorker benchmark"),
        36341: ("Emerging Global Benchmark (Pakistan)", "Back-of-hand slower ball and change-of-pace weapon"),
        7514: ("Prime Acquisition Target (Australia)", "Premier death yorker specialist; Sandeep Sharma partner"),
        49925: ("Emerging Global Benchmark (Pakistan)", "Unorthodox left-arm wrist spinner"),
        37324: ("Opposition Benchmark (CSK Retained)", "Slingy express death-overs execution benchmark"),
        6426: ("High-Value Target (Bangladesh)", "Powerplay defensive finger spinner"),
        65: ("Veteran Depth Target (India)", "Powerplay hit-the-deck experience"),
        6845: ("Prime Acquisition Target (Bangladesh)", "Left-arm swing and reverse-yorker death specialist"),
        775: ("Veteran Depth Target (New Zealand)", "Experienced change-of-pace death bowler")
    }
    
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
    
    # 3. Build Dedicated Emerging Talent Watchlist
    # Identify young (<25), uncapped, and emerging players in dataset & public domain
    emerging_data = [
        {
            "player_name": "Vaibhav Sooryavanshi",
            "player_id": 50284,
            "age": 14,
            "nationality": "India",
            "category": "Tier C: High-Potential (Insufficient Pressure Evidence)",
            "role": "Top-Order Left-Hand Batter",
            "franchise": "Rajasthan Royals (IPL 2025/2026)",
            "total_balls_dataset": 714,
            "hp_balls_dataset": 0,
            "dataset_strike_rate": 139.8,
            "pressure_reliability_score": "N/A (Unshrunk / Low HP)",
            "tactical_assessment": "Generational prodigy; fearless aggressive strokeplay against pace in powerplays. Lacks late-innings high-RRR pressure sample due to opening role, but represents RR's highest-ceiling developmental asset.",
            "recommendation_for_rr": "Back long-term developmental trajectory; groom in high-pressure match simulations without burdening with late-overs salvage duties."
        },
        {
            "player_name": "Vignesh Puthur",
            "player_id": 48557,
            "age": 22,
            "nationality": "India",
            "category": "Tier C: High-Potential (Insufficient Pressure Evidence)",
            "role": "Slow Left-Arm Orthodox Spinner",
            "franchise": "Rajasthan Royals (IPL 2026) / Mumbai Indians",
            "total_balls_dataset": 73,
            "hp_balls_dataset": 6,
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": "N/A (Small Sample)",
            "tactical_assessment": "Uncapped Kerala spinner scouted for deceptive flight and drift. Limited IPL exposure (73 balls in dataset), showing tight control in domestic circuits.",
            "recommendation_for_rr": "Develop as high-upside domestic spin depth for Jaipur home conditions; evaluate in pre-season camps against elite RHB batters."
        },
        {
            "player_name": "Naman Dhir",
            "player_id": 37052,
            "age": 24,
            "nationality": "India",
            "category": "Tier A: Proven Pressure Performer (Selected #6)",
            "role": "Top/Middle-Order Batter & Off-Break Bowler",
            "franchise": "Mumbai Indians",
            "total_balls_dataset": 603,
            "hp_balls_dataset": 184,
            "dataset_strike_rate": 158.4,
            "pressure_reliability_score": "93.30 (Rank #6 Batter)",
            "tactical_assessment": "Breakout young Indian star. Demonstrates Clutch Climber archetype (+0.078 PRC slope). Hits high pace over midwicket and inside-out against spin under steep run-rate pressure.",
            "recommendation_for_rr": "Top priority trade/auction target if un-retained; provides versatile top-3 tempo or middle-overs power."
        },
        {
            "player_name": "Prince Yadav",
            "player_id": 58246,
            "age": 23,
            "nationality": "India",
            "category": "Tier B: Emerging Pressure Performer (Rank #11 Bowler)",
            "role": "Right-Arm Fast Bowler",
            "franchise": "Lucknow Super Giants / India",
            "total_balls_dataset": 747,
            "hp_balls_dataset": 297,
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": "88.87 (Rank #11 Bowler)",
            "tactical_assessment": "Elite domestic pace discovery. Ice Cold Anchor archetype (88.87 score across 297 HP deliveries). Bowls heavy hard lengths with 140+ km/h speed, highly resilient at death.",
            "recommendation_for_rr": "Prime fast-bowling acquisition target; solves domestic pace depth alongside Prasidh Krishna."
        },
        {
            "player_name": "Rasikh Salam",
            "player_id": 7327,
            "age": 24,
            "nationality": "India",
            "category": "Tier B: Emerging Pressure Performer (Rank #20 Bowler)",
            "role": "Right-Arm Medium-Fast Bowler",
            "franchise": "Royal Challengers Bengaluru / DC / India A",
            "total_balls_dataset": 571,
            "hp_balls_dataset": 140,
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": "82.06 (Rank #20 Bowler)",
            "tactical_assessment": "Skilful death executor with deceptive back-of-the-hand slower balls and yorkers. Strong performance in Emerging Teams Asia Cup.",
            "recommendation_for_rr": "High-value Indian pace asset for middle and death overs; cost-effective domestic squad depth."
        },
        {
            "player_name": "Allah Ghazanfar",
            "player_id": 48312,
            "age": 18,
            "nationality": "Afghanistan",
            "category": "Tier B: Emerging Pressure Performer (Rank #17 Bowler)",
            "role": "Right-Arm Mystery Off-Break Spinner",
            "franchise": "Kolkata Knight Riders / Afghanistan A",
            "total_balls_dataset": 612,
            "hp_balls_dataset": 212,
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": "83.68 (Rank #17 Bowler)",
            "tactical_assessment": "Teenage mystery spinner with carrom ball and quick arm speed. Holds Ice Cold Anchor profile across 212 high-pressure balls in international and emerging fixtures.",
            "recommendation_for_rr": "Elite overseas wrist/finger spin target; extreme ceiling for Jaipur surfaces."
        },
        {
            "player_name": "Abbas Afridi",
            "player_id": 36341,
            "age": 23,
            "nationality": "Pakistan",
            "category": "Tier A: Proven Pressure Performer (Rank #3 Bowler)",
            "role": "Right-Arm Medium-Fast Seamer",
            "franchise": "Pakistan / Pakistan A",
            "total_balls_dataset": 589,
            "hp_balls_dataset": 232,
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": "91.88 (Rank #3 Bowler)",
            "tactical_assessment": "Elite change-of-pace death bowler. Possesses dip, wide yorkers, and cutter variations under extreme leverage. Statistical excellence benchmark.",
            "recommendation_for_rr": "Benchmark for death-overs variation modeling (BCCI policy restricts IPL participation; study tactical mechanics for RR bowling group)."
        },
        {
            "player_name": "Sufiyan Muqeem",
            "player_id": 49925,
            "age": 24,
            "nationality": "Pakistan",
            "category": "Tier A: Proven Pressure Performer (Rank #5 Bowler)",
            "role": "Left-Arm Wrist Spinner (Chinaman)",
            "franchise": "Pakistan / Pakistan A",
            "total_balls_dataset": 528,
            "hp_balls_dataset": 213,
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": "91.41 (Rank #5 Bowler)",
            "tactical_assessment": "Rare left-arm wrist spin angle, high revs, sharp googly under pressure. Unflappable economy when batters are on the attack.",
            "recommendation_for_rr": "Tactical benchmark for wrist-spin release points and defensive line variation."
        },
        {
            "player_name": "Harpreet Brar",
            "player_id": 6019,
            "age": 29,
            "nationality": "India",
            "category": "Tier B: Emerging/Established Pressure Asset (Rank #14 Bowler)",
            "role": "Slow Left-Arm Orthodox Spinner",
            "franchise": "Punjab Kings",
            "total_balls_dataset": 782,
            "hp_balls_dataset": 257,
            "dataset_strike_rate": "N/A (Bowler)",
            "pressure_reliability_score": "87.73 (Rank #14 Bowler)",
            "tactical_assessment": "Clutch Climber archetype. Unmatched ability to fire flat, tight lengths at 95 km/h against high-leverage right-hand power hitters.",
            "recommendation_for_rr": "Prime domestic acquisition target to execute the Jaipur Squeeze at SMS Stadium."
        },
        {
            "player_name": "Rinku Singh",
            "player_id": 6023,
            "age": 27,
            "nationality": "India",
            "category": "Tier A: Proven Pressure Performer (Rank #11 Batter)",
            "role": "Left-Hand Middle-Order Finisher",
            "franchise": "Kolkata Knight Riders (Retained)",
            "total_balls_dataset": 1120,
            "hp_balls_dataset": 418,
            "dataset_strike_rate": 152.6,
            "pressure_reliability_score": "92.37 (Rank #11 Batter)",
            "tactical_assessment": "The gold standard of Indian domestic clutch hitting. Missed top 10 by a razor-thin 0.08 points. Exceptional calm in final-over chases.",
            "recommendation_for_rr": "Tactical case study in pressure mindset and bat-speed timing; benchmark for Dhruv Jurel and lower-order development."
        }
    ]
    
    em_df = pd.DataFrame(emerging_data)
    em_df.to_csv("data/processed/emerging_talent_watchlist.csv", index=False)
    print("Saved emerging_talent_watchlist.csv (10 detailed profiles)")

if __name__ == "__main__":
    main()

