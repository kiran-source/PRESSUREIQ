"""
Build player-level franchise accounting reconciliation dataset.
Reads official squad rosters and released player audits and reconciles core vs extended pool.
"""

import os
import json
import pandas as pd

ROSTER_CSV = "data/processed/ipl_2027_official_squad_rosters.csv"
RELEASE_CSV = "data/processed/ipl_2027_released_players_audit.csv"

df_roster = pd.read_csv(ROSTER_CSV)
df_release = pd.read_csv(RELEASE_CSV)

# Core 25-man classification boundary for releases across the 10 franchises
CORE_SQUAD_RELEASES = {
    "CSK": {"Spencer Johnson", "Matthew Short", "Matt Henry", "Prashant Veer", "Zak Foulkes"},
    "DC": {"Nitish Rana", "Abishek Porel", "Pathum Nissanka", "Ben Duckett", "Karun Nair", "Dushmantha Chameera", "Rehan Ahmed", "Ajay Mandal"},
    "GT": {"Shahrukh Khan", "Ishant Sharma", "Luke Wood", "Connor Esterhuizen"},
    "KKR": {"Matheesha Pathirana", "Mustafizur Rahman", "Rachin Ravindra", "Ajinkya Rahane", "Rahul Tripathi", "Umran Malik", "Akash Deep", "Navdeep Saini"},
    "LSG": {"Avesh Khan", "Anrich Nortje", "Wanindu Hasaranga", "George Linde", "Naman Tiwari", "Matthew Breetzke", "Arshin Kulkarni"},
    "MI": {"Trent Boult", "Deepak Chahar", "Allah Ghazanfar", "Keshav Maharaj", "Atharva Ankolekar", "Mayank Markande", "Danish Malewar", "Mayank Rawat", "Mohammed Izhar"},
    "PBKS": {"Lockie Ferguson", "Nehal Wadhera", "Mitchell Owen", "Praveen Dubey", "Vishal Nishad"},
    "RR": {"Shimron Hetmyer", "Tushar Deshpande", "Adam Milne", "Kwena Maphaka"},
    "RCB": {"Jacob Bethell", "Mangesh Yadav", "Richard Gleeson", "Vihaan Malhotra", "Swastik Chikara"},
    "SRH": {"Gerald Coetzee", "David Payne", "Jaydev Unadkat", "Shivam Mavi", "Kamindu Mendis", "Dilshan Madushanka"},
}

TRADES_OUT = [
    ("CSK", "Khaleel Ahmed", "Sunrisers Hyderabad", "₹4.80 crore"),
    ("CSK", "Nathan Ellis", "Sunrisers Hyderabad", "₹2 crore"),
    ("DC", "Kuldeep Yadav", "Lucknow Super Giants", "₹13.50 crore"),
    ("DC", "T Natarajan", "Sunrisers Hyderabad", "₹5 crore"),
    ("MI", "Hardik Pandya", "Punjab Kings", "₹18 crore"),
    ("LSG", "Rishabh Pant", "Delhi Capitals", "₹15 crore"),
    ("LSG", "Mohammed Shami", "Rajasthan Royals", "₹8 crore"),
    ("LSG", "Manimaran Siddharth", "Rajasthan Royals", "₹75 lakh"),
    ("PBKS", "Arshdeep Singh", "Mumbai Indians", "₹18 crore"),
    ("PBKS", "Harshal Patel", "Gujarat Titans", "₹4 crore"),
    ("RR", "Sam Curran", "Lucknow Super Giants", "₹2.40 crore"),
    ("SRH", "Liam Livingstone", "Chennai Super Kings", "₹6 crore"),
    ("SRH", "Jack Edwards", "Chennai Super Kings", "₹3 crore"),
    ("SRH", "Zeeshan Ansari", "Delhi Capitals", "₹40 lakh"),
]

rows = []

# 1. Official 2027 Rostered Players (183)
for _, r in df_roster.iterrows():
    team = r["franchise"]
    p_name = r["player_name"]
    cid = int(r["canonical_player_id"])
    marker = r["visual_marker"]
    desc = r["marker_interpretation"]
    status = r["retention_status"]
    trade_from = r["incoming_trade_from"]
    fee = r["trade_fee"]

    if status == "Confirmed Trade":
        trans_type = "Traded In"
        prev_squad = 0
        final_roster = 1
        note = f"Acquired via trade from {trade_from} for {fee}"
    else:
        trans_type = "Retained Without Transfer"
        prev_squad = 1
        final_roster = 1
        note = f"Core squad retention ({desc})"

    rows.append({
        "franchise": team,
        "player_name": p_name,
        "canonical_player_id": cid,
        "previous_squad_membership": prev_squad,
        "transition_type": trans_type,
        "final_2027_roster_membership": final_roster,
        "visual_marker_on_graphic": marker,
        "accounting_notes": note,
        "source_url": r["source_url"],
        "verification_timestamp": r["verification_timestamp"]
    })

# 2. Traded Out Players (14)
for team, p_name, dest_team, fee in TRADES_OUT:
    # Match canonical ID from releases or roster if possible
    m = df_roster[df_roster["player_name"] == p_name]
    if len(m) > 0:
        cid = int(m.iloc[0]["canonical_player_id"])
    else:
        m2 = df_release[df_release["player_name"] == p_name]
        cid = int(m2.iloc[0]["canonical_player_id"]) if len(m2) > 0 else 999999

    rows.append({
        "franchise": team,
        "player_name": p_name,
        "canonical_player_id": cid,
        "previous_squad_membership": 1,
        "transition_type": "Traded Out",
        "final_2027_roster_membership": 0,
        "visual_marker_on_graphic": "Not Listed (Traded Out)",
        "accounting_notes": f"Traded out to {dest_team} for {fee}",
        "source_url": "https://www.instagram.com/p/Df2lhqjjb-h/",
        "verification_timestamp": "2026-11-17 20:05:00 IST"
    })

# 3. Exits (78)
for _, r in df_release.iterrows():
    team = r["prior_franchise"]
    p_name = r["player_name"]
    cid = int(r["canonical_player_id"])
    cat = r["exit_category"]
    fee = r["previous_fee"]

    if "Retired" in cat:
        trans_type = "Retired / Transition"
        prev_squad = 1
        note_text = "Legend icon / transition to mentor & uncapped roster category"
    elif "Opted Out" in cat:
        trans_type = "Opted Out / Unavailable"
        prev_squad = 1
        note_text = "Unavailable for IPL 2027 due to international scheduling/workload"
    else:
        if p_name in CORE_SQUAD_RELEASES.get(team, set()):
            trans_type = "Released (Core Squad)"
            prev_squad = 1
            note_text = f"Formal release from registered core squad (Fee: {fee})"
        else:
            trans_type = "Released (Extended Pool)"
            prev_squad = 0
            note_text = f"Lapsed replacement / trialist contract clearance (Fee: {fee})"

    rows.append({
        "franchise": team,
        "player_name": p_name,
        "canonical_player_id": cid,
        "previous_squad_membership": prev_squad,
        "transition_type": trans_type,
        "final_2027_roster_membership": 0,
        "visual_marker_on_graphic": "Not Listed (Exited)",
        "accounting_notes": note_text,
        "source_url": r["source_url"],
        "verification_timestamp": r["verification_timestamp"]
    })

df_rec = pd.DataFrame(rows)

out_csv = "data/processed/ipl_2027_franchise_accounting_reconciliation.csv"
handover_csv = "submission_handover/03_Evidence_CSVs_And_Provenance/ipl_2027_franchise_accounting_reconciliation.csv"

df_rec.to_csv(out_csv, index=False)
df_rec.to_csv(handover_csv, index=False)
print(f"Exported {len(df_rec)} reconciliation records!")

# Summary Table
summary = []
for t in ["CSK", "DC", "GT", "KKR", "LSG", "MI", "PBKS", "RR", "RCB", "SRH"]:
    tdf = df_rec[df_rec["franchise"] == t]
    rostered = (tdf["final_2027_roster_membership"] == 1).sum()
    retained = (tdf["transition_type"] == "Retained Without Transfer").sum()
    traded_in = (tdf["transition_type"] == "Traded In").sum()
    traded_out = (tdf["transition_type"] == "Traded Out").sum()
    core_rel = (tdf["transition_type"] == "Released (Core Squad)").sum()
    ext_rel = (tdf["transition_type"] == "Released (Extended Pool)").sum()
    retired = (tdf["transition_type"] == "Retired / Transition").sum()
    opted_out = (tdf["transition_type"] == "Opted Out / Unavailable").sum()

    core_prior = retained + traded_out + core_rel + retired + opted_out
    vacancies = 25 - rostered

    summary.append({
        "Team": t,
        "2027 Roster": int(rostered),
        "Retained": int(retained),
        "Traded In": int(traded_in),
        "Traded Out": int(traded_out),
        "Core Released": int(core_rel),
        "Extended Released": int(ext_rel),
        "Retired": int(retired),
        "Opted Out": int(opted_out),
        "Core Prior Squad": int(core_prior),
        "Theoretical Vacancies (25-Cap)": int(vacancies)
    })

df_sum = pd.DataFrame(summary)
print("\n" + df_sum.to_string(index=False))

with open("audit/final_v66/franchise_accounting_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)
print("Saved summary JSON!")
