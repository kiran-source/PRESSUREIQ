import pandas as pd
import numpy as np

# Let's inspect how BPI / BoPI / RRR change under different bye treatments
# In an innings of 120 balls, how many byes/legbyes occur on average?
# Total balls: 200,999. Total byes + legbyes = 529 + 2748 = 3277 across 867 matches.
# Average byes+legbyes per match: 3277 / 867 = 3.78 per match (approx 1.89 per innings!).

avg_byes_per_inn = (529 + 2748) / (867 * 2)
print(f"Average byes + leg-byes per innings: {avg_byes_per_inn:.2f} deliveries")
print(f"Percentage of total deliveries: {3277 / 200999 * 100:.2f}%")

