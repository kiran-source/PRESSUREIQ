"""Ingest confirmed IPL 2027 player trades into the audited market ledger & change log."""

import os
import shutil
from datetime import datetime
from pathlib import Path
import pandas as pd

SOURCE_URL = "https://www.jagranjosh.com/general-knowledge/ipl-2027-trade-list-hardik-pandya-arshdeep-singh-1820013788-1"
SOURCE_TITLE = "IPL 2027 Trade List: Hardik Pandya, Arshdeep Singh and more"
PUBLISHER = "Jagran Josh / BCCI IPL Trade Window"
VERIFICATION_TS = "2026-11-17 19:01:00"
PUB_DATE = "2026-11-17"
SNAPSHOT_LABEL = "audit_2026_11_17_trades"

TRADES = [
    {
        "player_id": 3330,
        "player_name": "Hardik Pandya",
        "previous_franchise": "Mumbai Indians",
        "current_verified_franchise": "Punjab Kings",
        "fee": "₹18 crore",
    },
    {
        "player_id": 6464,
        "player_name": "Arshdeep Singh",
        "previous_franchise": "Punjab Kings",
        "current_verified_franchise": "Mumbai Indians",
        "fee": "₹18 crore",
    },
    {
        "player_id": 4703,
        "player_name": "Rishabh Pant",
        "previous_franchise": "Lucknow Super Giants",
        "current_verified_franchise": "Delhi Capitals",
        "fee": "₹15 crore",
    },
    {
        "player_id": 3644,
        "player_name": "Kuldeep Yadav",
        "previous_franchise": "Delhi Capitals",
        "current_verified_franchise": "Lucknow Super Giants",
        "fee": "₹13.50 crore",
    },
    {
        "player_id": 4265,
        "player_name": "T Natarajan",
        "previous_franchise": "Delhi Capitals",
        "current_verified_franchise": "Sunrisers Hyderabad",
        "fee": "₹5 crore",
    },
    {
        "player_id": 4824,
        "player_name": "Zeeshan Ansari",
        "previous_franchise": "Sunrisers Hyderabad",
        "current_verified_franchise": "Delhi Capitals",
        "fee": "₹40 lakh",
    },
    {
        "player_id": 4391,
        "player_name": "Liam Livingstone",
        "previous_franchise": "Sunrisers Hyderabad",
        "current_verified_franchise": "Chennai Super Kings",
        "fee": "₹6 crore",
    },
    {
        "player_id": 6166,
        "player_name": "Jack Edwards",
        "previous_franchise": "Sunrisers Hyderabad",
        "current_verified_franchise": "Chennai Super Kings",
        "fee": "₹3 crore",
    },
    {
        "player_id": 4816,
        "player_name": "Khaleel Ahmed",
        "previous_franchise": "Chennai Super Kings",
        "current_verified_franchise": "Sunrisers Hyderabad",
        "fee": "₹4.80 crore",
    },
    {
        "player_id": 7920,
        "player_name": "Nathan Ellis",
        "previous_franchise": "Chennai Super Kings",
        "current_verified_franchise": "Sunrisers Hyderabad",
        "fee": "₹2 crore",
    },
    {
        "player_id": 2261,
        "player_name": "Harshal Patel",
        "previous_franchise": "Punjab Kings",
        "current_verified_franchise": "Gujarat Titans",
        "fee": "₹4 crore",
        "source_url": "https://www.mykhel.com/cricket/ipl-2027-trade-window-full-list-of-traded-players-ahead-of-retention-deadline-329841.html",
        "source_title": "IPL 2027 Trade Window: Full list of traded players ahead of retention deadline",
        "publisher": "MyKhel / BCCI IPL Trade Window",
        "evidence_excerpt": "Confirmed IPL 2027 trade: Harshal Patel traded from Punjab Kings to Gujarat Titans in all-cash deal for ₹4 crore.",
        "conflicting_evidence": "None. Contracted to Gujarat Titans for IPL 2027 (not available in open auction).",
    },
    {
        "player_id": 1566,
        "player_name": "Mohammed Shami",
        "previous_franchise": "Lucknow Super Giants",
        "current_verified_franchise": "Rajasthan Royals",
        "fee": "₹8 crore",
        "evidence_excerpt": "Confirmed IPL 2027 trade: Mohammed Shami traded from Lucknow Super Giants to Rajasthan Royals for fee of ₹8 crore.",
        "conflicting_evidence": "None. Contracted to Rajasthan Royals for IPL 2027 (inflow to RR squad, not in open auction).",
    },
    {
        "player_id": 6237,
        "player_name": "Manimaran Siddharth",
        "previous_franchise": "Lucknow Super Giants",
        "current_verified_franchise": "Rajasthan Royals",
        "fee": "₹75 lakh",
        "evidence_excerpt": "Confirmed IPL 2027 trade: Manimaran Siddharth traded from Lucknow Super Giants to Rajasthan Royals for fee of ₹75 lakh.",
        "conflicting_evidence": "None. Contracted to Rajasthan Royals for IPL 2027 (inflow to RR squad, not in open auction).",
    },
    {
        "player_id": 4409,
        "player_name": "Sam Curran",
        "previous_franchise": "Rajasthan Royals",
        "current_verified_franchise": "Lucknow Super Giants",
        "fee": "₹2.40 crore",
        "evidence_excerpt": "Confirmed IPL 2027 trade: Sam Curran traded from Rajasthan Royals to Lucknow Super Giants for fee of ₹2.40 crore.",
        "conflicting_evidence": "None. Contracted to Lucknow Super Giants for IPL 2027 (outflow from RR squad, not in open auction).",
    },
]


def main():
    template_path = Path("data/processed/ipl_2027_player_market_template.csv")
    changelog_path = Path("data/processed/ipl_2027_market_change_log.csv")
    snap_dir = Path("data/processed/snapshots")
    snap_dir.mkdir(parents=True, exist_ok=True)

    # 1. Preserve backup snapshot before modification
    if template_path.exists():
        snap_backup = snap_dir / f"ipl_2027_market_snapshot_20261117_pre_v65_trades.csv"
        shutil.copy2(template_path, snap_backup)
        print(f"Preserved historical snapshot to: {snap_backup}")

    df_template = pd.read_csv(template_path) if template_path.exists() else pd.DataFrame()
    df_changelog = pd.read_csv(changelog_path) if changelog_path.exists() else pd.DataFrame()

    existing_pids = set(df_template["player_id"]) if not df_template.empty else set()
    changelog_rows = []

    for t in TRADES:
        pid = t["player_id"]
        pname = t["player_name"]
        prev = t["previous_franchise"]
        curr = t["current_verified_franchise"]
        fee = t["fee"]
        s_url = t.get("source_url", SOURCE_URL)
        s_title = t.get("source_title", SOURCE_TITLE)
        s_pub = t.get("publisher", PUBLISHER)
        excerpt = t.get("evidence_excerpt", f"Confirmed IPL 2027 trade: {pname} traded from {prev} to {curr} for fee of {fee}.")
        conf_ev = t.get("conflicting_evidence", f"None. Contracted to {curr} for IPL 2027 (not available in open auction).")

        row_data = {
            "player_id": pid,
            "player_name": pname,
            "previous_franchise": prev,
            "current_verified_franchise": curr,
            "official_retention_status": "Confirmed Trade",
            "official_release_status": "Not Applicable (Trade)",
            "confirmed_trade_status": "Confirmed Trade",
            "transaction_mechanism": f"IPL 2027 pre-retention trade ({prev} -> {curr}, Fee: {fee})",
            "rumour_status": f"None — Officially confirmed pre-2027 trade ({fee})",
            "source_url": s_url,
            "source_title": s_title,
            "publisher": s_pub,
            "source_publication_date": PUB_DATE,
            "verification_timestamp": VERIFICATION_TS,
            "confidence_classification": "Officially Confirmed (Pre-2027 Trade)",
            "evidence_excerpt": excerpt,
            "conflicting_evidence": conf_ev,
            "snapshot_label": SNAPSHOT_LABEL,
            "last_updated": PUB_DATE,
        }

        if pid in existing_pids:
            # Update existing row
            idx = df_template[df_template["player_id"] == pid].index[0]
            old_status = df_template.loc[idx, "official_retention_status"]
            old_team = df_template.loc[idx, "current_verified_franchise"]
            for k, v in row_data.items():
                df_template.loc[idx, k] = v
            print(f"Updated existing player {pname} (ID {pid}): [{old_team} | {old_status}] -> [{curr} | Confirmed Trade]")
        else:
            # Append new row
            df_template = pd.concat([df_template, pd.DataFrame([row_data])], ignore_index=True)
            print(f"Added new traded player {pname} (ID {pid}): {prev} -> {curr} ({fee})")

        # Append to changelog if not already logged
        cl_entry = {
            "timestamp": VERIFICATION_TS,
            "player_id": pid,
            "player_name": pname,
            "event_type": "TRADE_CONFIRMED",
            "previous_status": f"{prev} Roster",
            "new_status": f"{curr} Roster (Confirmed Trade - {fee})",
            "verified_by": s_pub,
            "source_url": s_url,
            "notes": f"Confirmed IPL 2027 trade: {pname} from {prev} to {curr} for {fee}.",
        }
        changelog_rows.append(cl_entry)

    # Save updated template
    df_template.to_csv(template_path, index=False)
    print(f"Saved updated market template ({len(df_template)} players) to {template_path}")

    # Save updated changelog
    if not df_changelog.empty:
        # Check for duplicate events
        new_cl_df = pd.DataFrame(changelog_rows)
        # Avoid duplicating same timestamp + player_id
        merged_cl = pd.concat([df_changelog, new_cl_df], ignore_index=True).drop_duplicates(subset=["timestamp", "player_id", "event_type"])
    else:
        merged_cl = pd.DataFrame(changelog_rows)

    merged_cl.to_csv(changelog_path, index=False)
    print(f"Saved updated changelog ({len(merged_cl)} audit records) to {changelog_path}")


if __name__ == "__main__":
    main()
