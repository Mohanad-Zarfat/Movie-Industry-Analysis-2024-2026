-- ============================================================
-- MOVIE INDUSTRY DATA ANALYSIS
-- PostgreSQL
-- Dataset: cleaned_movies_2024_2026.csv
-- ============================================================


-- ============================================================
-- 0. REMOVE OLD TABLE
-- ============================================================

DROP TABLE IF EXISTS cleaned_movies;


-- ============================================================
-- 1. CREATE TABLE
-- ============================================================

CREATE TABLE cleaned_movies (
    title VARCHAR(255),
    release_year INT,
    release_month VARCHAR(50),
    release_day INT,
    genres TEXT,
    rating_out_of_10 NUMERIC(3,1),
    vote_count INT,
    runtime_minutes INT,
    box_office_usd NUMERIC(15,2),
    budget_usd NUMERIC(15,2),
    director VARCHAR(255),
    screenwriter VARCHAR(255),
    "cast" TEXT,
    production_company VARCHAR(255),
    content_rating VARCHAR(50),
    language VARCHAR(50),
    country VARCHAR(100),
    synopsis TEXT,
    wikipedia_url TEXT,
    poster_url TEXT,

    -- IMPORTANT:
    -- release_date comes BEFORE genre columns
    release_date DATE,

    genre_adventure INT,
    genre_drama INT,
    genre_sci_fi INT,
    genre_action INT,
    genre_thriller INT,
    genre_history INT,
    genre_horror INT,
    genre_mystery INT,
    genre_comedy INT,
    genre_family INT
);


-- ============================================================
-- 2. CHECK TABLE STRUCTURE
-- ============================================================

SELECT
    column_name,
    data_type,
    ordinal_position
FROM information_schema.columns
WHERE table_name = 'cleaned_movies'
ORDER BY ordinal_position;


-- ============================================================
-- 3. DESCRIPTIVE SUMMARY STATISTICS
-- ============================================================

SELECT
    COUNT(*) AS total_movies,

    ROUND(AVG(rating_out_of_10), 2) AS avg_rating,

    ROUND(AVG(runtime_minutes), 1) AS avg_runtime_min,

    ROUND(AVG(box_office_usd), 2) AS avg_box_office_usd,

    ROUND(AVG(budget_usd), 2) AS avg_budget_usd,

    ROUND(AVG(vote_count), 0) AS avg_vote_count

FROM cleaned_movies;


-- ============================================================
-- 4. TOP 5 BOX OFFICE MOVIES
-- ============================================================

SELECT
    title,
    production_company,
    release_year,
    box_office_usd
FROM cleaned_movies
WHERE box_office_usd IS NOT NULL
ORDER BY box_office_usd DESC
LIMIT 5;


-- ============================================================
-- 5. BOTTOM 5 BOX OFFICE MOVIES
-- ============================================================

SELECT
    title,
    production_company,
    release_year,
    box_office_usd
FROM cleaned_movies
WHERE box_office_usd IS NOT NULL
ORDER BY box_office_usd ASC
LIMIT 5;


-- ============================================================
-- 6. TOP 5 HIGHEST-RATED MOVIES
-- ============================================================

SELECT
    title,
    rating_out_of_10,
    vote_count,
    production_company
FROM cleaned_movies
WHERE rating_out_of_10 IS NOT NULL
ORDER BY
    rating_out_of_10 DESC,
    vote_count DESC
LIMIT 5;


-- ============================================================
-- 7. ROI ANALYSIS
--
-- ROI = (Revenue - Budget) / Budget
-- ============================================================

SELECT
    title,
    budget_usd,
    box_office_usd,

    ROUND(
        (box_office_usd - budget_usd)
        / NULLIF(budget_usd, 0),
        2
    ) AS roi

FROM cleaned_movies

WHERE
    budget_usd > 0
    AND box_office_usd IS NOT NULL

ORDER BY roi DESC
LIMIT 10;


-- ============================================================
-- 8. RELEASE MONTH ANALYSIS
-- ============================================================

SELECT
    release_month,

    COUNT(*) AS total_releases,

    ROUND(
        AVG(box_office_usd),
        2
    ) AS avg_box_office,

    ROUND(
        SUM(box_office_usd),
        2
    ) AS total_box_office

FROM cleaned_movies

WHERE box_office_usd IS NOT NULL

GROUP BY release_month

ORDER BY avg_box_office DESC;


-- ============================================================
-- 9. PRODUCTION COMPANIES
-- ============================================================

SELECT
    production_company,

    COUNT(*) AS total_movies_produced,

    ROUND(
        SUM(box_office_usd),
        2
    ) AS total_box_office_usd,

    ROUND(
        AVG(rating_out_of_10),
        2
    ) AS avg_rating

FROM cleaned_movies

WHERE production_company IS NOT NULL

GROUP BY production_company

ORDER BY total_box_office_usd DESC

LIMIT 10;


-- ============================================================
-- 10. PG-13 VS R
-- ============================================================

SELECT
    content_rating,

    COUNT(*) AS total_movies,

    ROUND(
        AVG(rating_out_of_10),
        2
    ) AS avg_rating,

    ROUND(
        AVG(box_office_usd),
        2
    ) AS avg_box_office,

    ROUND(
        AVG(budget_usd),
        2
    ) AS avg_budget

FROM cleaned_movies

WHERE content_rating IN ('PG-13', 'R')

GROUP BY content_rating

ORDER BY content_rating;


-- ============================================================
-- 11. GENRE ANALYSIS
-- ============================================================

SELECT
    'Adventure' AS genre,
    COUNT(*) FILTER (WHERE genre_adventure = 1) AS movie_count
FROM cleaned_movies

UNION ALL

SELECT
    'Drama',
    COUNT(*) FILTER (WHERE genre_drama = 1)
FROM cleaned_movies

UNION ALL

SELECT
    'Sci-Fi',
    COUNT(*) FILTER (WHERE genre_sci_fi = 1)
FROM cleaned_movies

UNION ALL

SELECT
    'Action',
    COUNT(*) FILTER (WHERE genre_action = 1)
FROM cleaned_movies

UNION ALL

SELECT
    'Thriller',
    COUNT(*) FILTER (WHERE genre_thriller = 1)
FROM cleaned_movies

UNION ALL

SELECT
    'History',
    COUNT(*) FILTER (WHERE genre_history = 1)
FROM cleaned_movies

UNION ALL

SELECT
    'Horror',
    COUNT(*) FILTER (WHERE genre_horror = 1)
FROM cleaned_movies

UNION ALL

SELECT
    'Mystery',
    COUNT(*) FILTER (WHERE genre_mystery = 1)
FROM cleaned_movies

UNION ALL

SELECT
    'Comedy',
    COUNT(*) FILTER (WHERE genre_comedy = 1)
FROM cleaned_movies

UNION ALL

SELECT
    'Family',
    COUNT(*) FILTER (WHERE genre_family = 1)
FROM cleaned_movies

ORDER BY movie_count DESC;


-- ============================================================
-- 12. AVERAGE PERFORMANCE BY GENRE
-- ============================================================

SELECT
    'Adventure' AS genre,
    COUNT(*) AS movies,
    ROUND(AVG(box_office_usd), 2) AS avg_box_office,
    ROUND(AVG(rating_out_of_10), 2) AS avg_rating
FROM cleaned_movies
WHERE genre_adventure = 1

UNION ALL

SELECT
    'Drama',
    COUNT(*),
    ROUND(AVG(box_office_usd), 2),
    ROUND(AVG(rating_out_of_10), 2)
FROM cleaned_movies
WHERE genre_drama = 1

UNION ALL

SELECT
    'Sci-Fi',
    COUNT(*),
    ROUND(AVG(box_office_usd), 2),
    ROUND(AVG(rating_out_of_10), 2)
FROM cleaned_movies
WHERE genre_sci_fi = 1

UNION ALL

SELECT
    'Action',
    COUNT(*),
    ROUND(AVG(box_office_usd), 2),
    ROUND(AVG(rating_out_of_10), 2)
FROM cleaned_movies
WHERE genre_action = 1

UNION ALL

SELECT
    'Thriller',
    COUNT(*),
    ROUND(AVG(box_office_usd), 2),
    ROUND(AVG(rating_out_of_10), 2)
FROM cleaned_movies
WHERE genre_thriller = 1

UNION ALL

SELECT
    'History',
    COUNT(*),
    ROUND(AVG(box_office_usd), 2),
    ROUND(AVG(rating_out_of_10), 2)
FROM cleaned_movies
WHERE genre_history = 1

UNION ALL

SELECT
    'Horror',
    COUNT(*),
    ROUND(AVG(box_office_usd), 2),
    ROUND(AVG(rating_out_of_10), 2)
FROM cleaned_movies
WHERE genre_horror = 1

UNION ALL

SELECT
    'Mystery',
    COUNT(*),
    ROUND(AVG(box_office_usd), 2),
    ROUND(AVG(rating_out_of_10), 2)
FROM cleaned_movies
WHERE genre_mystery = 1

UNION ALL

SELECT
    'Comedy',
    COUNT(*),
    ROUND(AVG(box_office_usd), 2),
    ROUND(AVG(rating_out_of_10), 2)
FROM cleaned_movies
WHERE genre_comedy = 1

UNION ALL

SELECT
    'Family',
    COUNT(*),
    ROUND(AVG(box_office_usd), 2),
    ROUND(AVG(rating_out_of_10), 2)
FROM cleaned_movies
WHERE genre_family = 1

ORDER BY avg_box_office DESC;


-- ============================================================
-- 13. TOP MOVIE PER PRODUCTION COMPANY
-- WINDOW FUNCTION
-- ============================================================

WITH RankedMovies AS (

    SELECT
        title,
        production_company,
        box_office_usd,

        DENSE_RANK() OVER (
            PARTITION BY production_company
            ORDER BY box_office_usd DESC
        ) AS rank_in_company

    FROM cleaned_movies

    WHERE
        production_company IS NOT NULL
        AND box_office_usd IS NOT NULL
)

SELECT
    production_company,
    title AS highest_grossing_movie,
    box_office_usd

FROM RankedMovies

WHERE rank_in_company = 1

ORDER BY box_office_usd DESC

LIMIT 10;


-- ============================================================
-- 14. DATA QUALITY CHECK
-- ============================================================

SELECT
    COUNT(*) AS total_rows,

    COUNT(*) FILTER (
        WHERE title IS NULL
    ) AS missing_titles,

    COUNT(*) FILTER (
        WHERE release_date IS NULL
    ) AS missing_release_dates,

    COUNT(*) FILTER (
        WHERE budget_usd IS NULL
    ) AS missing_budgets,

    COUNT(*) FILTER (
        WHERE box_office_usd IS NULL
    ) AS missing_box_office,

    COUNT(*) FILTER (
        WHERE rating_out_of_10 IS NULL
    ) AS missing_ratings

FROM cleaned_movies;


-- ============================================================
-- 15. FINAL PREVIEW
-- ============================================================

SELECT *
FROM cleaned_movies
LIMIT 10;