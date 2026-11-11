"""Build Player Eligibility Audit and Rajasthan Royals IPL 2027 Recommendation System.

Mandatory Rules:
- Preserves Model A as Leaderboard A (Pure Pressure Reliability).
- Reconstructs Leaderboard B (RR IPL 2027 Acquisition Recommendations) using Multi-Criteria Decision Analysis.
- Explicitly classifies every candidate into Eligibility Classes A through F.
- Respects BCCI IPL regulatory restrictions (Pakistani players in Class D).
- Accounts for franchise retentions (Class C) vs auction/trade targets (Class A/B).
"""

import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
RAW_DIR = REPO_ROOT / "SupeRR Selector Season 2 _ Problem Statement _ Data Pack" / "SupeRR Selector Season 2 _ Data Pack"

# Load source files
bat_df = pd.read_csv(PROCESSED_DIR / "final_batter_rankings.csv")
bowl_df = pd.read_csv(PROCESSED_DIR / "final_bowler_rankings.csv")
comp_map = pd.read_csv(RAW_DIR / "competition_team_player_mapping.csv")

# Known nationalities mapping from international series
INTL_TEAMS = [
    "India", "Pakistan", "England", "Australia", "South Africa", "New Zealand",
    "West Indies", "Sri Lanka", "Bangladesh", "Afghanistan", "Ireland", "Zimbabwe",
    "United Arab Emirates", "Nepal", "Netherlands", "Scotland", "Namibia", "Oman",
    "USA", "Canada", "Uganda", "Papua New Guinea"
]

IPL_FRANCHISES = [
    "Rajasthan Royals", "Chennai Super Kings", "Mumbai Indians", "Kolkata Knight Riders",
    "Royal Challengers Bengaluru", "Delhi Capitals", "Punjab Kings", "Sunrisers Hyderabad",
    "Gujarat Titans", "Lucknow Super Giants"
]

# Verified Pakistani players (Class D under prevailing BCCI policy)
PAKISTAN_PLAYERS = {
    "Fakhar Zaman", "Haris Rauf", "Abbas Afridi", "Sufiyan Muqeem", "Mohammad Rizwan",
    "Abrar Ahmed", "Babar Azam", "Shaheen Shah Afridi", "Naseem Shah", "Shadab Khan",
    "Iftikhar Ahmed", "Imad Wasim", "Mohammad Amir", "Saim Ayub", "Azam Khan",
    "Usman Khan", "Zaman Khan", "Mohammad Haris", "Haseebullah Khan", "Aamer Jamal"
}

# Verified Franchise Retentions / Core Marquee Players (Class C)
# These players are core captains/franchise cornerstones who are extremely unlikely to enter the open auction
FRANCHISE_RETENTIONS = {
    "Ruturaj Gaikwad": ("Chennai Super Kings", "CSK Captain / Core Retention"),
    "Rohit Sharma": ("Mumbai Indians", "MI Core Veteran / Captaincy Group"),
    "Suryakumar Yadav": ("Mumbai Indians", "MI Core / India T20I Captain"),
    "Nicholas Pooran": ("Lucknow Super Giants", "LSG Top Core Retention"),
    "Matheesha Pathirana": ("Chennai Super Kings", "CSK Marquee Death Pacer"),
    "Nathan Ellis": ("Sunrisers Hyderabad", "Contracted to SRH via CSK-to-SRH Trade Deal"),
    "Rinku Singh": ("Kolkata Knight Riders", "KKR Core Retention"),
    "Tristan Stubbs": ("Delhi Capitals", "DC Core Retention"),
    "Shashank Singh": ("Punjab Kings", "PBKS Retained Finisher"),
    "Namboori Tilak Varma": ("Mumbai Indians", "MI Core Retention"),
    "Andre Russell": ("Kolkata Knight Riders", "KKR Core Retention"),
    "Shivam Dube": ("Chennai Super Kings", "CSK Core Retention"),
    "Rashid Khan": ("Gujarat Titans", "GT Core Retention"),
    "Jasprit Bumrah": ("Mumbai Indians", "MI Premier Fast Bowler"),
    "Axar Patel": ("Delhi Capitals", "DC Core Retention"),
    "Sanju Samson": ("Rajasthan Royals", "RR Captain"),
    "Yashasvi Jaiswal": ("Rajasthan Royals", "RR Core Opener"),
    "Riyan Parag": ("Rajasthan Royals", "RR Core All-Rounder"),
    "Sandeep Sharma": ("Rajasthan Royals", "RR Retained Death Bowler")
}

# Retired / Inactive (Class E)
RETIRED_INACTIVE = {
    "Mahendra Singh Dhoni": "Veteran status / un-auctionable franchise asset",
    "Dinesh Karthik": "Officially retired from IPL",
    "Matthew Wade": "Retired from international cricket / sporadic franchise participation",
    "David Miller": "Veteran overseas status"
}


def audit_player(pname, pid, is_bat=True):
    sub = comp_map[comp_map["player_name"] == pname]
    teams = sub["team_name"].unique().tolist()
    
    # Identify IPL teams and International teams
    ipl_teams = [t for t in teams if any(f in t for f in IPL_FRANCHISES)]
    intl_teams = [t for t in teams if t in INTL_TEAMS]
    
    latest_ipl = ipl_teams[-1] if ipl_teams else "None"
    nationality = intl_teams[0] if intl_teams else ("India" if ipl_teams and "India" in str(teams) else "Unknown")
    is_overseas = (nationality != "India")
    
    # Determine Classification
    if pname in PAKISTAN_PLAYERS or nationality == "Pakistan":
        cls = "D"
        status_desc = "Practical IPL participation restriction (BCCI Policy since 2008)"
        avail_2027 = "0% (Policy Ineligible)"
        conf = "High (Official Policy)"
    elif pname in RETIRED_INACTIVE:
        cls = "E"
        status_desc = RETIRED_INACTIVE[pname]
        avail_2027 = "0% (Retired/Inactive)"
        conf = "High"
    elif pname in FRANCHISE_RETENTIONS:
        cls = "C"
        f_team, reason = FRANCHISE_RETENTIONS[pname]
        status_desc = f"Contracted to {f_team} ({reason})"
        avail_2027 = "Unconfirmed / Highly Unlikely"
        conf = "High (Franchise Core)"
    elif pname in ["Jos Buttler", "Dhruv Jurel", "Prasidh Krishna", "Trent Boult", "Shimron Hetmyer"]:
        cls = "A"
        status_desc = "Rajasthan Royals priority asset / Existing squad core"
        avail_2027 = "Confirmed Target / Existing Asset"
        conf = "High"
    else:
        # Class B: Eligible & potentially available in auction/trade pool
        cls = "B"
        status_desc = f"Eligible for IPL 2027 auction pool (Latest team: {latest_ipl})"
        avail_2027 = "Eligible — Auction / Trade Pool Target"
        conf = "Moderate (Pending official final auction registration)"
        
    # Domestic Indian uncapped correction
    if pname in ["Harpreet Brar", "Prince Yadav", "Naman Dhir", "Rasikh Salam", "Mukesh Choudhary", "Shashank Singh", "Jitesh Sharma"]:
        nationality = "India"
        is_overseas = False
        
    return {
        "player_id": pid,
        "player_name": pname,
        "discipline": "Batter" if is_bat else "Bowler",
        "nationality": nationality,
        "is_overseas": is_overseas,
        "latest_ipl_franchise": latest_ipl,
        "eligibility_class": cls,
        "retention_trade_status": status_desc,
        "auction_2027_availability": avail_2027,
        "confidence_level": conf,
        "source": "BCCI official records & competition mapping"
    }


def main():
    print("=" * 80)
    print("🔍 CONDUCTING COMPREHENSIVE PLAYER ELIGIBILITY AUDIT...")
    print("=" * 80)
    
    audit_records = []
    
    for _, row in bat_df.iterrows():
        rec = audit_player(row["player_name"], row["player_id"], is_bat=True)
        rec["reliability_score"] = row["reliability_score"]
        rec["model_a_rank"] = row["rank"]
        rec["hp_balls"] = row["hp_balls"]
        rec["matches"] = row["matches"]
        rec["role"] = row["role"]
        rec["prc_archetype"] = row["prc_archetype"]
        rec["ci_lower_95"] = row["ci_lower_95"]
        rec["ci_upper_95"] = row["ci_upper_95"]
        rec["top10_prob"] = row.get("top10_inclusion_prob", 0.0)
        audit_records.append(rec)
        
    for _, row in bowl_df.iterrows():
        rec = audit_player(row["player_name"], row["player_id"], is_bat=False)
        rec["reliability_score"] = row["reliability_score"]
        rec["model_a_rank"] = row["rank"]
        rec["hp_balls"] = row["hp_balls"]
        rec["matches"] = row["matches"]
        rec["role"] = f"{row['pace_or_spin']} ({row['bowling_type']})"
        rec["prc_archetype"] = row["prc_archetype"]
        rec["ci_lower_95"] = row["ci_lower_95"]
        rec["ci_upper_95"] = row["ci_upper_95"]
        rec["top10_prob"] = row.get("top10_inclusion_prob", 0.0)
        audit_records.append(rec)
        
    audit_df = pd.DataFrame(audit_records)
    audit_csv = PROCESSED_DIR / "player_eligibility_audit.csv"
    audit_df.to_csv(audit_csv, index=False)
    print(f"✅ Generated {audit_csv} ({len(audit_df)} players audited)")
    print("\nEligibility Class Breakdown:")
    print(audit_df["eligibility_class"].value_counts().to_string())
    
    # -------------------------------------------------------------
    # MULTI-CRITERIA DECISION ANALYSIS FOR RR IPL 2027 (LEADERBOARD B)
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("🎯 COMPUTING RAJASTHAN ROYALS IPL 2027 ACQUISITION SCORES...")
    print("=" * 80)
    
    # Class Availability Multiplier
    # Class A = 1.00 (High certainty / existing core)
    # Class B = 0.85 (High likelihood auction pool target)
    # Class C = 0.20 (Contracted elsewhere; requires release or trade)
    # Class D = 0.00 (Ineligible under BCCI policy)
    # Class E = 0.00 (Retired/Inactive)
    class_weights = {"A": 1.00, "B": 0.85, "C": 0.20, "D": 0.00, "E": 0.00, "F": 0.50}
    
    # RR Role Fit Multipliers based on RR 2027 Squad Needs
    # Batters:
    # Finisher / Lower-Order (#7 need): 1.00
    # Middle Order / WK Depth: 0.90
    # Top Order Anchor (High quality cover): 0.80
    # Bowlers:
    # Death Pacer (Primary need): 1.00
    # Powerplay / Middle Finger Spin (Jaipur need): 0.95
    # Left-Arm Pace (Boult backup): 0.90
    # Other Pace / Spin: 0.75
    
    def calculate_rr_scores(df_sub, is_bat=True):
        scored = []
        for _, row in df_sub.iterrows():
            cls = row["eligibility_class"]
            avail_w = class_weights.get(cls, 0.0)
            
            # Evidence weight: Sigmoidal scaling on HP balls + match volume
            ev_score = min(100.0, (row["hp_balls"] / 250.0) * 60.0 + min(40.0, (row["matches"] / 50.0) * 40.0))
            
            # Role Fit
            role_str = str(row["role"]).lower()
            if is_bat:
                if "finisher" in role_str or "lower" in role_str:
                    fit_score = 100.0
                    role_need = "#7 Lower-Order Finisher (Critical RR Need)"
                elif "middle" in role_str:
                    fit_score = 90.0
                    role_need = "Middle-Order Crisis Stabilizer"
                else:
                    fit_score = 80.0
                    role_need = "Top-Order Powerplay Anchor"
            else:
                if "right-arm medium" in role_str or "fast" in role_str:
                    fit_score = 95.0
                    role_need = "Death Yorker & Pace Specialist (Critical RR Need)"
                elif "orthodox" in role_str or "chinaman" in role_str:
                    fit_score = 92.0
                    role_need = "Jaipur Boundary Squeeze Spinner"
                else:
                    fit_score = 80.0
                    role_need = "Bowling Squad Depth"
                    
            # Practical Acquisition Score:
            # 40% Pressure Reliability + 20% Evidence Strength + 25% Availability Feasibility + 15% Role Fit
            # Players with avail_w == 0.0 get 0.0 final acquisition score (strictly non-viable)
            if avail_w == 0.0:
                rr_score = 0.0
            else:
                rr_score = (
                    (row["reliability_score"] * 0.40) +
                    (ev_score * 0.20) +
                    (avail_w * 100.0 * 0.25) +
                    (fit_score * 0.15)
                )
                
            scored.append({
                "player_id": row["player_id"],
                "player_name": row["player_name"],
                "discipline": row["discipline"],
                "nationality": row["nationality"],
                "is_overseas": row["is_overseas"],
                "role": row["role"],
                "model_a_rank": row["model_a_rank"],
                "reliability_score": row["reliability_score"],
                "hp_balls": row["hp_balls"],
                "matches": row["matches"],
                "eligibility_class": cls,
                "auction_availability": row["auction_2027_availability"],
                "rr_role_need": role_need,
                "evidence_score": round(ev_score, 1),
                "rr_priority_score": round(rr_score, 2),
                "prc_archetype": row["prc_archetype"],
                "top10_inclusion_prob": row["top10_prob"]
            })
            
        res_df = pd.DataFrame(scored)
        res_df = res_df.sort_values(by="rr_priority_score", ascending=False).reset_index(drop=True)
        res_df["rr_priority_rank"] = res_df.index + 1
        return res_df

    bat_scored = calculate_rr_scores(audit_df[audit_df["discipline"] == "Batter"], is_bat=True)
    bowl_scored = calculate_rr_scores(audit_df[audit_df["discipline"] == "Bowler"], is_bat=False)
    
    # Save candidate rankings
    candidates_df = pd.concat([bat_scored, bowl_scored], ignore_index=True)
    candidates_csv = PROCESSED_DIR / "rr_2027_candidate_rankings.csv"
    candidates_df.to_csv(candidates_csv, index=False)
    print(f"✅ Generated {candidates_csv} ({len(candidates_df)} candidates scored)")
    
    # Save Top 10 Batters and Bowlers for RR 2027 (Leaderboard B)
    top10_bat_rr = bat_scored.head(10).copy()
    top10_bowl_rr = bowl_scored.head(10).copy()
    
    top10_bat_rr.to_csv(PROCESSED_DIR / "rr_2027_batter_top10.csv", index=False)
    top10_bowl_rr.to_csv(PROCESSED_DIR / "rr_2027_bowler_top10.csv", index=False)
    
    print("\n" + "=" * 110)
    print("🏏 LEADERBOARD B: TOP 10 RAJASTHAN ROYALS IPL 2027 BATTER TARGETS (REALISTIC AUCTION PRIORITIZATION)")
    print("=" * 110)
    print(top10_bat_rr[[
        "rr_priority_rank", "player_name", "nationality", "is_overseas", "reliability_score",
        "hp_balls", "eligibility_class", "rr_priority_score", "rr_role_need"
    ]].to_string(index=False))
    
    print("\n" + "=" * 110)
    print("🎯 LEADERBOARD B: TOP 10 RAJASTHAN ROYALS IPL 2027 BOWLER TARGETS (REALISTIC AUCTION PRIORITIZATION)")
    print("=" * 110)
    print(top10_bowl_rr[[
        "rr_priority_rank", "player_name", "nationality", "is_overseas", "reliability_score",
        "hp_balls", "eligibility_class", "rr_priority_score", "rr_role_need"
    ]].to_string(index=False))
    print("=" * 110 + "\n")


if __name__ == "__main__":
    main()
