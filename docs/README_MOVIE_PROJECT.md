# MoviePulse — Excel + SQL + Tableau

Project overview
----------------
MoviePulse is a simple, hand-crafted movie analytics project built with Microsoft Excel (CSV), SQL, and Tableau. The goal is to provide a realistic dataset that fits the Tableau dashboards you showed, with clear steps so anyone can reproduce the analysis using Excel, a local SQL database (SQLite/Postgres), and Tableau Desktop or Tableau Public.

What I added
------------
- data/movies.csv — movie-level dataset (key fields: title, release_date, budget, revenue, profit, popularity, vote_count, language, genre)
- data/movies_2015_monthly.csv — monthly aggregates for 2015 (used for the "2015 Movie Overview" dashboard)
- sql/load_movies.sql — instructions and SQL snippets to import CSV into SQLite or PostgreSQL

Project name
------------
MoviePulse-ExcelSQL-Tableau

How this dataset maps to your Tableau dashboard visuals
------------------------------------------------------
- KPI tiles (Total Revenue, Total Profit, Total Budget): aggregate revenue_m, profit_m, budget_m across the dataset or filtered year range.
- Scatter (Popularity vs Vote Count): use popularity and vote_count, color by release_year or language, size by revenue_m.
- Bar chart (Profit by Year): group by release_year and sum profit_m.
- Budget vs Revenue area/line chart: aggregate by release_year or month (use movies_2015_monthly.csv for detailed 2015 month view).
- Treemap (Top Titles by Revenue in 2015): filter movies.csv to release_year=2015 and use revenue_m as size.
- Pie/Donut (Language Percentage): group by original_language and compute percentage counts or revenue share.

Quick steps to reproduce (Excel + SQLite + Tableau)
--------------------------------------------------
1) Open `data/movies.csv` in Excel
   - Inspect columns, formats, and optionally add calculated columns (e.g., profit_m = revenue_m - budget_m).
   - Save as Excel if desired: File > Save As > Excel Workbook (.xlsx).

2) Load into a local SQL database
   - SQLite (recommended for local testing):
     - With sqlite3 installed: `sqlite3 movies.db` then at the sqlite prompt run:
       .mode csv
       .import data/movies.csv movies
     - Or create the table using `sql/load_movies.sql` and then import via a Python script.
   - PostgreSQL:
     - Create table using the SQL in `sql/load_movies.sql` and run the COPY command with the full path to the CSV.

3) Open Tableau Desktop / Tableau Public
   - Connect to the CSV or to the SQLite/Postgres database.
   - If using CSV: Connect > Text File > select `data/movies.csv`.
   - Build views matching the dashboard: KPIs (SUM of revenue_m, profit_m, budget_m), scatter (popularity on X, vote_count on Y), bar (SUM(profit_m) by release_year), treemap (filter release_year=2015, size by revenue_m), and donut/pie for language share.

Notes and next steps I can do for you
------------------------------------
- Generate an Excel (.xlsx) version of the dataset and include the file in the repo.
- Create a step-by-step Tableau workbook (.twb) template with the sheets laid out (I can include a placeholder or instructions for the exact shelf placements).
- Make a GitHub Pages demo that embeds a Tableau Public dashboard once you publish it publicly.

If you want the Excel workbook included now, say "Add Excel" and I'll add `data/movies_dataset.xlsx` (with the same content) and update the README with direct Excel instructions. If you want me to build a starter Tableau workbook file, publish the dataset to Tableau Public (or give me a sample published URL) and I will embed it.
