"""
Movie Industry Analysis 2024-2026 - chart generation pipeline.

Run:  python src/generate_charts.py
Out:  images/*.png (dark cinematic theme)
"""

import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

sys.path.insert(0, str(__file__.rsplit("/", 1)[0]))
from config import (  # noqa: E402
    AMBER, BG, BLUE, CAT_CYCLE, CORAL, GENRE_COLS, GENRE_LABELS, GOLD,
    GRID, IMAGES_DIR, PANEL, PURPLE, TEAL, TEXT, TEXT_MUT, apply_theme,
    load_movies, money,
)

mpl = plt.matplotlib  # noqa: F841 - kept for readability of style names

TITLE_KW = dict(loc="left")
SUB_KW = dict(ha="left", color=TEXT_MUT, fontsize=9.5)


def _title(ax, title, sub=None):
    ax.set_title(title, **TITLE_KW)
    if sub:
        ax.text(0, 1.015, sub, transform=ax.transAxes, **SUB_KW)


def _style_axes(ax):
    ax.grid(axis="y", alpha=0.6)
    ax.grid(axis="x", alpha=0.25)


def _save(fig, name):
    path = IMAGES_DIR / name
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {name}")


def _desc_axes(fig, ax):
    ax.set_facecolor(BG)
    _style_axes(ax)


# --------------------------------------------------------------------------- #
# 1. Top 15 box office
# --------------------------------------------------------------------------- #
def top_box_office(df):
    top = df.nlargest(15, "box_office_usd").sort_values("box_office_usd")
    fig, ax = plt.subplots(figsize=(10.5, 6.4), constrained_layout=True)
    colors = [GOLD if v == top.box_office_usd.max() else TEAL for v in top.box_office_usd]
    bars = ax.barh(top.title, top.box_office_usd, color=colors, height=0.68)
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(money))
    for b, (v, r) in zip(bars, zip(top.box_office_usd, top.rating_out_of_10)):
        ax.text(b.get_width() + top.box_office_usd.max() * 0.01, b.get_y() + b.get_height() / 2,
                f"{money(v)}  |  {r:.1f}★", va="center", color=TEXT, fontsize=8.6)
    ax.set_xlim(0, top.box_office_usd.max() * 1.22)
    _title(ax, "Top 15 Highest-Grossing Movies (2024-2026)",
           "Box office revenue in USD · gold = #1 · label shows revenue and rating")
    ax.grid(axis="x", alpha=0.5)
    ax.grid(axis="y", alpha=0)
    _save(fig, "01_top_box_office.png")


# --------------------------------------------------------------------------- #
# 2. Revenue by year
# --------------------------------------------------------------------------- #
def revenue_by_year(df):
    g = df.groupby("release_year", observed=True).agg(
        total=("box_office_usd", "sum"), avg=("box_office_usd", "mean"), n=("title", "count"))
    fig, ax = plt.subplots(figsize=(9.5, 5.6), constrained_layout=True)
    bars = ax.bar(g.index.astype(str), g.total, color=[BLUE, GOLD, AMBER], width=0.55)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(money))
    for b, (t, n) in zip(bars, zip(g.total, g.n)):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + g.total.max() * 0.015,
                f"{money(t)}\n({n} movies)", ha="center", color=TEXT, fontsize=9)
    ax.set_ylim(0, g.total.max() * 1.18)
    ax.set_ylabel("Total box office")
    _title(ax, "Total Box Office by Release Year",
           "Aggregate revenue of all tracked releases per year")
    _save(fig, "02_revenue_by_year.png")


# --------------------------------------------------------------------------- #
# 3. Monthly release pattern
# --------------------------------------------------------------------------- #
def monthly_pattern(df):
    g = df.groupby("release_month", observed=False).agg(
        n=("title", "count"), avg=("box_office_usd", "mean"))
    x = np.arange(12)
    fig, ax = plt.subplots(figsize=(11.5, 5.8), constrained_layout=True)
    ax.bar(x, g.n, color=PANEL, edgecolor=GRID, width=0.62, label="Movies released")
    ax.set_ylabel("Movies released", color=TEXT_MUT)
    ax.set_ylim(0, g.n.max() * 1.35)
    ax2 = ax.twinx()
    ax2.plot(x, g.avg, color=GOLD, marker="o", lw=2.4, label="Avg box office")
    ax2.yaxis.set_major_formatter(mtick.FuncFormatter(money))
    ax2.set_ylabel("Avg box office", color=GOLD)
    ax2.grid(False)
    ax2.set_ylim(0, g.avg.max() * 1.3)
    ax.set_xticks(x)
    ax.set_xticklabels([m[:3] for m in g.index])
    best = g.avg.idxmax()
    ax2.annotate(f"peak: {best[:3]} · {money(g.avg.max())}",
                 xy=(list(g.index).index(best), g.avg.max()),
                 xytext=(0.32, 0.92), textcoords="axes fraction", color=GOLD,
                 arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.4), fontsize=9)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left", bbox_to_anchor=(0.0, 1.14), ncols=2, frameon=False)
    _title(ax, "Release Timing: Volume vs. Average Box Office by Month",
           "Bars = number of releases · line = average box office per release")
    _save(fig, "03_monthly_pattern.png")


# --------------------------------------------------------------------------- #
# 4. Genre footprint
# --------------------------------------------------------------------------- #
def genre_count(df):
    counts = df[GENRE_COLS].sum().sort_values()
    labels = [GENRE_LABELS[c] for c in counts.index]
    fig, ax = plt.subplots(figsize=(9.5, 5.8), constrained_layout=True)
    norm = plt.matplotlib.colors.Normalize(vmin=counts.min(), vmax=counts.max())
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list("darkgold", [PANEL, GOLD])
    ax.barh(labels, counts.values, color=[cmap(norm(v)) for v in counts.values], height=0.66)
    for i, v in enumerate(counts.values):
        ax.text(v + counts.max() * 0.012, i, f"{v} ({v / len(df) * 100:.0f}%)",
                va="center", color=TEXT, fontsize=8.8)
    ax.set_xlim(0, counts.max() * 1.18)
    ax.grid(axis="x", alpha=0.5)
    ax.grid(axis="y", alpha=0)
    _title(ax, "Genre Footprint: How Many Movies Carry Each Genre",
           f"Movies can have multiple genres · base = {len(df)} releases")
    _save(fig, "04_genre_count.png")


# --------------------------------------------------------------------------- #
# 5. Genre performance (avg revenue + avg rating)
# --------------------------------------------------------------------------- #
def genre_performance(df):
    rows = []
    for c in GENRE_COLS:
        sub = df[df[c] == 1]
        rows.append((GENRE_LABELS[c], len(sub), sub.box_office_usd.mean(), sub.rating_out_of_10.mean()))
    g = pd.DataFrame(rows, columns=["genre", "n", "avg_rev", "avg_rating"]).sort_values("avg_rev")
    fig, ax = plt.subplots(figsize=(10.5, 6.2), constrained_layout=True)
    ax.barh(g.genre, g.avg_rev, color=TEAL, height=0.62, label="Avg box office")
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(money))
    ax.set_xlim(0, g.avg_rev.max() * 1.30)
    for i, (rev, rat, n) in enumerate(zip(g.avg_rev, g.avg_rating, g.n)):
        ax.text(rev + g.avg_rev.max() * 0.015, i, f"{money(rev)} · {rat:.1f}★ ({n})",
                va="center", color=TEXT, fontsize=8.6)
    ax.grid(axis="x", alpha=0.5)
    ax.grid(axis="y", alpha=0)
    _title(ax, "Genre Performance: Average Box Office per Genre",
           "Label = avg revenue · avg rating · movie count (a movie can span genres)")
    _save(fig, "05_genre_performance.png")


# --------------------------------------------------------------------------- #
# 6. Budget vs revenue scatter
# --------------------------------------------------------------------------- #
def budget_vs_revenue(df):
    fig, ax = plt.subplots(figsize=(10.5, 6.8), constrained_layout=True)
    sc = ax.scatter(df.budget_usd / 1e6, df.box_office_usd / 1e6,
                    c=df.rating_out_of_10, cmap="copper", s=34,
                    alpha=0.85, edgecolor=GRID, linewidth=0.4)
    lim = max(df.budget_usd.max(), df.box_office_usd.max()) / 1e6 * 1.05
    ax.plot([0, lim], [0, lim], color=CORAL, ls="--", lw=1.6, label="Break-even line")
    ax.plot([0, lim], [0, lim * 2.5], color=TEAL, ls=":", lw=1.4, label="2.5x revenue line")
    ax.set_xlabel("Budget ($M)")
    ax.set_ylabel("Box office ($M)")
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    cb = fig.colorbar(sc, ax=ax, pad=0.015)
    cb.set_label("Rating", color=TEXT_MUT)
    cb.ax.yaxis.set_tick_params(color=TEXT_MUT)
    cb.outline.set_edgecolor(GRID)
    ax.legend(loc="upper left", bbox_to_anchor=(0.01, 0.99))
    _title(ax, "Budget vs. Box Office: Where Does the Money Land?",
           "Every dot is a movie · dashed red = revenue equals budget")
    _save(fig, "06_budget_vs_revenue.png")


# --------------------------------------------------------------------------- #
# 7. Top ROI
# --------------------------------------------------------------------------- #
def top_roi(df):
    top = df.nlargest(15, "roi_pct").sort_values("roi_pct")
    fig, ax = plt.subplots(figsize=(10.5, 6.4), constrained_layout=True)
    bars = ax.barh(top.title, top.roi_pct, color=GOLD, height=0.68)
    for b, (roi, prof) in zip(bars, zip(top.roi_pct, top.profit_usd)):
        ax.text(b.get_width() + top.roi_pct.max() * 0.012, b.get_y() + b.get_height() / 2,
                f"+{roi:,.0f}%  ({money(prof)} profit)", va="center", color=TEXT, fontsize=8.6)
    ax.set_xlim(0, top.roi_pct.max() * 1.30)
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v:,.0f}%"))
    ax.grid(axis="x", alpha=0.5)
    ax.grid(axis="y", alpha=0)
    _title(ax, "Top 15 Return-on-Investment Champions",
           "ROI = (box office - budget) / budget · label shows ROI and absolute profit")
    _save(fig, "07_top_roi.png")


# --------------------------------------------------------------------------- #
# 8. ROI distribution
# --------------------------------------------------------------------------- #
def roi_distribution(df):
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.2), constrained_layout=True)
    ax = axes[0]
    ax.hist(df.roi_pct, bins=40, color=BLUE, edgecolor=BG)
    med = df.roi_pct.median()
    ax.axvline(med, color=GOLD, lw=2, ls="--")
    ax.text(med, ax.get_ylim()[1] * 0.92, f" median {med:.0f}%", color=GOLD, fontsize=9)
    ax.set_xlabel("ROI (%)")
    ax.set_ylabel("Movies")
    _title(ax, "ROI Distribution", "Most movies earn 20-40% over budget")

    ax = axes[1]
    bp = ax.boxplot(df.roi_pct, vert=False, widths=0.5, patch_artist=True,
                    medianprops=dict(color=GOLD, lw=2),
                    boxprops=dict(facecolor=PANEL, edgecolor=GRID),
                    whiskerprops=dict(color=TEXT_MUT), capprops=dict(color=TEXT_MUT),
                    flierprops=dict(marker="o", markerfacecolor=CORAL, markersize=4,
                                    markeredgecolor="none", alpha=0.6))
    ax.set_yticks([])
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v:,.0f}%"))
    _title(ax, "ROI Spread & Outliers", "Red dots = outlier performers")
    _save(fig, "08_roi_distribution.png")


# --------------------------------------------------------------------------- #
# 9. Studio revenue
# --------------------------------------------------------------------------- #
def studio_revenue(df):
    g = df.groupby("primary_studio").agg(total=("box_office_usd", "sum"),
                                         n=("title", "count")).nlargest(15, "total").sort_values("total")
    fig, ax = plt.subplots(figsize=(10.5, 6.6), constrained_layout=True)
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list("goldteal", [TEAL, GOLD])
    norm = plt.matplotlib.colors.Normalize(vmin=g.total.min(), vmax=g.total.max())
    ax.barh(g.index, g.total, color=[cmap(norm(v)) for v in g.total], height=0.68)
    for i, (v, n) in enumerate(zip(g.total, g.n)):
        ax.text(v + g.total.max() * 0.012, i, f"{money(v)} · {n} movies",
                va="center", color=TEXT, fontsize=8.6)
    ax.set_xlim(0, g.total.max() * 1.25)
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(money))
    ax.grid(axis="x", alpha=0.5)
    ax.grid(axis="y", alpha=0)
    _title(ax, "Top 15 Studios by Total Box Office",
           "Studio = first company of the production chain · label = revenue · output")
    _save(fig, "09_studio_revenue.png")


# --------------------------------------------------------------------------- #
# 10. Studio volume vs quality
# --------------------------------------------------------------------------- #
def studio_volume(df):
    g = df.groupby("primary_studio").agg(n=("title", "count"),
                                         avg_rev=("box_office_usd", "mean"),
                                         avg_rating=("rating_out_of_10", "mean"))
    g = g[g.n >= 5].nlargest(12, "n")
    fig, ax = plt.subplots(figsize=(10.5, 6.8), constrained_layout=True)
    sc = ax.scatter(g.n, g.avg_rev / 1e6, c=g.avg_rating, cmap="copper", s=170,
                    edgecolor=GRID, linewidth=0.8)
    # simple collision avoidance: alternate labels above/below when points cluster
    pts = sorted(zip(g.n, g.avg_rev / 1e6, g.index), key=lambda p: (p[0], p[1]))
    placed = []
    for x, y, name in pts:
        off = 9
        for px, py in placed:
            if abs(px - x) < 7 and abs(py - y) < 9:
                off = -off if off > 0 else 9  # flip below, then back above
        ax.annotate(name, (x, y), xytext=(0, off), textcoords="offset points",
                    ha="center", color=TEXT, fontsize=7.8)
        placed.append((x, y))
    ax.set_xlabel("Movies produced (volume)")
    ax.set_ylabel("Average box office ($M)")
    cb = fig.colorbar(sc, ax=ax, pad=0.015)
    cb.set_label("Avg rating", color=TEXT_MUT)
    cb.outline.set_edgecolor(GRID)
    ax.set_ylim(0, (g.avg_rev / 1e6).max() * 1.15)
    _title(ax, "Studio Volume vs. Box Office Punch (5+ movies)",
           "Bubble color = average rating · positioned by output and average revenue")
    _save(fig, "10_studio_volume.png")


# --------------------------------------------------------------------------- #
# 11. Rating distribution
# --------------------------------------------------------------------------- #
def rating_distribution(df):
    fig, ax = plt.subplots(figsize=(9.8, 5.4), constrained_layout=True)
    n, bins, patches = ax.hist(df.rating_out_of_10, bins=np.arange(6.0, 9.45, 0.2),
                               color=BLUE, edgecolor=BG)
    for p, b in zip(patches, bins[:-1]):
        if b >= 9.0:
            p.set_facecolor(GOLD)
        elif b < 7.0:
            p.set_facecolor(CORAL)
    mean = df.rating_out_of_10.mean()
    ax.axvline(mean, color=GOLD, lw=2, ls="--")
    ax.text(mean + 0.03, ax.get_ylim()[1] * 0.9, f"mean {mean:.2f}", color=GOLD, fontsize=9.5)
    ax.set_xlabel("Rating (out of 10)")
    ax.set_ylabel("Movies")
    ax.text(0.985, 0.55, "9.0+ = gold\n6.0-6.9 = red", transform=ax.transAxes,
            ha="right", color=TEXT_MUT, fontsize=8.6)
    _title(ax, "How Are 2024-2026 Movies Rated?",
           "Distribution of ratings · red = weak (<7.0), gold = outstanding (9.0+)")
    _save(fig, "11_rating_distribution.png")


# --------------------------------------------------------------------------- #
# 12. Rating vs votes
# --------------------------------------------------------------------------- #
def rating_vs_votes(df):
    fig, ax = plt.subplots(figsize=(10.5, 6.6), constrained_layout=True)
    sc = ax.scatter(df.rating_out_of_10, df.vote_count / 1e3,
                    s=df.box_office_usd / 4e6, c=df.vote_count, cmap="copper",
                    alpha=0.85, edgecolor=GRID, linewidth=0.4)
    ax.set_xlabel("Rating (out of 10)")
    ax.set_ylabel("Votes (thousands)")
    cb = fig.colorbar(sc, ax=ax, pad=0.015)
    cb.set_label("Vote count", color=TEXT_MUT)
    cb.outline.set_edgecolor(GRID)
    ax.text(0.02, 0.96, "Bubble size = box office", transform=ax.transAxes,
            color=TEXT_MUT, fontsize=9, va="top")
    _title(ax, "Rating vs. Audience Engagement",
           "Do better-rated movies attract more votes? (bubble = revenue)")
    _save(fig, "12_rating_vs_votes.png")


# --------------------------------------------------------------------------- #
# 13. Runtime analysis
# --------------------------------------------------------------------------- #
def runtime_analysis(df):
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.2), constrained_layout=True)
    ax = axes[0]
    ax.hist(df.runtime_minutes, bins=30, color=PURPLE, edgecolor=BG)
    ax.axvline(df.runtime_minutes.median(), color=GOLD, ls="--", lw=2)
    ax.text(df.runtime_minutes.median() + 1, ax.get_ylim()[1] * 0.9,
            f" median {df.runtime_minutes.median():.0f} min", color=GOLD, fontsize=9)
    ax.set_xlabel("Runtime (minutes)")
    ax.set_ylabel("Movies")
    _title(ax, "Runtime Distribution", "Typical release runs about two hours")

    ax = axes[1]
    g = df.groupby("runtime_band", observed=False).box_office_usd.mean()
    colors = [GOLD if v == g.max() else BLUE for v in g.values]
    ax.bar(g.index.astype(str), g.values, color=colors, width=0.6)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(money))
    ax.set_ylabel("Avg box office")
    ax.set_xlabel("Runtime band")
    _title(ax, "Avg Box Office by Runtime Band", "Gold = strongest band")
    _save(fig, "13_runtime_analysis.png")


# --------------------------------------------------------------------------- #
# 14. Content rating comparison
# --------------------------------------------------------------------------- #
def content_rating(df):
    g = df.groupby("content_rating", observed=True).agg(
        n=("title", "count"), rating=("rating_out_of_10", "mean"),
        rev=("box_office_usd", "mean"), bud=("budget_usd", "mean"),
        roi=("roi_pct", "median")).reindex(["PG", "PG-13", "R"]).dropna(how="all")
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.6), constrained_layout=True)
    panels = [
        ("n", "Movies released", "{}", [BLUE, GOLD, AMBER]),
        ("rating", "Average rating", "{:.2f}★", [TEAL, GOLD, AMBER]),
        ("rev", "Avg box office", money, [TEAL, GOLD, AMBER]),
        ("roi", "Median ROI", "{:.0f}%", [TEAL, GOLD, AMBER]),
    ]
    for ax, (col, label, fmt, palette) in zip(axes.flat, panels):
        vals = g[col].values
        cols = palette[: len(vals)]
        bars = ax.bar(g.index, vals, color=cols, width=0.55)
        for b, v in zip(bars, vals):
            txt = fmt(v) if callable(fmt) else fmt.format(v)
            ax.text(b.get_x() + b.get_width() / 2, b.get_height(),
                    txt, ha="center", va="bottom", color=TEXT, fontsize=9.5)
        ax.set_title(label, fontsize=11, loc="left", color=TEXT)
        ax.grid(axis="y", alpha=0.5)
        ax.set_ylim(0, np.nanmax(vals) * 1.22 if np.nanmax(vals) > 0 else 1)
        if col in ("rev", "bud"):
            ax.yaxis.set_major_formatter(mtick.FuncFormatter(money))
    fig.suptitle("Content Rating Face-off: PG · PG-13 · R", color=TEXT,
                 fontsize=15, fontweight="bold", x=0.02, ha="left")
    fig.text(0.02, 0.925, "Four lenses on the same three audience brackets",
             color=TEXT_MUT, fontsize=9.5)
    _save(fig, "14_content_rating.png")


# --------------------------------------------------------------------------- #
# 15. Correlation heatmap
# --------------------------------------------------------------------------- #
def correlation_heatmap(df):
    cols = {
        "rating_out_of_10": "Rating", "vote_count": "Votes",
        "runtime_minutes": "Runtime", "box_office_usd": "Box office",
        "budget_usd": "Budget", "roi_pct": "ROI", "profit_usd": "Profit",
    }
    corr = df[list(cols)].rename(columns=cols).corr()
    fig, ax = plt.subplots(figsize=(8.6, 7.2), constrained_layout=True)
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list(
        "cine", [CORAL, BG, GOLD])
    im = ax.imshow(corr, cmap=cmap, vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr)), corr.columns, rotation=38, ha="right")
    ax.set_yticks(range(len(corr)), corr.columns)
    ax.grid(False)
    for i in range(len(corr)):
        for j in range(len(corr)):
            v = corr.iloc[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    color=TEXT if abs(v) < 0.75 else BG, fontsize=8.8,
                    fontweight="bold" if abs(v) >= 0.5 else "normal")
    cb = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    cb.outline.set_edgecolor(GRID)
    _title(ax, "What Moves With What? Correlation Matrix",
           "Pearson correlation · gold = positive, red = negative")
    _save(fig, "15_correlation_heatmap.png")


# --------------------------------------------------------------------------- #
# 16. Genre share by year
# --------------------------------------------------------------------------- #
def genre_share_by_year(df):
    share = df.groupby("release_year", observed=True)[GENRE_COLS].mean() * 100
    order = share.mean().sort_values(ascending=False).index
    share = share[order]
    labels = [GENRE_LABELS[c] for c in share.columns]
    x = np.arange(len(labels))
    year_styles = {"2024": GOLD, "2025": TEAL, "2026": AMBER}
    fig, ax = plt.subplots(figsize=(11.5, 6.0), constrained_layout=True)
    for year in share.index:
        ys = share.loc[year].values
        c = year_styles.get(str(year), BLUE)
        ax.plot(x, ys, marker="o", lw=2.4, color=c, label=str(year))
        for xi, v in zip(x, ys):
            ax.annotate(f"{v:.0f}", (xi, v), xytext=(0, 7),
                        textcoords="offset points", ha="center",
                        color=c, fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Share of releases carrying genre (%)")
    ax.set_ylim(0, share.values.max() * 1.18)
    ax.legend(loc="upper right", frameon=False)
    _title(ax, "Genre Mix by Year: What Hollywood Is Making",
           "% of that year's releases carrying each genre · a movie can carry several genres")
    _save(fig, "16_genre_share_by_year.png")


# --------------------------------------------------------------------------- #
# Hero banner for README
# --------------------------------------------------------------------------- #
def hero_banner(df):
    total_rev = df.box_office_usd.sum()
    kpis = [
        (f"{len(df):,}", "movies analyzed"),
        (money(total_rev), "total box office"),
        (f"{df.rating_out_of_10.mean():.2f} / 10", "average rating"),
        (money(df.budget_usd.median()), "median budget"),
        (f"{df.runtime_minutes.mean():.0f} min", "average runtime"),
        (f"{df.release_year.nunique()}", "years covered"),
    ]
    fig, ax = plt.subplots(figsize=(13.4, 2.6), constrained_layout=True)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1)
    ax.axis("off")
    for i, (val, lab) in enumerate(kpis):
        x0 = i + 0.06
        ax.add_patch(plt.Rectangle((x0, 0.06), 0.88, 0.88, facecolor=PANEL,
                                   edgecolor=GRID, linewidth=1, zorder=1))
        ax.text(x0 + 0.44, 0.60, val, ha="center", color=GOLD, fontsize=17,
                fontweight="bold", zorder=2)
        ax.text(x0 + 0.44, 0.26, lab, ha="center", color=TEXT_MUT, fontsize=8.6, zorder=2)
    _save(fig, "hero_banner.png")


# --------------------------------------------------------------------------- #
def main():
    apply_theme()
    print("Loading data ...")
    df = load_movies()
    print(f"{len(df)} movies · {df.release_year.min()}-{df.release_year.max()}")
    print("Generating charts ...")
    steps = [
        hero_banner, top_box_office, revenue_by_year, monthly_pattern,
        genre_count, genre_performance, budget_vs_revenue, top_roi,
        roi_distribution, studio_revenue, studio_volume, rating_distribution,
        rating_vs_votes, runtime_analysis, content_rating,
        correlation_heatmap, genre_share_by_year,
    ]
    for fn in steps:
        fn(df)
    print("Done.")


if __name__ == "__main__":
    main()
