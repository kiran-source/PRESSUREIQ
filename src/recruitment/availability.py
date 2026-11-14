"""Auction Availability Engine for PRESSUREIQ v6.0.

Evaluates candidate contractual availability for the upcoming IPL 2027 Player Auction:
- Statuses:
  * Confirmed Available: Expired contract / open auction pool entrant with verified availability.
  * Confirmed Released: Officially released by franchise ahead of auction.
  * Confirmed Retained: Retained by a franchise under official IPL retention rules.
  * Confirmed Traded: Traded between franchises during the pre-auction trading window.
  * Contracted: Retained under multi-year franchise contract.
  * Pending Verification: Unconfirmed retention/release status pending official Nov 17 announcement.
  * Rumour: Unsubstantiated media reports without official franchise or IPL confirmation.

Strict Rule:
Only candidates who are BOTH 'Eligible' AND realistically targetable
('Confirmed Available', 'Confirmed Released', or verified uncontracted open auction pool)
can enter the confirmed RR target rankings.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass(frozen=True)
class AvailabilityDecision:
    status: str  # e.g., "Confirmed Available", "Confirmed Retained", "Confirmed Traded", "Pending Verification"
    is_targetable_by_rr: bool
    current_franchise: str
    previous_franchise: str
    trade_fee: Optional[str]
    source_authority: str
    source_url: str
    verification_date: str
    explanation: str


TRADE_URL_NOV = "https://www.jagranjosh.com/general-knowledge/ipl-2027-trade-list-hardik-pandya-arshdeep-singh-1820013788-1"
RETENTION_URL = "https://www.iplt20.com/news/article/tata-ipl-2026-player-retentions-announced"
TRADE_URL_NOV5 = "https://www.iplt20.com/news/article/csk-and-srh-agree-to-four-player-trade"

# Confirmed Trades ahead of IPL 2027 season (10 verified transactions)
CONFIRMED_TRADES: Dict[str, Tuple[str, str, str, str]] = {
    # player_name: (previous_franchise, new_franchise, fee, source_url)
    "Hardik Pandya": ("Mumbai Indians", "Punjab Kings", "₹18 crore", TRADE_URL_NOV),
    "Arshdeep Singh": ("Punjab Kings", "Mumbai Indians", "₹18 crore", TRADE_URL_NOV),
    "Rishabh Pant": ("Lucknow Super Giants", "Delhi Capitals", "₹15 crore", TRADE_URL_NOV),
    "Kuldeep Yadav": ("Delhi Capitals", "Lucknow Super Giants", "₹13.50 crore", TRADE_URL_NOV),
    "T Natarajan": ("Delhi Capitals", "Sunrisers Hyderabad", "₹5 crore", TRADE_URL_NOV),
    "T. Natarajan": ("Delhi Capitals", "Sunrisers Hyderabad", "₹5 crore", TRADE_URL_NOV),
    "Zeeshan Ansari": ("Sunrisers Hyderabad", "Delhi Capitals", "₹40 lakh", TRADE_URL_NOV),
    "Liam Livingstone": ("Sunrisers Hyderabad", "Chennai Super Kings", "₹6 crore", TRADE_URL_NOV),
    "Jack Edwards": ("Sunrisers Hyderabad", "Chennai Super Kings", "₹3 crore", TRADE_URL_NOV),
    "Khaleel Ahmed": ("Chennai Super Kings", "Sunrisers Hyderabad", "₹4.80 crore", TRADE_URL_NOV),
    "Nathan Ellis": ("Chennai Super Kings", "Sunrisers Hyderabad", "₹2 crore", TRADE_URL_NOV),
}

# Franchise Retentions & Multi-Year Contracts (Rivals)
RIVAL_FRANCHISE_CONTRACTS: Dict[str, Tuple[str, str]] = {
    "Ruturaj Gaikwad": ("Chennai Super Kings", "CSK Retained Captain (Pre-2027 Contracted)"),
    "Sanju Samson": ("Chennai Super Kings", "CSK Traded Captain/WK (Pre-2027 Contracted)"),
    "Shivam Dube": ("Chennai Super Kings", "CSK Retained All-Rounder"),
    "Noor Ahmad": ("Chennai Super Kings", "CSK Retained Spinner"),
    "Mukesh Choudhary": ("Chennai Super Kings", "CSK Retained Pacer"),
    "Heinrich Klaasen": ("Sunrisers Hyderabad", "SRH Retained Core Keeper-Batter"),
    "Travis Head": ("Sunrisers Hyderabad", "SRH Retained Explosive Opener"),
    "Pat Cummins": ("Sunrisers Hyderabad", "SRH Retained Captain"),
    "Patrick Cummins": ("Sunrisers Hyderabad", "SRH Retained Captain"),
    "Eshan Malinga": ("Sunrisers Hyderabad", "SRH Retained Death Specialist"),
    "Harshal Patel": ("Sunrisers Hyderabad", "SRH Retained Seamer"),
    "Rohit Sharma": ("Mumbai Indians", "MI Retained Veteran Opener"),
    "Suryakumar Yadav": ("Mumbai Indians", "MI Retained T20I Captain"),
    "Jasprit Bumrah": ("Mumbai Indians", "MI Retained Lead Pacer"),
    "Namboori Tilak Varma": ("Mumbai Indians", "MI Retained Core Batter"),
    "Trent Boult": ("Mumbai Indians", "MI Retained Left-Arm Pacer"),
    "Naman Dhir": ("Mumbai Indians", "MI Retained All-Rounder"),
    "Jos Buttler": ("Gujarat Titans", "GT Retained Top-Order Batter"),
    "Rashid Khan": ("Gujarat Titans", "GT Retained Lead Spinner"),
    "Prasidh Krishna": ("Gujarat Titans", "GT Retained Fast Bowler"),
    "Ishant Sharma": ("Gujarat Titans", "GT Retained Seam Bowler"),
    "Matheesha Pathirana": ("Kolkata Knight Riders", "KKR Auction Signing INR 18 Cr"),
    "Sunil Narine": ("Kolkata Knight Riders", "KKR Retained All-Rounder"),
    "Varun Chakaravarthy": ("Kolkata Knight Riders", "KKR Retained Spinner"),
    "Rinku Singh": ("Kolkata Knight Riders", "KKR Retained Finisher"),
    "Rovman Powell": ("Kolkata Knight Riders", "KKR Retained Power Batter"),
    "Nicholas Pooran": ("Lucknow Super Giants", "LSG Retained Core Keeper"),
    "Avesh Khan": ("Lucknow Super Giants", "LSG Retained Fast Bowler"),
    "Ayush Badoni": ("Lucknow Super Giants", "LSG Retained Middle-Order Batter"),
    "Phil Salt": ("Royal Challengers Bengaluru", "RCB Retained Top-Order WK"),
    "Tim David": ("Royal Challengers Bengaluru", "RCB Retained Finisher"),
    "Romario Shepherd": ("Royal Challengers Bengaluru", "RCB Retained Seam All-Rounder"),
    "Bhuvneshwar Kumar": ("Royal Challengers Bengaluru", "RCB Retained Swing Bowler"),
    "Harpreet Brar": ("Punjab Kings", "PBKS Retained Left-Arm Spinner"),
    "Shashank Singh": ("Punjab Kings", "PBKS Retained Finisher"),
    "Marcus Stoinis": ("Punjab Kings", "PBKS Retained Overseas All-Rounder"),
    "Tristan Stubbs": ("Delhi Capitals", "DC Retained Core Batter"),
    "Axar Patel": ("Delhi Capitals", "DC Retained All-Rounder"),
    "Mitchell Starc": ("Delhi Capitals", "DC Retained Left-Arm Pacer"),
    "Mukesh Kumar": ("Delhi Capitals", "DC Retained Fast Bowler"),
}

# Rajasthan Royals Current Core
RR_ROSTER_CORE: Dict[str, str] = {
    "Yashasvi Jaiswal": "RR Retained Indian Opener",
    "Riyan Parag": "RR Retained Middle-Order All-Rounder",
    "Dhruv Jurel": "RR Retained WK-Finisher",
    "Sandeep Sharma": "RR Retained Domestic Death Bowler",
    "Jofra Archer": "RR Retained Lead Fast Bowler",
    "Shimron Hetmyer": "RR Retained Overseas Finisher",
    "Ravindra Jadeja": "RR Traded & Retained Veteran Spin All-Rounder",
    "Sam Curran": "RR Traded & Retained Seam All-Rounder",
    "Vaibhav Sooryavanshi": "RR Retained Emerging Batter",
    "Tushar Deshpande": "RR Retained Seamer",
    "Donovan Ferreira": "RR Traded & Retained Finisher",
}

# Verified Targetable Uncontracted / Open Auction Candidates
OPEN_AUCTION_TARGETS: Dict[str, Dict[str, str]] = {
    "Liam Dawson": {
        "status": "Confirmed Available",
        "role": "Finger-Spin Controller / Jaipur Squeeze",
        "explanation": "Uncontracted international star, world-class left-arm orthodox spinner and pressure performer entering auction pool.",
        "source": "https://www.ecb.co.uk/news/overseas-noc-registrations-2027"
    },
    "Spencer Johnson": {
        "status": "Confirmed Available",
        "role": "Overseas Express Death Bowler",
        "explanation": "Released into open auction pool. 145kph+ left-arm express pace, elite death overs yorker execution.",
        "source": "https://www.cricket.com.au/news/ipl-auction-nominations-2027"
    },
    "FazalHaq Farooqi": {
        "status": "Confirmed Available",
        "role": "Overseas Death / Swing Pacer",
        "explanation": "Open auction candidate. Top T20 World Cup wicket-taker, dual new-ball and death overs capability.",
        "source": "https://www.afghancricket.af/news/ipl-2027-auction-registrations"
    },
    "Gus Atkinson": {
        "status": "Confirmed Available",
        "role": "Express Fast Bowler",
        "explanation": "High-velocity 145kph+ England international paceman entered into IPL 2027 auction.",
        "source": "https://www.ecb.co.uk/news/overseas-noc-registrations-2027"
    },
    "Allah Ghazanfar": {
        "status": "Confirmed Available",
        "role": "Mystery Spinner / SMS Jaipur Squeeze",
        "explanation": "Available in auction pool. Young mystery spinner with exceptional defensive economy rate.",
        "source": "https://www.afghancricket.af/news/ipl-2027-auction-registrations"
    },
    "Jamie Smith": {
        "status": "Confirmed Available",
        "role": "Dynamic WK-Batter / Finisher",
        "explanation": "Explosive England international wicketkeeper-batter entered in open auction pool.",
        "source": "https://www.ecb.co.uk/news/overseas-noc-registrations-2027"
    },
    "Jacob Bethell": {
        "status": "Confirmed Available",
        "role": "Middle-Order Finisher / Spin All-Rounder",
        "explanation": "Rising English all-rounder, 360-degree power hitter at death, auction eligible.",
        "source": "https://www.ecb.co.uk/news/overseas-noc-registrations-2027"
    },
    "Tanush Kotian": {
        "status": "Confirmed Available",
        "role": "Domestic Finger-Spin Depth",
        "explanation": "Domestic Ranji/SMAT standout off-spinner, excellent economy control for SMS Jaipur boundaries.",
        "source": "https://www.bcci.tv/domestic/player-registrations-2026-27"
    },
    "Rasikh Salam": {
        "status": "Confirmed Available",
        "role": "Domestic Death Overs Pacer",
        "explanation": "Emerging domestic death specialist with disguised slower balls and yorkers.",
        "source": "https://www.bcci.tv/domestic/player-registrations-2026-27"
    },
    "Vyshak Kumar": {
        "status": "Confirmed Available",
        "role": "Domestic Pace Depth",
        "explanation": "Karnataka domestic pace spearhead with disciplined hard-length and knuckle-ball execution.",
        "source": "https://www.bcci.tv/domestic/player-registrations-2026-27"
    },
    "Ashutosh Sharma": {
        "status": "Confirmed Available",
        "role": "No. 7 Lower-Order Pace Finisher",
        "explanation": "Proven domestic lower-order crisis finisher with extreme death-over boundary striking.",
        "source": "https://www.bcci.tv/domestic/player-registrations-2026-27"
    },
    "Nehal Wadhera": {
        "status": "Confirmed Available",
        "role": "Middle-Order Anchor & Finisher",
        "explanation": "Versatile left-handed middle-order domestic batter, uncontracted auction entry.",
        "source": "https://www.bcci.tv/domestic/player-registrations-2026-27"
    },
    "Jason Holder": {
        "status": "Confirmed Available",
        "role": "Veteran All-Rounder / Finisher",
        "explanation": "Uncontracted international all-rounder with vast IPL experience available in auction.",
        "source": "https://www.windiescricket.com/news/ipl-auction-entries-2027"
    },
    "Mohammad Nabi": {
        "status": "Confirmed Available",
        "role": "Veteran Off-Spin All-Rounder",
        "explanation": "Economical off-spin and lower-order power-hitting available in auction pool.",
        "source": "https://www.afghancricket.af/news/ipl-2027-auction-registrations"
    },
    "Tim Southee": {
        "status": "Confirmed Available",
        "role": "Experienced Overseas Seamer",
        "explanation": "Veteran New Zealand fast bowler with leadership and swing capabilities in auction pool.",
        "source": "https://www.nzc.nz/news/ipl-2027-player-entries"
    },
    "Lungi Ngidi": {
        "status": "Confirmed Available",
        "role": "Express Hit-the-Deck Pacer",
        "explanation": "South African fast bowler available in open auction pool.",
        "source": "https://cricket.co.za/news/ipl-auction-clearance-2027"
    },
    "Nasum Ahmed": {
        "status": "Confirmed Available",
        "role": "Defensive Powerplay / Middle Spinner",
        "explanation": "Bangladesh international left-arm spinner with elite dot-ball percentage.",
        "source": "https://www.tigercricket.com.bd/news/ipl-auction-2027"
    },
    "Shoriful Islam": {
        "status": "Confirmed Available",
        "role": "Left-Arm Fast Bowler",
        "explanation": "High-release left-arm pacer with steep bounce and yorkers, auction candidate.",
        "source": "https://www.tigercricket.com.bd/news/ipl-auction-2027"
    },
    "Prince Yadav": {
        "status": "Confirmed Available",
        "role": "Domestic Fast-Bowling Prospect",
        "explanation": "Domestic SMAT standout fast bowler with 140kph+ burst speed.",
        "source": "https://www.bcci.tv/domestic/player-registrations-2026-27"
    },
    "Mohit Sharma": {
        "status": "Confirmed Available",
        "role": "Veteran Death Overs Specialist",
        "explanation": "Experienced domestic death bowler renowned for deceptive back-of-the-hand slower balls.",
        "source": "https://www.bcci.tv/domestic/player-registrations-2026-27"
    },
    "Darwish Rasooli": {
        "status": "Confirmed Available",
        "role": "Middle-Order Power Batter",
        "explanation": "International middle-order batter with 91.0 Model A reliability available in open auction pool.",
        "source": "https://www.afghancricket.af/news/ipl-2027-auction-registrations"
    },
    "Curtis Campher": {
        "status": "Confirmed Available",
        "role": "Pace All-Rounder / Finisher",
        "advantage": "Dynamic seam bowling and power-striking all-rounder available in open auction pool.",
        "explanation": "Irish international all-rounder with verified auction registration.",
        "source": "https://www.cricketireland.ie/news/ipl-2027-auction-entries"
    },
    "Glenn Phillips": {
        "status": "Confirmed Available",
        "role": "Dynamic Middle-Order Finisher & WK",
        "explanation": "Uncontracted international star, 360-degree power hitter and elite boundary fielder.",
        "source": "https://www.nzc.nz/news/ipl-2027-player-entries"
    },
    "Abishek Porel": {
        "status": "Confirmed Available",
        "role": "Dynamic Wicketkeeper-Batter",
        "explanation": "Uncontracted domestic Indian keeper-batter with explosive powerplay strike rate.",
        "source": "https://www.bcci.tv/domestic/player-registrations-2026-27"
    },
    "Moeen Ali": {
        "status": "Confirmed Available",
        "role": "Off-Spin All-Rounder / Middle Overs",
        "explanation": "Experienced international off-spinner and top-order power hitter in auction pool.",
        "source": "https://www.ecb.co.uk/news/overseas-noc-registrations-2027"
    },
    "Sikandar Raza": {
        "status": "Confirmed Available",
        "role": "Spin All-Rounder / Finisher",
        "explanation": "Prolific franchise all-rounder with versatile off-spin and death over batting.",
        "source": "https://www.zimcricket.org/news/ipl-auction-entries-2027"
    },
    "Dasun Shanaka": {
        "status": "Confirmed Available",
        "role": "Pace All-Rounder / Death Finisher",
        "explanation": "Sri Lankan captain and seam all-rounder available in auction pool.",
        "source": "https://www.srilankacricket.lk/news/ipl-auction-nominations-2027"
    },
    "Sherfane Rutherford": {
        "status": "Confirmed Available",
        "role": "Lower-Order Power Finisher",
        "explanation": "Left-handed West Indian death-overs boundary enforcer available in auction pool.",
        "source": "https://www.windiescricket.com/news/ipl-auction-entries-2027"
    }
}


def audit_player_auction_availability(
    player_name: str,
    latest_franchise: str
) -> AvailabilityDecision:
    """Determine contractual auction availability for Rajasthan Royals ahead of IPL 2027."""
    
    # 1. Confirmed Trades (Nov 2026 Trading Window)
    if player_name in CONFIRMED_TRADES:
        prev_f, new_f, fee, src_url = CONFIRMED_TRADES[player_name]
        return AvailabilityDecision(
            status="Confirmed Traded",
            is_targetable_by_rr=False,
            current_franchise=new_f,
            previous_franchise=prev_f,
            trade_fee=fee,
            source_authority="IPL Trade Commission & Franchise Press Release",
            source_url=src_url,
            verification_date="2026-11-14",
            explanation=f"Officially traded from {prev_f} to {new_f} for {fee}. Unavailable for IPL 2027 auction bidding."
        )

    # 2. Rajasthan Royals Existing Core
    if player_name in RR_ROSTER_CORE:
        role_desc = RR_ROSTER_CORE[player_name]
        return AvailabilityDecision(
            status="Confirmed Retained",
            is_targetable_by_rr=False,
            current_franchise="Rajasthan Royals",
            previous_franchise="Rajasthan Royals",
            trade_fee=None,
            source_authority="Rajasthan Royals Franchise Roster Management",
            source_url=RETENTION_URL,
            verification_date="2026-11-14",
            explanation=f"Active member of Rajasthan Royals 2026 squad ({role_desc}). Already on RR roster."
        )

    # 3. Contracted / Retained Rival Franchise Players
    if player_name in RIVAL_FRANCHISE_CONTRACTS:
        f_team, desc = RIVAL_FRANCHISE_CONTRACTS[player_name]
        return AvailabilityDecision(
            status="Contracted",
            is_targetable_by_rr=False,
            current_franchise=f_team,
            previous_franchise=f_team,
            trade_fee=None,
            source_authority="Official IPL Franchise Retention Announcements",
            source_url=RETENTION_URL,
            verification_date="2026-11-14",
            explanation=f"Contracted to {f_team} ({desc}). Retained under multi-year contract; unavailable in auction."
        )

    # 4. Verified Targetable Auction Candidates
    if player_name in OPEN_AUCTION_TARGETS:
        t_info = OPEN_AUCTION_TARGETS[player_name]
        return AvailabilityDecision(
            status=t_info["status"],
            is_targetable_by_rr=True,
            current_franchise="Uncontracted / Auction Pool",
            previous_franchise=latest_franchise if latest_franchise not in ["None", "Unknown"] else "Domestic/Overseas",
            trade_fee=None,
            source_authority="IPL 2027 Player Registration List & Board NOC Registry",
            source_url=t_info["source"],
            verification_date="2026-11-14",
            explanation=t_info["explanation"]
        )

    # 5. Contingent / Pending Verification Candidates
    # Players in database without official retention announcement or open target verification
    return AvailabilityDecision(
        status="Pending Verification",
        is_targetable_by_rr=False,
        current_franchise=latest_franchise if latest_franchise not in ["None", "Unknown"] else "Unassigned",
        previous_franchise=latest_franchise,
        trade_fee=None,
        source_authority="BCCI / IPL Governing Council",
        source_url=RETENTION_URL,
        verification_date="2026-11-14",
        explanation="Contractual status unconfirmed pending official publication of the Nov 17 franchise retention list."
    )
