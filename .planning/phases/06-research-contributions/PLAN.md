# PHASE 06: Original Research Contributions Plan

## Goal
Implement Pressure Response Curves (PRC), Archetype Classification, and Five-Pillar Reliability Decomposition.

## Tasks
1. Pressure Response Curve (PRC):
   - Model individual player value as a function of pressure: $f(\text{Pressure}) \to \text{PAVA/ball}$.
   - Classify players into archetypes based on slope and retention:
     - `Clutch Climber`: Value increases under rising pressure ($\text{slope} > 0$, positive retention).
     - `Ice Cold Anchor`: Flat, unflappable value across all pressure ranges ($\text{slope} \approx 0$).
     - `Gradual Decliner`: Slight drop under extreme pressure ($\text{slope} < 0$).
     - `Pressure Fragile`: Severe collapse under high pressure.
2. Five-Pillar Reliability Decomposition:
   - Pillar 1: Absolute Pressure Performance (PAVA/ball under high pressure).
   - Pillar 2: Retention Delta ($\Delta_{\text{high}} - \Delta_{\text{low}}$).
   - Pillar 3: Match Consistency (Innings/Spell PAVA standard deviation & positive contribution rate).
   - Pillar 4: Context Adaptability (Performance across both 1st & 2nd innings, IPL & T20I).
   - Pillar 5: Sample Evidence Strength (Log sample volume weight).

## Acceptance Criteria
- PRC slopes and archetypes assigned to all qualified players.
- Five pillars normalized on 0–100 scale.

