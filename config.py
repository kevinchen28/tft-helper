"""Per-set configuration for the Codex pipeline.
Update this block for each new set; everything else is generic.
"""
SET         = 19
SET_NAME    = "Prismatic Tour"
CODEX_TITLE = "Prismatic Tour Codex"
LAUNCH      = "Dec 1, 2026 · patch 19.1"
MAX_COST    = 7   # Set 19 has 7-costs

# Hidden combo trait (like Set 18's Eclipse = Solar+Lunar). None if the set has none.
# shape: {"name": "Eclipse", "a": "Solar", "b": "Lunar"}
HIDDEN_TRAIT = None

# Flavor callouts shown at the top of the page. accent: gold | violet | green
CALLOUTS = [
    {"accent": "gold",   "title": "New mechanic · Unlocks",
     "body": "32 champions start locked — each has its own condition (field certain champions, hit trait milestones) that unlocks it into your shop."},
    {"accent": "violet", "title": "Theme · Prismatic Tour",
     "body": "A music-themed set and a Set 10 callback: a live board mixer, 7-cost legends, and a True Damage “Tour Collection” you can retune mid-game."},
]

# Cost tier colors (gems / borders)
COST_COLORS = {1: "#8a9a8d", 2: "#3fae6a", 3: "#2f8fd4", 4: "#a06fe0",
               5: "#e0b23f", 6: "#e07b53", 7: "#e0556f"}

# Derived — do not edit
DUMP   = f"metatft_set{SET}.json"       # champion/trait/item dump (written by run_refresh.sh)
DATA   = f"set{SET}_full.json"          # assembled dataset
HTML   = f"set{SET}_explorer.html"      # built page
PREFIX = f"TFT{SET}_"                   # apiName prefix
TFT_SET = f"TFTSet{SET}"                # tft_set identifier in MetaTFT responses
