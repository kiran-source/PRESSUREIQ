"""Generate official Rajasthan Royals Recruitment Intelligence PDF report for IPL 2027."""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
PDF_PATH = PROCESSED_DIR / "RR_IPL_2027_RECRUITMENT_INTELLIGENCE.pdf"


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page numbers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#282321"))
        
        # Suppress header on cover page
        if self._pageNumber > 1:
            self.drawString(54, 750, "PRESSUREIQ v6.0 — Rajasthan Royals Recruitment Intelligence | IPL 2027")
            self.setStrokeColor(colors.HexColor("#BD6548"))
            self.setLineWidth(0.75)
            self.line(54, 744, 558, 744)

        # Footer on all pages
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#77675D"))
        self.drawString(54, 36, "CONFIDENTIAL — RAJASTHAN ROYALS AUCTION DECISION SUPPORT")
        self.drawRightString(558, 36, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#D8CBBE"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()


def build_pdf():
    print(f"Generating {PDF_PATH}...")
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Brand Colors
    c_ink = colors.HexColor("#282321")
    c_terra = colors.HexColor("#BD6548")
    c_cream = colors.HexColor("#F8F4EC")
    c_gold = colors.HexColor("#C5A46D")
    c_muted = colors.HexColor("#77675D")
    c_border = colors.HexColor("#D8CBBE")

    title_style = ParagraphStyle(
        "CoverTitle", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=24, leading=28,
        textColor=c_ink, spaceAfter=8
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle", parent=styles["Normal"],
        fontName="Helvetica", fontSize=11, leading=15,
        textColor=c_terra, spaceAfter=16
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=13, leading=16,
        textColor=c_ink, spaceBefore=14, spaceAfter=6
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=10, leading=13,
        textColor=c_terra, spaceBefore=8, spaceAfter=4
    )
    body_style = ParagraphStyle(
        "Body_Custom", parent=styles["Normal"],
        fontName="Helvetica", fontSize=8.5, leading=11.5,
        textColor=c_ink, spaceAfter=5
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer_Custom", parent=styles["Normal"],
        fontName="Helvetica-Oblique", fontSize=8, leading=11,
        textColor=colors.HexColor("#822F19")
    )
    table_cell = ParagraphStyle(
        "TableCell", parent=styles["Normal"],
        fontName="Helvetica", fontSize=7.5, leading=9.5,
        textColor=c_ink
    )
    table_cell_bold = ParagraphStyle(
        "TableCellBold", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=7.5, leading=9.5,
        textColor=c_ink
    )

    elements = []

    # 1. Header & Title Block
    elements.append(Paragraph("PRESSUREIQ v6.0 &bull; STRATEGIC FRANCHISE SCOUTING", subtitle_style))
    elements.append(Paragraph("Rajasthan Royals IPL 2027 Recruitment Intelligence", title_style))
    elements.append(Paragraph(
        "An evidence-driven, decision-support platform answering the 7 core scouting questions: "
        "pressure reliability, regulatory eligibility, contractual auction availability, squad fit, "
        "downside risk, and contingency alternatives ahead of the IPL 2027 Player Auction.",
        body_style
    ))
    elements.append(Spacer(1, 10))

    # Mandatory Disclaimer Box
    disclaimer_text = (
        "<b>MANDATORY ANALYTICAL DISCLAIMER:</b> "
        "PRESSUREIQ provides an independent analytical recruitment assessment. It does not represent an official "
        "Rajasthan Royals recruitment decision or guarantee player eligibility, auction availability, selection, "
        "or future performance."
    )
    disclaimer_table = Table(
        [[Paragraph(disclaimer_text, disclaimer_style)]],
        colWidths=[504]
    )
    disclaimer_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FDF8F5")),
        ("BORDER", (0, 0), (-1, -1), 1, c_terra),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(disclaimer_table)
    elements.append(Spacer(1, 14))

    # 2. Dual-Model Architecture & 6-Component Scoring
    elements.append(Paragraph("1. Dual-Model Architecture & Recruitment Scoring Formulation", h1_style))
    elements.append(Paragraph(
        "Model A (Tournament Composure) remains strictly frozen and immutable across 109 batters and 147 bowlers. "
        "Model B (RR Recruitment Intelligence) applies multi-criteria decision analysis (MCDA) across six weighted dimensions:",
        body_style
    ))

    formula_table_data = [
        [Paragraph("<b>Component</b>", table_cell_bold), Paragraph("<b>Weight</b>", table_cell_bold), Paragraph("<b>Operationalization & Data Source</b>", table_cell_bold)],
        [Paragraph("Pressure Reliability", table_cell), Paragraph("<b>25%</b>", table_cell), Paragraph("Preserved Model A Reliability Score (Phi(Z) * 100), shrunk HP PAVA & PRC slope.", table_cell)],
        [Paragraph("Overall T20 Performance", table_cell), Paragraph("<b>20%</b>", table_cell), Paragraph("Career Strike Rate, Batting Average, Economy & Dot Ball % across 200,999 balls.", table_cell)],
        [Paragraph("Predictive ML Performance", table_cell), Paragraph("<b>15%</b>", table_cell), Paragraph("Chronological LightGBM holdout prediction under high pressure (2026 Test Set).", table_cell)],
        [Paragraph("Role Suitability", table_cell), Paragraph("<b>15%</b>", table_cell), Paragraph("Phase-specific situational execution (PP, Middle, Death) against positional benchmarks.", table_cell)],
        [Paragraph("RR Squad Fit", table_cell), Paragraph("<b>15%</b>", table_cell), Paragraph("Alignment with SMS Jaipur (78m boundaries) and RR's 4 core tactical deficits.", table_cell)],
        [Paragraph("Consistency & Risk", table_cell), Paragraph("<b>10%</b>", table_cell), Paragraph("Match-level CV, downside failure rate mitigation (100 * [1 - P(fail)]), and Kish ESS.", table_cell)],
    ]
    t_formula = Table(formula_table_data, colWidths=[120, 50, 334])
    t_formula.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1E9DD")),
        ("BORDER", (0, 0), (-1, -1), 0.5, c_border),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAF6F0")]),
    ]))
    elements.append(t_formula)
    elements.append(Spacer(1, 14))

    # 3. Tactical Gaps at SMS Jaipur
    elements.append(Paragraph("2. Rajasthan Royals Strategic Deficits Ahead of IPL 2027", h1_style))
    elements.append(Paragraph(
        "Sawai Mansingh Stadium (Jaipur) features massive 78m square boundaries. Roster analysis following the departure "
        "of Sanju Samson (CSK), Nathan Ellis (SRH), and Khaleel Ahmed (SRH), alongside arrivals of Jadeja and Curran, reveals 4 core gaps:",
        body_style
    ))

    gaps_data = [
        [Paragraph("<b>Deficit</b>", table_cell_bold), Paragraph("<b>Tactical Need & Context</b>", table_cell_bold), Paragraph("<b>Recommended Primary & Backup</b>", table_cell_bold)],
        [Paragraph("<b>1. Overseas Death Seamer</b>", table_cell), Paragraph("Overs 17–20 specialist partner for Sandeep Sharma; protect against Archer workload.", table_cell), Paragraph("<b>Spencer Johnson</b> (Primary, 145kph left-arm)<br/><i>Alt: Fazalhaq Farooqi (Afghanistan)</i>", table_cell)],
        [Paragraph("<b>2. Jaipur Spin Squeeze</b>", table_cell), Paragraph("Defensive finger-spin control exploiting 78m boundaries in middle overs (6.5–7.2 rpo).", table_cell), Paragraph("<b>Liam Dawson</b> (#1 Model A Bowler, 95.4 Rel)<br/><i>Alt: Allah Ghazanfar / Tanush Kotian</i>", table_cell)],
        [Paragraph("<b>3. No. 7 Pace Finisher</b>", table_cell), Paragraph("Ball-one boundary striker against 140kph+ bowling; lower-order death acceleration.", table_cell), Paragraph("<b>Jamie Smith</b> (Dynamic WK-Batter)<br/><i>Alt: Ashutosh Sharma (Domestic, 188 SR)</i>", table_cell)],
        [Paragraph("<b>4. Domestic Seam Depth</b>", table_cell), Paragraph("High-tempo Indian pacers with hard-length tennis bounce for pitch rotation.", table_cell), Paragraph("<b>Rasikh Salam</b> (Knuckle-ball death specialist)<br/><i>Alt: Prince Yadav / Vyshak Kumar</i>", table_cell)],
    ]
    t_gaps = Table(gaps_data, colWidths=[120, 204, 180])
    t_gaps.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1E9DD")),
        ("BORDER", (0, 0), (-1, -1), 0.5, c_border),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAF6F0")]),
    ]))
    elements.append(t_gaps)
    elements.append(Spacer(1, 14))

    # Page Break to Page 2
    elements.append(PageBreak())

    # 4. Top Target Recruitment Boards
    elements.append(Paragraph("3. Confirmed Rajasthan Royals Target Boards (Model B)", h1_style))
    elements.append(Paragraph(
        "Strictly excludes rival retained and confirmed traded players. Only verified eligible, open auction candidates appear here:",
        body_style
    ))

    # Batters Table
    elements.append(Paragraph("Top Actionable Target Batters", h2_style))
    bat_data = [
        [Paragraph("<b>Rank</b>", table_cell_bold), Paragraph("<b>Candidate</b>", table_cell_bold), Paragraph("<b>Origin</b>", table_cell_bold), Paragraph("<b>Role</b>", table_cell_bold), Paragraph("<b>Model B</b>", table_cell_bold), Paragraph("<b>Pressure Rel</b>", table_cell_bold), Paragraph("<b>Addressed RR Need</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("<b>Jamie Smith</b>", table_cell), Paragraph("England", table_cell), Paragraph("WK-Batter / Finisher", table_cell), Paragraph("91.2", table_cell_bold), Paragraph("82.5", table_cell), Paragraph("No. 7 Lower-Order Finisher / WK Depth", table_cell)],
        [Paragraph("2", table_cell), Paragraph("<b>Ashutosh Sharma</b>", table_cell), Paragraph("India", table_cell), Paragraph("Lower-Order Finisher", table_cell), Paragraph("92.1", table_cell_bold), Paragraph("84.0", table_cell), Paragraph("No. 7 Finisher (Frees Overseas Slot)", table_cell)],
        [Paragraph("3", table_cell), Paragraph("<b>Jacob Bethell</b>", table_cell), Paragraph("England", table_cell), Paragraph("Finisher / All-Rounder", table_cell), Paragraph("90.4", table_cell_bold), Paragraph("81.8", table_cell), Paragraph("Multi-Dimensional All-Round Depth", table_cell)],
        [Paragraph("4", table_cell), Paragraph("<b>Nehal Wadhera</b>", table_cell), Paragraph("India", table_cell), Paragraph("Middle-Order Anchor", table_cell), Paragraph("89.1", table_cell_bold), Paragraph("82.0", table_cell), Paragraph("Middle-Order Spin Stabilization", table_cell)],
        [Paragraph("5", table_cell), Paragraph("<b>Jason Holder</b>", table_cell), Paragraph("West Indies", table_cell), Paragraph("Pace All-Rounder", table_cell), Paragraph("88.7", table_cell_bold), Paragraph("91.3 (#13 A)", table_cell), Paragraph("Veteran Composure & Height", table_cell)],
    ]
    t_bat = Table(bat_data, colWidths=[24, 90, 50, 100, 45, 65, 130])
    t_bat.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1E9DD")),
        ("BORDER", (0, 0), (-1, -1), 0.5, c_border),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAF6F0")]),
    ]))
    elements.append(t_bat)
    elements.append(Spacer(1, 10))

    # Bowlers Table
    elements.append(Paragraph("Top Actionable Target Bowlers", h2_style))
    bowl_data = [
        [Paragraph("<b>Rank</b>", table_cell_bold), Paragraph("<b>Candidate</b>", table_cell_bold), Paragraph("<b>Origin</b>", table_cell_bold), Paragraph("<b>Discipline Style</b>", table_cell_bold), Paragraph("<b>Model B</b>", table_cell_bold), Paragraph("<b>Pressure Rel</b>", table_cell_bold), Paragraph("<b>Addressed RR Need</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("<b>Liam Dawson</b>", table_cell), Paragraph("England", table_cell), Paragraph("Left-Arm Orthodox", table_cell), Paragraph("93.8", table_cell_bold), Paragraph("95.4 (#1 A)", table_cell), Paragraph("SMS Jaipur Finger-Spin Squeeze", table_cell)],
        [Paragraph("2", table_cell), Paragraph("<b>Spencer Johnson</b>", table_cell), Paragraph("Australia", table_cell), Paragraph("Left-Arm Fast (145kph)", table_cell), Paragraph("92.4", table_cell_bold), Paragraph("83.2", table_cell), Paragraph("Overseas Death Seamer (Overs 17–20)", table_cell)],
        [Paragraph("3", table_cell), Paragraph("<b>Fazalhaq Farooqi</b>", table_cell), Paragraph("Afghanistan", table_cell), Paragraph("Left-Arm Medium-Fast", table_cell), Paragraph("91.6", table_cell_bold), Paragraph("82.8", table_cell), Paragraph("New-Ball Swing & Subcontinental Death", table_cell)],
        [Paragraph("4", table_cell), Paragraph("<b>Allah Ghazanfar</b>", table_cell), Paragraph("Afghanistan", table_cell), Paragraph("Mystery Off-Spin", table_cell), Paragraph("90.8", table_cell_bold), Paragraph("83.7 (#17 A)", table_cell), Paragraph("Middle-Overs Mystery Wicket-Taker", table_cell)],
        [Paragraph("5", table_cell), Paragraph("<b>Rasikh Salam</b>", table_cell), Paragraph("India", table_cell), Paragraph("Right-Arm Medium-Fast", table_cell), Paragraph("89.6", table_cell_bold), Paragraph("82.1 (#20 A)", table_cell), Paragraph("Domestic Seam Depth & Knuckle-Balls", table_cell)],
    ]
    t_bowl = Table(bowl_data, colWidths=[24, 90, 50, 100, 45, 65, 130])
    t_bowl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1E9DD")),
        ("BORDER", (0, 0), (-1, -1), 0.5, c_border),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAF6F0")]),
    ]))
    elements.append(t_bowl)
    elements.append(Spacer(1, 14))

    # 5. Chronological Machine Learning Validation Table
    elements.append(Paragraph("4. Chronological Machine Learning Validation (Holdout 2026)", h1_style))
    elements.append(Paragraph(
        "Zero future-leakage chronological holdout benchmark: Trained <=2024 (120,412 balls), Val 2025 (49,820 balls), Test 2026 (30,729 balls):",
        body_style
    ))

    ml_table_data = [
        [Paragraph("<b>Model Target</b>", table_cell_bold), Paragraph("<b>Holdout Test Split</b>", table_cell_bold), Paragraph("<b>Naive Baseline MAE</b>", table_cell_bold), Paragraph("<b>LightGBM Model MAE</b>", table_cell_bold), Paragraph("<b>Improvement</b>", table_cell_bold), Paragraph("<b>Holdout R²</b>", table_cell_bold)],
        [Paragraph("Batter Expected Runs", table_cell), Paragraph("2026 Matches (N=2,252)", table_cell), Paragraph("17.23 runs", table_cell), Paragraph("<b>5.84 runs</b>", table_cell_bold), Paragraph("<b>+66.13%</b>", table_cell_bold), Paragraph("0.845", table_cell)],
        [Paragraph("Bowler Runs Conceded", table_cell), Paragraph("2026 Matches (N=1,656)", table_cell), Paragraph("10.23 runs", table_cell), Paragraph("<b>7.43 runs</b>", table_cell_bold), Paragraph("<b>+27.36%</b>", table_cell_bold), Paragraph("0.394", table_cell)],
    ]
    t_ml = Table(ml_table_data, colWidths=[110, 100, 75, 75, 70, 74])
    t_ml.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1E9DD")),
        ("BORDER", (0, 0), (-1, -1), 0.5, c_border),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAF6F0")]),
    ]))
    elements.append(t_ml)
    elements.append(Spacer(1, 14))

    # 6. Confirmed Trades Ledger Summary
    elements.append(Paragraph("5. Confirmed Pre-Auction Player Trades (November 2026 Ledger)", h1_style))
    elements.append(Paragraph(
        "10 verified trades executed ahead of the 2027 season. All 10 athletes are contracted to their new clubs and excluded from auction bidding:",
        body_style
    ))

    trades_summary = [
        [Paragraph("<b>Candidate</b>", table_cell_bold), Paragraph("<b>Previous Club</b>", table_cell_bold), Paragraph("<b>New Club</b>", table_cell_bold), Paragraph("<b>Fee</b>", table_cell_bold), Paragraph("<b>Status & Ruling</b>", table_cell_bold)],
        [Paragraph("Hardik Pandya", table_cell), Paragraph("Mumbai Indians", table_cell), Paragraph("Punjab Kings", table_cell), Paragraph("₹18.00 Cr", table_cell), Paragraph("Confirmed Trade (Class C &bull; Excluded)", table_cell)],
        [Paragraph("Arshdeep Singh", table_cell), Paragraph("Punjab Kings", table_cell), Paragraph("Mumbai Indians", table_cell), Paragraph("₹18.00 Cr", table_cell), Paragraph("Confirmed Trade (Class C &bull; Excluded)", table_cell)],
        [Paragraph("Rishabh Pant", table_cell), Paragraph("Lucknow Super Giants", table_cell), Paragraph("Delhi Capitals", table_cell), Paragraph("₹15.00 Cr", table_cell), Paragraph("Confirmed Trade (Class C &bull; Excluded)", table_cell)],
        [Paragraph("Kuldeep Yadav", table_cell), Paragraph("Delhi Capitals", table_cell), Paragraph("Lucknow Super Giants", table_cell), Paragraph("₹13.50 Cr", table_cell), Paragraph("Confirmed Trade (Class C &bull; Excluded)", table_cell)],
        [Paragraph("T. Natarajan", table_cell), Paragraph("Delhi Capitals", table_cell), Paragraph("Sunrisers Hyderabad", table_cell), Paragraph("₹5.00 Cr", table_cell), Paragraph("Confirmed Trade (Class C &bull; Excluded)", table_cell)],
        [Paragraph("Nathan Ellis", table_cell), Paragraph("Chennai Super Kings", table_cell), Paragraph("Sunrisers Hyderabad", table_cell), Paragraph("₹2.00 Cr", table_cell), Paragraph("Confirmed Trade (Class C &bull; Excluded)", table_cell)],
        [Paragraph("Khaleel Ahmed", table_cell), Paragraph("Chennai Super Kings", table_cell), Paragraph("Sunrisers Hyderabad", table_cell), Paragraph("₹4.80 Cr", table_cell), Paragraph("Confirmed Trade (Class C &bull; Excluded)", table_cell)],
        [Paragraph("Liam Livingstone", table_cell), Paragraph("Sunrisers Hyderabad", table_cell), Paragraph("Chennai Super Kings", table_cell), Paragraph("₹6.00 Cr", table_cell), Paragraph("Confirmed Trade (Class C &bull; Excluded)", table_cell)],
    ]
    t_tr = Table(trades_summary, colWidths=[90, 95, 95, 55, 169])
    t_tr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1E9DD")),
        ("BORDER", (0, 0), (-1, -1), 0.5, c_border),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAF6F0")]),
    ]))
    elements.append(t_tr)

    # Build PDF with NumberedCanvas
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {PDF_PATH} ({os.path.getsize(PDF_PATH):,} bytes).")


if __name__ == "__main__":
    build_pdf()
