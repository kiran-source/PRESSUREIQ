"""Build Player Eligibility Audit and Rajasthan Royals IPL 2027 Recommendation System.

Mandatory Rules:
- Preserves Model A as Leaderboard A (Pure Pressure Reliability).
- Reconstructs Leaderboard B (RR IPL 2027 Acquisition Recommendations) using Multi-Criteria Decision Analysis.
- Integrates the audited market intelligence ledger (data/processed/ipl_2027_player_market_template.csv).
- Strictly prohibits displaying Pending Verification, Rumour, or Policy/Eligibility Review
  records as Confirmed Available or Confirmed Released.
- Respects longstanding BCCI/diplomatic restriction (Pakistani players in Class D).
- Accounts for 2026 franchise contracts / Nov 5 2026 trades (Class C) vs contingent targets (Class B).
"""

from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
RAW_DIR = REPO_ROOT / "SupeRR Selector Season 2 _ Problem Statement _ Data Pack" / "SupeRR Selector Season 2 _ Data Pack"

# Load source files
bat_df = pd.read_csv(PROCESSED_DIR / "final_batter_rankings.csv")
bowl_df = pd.read_csv(PROCESSED_DIR / "final_bowler_rankings.csv")
comp_map = pd.read_csv(RAW_DIR / "competition_team_player_mapping.csv")

MARKET_PATH = PROCESSED_DIR / "ipl_2027_player_market_template.csv"
market_df = pd.read_csv(MARKET_PATH).fillna("None") if MARKET_PATH.exists() else pd.DataFrame()
market_by_id = market_df.set_index("player_id").to_dict(orient="index") if len(market_df) > 0 else {}

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

# Pakistan-registered players (Class D Policy/Eligibility Review under post-2008 BCCI/diplomatic stance)
PAKISTAN_PLAYERS = {
    "Fakhar Zaman", "Haris Rauf", "Abbas Afridi", "Sufiyan Muqeem", "Mohammad Rizwan",
    "Abrar Ahmed", "Babar Azam", "Shaheen Shah Afridi", "Naseem Shah", "Shadab Khan",
    "Iftikhar Ahmed", "Imad Wasim", "Mohammad Amir", "Saim Ayub", "Azam Khan",
    "Usman Khan", "Zaman Khan", "Mohammad Haris", "Haseebullah Khan", "Aamer Jamal"
}

# Verified RR 2026 Squad Core (awaiting Nov 17, 2026 retention list)
RR_EXISTING_CORE = {
    "Dhruv Jurel": "RR 2026 Retained Core WK-Batter (2027 List Pending Nov 17)",
    "Yashasvi Jaiswal": "RR 2026 Retained Opener (2027 List Pending Nov 17)",
    "Riyan Parag": "RR 2026 Retained Middle-Order All-Rounder (2027 List Pending Nov 17)",
    "Sandeep Sharma": "RR 2026 Retained Death Bowler (2027 List Pending Nov 17)",
    "Jofra Archer": "RR 2026 Retained Fast Bowler (2027 List Pending Nov 17)",
    "Shimron Hetmyer": "RR 2026 Retained Overseas Finisher (2027 List Pending Nov 17)",
    "Vaibhav Sooryavanshi": "RR 2026 Retained Emerging Opener (2027 List Pending Nov 17)",
    "Vignesh Puthur": "RR 2026 Auction Signing INR 30L (2027 List Pending Nov 17)",
    "Tushar Deshpande": "RR 2026 Retained Seam Bowler (2027 List Pending Nov 17)",
    "Ravindra Jadeja": "RR 2026 Traded & Retained All-Rounder (2027 List Pending Nov 17)",
    "Sam Curran": "RR 2026 Traded & Retained All-Rounder (2027 List Pending Nov 17)",
    "Donovan Ferreira": "RR 2026 Traded & Retained Finisher (2027 List Pending Nov 17)",
}

# Verified Non-RR Franchise Contracts from IPL 2026 Squads & Nov 5, 2026 Trade Window (Class C)
# Updated strictly against official TATA IPL 2026 Retentions (2025-11-15), 2026 Auction, and Nov 5 2026 Trade.
FRANCHISE_CONTRACTS = {
    "Ruturaj Gaikwad": ("Chennai Super Kings", "CSK 2026 Retained Captain (2027 List Pending Nov 17)"),
    "Sanju Samson": ("Chennai Super Kings", "CSK 2026 Traded Captain/WK (2027 List Pending Nov 17)"),
    "Shivam Dube": ("Chennai Super Kings", "CSK 2026 Retained All-Rounder (2027 List Pending Nov 17)"),
    "Noor Ahmad": ("Chennai Super Kings", "CSK 2026 Retained Spinner (2027 List Pending Nov 17)"),
    "Mukesh Choudhary": ("Chennai Super Kings", "CSK 2026 Retained Pacer (2027 List Pending Nov 17)"),
    "Nathan Ellis": ("Sunrisers Hyderabad", "Confirmed Trade CSK -> SRH (2026-11-05, 4-player deal)"),
    "Heinrich Klaasen": ("Sunrisers Hyderabad", "SRH 2026 Retained Keeper-Batter (2027 List Pending Nov 17)"),
    "Travis Head": ("Sunrisers Hyderabad", "SRH 2026 Retained Opener (2027 List Pending Nov 17)"),
    "Pat Cummins": ("Sunrisers Hyderabad", "SRH 2026 Retained Captain (2027 List Pending Nov 17)"),
    "Patrick Cummins": ("Sunrisers Hyderabad", "SRH 2026 Retained Captain (2027 List Pending Nov 17)"),
    "Mukesh Kumar": ("Delhi Capitals", "DC 2026 Retained Fast Bowler (2027 List Pending Nov 17)"),
    "Eshan Malinga": ("Sunrisers Hyderabad", "SRH 2026 Retained Death Bowler (2027 List Pending Nov 17)"),
    "Harshal Patel": ("Sunrisers Hyderabad", "SRH 2026 Retained Seam Bowler (2027 List Pending Nov 17)"),
    "Rohit Sharma": ("Mumbai Indians", "MI 2026 Retained Veteran Opener (2027 List Pending Nov 17)"),
    "Suryakumar Yadav": ("Mumbai Indians", "MI 2026 Retained India T20I Captain (2027 List Pending Nov 17)"),
    "Naman Dhir": ("Mumbai Indians", "MI 2026 Retained All-Rounder (2027 List Pending Nov 17)"),
    "Trent Boult": ("Mumbai Indians", "MI 2026 Retained Left-Arm Pacer (2027 List Pending Nov 17)"),
    "Mitchell Santner": ("Mumbai Indians", "MI 2026 Retained Spinner (2027 List Pending Nov 17)"),
    "Namboori Tilak Varma": ("Mumbai Indians", "MI 2026 Retained Core Batter (2027 List Pending Nov 17)"),
    "Jasprit Bumrah": ("Mumbai Indians", "MI 2026 Retained Lead Pacer (2027 List Pending Nov 17)"),
    "Jos Buttler": ("Gujarat Titans", "GT 2026 Retained Top-Order WK (526 runs in 2026; 2027 Pending Nov 17)"),
    "Prasidh Krishna": ("Gujarat Titans", "GT 2026 Retained Fast Bowler (2027 List Pending Nov 17)"),
    "Rashid Khan": ("Gujarat Titans", "GT 2026 Retained Lead Spinner (2027 List Pending Nov 17)"),
    "Ishant Sharma": ("Gujarat Titans", "GT 2026 Retained Seam Bowler (2027 List Pending Nov 17)"),
    "Matheesha Pathirana": ("Kolkata Knight Riders", "KKR 2026 Auction Signing INR 18 Cr (2027 List Pending Nov 17)"),
    "Rinku Singh": ("Kolkata Knight Riders", "KKR 2026 Retained Finisher (2027 List Pending Nov 17)"),
    "Rovman Powell": ("Kolkata Knight Riders", "KKR 2026 Retained Power Batter (2027 List Pending Nov 17)"),
    "Vaibhav Arora": ("Kolkata Knight Riders", "KKR 2026 Retained Seam Bowler (2027 List Pending Nov 17)"),
    "Sunil Narine": ("Kolkata Knight Riders", "KKR 2026 Retained All-Rounder (2027 List Pending Nov 17)"),
    "Varun Chakaravarthy": ("Kolkata Knight Riders", "KKR 2026 Retained Spinner (2027 List Pending Nov 17)"),
    "Nicholas Pooran": ("Lucknow Super Giants", "LSG 2026 Retained Core Keeper (2027 List Pending Nov 17)"),
    "Prince Yadav": ("Lucknow Super Giants", "LSG 2026 Retained Fast Bowler (2027 List Pending Nov 17)"),
    "Ayush Badoni": ("Lucknow Super Giants", "LSG 2026 Retained Middle-Order Batter (2027 List Pending Nov 17)"),
    "Avesh Khan": ("Lucknow Super Giants", "LSG 2026 Retained Fast Bowler (2027 List Pending Nov 17)"),
    "Jitesh Sharma": ("Royal Challengers Bengaluru", "RCB 2026 Retained Keeper-Batter (2027 List Pending Nov 17)"),
    "Romario Shepherd": ("Royal Challengers Bengaluru", "RCB 2026 Retained Seam All-Rounder (2027 List Pending Nov 17)"),
    "Phil Salt": ("Royal Challengers Bengaluru", "RCB 2026 Retained Top-Order WK (2027 List Pending Nov 17)"),
    "Tim David": ("Royal Challengers Bengaluru", "RCB 2026 Retained Finisher (2027 List Pending Nov 17)"),
    "Bhuvneshwar Kumar": ("Royal Challengers Bengaluru", "RCB 2026 Retained Swing Bowler (2027 List Pending Nov 17)"),
    "Rasikh Salam": ("Royal Challengers Bengaluru", "RCB 2026 Retained Fast Bowler (2027 List Pending Nov 17)"),
    "Harpreet Brar": ("Punjab Kings", "PBKS 2026 Retained Left-Arm Spinner (2027 List Pending Nov 17)"),
    "Shashank Singh": ("Punjab Kings", "PBKS 2026 Retained Finisher (2027 List Pending Nov 17)"),
    "Marcus Stoinis": ("Punjab Kings", "PBKS 2026 Retained Overseas All-Rounder (2027 List Pending Nov 17)"),
    "Azmatullah Omarzai": ("Punjab Kings", "PBKS 2026 Retained Overseas All-Rounder (2027 List Pending Nov 17)"),
    "Arshdeep Singh": ("Punjab Kings", "PBKS 2026 Retained Left-Arm Pacer (2027 List Pending Nov 17)"),
    "Yuzvendra Chahal": ("Punjab Kings", "PBKS 2026 Retained Leg-Spinner (2027 List Pending Nov 17)"),
    "Tristan Stubbs": ("Delhi Capitals", "DC 2026 Retained Core Batter (2027 List Pending Nov 17)"),
    "Axar Patel": ("Delhi Capitals", "DC 2026 Retained All-Rounder (2027 List Pending Nov 17)"),
    "Kuldeep Yadav": ("Delhi Capitals", "DC 2026 Retained Wrist-Spinner (2027 List Pending Nov 17)"),
    "Mitchell Starc": ("Delhi Capitals", "DC 2026 Retained Left-Arm Pacer (2027 List Pending Nov 17)"),
}

# Retired / Inactive (Class E)
RETIRED_INACTIVE = {
    "Mahendra Singh Dhoni": "Veteran franchise icon / non-auction asset",
    "Dinesh Karthik": "Retired from IPL active playing roster",
    "Matthew Wade": "Retired from international cricket / sporadic franchise availability",
    "David Miller": "Veteran overseas status / unconfirmed 2027 auction entry"
}


def audit_player(pname, pid, is_bat=True):
    sub = comp_map[comp_map["player_name"] == pname]
    teams = sub["team_name"].unique().tolist()

    ipl_teams = [t for t in teams if any(f in t for f in IPL_FRANCHISES)]
    intl_teams = [t for t in teams if t in INTL_TEAMS]

    latest_ipl = ipl_teams[-1] if ipl_teams else "None"
    nationality = intl_teams[0] if intl_teams else ("India" if ipl_teams and "India" in str(teams) else "Unknown")
    is_overseas = (nationality != "India")

    if pname in ["Harpreet Brar", "Prince Yadav", "Naman Dhir", "Rasikh Salam", "Mukesh Choudhary", "Shashank Singh", "Jitesh Sharma", "Vaibhav Arora", "Ayush Badoni"]:
        nationality = "India"
        is_overseas = False

    mkt_row = market_by_id.get(pid)
    if mkt_row:
        mkt_status = str(mkt_row.get("official_retention_status", "Pending Verification"))
        mkt_fran = str(mkt_row.get("current_verified_franchise", latest_ipl))
        mkt_url = str(mkt_row.get("source_url", ""))
        if mkt_fran not in {"None", "Unknown"}:
            latest_ipl = mkt_fran
    else:
        mkt_status = "Policy/Eligibility Review" if (pname in PAKISTAN_PLAYERS or nationality == "Pakistan") else "Pending Verification"
        mkt_url = "https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced"

    # Determine Classification strictly without falsely marking Pending records as Confirmed Available
    if pname in PAKISTAN_PLAYERS or nationality == "Pakistan":
        cls = "D"
        mkt_status = "Policy/Eligibility Review"
        status_desc = "Policy/Eligibility Review (Longstanding post-2008 bilateral/BCCI restriction)"
        avail_2027 = "0% (Policy/Eligibility Review — Not Available)"
        conf = "Established Policy Context"
    elif pname in RETIRED_INACTIVE:
        cls = "E"
        status_desc = RETIRED_INACTIVE[pname]
        avail_2027 = "0% (Retired/Inactive)"
        conf = "Historical Record"
    elif pname in RR_EXISTING_CORE:
        cls = "A"
        latest_ipl = "Rajasthan Royals"
        status_desc = RR_EXISTING_CORE[pname]
        avail_2027 = "Existing RR 2026 Core (2027 Retention Pending Verification)"
        conf = "Verified 2026 Squad / Pending Nov 17 List"
    elif pname in FRANCHISE_CONTRACTS:
        cls = "C"
        f_team, reason = FRANCHISE_CONTRACTS[pname]
        latest_ipl = f_team
        status_desc = f"Contracted to {f_team} ({reason})"
        if mkt_status == "Confirmed Trade":
            avail_2027 = f"Confirmed Trade to {f_team} — Unavailable for Auction"
            conf = "Officially Confirmed (Pre-2027 Trade)"
        elif mkt_status == "Confirmed Retained":
            avail_2027 = f"Confirmed Retained by {f_team} — Unavailable"
            conf = "Officially Confirmed"
        else:
            avail_2027 = f"Pending Verification (2026 Contract: {f_team}; Awaiting Nov 17 List)"
            conf = "Verified 2026 Squad / Pending 2027 List"
    else:
        # Class B: Uncontracted in 2026 retained lists or overseas free agent — still Pending Nov 17 & Nov 23 registration
        cls = "B"
        status_desc = f"Contingent Pool Candidate (Latest mapped team: {latest_ipl}; 2027 status unconfirmed)"
        avail_2027 = "Contingent Target — Pending Verification (Awaiting Nov 17 & Auction Registration)"
        conf = "Pending Official Auction Registration"

    return {
        "player_id": pid,
        "player_name": pname,
        "discipline": "Batter" if is_bat else "Bowler",
        "nationality": nationality,
        "is_overseas": is_overseas,
        "latest_ipl_franchise": latest_ipl,
        "eligibility_class": cls,
        "market_status": mkt_status,
        "retention_trade_status": status_desc,
        "auction_2027_availability": avail_2027,
        "confidence_level": conf,
        "source": mkt_url,
    }


def main():
    print("=" * 80)
    print("CONDUCTING AUDITED PLAYER ELIGIBILITY & MARKET INTEGRATION...")
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
    print(f"Generated {audit_csv} ({len(audit_df)} players audited)")
    print("\nEligibility Class Breakdown:")
    print(audit_df["eligibility_class"].value_counts().to_string())

    # Single-pass MCDA: 40% Rel + 20% Ev + 25% Avail + 15% Fit
    class_weights = {"A": 1.00, "B": 0.85, "C": 0.20, "D": 0.00, "E": 0.00, "F": 0.50}

    def calculate_rr_scores(df_sub, is_bat=True):
        scored = []
        for _, row in df_sub.iterrows():
            cls = row["eligibility_class"]
            avail_w = class_weights.get(cls, 0.0)
            ev_score = min(100.0, (row["hp_balls"] / 250.0) * 60.0 + min(40.0, (row["matches"] / 50.0) * 40.0))

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
                "latest_ipl_franchise": row["latest_ipl_franchise"],
                "role": row["role"],
                "model_a_rank": row["model_a_rank"],
                "reliability_score": row["reliability_score"],
                "hp_balls": row["hp_balls"],
                "matches": row["matches"],
                "eligibility_class": cls,
                "market_status": row["market_status"],
                "auction_availability": row["auction_2027_availability"],
                "market_source_url": row["source"],
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

    candidates_df = pd.concat([bat_scored, bowl_scored], ignore_index=True)
    candidates_csv = PROCESSED_DIR / "rr_2027_candidate_rankings.csv"
    candidates_df.to_csv(candidates_csv, index=False)
    print(f"Generated {candidates_csv} ({len(candidates_df)} candidates scored)")

    top10_bat_rr = bat_scored.head(10).copy()
    top10_bowl_rr = bowl_scored.head(10).copy()

    top10_bat_rr.to_csv(PROCESSED_DIR / "rr_2027_batter_top10.csv", index=False)
    top10_bowl_rr.to_csv(PROCESSED_DIR / "rr_2027_bowler_top10.csv", index=False)

    print("\n--- TOP 10 CONTINGENT BATTERS (LEADERBOARD B) ---")
    print(top10_bat_rr[["rr_priority_rank", "player_name", "latest_ipl_franchise", "eligibility_class", "market_status", "rr_priority_score"]].to_string(index=False))

    print("\n--- TOP 10 CONTINGENT BOWLERS (LEADERBOARD B) ---")
    print(top10_bowl_rr[["rr_priority_rank", "player_name", "latest_ipl_franchise", "eligibility_class", "market_status", "rr_priority_score"]].to_string(index=False))


if __name__ == "__main__":
    main()
