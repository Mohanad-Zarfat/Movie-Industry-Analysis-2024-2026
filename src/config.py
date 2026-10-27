"""
Central configuration: paths, visual theme and reusable helpers.

Dark Cinematic Theme
--------------------
A movie-industry inspired palette built around a deep navy "theater"
background with IMDb-style gold accents.
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.font_manager as fm
import pandas as pd

# --------------------------------------------------------------------------- #
# Paths (project root = two levels up from this file)
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
IMAGES_DIR = ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

DATA_FILE = DATA_DIR / "cleaned_movies_2024_2026.csv"

# --------------------------------------------------------------------------- #
# Dark cinematic palette
# --------------------------------------------------------------------------- #
BG        = "#0E1117"   # page / axes background  (deep theater black-blue)
PANEL     = "#161B22"   # card / figure panel
GRID      = "#242C38"   # grid lines
TEXT      = "#E6EDF3"   # main text
TEXT_MUT  = "#8B949E"   # secondary text

GOLD      = "#F5C518"   # primary accent (IMDb gold)
AMBER     = "#FF8C42"   # secondary accent
CORAL     = "#E8503A"   # negative / loss accent
TEAL      = "#2EC4B6"   # positive accent
BLUE      = "#5B9BD5"   # neutral accent
PURPLE    = "#9D7CD8"   # extra categorical
GREEN     = "#7BC950"   # extra categorical

# Categorical cycle used across charts
CAT_CYCLE = [GOLD, TEAL, AMBER, BLUE, CORAL, PURPLE, GREEN, "#D65A8A", "#A8B8C8"]

GENRE_COLS = [
    "genre_adventure", "genre_drama", "genre_sci_fi", "genre_action",
    "genre_thriller", "genre_history", "genre_horror", "genre_mystery",
    "genre_comedy", "genre_family",
]

GENRE_LABELS = {
    "genre_adventure": "Adventure", "genre_drama": "Drama",
    "genre_sci_fi": "Sci-Fi", "genre_action": "Action",
    "genre_thriller": "Thriller", "genre_history": "History",
    "genre_horror": "Horror", "genre_mystery": "Mystery",
    "genre_comedy": "Comedy", "genre_family": "Family",
}


def apply_theme() -> None:
    """Register fonts and apply the dark-cinematic rcParams globally."""
    for fp in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        try:
            fm.fontManager.addfont(fp)
        except Exception:  # pragma: no cover - font file missing on some systems
            pass

    mpl.rcParams.update(
        {
            # canvas
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
            "figure.edgecolor": BG,
            # text
            "text.color": TEXT,
            "axes.edgecolor": GRID,
            "axes.labelcolor": TEXT_MUT,
            "axes.titlecolor": TEXT,
            "xtick.color": TEXT_MUT,
            "ytick.color": TEXT_MUT,
            # typography
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans"],
            "axes.titleweight": "bold",
            "axes.titlepad": 14,
            "axes.titlesize": 13,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            # grid
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "axes.axisbelow": True,
            # legend
            "legend.facecolor": PANEL,
            "legend.edgecolor": GRID,
            "legend.framealpha": 0.9,
            "legend.labelcolor": TEXT,
            # lines / spines
            "axes.spines.top": False,
            "axes.spines.right": False,
            "lines.linewidth": 2.2,
            # output
            "figure.dpi": 110,
            "savefig.dpi": 160,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.25,
        }
    )


def load_movies() -> pd.DataFrame:
    """
    Load the cleaned dataset and add analyst-friendly derived columns.

    Adds
    ----
    release_date      : datetime (fallback to 1st of month when day missing)
    roi_pct           : (box_office - budget) / budget * 100
    profit_usd        : box_office - budget
    primary_studio    : first studio listed before any '/'
    decade_bands      : runtime bucket (Short / Standard / Long / Epic)
    """
    df = pd.read_csv(DATA_FILE)

    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["roi_pct"] = (df["box_office_usd"] - df["budget_usd"]) / df["budget_usd"] * 100
    df["profit_usd"] = df["box_office_usd"] - df["budget_usd"]
    df["primary_studio"] = (
        df["production_company"].astype(str).str.split("/").str[0].str.strip()
    )
    df["runtime_band"] = pd.cut(
        df["runtime_minutes"],
        bins=[0, 100, 120, 140, 300],
        labels=["<100 min", "100-120 min", "120-140 min", "140+ min"],
    )
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    df["release_month"] = pd.Categorical(df["release_month"], categories=month_order, ordered=True)
    return df


def money(x: float, pos: int | None = None) -> str:
    """$1.2M / $490M / $1.3B formatter for axis ticks and labels."""
    if abs(x) >= 1_000_000_000:
        return f"${x / 1_000_000_000:.1f}B"
    if abs(x) >= 1_000_000:
        return f"${x / 1_000_000:.0f}M"
    if abs(x) >= 1_000:
        return f"${x / 1_000:.0f}K"
    return f"${x:,.0f}"
