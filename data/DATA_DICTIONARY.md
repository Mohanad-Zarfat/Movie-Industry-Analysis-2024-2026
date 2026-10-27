# 📖 Data Dictionary — `cleaned_movies_2024_2026.csv`

**916 rows × 31 columns** · one row per movie release · encoding UTF-8 · delimiter `,`

## Core fields

| Column | Type | Description | Nulls |
|--------|------|-------------|-------|
| `title` | string | Movie title | 0 |
| `release_year` | int | Year of release (2024–2026) | 0 |
| `release_month` | string | Month name (January–December) | 0 |
| `release_day` | float | Day of month; **missing (676 rows)** when only the month is known | 676 |
| `genres` | string | Comma-separated genre list, e.g. `Horror, Mystery, Thriller` | 0 |
| `rating_out_of_10` | float | Community rating on a 0–10 scale (observed 6.0–9.2) | 0 |
| `vote_count` | int | Number of votes behind the rating (7,128–452,490) | 0 |
| `runtime_minutes` | int | Runtime in minutes (84–171) | 0 |
| `box_office_usd` | float | Total box office gross in USD ($25.3M–$510.7M) | 0 |
| `budget_usd` | float | Production budget in USD ($10.8M–$171.2M) | 0 |
| `director` | string | Director name(s); missing for 305 rows | 305 |
| `screenwriter` | string | Screenwriter name(s) | 22 |
| `cast` | string | Comma-separated principal cast | 0 |
| `production_company` | string | Studio chain, `/`-separated; first entry = `primary_studio` (derived) | 0 |
| `content_rating` | string | MPAA-style rating: `PG` (5), `PG-13` (806), `R` (105) | 0 |
| `language` | string | Always `English` in this dataset | 0 |
| `country` | string | Always `United States` in this dataset | 0 |
| `synopsis` | string | Auto-generated descriptive summary | 0 |
| `wikipedia_url` | string | Wikipedia page URL | 0 |
| `poster_url` | string | Poster image URL | 0 |
| `release_date` | date | ISO date `YYYY-MM-DD`; day falls back to `01` when unknown | 0 |

## One-hot genre flags (1 = movie carries the genre)

| Column | Genre | Count | % of releases |
|--------|-------|-------|---------------|
| `genre_adventure` | Adventure | 531 | 58% |
| `genre_drama` | Drama | 366 | 40% |
| `genre_sci_fi` | Sci-Fi | 349 | 38% |
| `genre_action` | Action | 166 | 18% |
| `genre_thriller` | Thriller | 165 | 18% |
| `genre_history` | History | 118 | 13% |
| `genre_horror` | Horror | 83 | 9% |
| `genre_mystery` | Mystery | 80 | 9% |
| `genre_comedy` | Comedy | 52 | 6% |
| `genre_family` | Family | 50 | 5% |

> A movie can carry several genre flags, so flag counts sum to more than 916.

## Derived columns (created in `src/config.py → load_movies()`)

| Column | Formula | Purpose |
|--------|---------|---------|
| `roi_pct` | `(box_office_usd − budget_usd) / budget_usd × 100` | Return on investment, % |
| `profit_usd` | `box_office_usd − budget_usd` | Absolute profit |
| `primary_studio` | first entry of `production_company` before `/` | Studio-level aggregation |
| `runtime_band` | `<100 / 100–120 / 120–140 / 140+` minutes | Runtime bucketing |

## Data quality summary

- ✅ No missing financial or rating values.
- ⚠️ `director` missing on 305 rows (33%) — labeled "Unknown" in analyses.
- ⚠️ `release_day` missing on 676 rows (74%) — day-level timing analysis avoided.
- ℹ️ 2 titles appear twice across different years (*The Long Game*, *Don't Move*) — kept
  as distinct release events.
- ℹ️ In this dataset all 916 releases gross above budget; ROI describes *relative*
  profitability, not break-even risk.
