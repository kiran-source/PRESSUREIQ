"""
Build comprehensive player-level franchise accounting reconciliation dataset.
Audits the exact transitions between previous squad membership and 2027 final roster
while resolving population definition boundaries (Core 25-man squad vs Extended trialist/replacement pool).
"""

import os
import sys
sys.path.append(os.path.abspath("."))
import json
import pandas as pd
from scripts.build_official_iplt20_rosters_and_releases import (
    ROSTERS,
    RELEASES,
    get_canonical_id,
    SOURCE_URL,
    SOURCE_PUBLISHER,
    SOURCE_DATE,
    VERIFICATION_TS
)

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

# 1. Process 2027 Official Rostered Players (Retained + Traded In)
for team, players in ROSTERS.items():
    for p in players:
        p_name, marker, marker_desc, status, trade_from, trade_fee = p
        cid = get_canonical_id(p_name)
        if status == "Confirmed Trade":
            trans_type = "Traded In"
            prev_squad = 0  # Was not in THIS team's previous squad
            final_roster = 1
            note = f"Acquired via trade from {trade_from} for {trade_fee}"
        else:
            trans_type = "Retained Without Transfer"
            prev_squad = 1  # Member of this team's core squad
            final_roster = 1
            note = f"Core squad retention ({marker_desc})"

        rows.append({
            "franchise": team,
            "player_name": p_name,
            "canonical_player_id": cid,
            "previous_squad_membership": prev_squad,
            "transition_type": trans_type,
            "final_2027_roster_membership": final_roster,
            "visual_marker_on_graphic": marker,
            "accounting_notes": note,
            "source_url": SOURCE_URL,
            "verification_timestamp": VERIFICATION_TS
        })

# 2. Process Traded Out Players
for team, p_name, dest_team, fee in TRADES_OUT:
    cid = get_canonical_id(p_name)
    rows.append({
        "franchise": team,
        "player_name": p_name,
        "canonical_player_id": cid,
        "previous_squad_membership": 1,
        "transition_type": "Traded Out",
        "final_2027_roster_membership": 0,
        "visual_marker_on_graphic": "Not Listed (Traded Out)",
        "accounting_notes": f"Traded out to {dest_team} for {fee}",
        "source_url": SOURCE_URL,
        "verification_timestamp": VERIFICATION_TS
    })

# 3. Process Exits (Retired, Opted Out, Released)
for rel in RELEASES:
    team, p_name, cat, fee, role, nat, note = rel
    cid = get_canonical_id(p_name)
    
    if "Retired" in cat:
        trans_type = "Retired / Transition"
        prev_squad = 1
        note_text = "Legend icon / transition to mentor & uncapped roster category"
    elif "Opted Out" in cat:
        trans_type = "Opted Out / Unavailable"
        prev_squad = 1
        note_text = "Unavailable for IPL 2027 due to international scheduling/workload"
    else:
        # Check if Core or Extended
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
        "source_url": SOURCE_URL,
        "verification_timestamp": VERIFICATION_TS
    })

df_rec = pd.DataFrame(rows)

# Save output
out_csv = "data/processed/ipl_2027_franchise_accounting_reconciliation.csv"
handover_csv = "submission_handover/03_Evidence_CSVs_And_Provenance/ipl_2027_franchise_accounting_reconciliation.csv"

df_rec.to_csv(out_csv, index=False)
df_rec.to_csv(handover_csv, index=False)

print(f"Exported {len(df_rec)} reconciliation records!")

# Summary Table by Franchise
print("\n--- FRANCHISE ACCOUNTING SUMMARY ---")
summary = []
for t in df_rec["franchise"].unique():
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
    total_departures = traded_out + core_rel + ext_rel + retired + opted_out
    vacancies = 25 - rostered
    
    summary.append({
        "Team": t,
        "2027 Roster": rostered,
        "Retained": retained,
        "Traded In": traded_in,
        "Traded Out": traded_out,
        "Core Released": core_rel,
        "Extended Released": ext_rel,
        "Retired": retired,
        "Opted Out": opted_out,
        "Core Prior Squad": core_prior,
        "Theoretical Vacancies (25-Cap)": vacancies
    })

df_sum = pd.DataFrame(summary)
print(df_sum.to_string(index=False))

with open("audit/final_v66/franchise_accounting_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)
