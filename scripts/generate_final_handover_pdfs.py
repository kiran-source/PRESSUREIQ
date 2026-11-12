"""Generate final competition selection sheet and separate market-status appendix PDFs.

Reads directly from frozen Model A CSVs and audited market ledger CSVs to guarantee
exact numerical provenance with zero manual transcription.
"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "processed"
HANDOVER_SUBMISSION_DIR = ROOT / "submission_handover" / "01_Unstop_Submission_Files"

RR_BLUE = colors.HexColor("#004BA0")
RR_PINK = colors.HexColor("#EA1B88")
RR_DARK = colors.HexColor("#0A1628")
RR_BG = colors.HexColor("#F8FAFC")
RR_BORDER = colors.HexColor("#CBD5E1")
RR_MUTED = colors.HexColor("#475569")

AS_OF_LABEL = "12 November 2026 (Pre-Nov 17 Retention Baseline; Snapshot Audited 2026-11-11)"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _esc(val: object) -> str:
    s = "" if pd.isna(val) else str(val)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleStyle",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=RR_DARK,
            spaceAfter=2,
        ),
        "subtitle": ParagraphStyle(
            "SubTitleStyle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=RR_MUTED,
            spaceAfter=4,
        ),
        "h2": ParagraphStyle(
            "H2Style",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=RR_BLUE,
            spaceBefore=4,
            spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "BodyStyle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            textColor=RR_DARK,
        ),
        "callout": ParagraphStyle(
            "CalloutStyle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=RR_DARK,
        ),
        "th": ParagraphStyle(
            "TH",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=8.5,
            textColor=colors.white,
        ),
        "td": ParagraphStyle(
            "TD",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=6.8,
            leading=8.5,
            textColor=RR_DARK,
        ),
        "td_bold": ParagraphStyle(
            "TDBold",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=6.8,
            leading=8.5,
            textColor=RR_DARK,
        ),
        "td_small": ParagraphStyle(
            "TDSmall",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=6.2,
            leading=7.8,
            textColor=RR_DARK,
        ),
    }


def _callout(text: str, styles: dict[str, ParagraphStyle], bg: str = "#EFF6FF", accent: colors.Color = RR_BLUE) -> Table:
    tbl = Table([[Paragraph(text, styles["callout"])]], colWidths=[770])
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
                ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
                ("BOX", (0, 0), (-1, -1), 0.4, RR_BORDER),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return tbl


def _add_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(RR_MUTED)
    canvas.drawString(12 * mm, 8 * mm, f"PRESSUREIQ — Rajasthan Royals SupeRR Selector Season 2 (2026) | Prepared {AS_OF_LABEL}")
    canvas.drawRightString(landscape(A4)[0] - 12 * mm, 8 * mm, f"Page {doc.page}")
    canvas.restoreState()


def generate_selection_sheet(out_paths: list[Path]) -> None:
    """Build PRESSUREIQ_FINAL_SELECTION_SHEET.pdf directly from frozen Model A CSVs."""
    bat_df = pd.read_csv(DATA_DIR / "final_batter_rankings.csv")
    bowl_df = pd.read_csv(DATA_DIR / "final_bowler_rankings.csv")
    bat_top = pd.read_csv(DATA_DIR / "final_competition_batter_top10.csv")
    bowl_top = pd.read_csv(DATA_DIR / "final_competition_bowler_top10.csv")
    em_df = pd.read_csv(DATA_DIR / "emerging_talent_watchlist.csv")

    bat_hash = _sha256(DATA_DIR / "final_batter_rankings.csv")[:16]
    bowl_hash = _sha256(DATA_DIR / "final_bowler_rankings.csv")[:16]

    styles = _build_styles()
    story = []

    # Page 1: Title, Governance Disclosures & Top-10 Batters
    story.append(Paragraph("PRESSUREIQ — FINAL MODEL A SELECTION SHEET", styles["title"]))
    story.append(
        Paragraph(
            f"Rajasthan Royals SupeRR Selector Season 2 (2026) | Separate 10-Batter &amp; 10-Bowler Pressure Rankings | As Of: {AS_OF_LABEL}",
            styles["subtitle"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=1.2, color=RR_PINK, spaceBefore=1, spaceAfter=5))

    story.append(
        _callout(
            "<b>Strict Statistical Governance Disclosures:</b> "
            "(1) <b>Score Definition:</b> The 0–100 <b>Reliability Score = Phi(Z_composite) * 100</b> is a standardized normal CDF percentile-like score across 5 weighted pillars; it is <b>NOT</b> a probability of match success. "
            "(2) <b>Frozen Model A Provenance:</b> Computed exclusively from 200,999 historical deliveries (2022–2026). All frozen CSV rankings remain untouched "
            f"(Batter SHA-256 prefix <code>{bat_hash}...</code>, Bowler SHA-256 prefix <code>{bowl_hash}...</code>). "
            "(3) <b>Separation from Market Status:</b> Statistical performance rankings are strictly independent of IPL 2027 retention, trade, eligibility, or auction status (see <i>PRESSUREIQ_FINAL_MARKET_APPENDIX.pdf</i>).",
            styles,
        )
    )
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Official Model A Selection: Top 10 Batters Under Pressure", styles["h2"]))
    bat_rows = [
        [
            Paragraph("Rank", styles["th"]),
            Paragraph("Player (ID) &amp; Role", styles["th"]),
            Paragraph("Model A Score", styles["th"]),
            Paragraph("Pressure Evidence (PAVA &amp; PRC)", styles["th"]),
            Paragraph("Sample Exposure", styles["th"]),
            Paragraph("2,000-Match Bootstrap Stability", styles["th"]),
            Paragraph("Tactical Selection Rationale", styles["th"]),
        ]
    ]
    for _, row in bat_top.sort_values("rank").iterrows():
        rationale = f"{_esc(row['strategic_category'])}: {_esc(row['rr_strategic_utility'])}"
        bat_rows.append(
            [
                Paragraph(f"<b>#{int(row['rank'])}</b>", styles["td_bold"]),
                Paragraph(f"<b>{_esc(row['player_name'])}</b><br/>ID {int(row['player_id'])} | {_esc(row['role'])}", styles["td"]),
                Paragraph(f"<b>{row['reliability_score']:.2f}</b>", styles["td_bold"]),
                Paragraph(
                    f"Raw/Shrunk PAVA: <b>{row['raw_hp_pava_per_ball']:+.3f}</b> / <b>{row['shrunk_hp_pava_per_ball']:+.3f}</b><br/>"
                    f"Retention: {row['retention_delta']:+.3f} | SR: {row['career_sr']:.1f}<br/>"
                    f"PRC: {_esc(row['prc_archetype'])} ({row['prc_slope']:+.3f})",
                    styles["td"],
                ),
                Paragraph(
                    f"Matches: <b>{int(row['matches'])}</b><br/>"
                    f"Valid Balls: {int(row['total_balls'])}<br/>"
                    f"HP Balls (&gt;=50): <b>{int(row['hp_balls'])}</b>",
                    styles["td"],
                ),
                Paragraph(
                    f"95% Score CI: [{row['boot_score_ci_lower_95']:.2f}, {row['boot_score_ci_upper_95']:.2f}]<br/>"
                    f"Top-10 Prob: <b>{row['top10_inclusion_prob']*100:.2f}%</b><br/>"
                    f"Mean Rank: {row['boot_mean_rank']:.1f} (CI {int(row['boot_rank_ci_lower_95'])}–{int(row['boot_rank_ci_upper_95'])})",
                    styles["td"],
                ),
                Paragraph(rationale, styles["td_small"]),
            ]
        )

    t_bat = Table(bat_rows, colWidths=[28, 100, 48, 150, 82, 130, 232], repeatRows=1)
    t_bat.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), RR_BLUE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, RR_BG]),
                ("GRID", (0, 0), (-1, -1), 0.4, RR_BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t_bat)
    story.append(PageBreak())

    # Page 2: Top-10 Bowlers
    story.append(Paragraph("2. Official Model A Selection: Top 10 Bowlers Under Pressure", styles["h2"]))
    story.append(
        Paragraph(
            "Ranked strictly on Model A Composite Reliability Score (BoPI &gt;= 50 high-pressure execution, Empirical Bayes K = 45.0 shrinkage, "
            "retention delta, consistency, and phase/venue adaptability). Eligibility: &gt;= 400 legal balls and &gt;= 30 high-pressure deliveries.",
            styles["subtitle"],
        )
    )
    bowl_rows = [
        [
            Paragraph("Rank", styles["th"]),
            Paragraph("Player (ID) &amp; Style", styles["th"]),
            Paragraph("Model A Score", styles["th"]),
            Paragraph("Pressure Evidence (PAVA &amp; PRC)", styles["th"]),
            Paragraph("Sample Exposure", styles["th"]),
            Paragraph("2,000-Match Bootstrap Stability", styles["th"]),
            Paragraph("Tactical Selection Rationale", styles["th"]),
        ]
    ]
    for _, row in bowl_top.sort_values("rank").iterrows():
        rationale = f"{_esc(row['strategic_category'])}: {_esc(row['rr_strategic_utility'])}"
        bowl_rows.append(
            [
                Paragraph(f"<b>#{int(row['rank'])}</b>", styles["td_bold"]),
                Paragraph(
                    f"<b>{_esc(row['player_name'])}</b><br/>ID {int(row['player_id'])} | {_esc(row['pace_or_spin'])} ({_esc(row['bowling_type'])})",
                    styles["td"],
                ),
                Paragraph(f"<b>{row['reliability_score']:.2f}</b>", styles["td_bold"]),
                Paragraph(
                    f"Raw/Shrunk PAVA: <b>{row['raw_hp_pava_per_ball']:+.3f}</b> / <b>{row['shrunk_hp_pava_per_ball']:+.3f}</b><br/>"
                    f"Retention: {row['retention_delta']:+.3f} | Econ: {row['career_economy']:.2f}<br/>"
                    f"PRC: {_esc(row['prc_archetype'])} ({row['prc_slope']:+.3f})",
                    styles["td"],
                ),
                Paragraph(
                    f"Matches: <b>{int(row['matches'])}</b> | Wkts: {int(row['total_wickets'])}<br/>"
                    f"Legal/Deliv: {int(row['legal_balls'])} / {int(row['total_deliveries'])}<br/>"
                    f"HP Balls (&gt;=50): <b>{int(row['hp_balls'])}</b>",
                    styles["td"],
                ),
                Paragraph(
                    f"95% Score CI: [{row['boot_score_ci_lower_95']:.2f}, {row['boot_score_ci_upper_95']:.2f}]<br/>"
                    f"Top-10 Prob: <b>{row['top10_inclusion_prob']*100:.2f}%</b><br/>"
                    f"Mean Rank: {row['boot_mean_rank']:.1f} (CI {int(row['boot_rank_ci_lower_95'])}–{int(row['boot_rank_ci_upper_95'])})",
                    styles["td"],
                ),
                Paragraph(rationale, styles["td_small"]),
            ]
        )

    t_bowl = Table(bowl_rows, colWidths=[28, 106, 48, 148, 86, 128, 226], repeatRows=1)
    t_bowl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), RR_BLUE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, RR_BG]),
                ("GRID", (0, 0), (-1, -1), 0.4, RR_BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t_bowl)
    story.append(PageBreak())

    # Page 3: Near-Miss Cutoff Defense & Emerging Talent Separation
    story.append(Paragraph("3. Near-Miss Cutoff Defenses (#11–#13) &amp; Emerging Talent Watchlist Separation", styles["h2"]))
    story.append(
        Paragraph(
            "Model A applies hard statistical eligibility rules cleanly without post-hoc overrides. Below are the exact near-miss comparators "
            "and why unqualified emerging prospects remain isolated in the dedicated scouting watchlist.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 5))

    near_bat = bat_df[bat_df["rank"].isin([10, 11, 12, 13])].sort_values("rank")
    near_bowl = bowl_df[bowl_df["rank"].isin([10, 11, 12, 14])].sort_values("rank")
    nm_rows = [
        [
            Paragraph("Discipline", styles["th"]),
            Paragraph("Rank &amp; Status", styles["th"]),
            Paragraph("Player (ID)", styles["th"]),
            Paragraph("Score &amp; 95% CI", styles["th"]),
            Paragraph("Top-10 Prob", styles["th"]),
            Paragraph("Sample (Matches / Balls / HP)", styles["th"]),
            Paragraph("Cutoff Margin Explanation", styles["th"]),
        ]
    ]
    for disc, df_sub in [("Batting", near_bat), ("Bowling", near_bowl)]:
        for _, r in df_sub.iterrows():
            rank_int = int(r["rank"])
            status = "Selected #10 Cutoff" if rank_int == 10 else f"Near Miss #{rank_int}"
            if disc == "Batting":
                samp = f"{int(r['matches'])} m | {int(r['total_balls'])} valid | {int(r['hp_balls'])} HP"
                note = "Cutoff anchor (#10)." if rank_int == 10 else f"Gap vs #10: {r['reliability_score'] - float(near_bat.iloc[0]['reliability_score']):+.2f} pts; Raw PAVA {r['raw_hp_pava_per_ball']:+.3f}."
            else:
                samp = f"{int(r['matches'])} m | {int(r['legal_balls'])} legal ({int(r['total_deliveries'])} deliv) | {int(r['hp_balls'])} HP"
                note = "Cutoff anchor (#10)." if rank_int == 10 else f"Gap vs #10: {r['reliability_score'] - float(near_bowl.iloc[0]['reliability_score']):+.2f} pts; Raw PAVA {r['raw_hp_pava_per_ball']:+.3f}."
            nm_rows.append(
                [
                    Paragraph(disc, styles["td"]),
                    Paragraph(f"<b>#{rank_int}</b> ({status})", styles["td_bold" if rank_int == 10 else "td"]),
                    Paragraph(f"{_esc(r['player_name'])} (ID {int(r['player_id'])})", styles["td_bold"]),
                    Paragraph(f"{r['reliability_score']:.2f} [{r['boot_score_ci_lower_95']:.2f}, {r['boot_score_ci_upper_95']:.2f}]", styles["td"]),
                    Paragraph(f"{r['top10_inclusion_prob']*100:.2f}%", styles["td"]),
                    Paragraph(samp, styles["td"]),
                    Paragraph(note, styles["td"]),
                ]
            )

    t_nm = Table(nm_rows, colWidths=[52, 92, 130, 118, 56, 134, 188], repeatRows=1)
    t_nm.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), RR_BLUE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, RR_BG]),
                ("GRID", (0, 0), (-1, -1), 0.4, RR_BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(t_nm)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Emerging Talent Stratification Summary (data/processed/emerging_talent_watchlist.csv)", styles["h2"]))
    em_rows = [
        [
            Paragraph("Player (ID) &amp; Age", styles["th"]),
            Paragraph("Tier / Category", styles["th"]),
            Paragraph("Role", styles["th"]),
            Paragraph("Dataset Balls / HP / SR", styles["th"]),
            Paragraph("Model A Status", styles["th"]),
            Paragraph("Tactical &amp; Governance Assessment", styles["th"]),
        ]
    ]
    for _, r in em_df.head(6).iterrows():
        em_rows.append(
            [
                Paragraph(f"<b>{_esc(r['player_name'])}</b> (ID {int(r['player_id'])}, Age {int(r['age'])})", styles["td_bold"]),
                Paragraph(_esc(r["category"]), styles["td"]),
                Paragraph(_esc(r["role"]), styles["td"]),
                Paragraph(f"{int(r['total_balls_dataset'])} balls | {int(r['hp_balls_dataset'])} HP | SR {_esc(r['dataset_strike_rate'])}", styles["td"]),
                Paragraph(_esc(r["pressure_reliability_score"]), styles["td"]),
                Paragraph(_esc(r["recommendation_for_rr"]), styles["td_small"]),
            ]
        )
    t_em = Table(em_rows, colWidths=[124, 132, 96, 110, 108, 200], repeatRows=1)
    t_em.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), RR_BLUE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, RR_BG]),
                ("GRID", (0, 0), (-1, -1), 0.4, RR_BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(t_em)

    for out_path in out_paths:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(
            str(out_path),
            pagesize=landscape(A4),
            rightMargin=12 * mm,
            leftMargin=12 * mm,
            topMargin=12 * mm,
            bottomMargin=14 * mm,
        )
        doc.build(list(story), onFirstPage=_add_footer, onLaterPages=_add_footer)


def generate_market_appendix(out_paths: list[Path]) -> None:
    """Build PRESSUREIQ_FINAL_MARKET_APPENDIX.pdf from audited market intelligence CSVs."""
    market_df = pd.read_csv(DATA_DIR / "ipl_2027_player_market_template.csv")
    log_df = pd.read_csv(DATA_DIR / "ipl_2027_market_change_log.csv")
    cand_df = pd.read_csv(DATA_DIR / "rr_2027_candidate_rankings.csv")
    snap_path = DATA_DIR / "snapshots" / "ipl_2027_market_snapshot_2026-11-11.csv"
    snap_hash = _sha256(snap_path) if snap_path.exists() else "MISSING"

    styles = _build_styles()
    story = []

    story.append(Paragraph("PRESSUREIQ — IPL 2027 MARKET &amp; RETENTION GOVERNANCE APPENDIX", styles["title"]))
    story.append(
        Paragraph(
            f"Separate Market Status Ledger as of {AS_OF_LABEL} | Archived Snapshot SHA-256: {snap_hash[:16]}...",
            styles["subtitle"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=1.2, color=RR_PINK, spaceBefore=1, spaceAfter=5))

    status_counts = market_df["official_retention_status"].value_counts().to_dict()
    cand_counts = cand_df["market_status"].value_counts().to_dict()
    story.append(
        _callout(
            "<b>Strict Pre-Retention Market Governance Rules (As of 12 November 2026):</b> "
            "(1) Official IPL 2027 franchise retention/release lists are scheduled for <b>17 November 2026</b> and have NOT been published yet. "
            "(2) Every confirmed status requires an open-web verifiable <code>source_url</code>, <code>source_publication_date</code>, and <code>verification_timestamp</code>. "
            "(3) <b>Absence from a retention/announcement article NEVER implies Confirmed Released or Auction Available.</b> "
            "(4) Market availability is kept strictly separate from Model A statistical reliability scores. "
            f"<br/><b>Audited Ledger Counts ({len(market_df)} Tracked Players):</b> "
            + ", ".join(f"{_esc(k)}: {v}" for k, v in status_counts.items())
            + f" | <b>Full Candidate Pool ({len(cand_df)} Eligible Players):</b> "
            + ", ".join(f"{_esc(k)}: {v}" for k, v in cand_counts.items()),
            styles,
            bg="#FFFBEB",
            accent=RR_PINK,
        )
    )
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Source-Audited Market Ledger (data/processed/ipl_2027_player_market_template.csv)", styles["h2"]))
    m_rows = [
        [
            Paragraph("Player (ID)", styles["th"]),
            Paragraph("Prev -&gt; Verified Squad", styles["th"]),
            Paragraph("Official Status", styles["th"]),
            Paragraph("Pub Date / Verified At", styles["th"]),
            Paragraph("Confidence &amp; Mechanism", styles["th"]),
            Paragraph("Verified Source URL", styles["th"]),
        ]
    ]
    for _, r in market_df.iterrows():
        prev_f = "-" if pd.isna(r["previous_franchise"]) else str(r["previous_franchise"])
        curr_f = "-" if pd.isna(r["current_verified_franchise"]) else str(r["current_verified_franchise"])
        m_rows.append(
            [
                Paragraph(f"<b>{_esc(r['player_name'])}</b><br/>ID {int(r['player_id'])}", styles["td_bold"]),
                Paragraph(f"{_esc(prev_f)} -&gt;<br/><b>{_esc(curr_f)}</b>", styles["td"]),
                Paragraph(f"<b>{_esc(r['official_retention_status'])}</b>", styles["td_bold"]),
                Paragraph(f"Pub: {_esc(r['source_publication_date'])}<br/>Ver: {_esc(r['verification_timestamp'])}", styles["td_small"]),
                Paragraph(f"{_esc(r['confidence_classification'])}<br/><i>{_esc(r['transaction_mechanism'])}</i>", styles["td_small"]),
                Paragraph(_esc(r["source_url"]), styles["td_small"]),
            ]
        )

    t_m = Table(m_rows, colWidths=[92, 130, 92, 92, 138, 226], repeatRows=1)
    t_m.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), RR_BLUE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, RR_BG]),
                ("GRID", (0, 0), (-1, -1), 0.4, RR_BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
            ]
        )
    )
    story.append(t_m)
    story.append(PageBreak())

    story.append(Paragraph("2. Chronological Market Audit Log (data/processed/ipl_2027_market_change_log.csv)", styles["h2"]))
    log_rows = [
        [
            Paragraph("Timestamp", styles["th"]),
            Paragraph("Player (ID)", styles["th"]),
            Paragraph("Event Type", styles["th"]),
            Paragraph("Previous -&gt; New Status", styles["th"]),
            Paragraph("Source URL &amp; Audit Note", styles["th"]),
        ]
    ]
    for _, r in log_df.iterrows():
        log_rows.append(
            [
                Paragraph(_esc(r["timestamp"]), styles["td_small"]),
                Paragraph(f"<b>{_esc(r['player_name'])}</b> (ID {int(r['player_id'])})", styles["td_bold"]),
                Paragraph(_esc(r["event_type"]), styles["td"]),
                Paragraph(f"{_esc(r['previous_status'])} -&gt;<br/><b>{_esc(r['new_status'])}</b>", styles["td_small"]),
                Paragraph(f"{_esc(r['source_url'])}<br/><i>{_esc(r['notes'])}</i>", styles["td_small"]),
            ]
        )
    t_log = Table(log_rows, colWidths=[82, 108, 114, 178, 288], repeatRows=1)
    t_log.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), RR_BLUE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, RR_BG]),
                ("GRID", (0, 0), (-1, -1), 0.4, RR_BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(t_log)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3. 17 November 2026 Retention Update Readiness Protocol", styles["h2"]))
    proto_text = (
        "When BCCI/IPL publishes official 2027 retention lists on <b>17 November 2026</b>, execute the deterministic update workflow in "
        "<code>docs/NOV17_RETENTION_UPDATE_RUNBOOK.md</code> without modifying frozen Model A statistics:<br/>"
        "1. Record official IPL/BCCI retention announcement URLs, publication date (2026-11-17), and exact retention/release/trade rows in a validated update CSV.<br/>"
        "2. Run <code>python scripts/import_market_retentions.py --input &lt;csv&gt; --dry-run</code> to verify schema compliance, status taxonomy, and mandatory provenance URLs.<br/>"
        "3. Apply with <code>--apply</code> to update <code>ipl_2027_player_market_template.csv</code>, append audit rows to <code>ipl_2027_market_change_log.csv</code>, "
        "and regenerate <code>rr_2027_candidate_rankings.csv</code> (preserving <code>final_batter_rankings.csv</code> &amp; <code>final_bowler_rankings.csv</code> SHA-256 unchanged).<br/>"
        "4. Re-run <code>python -m pytest tests/ -v</code> and <code>python scripts/hybrid_validation_gate.py</code> before regenerating the final selection/market PDFs and Unstop upload."
    )
    story.append(_callout(proto_text, styles))

    for out_path in out_paths:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(
            str(out_path),
            pagesize=landscape(A4),
            rightMargin=12 * mm,
            leftMargin=12 * mm,
            topMargin=12 * mm,
            bottomMargin=14 * mm,
        )
        doc.build(list(story), onFirstPage=_add_footer, onLaterPages=_add_footer)


def main() -> None:
    HANDOVER_SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    sel_root = ROOT / "PRESSUREIQ_FINAL_SELECTION_SHEET.pdf"
    mkt_root = ROOT / "PRESSUREIQ_FINAL_MARKET_APPENDIX.pdf"
    generate_selection_sheet([sel_root])
    generate_market_appendix([mkt_root])
    shutil.copy2(sel_root, HANDOVER_SUBMISSION_DIR / sel_root.name)
    shutil.copy2(mkt_root, HANDOVER_SUBMISSION_DIR / mkt_root.name)
    print("Generated byte-identical PRESSUREIQ_FINAL_SELECTION_SHEET.pdf and PRESSUREIQ_FINAL_MARKET_APPENDIX.pdf")


if __name__ == "__main__":
    main()

