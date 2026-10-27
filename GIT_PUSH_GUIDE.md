# 🚀 How to Push This Project to Your GitHub

Follow these steps in order. Total time: **~3 minutes**.

---

## Step 0 — Download & unzip
Download **`movie-industry-analysis-2024-2026.zip`** and unzip it anywhere you like
(e.g. `Documents/Projects/`). You should see a folder named
`movie-industry-analysis-2024-2026/` containing `README.md`, `data/`, `src/`, etc.

## Step 1 — Create an empty repo on GitHub
1. Go to **github.com** → click the **+** icon (top-right) → **New repository**.
2. Repository name: `movie-industry-analysis-2024-2026`
3. Add a description, e.g.: `Full-stack movie industry analysis (2024–2026): Python EDA, PostgreSQL & Power BI`
4. Set to **Public** (recommended for a portfolio).
5. ⚠️ **Do NOT** check "Add a README", ".gitignore" or "License" — the project already has them.
6. Click **Create repository**. Leave the page open.

## Step 2 — Push from your terminal

Open a terminal (or Git Bash / PowerShell on Windows) **inside the unzipped folder**:

```bash
cd path/to/movie-industry-analysis-2024-2026

git init
git add .
git commit -m "Movie industry analysis 2024-2026: Python EDA + SQL + Power BI"
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/movie-industry-analysis-2024-2026.git
git push -u origin main
```

> Replace `<YOUR-USERNAME>` with your GitHub username.

**When prompted to log in:** GitHub no longer accepts passwords. Use
**"Sign in with your browser"** (Git Credential Manager pops up automatically on
Windows/Mac), or use a **Personal Access Token** (GitHub → Settings → Developer
settings → Tokens) as the password.

## Step 3 — Verify & polish (optional but recommended)
1. Refresh your repo page — README renders with the hero banner and chart gallery automatically.
2. Add **Topics** for discoverability: repo page → ⚙️ next to *About* → add
   `data-analysis`, `python`, `pandas`, `matplotlib`, `sql`, `powerbi`, `eda`, `movies`.
3. Check that `images/` chart previews all render in the README.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `git: command not found` | Install git: <https://git-scm.com/downloads> |
| `remote origin already exists` | Run `git remote set-url origin https://github.com/<YOUR-USERNAME>/movie-industry-analysis-2024-2026.git` |
| `rejected - remote contains work` | You accidentally initialized the repo with a README: run `git pull origin main --allow-unrelated-histories` then `git push` |
| Authentication failed | Use a Personal Access Token instead of your password |
| `user.name` not set errors | `git config --global user.name "Your Name"` and `git config --global user.email "you@email.com"` |

## Before you share it
- ✏️ Edit `LICENSE` and replace `<Your Name>` with your real name.
- 🖼 Want a nicer repo card? Add a `preview.png` (screenshot of a chart grid) and set it
  in the repo's social preview (Settings → General → Social preview).
- 🔁 Later updates: just `git add . && git commit -m "update" && git push`.
