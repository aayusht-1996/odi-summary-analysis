## 📌 Project Workflow Overview

### 1. **Data Source (Live from Web)**
- Directly accessed and streamed ODI match data from `https://cricsheet.org/downloads/odis_json.zip`
- Each match is stored as an individual `.json` file within the zip

### 2. **Data Extraction & Transformation (Python)**
- Parsed JSON files directly in memory without saving locally
- Extracted relevant information:
  - Match metadata: date, venue, event, teams, outcome, toss info
  - Batting stats: total runs, overs (excluding wide/no balls), wickets
  - Additional context: player of match, target score, legitimate overs
- Handled cricket-specific logic (e.g., overs as decimal, extras filtering)
- Output saved as a clean and structured CSV: `odi_summary.csv`

### 3. **Data Ingestion into Azure Databricks**
- Uploaded curated CSV files to Azure Databricks
- Created two sandbox tables:
  - `odi_summary`: match-level structured data
  - `stadiums`: cleaned stadium and location mapping 

### 4. **SQL Analysis in Databricks Notebooks**
- Wrote SQL queries to analyze:
  - Top 5 Most Dominant Wins by Margin (All Time)
  - Toss Impact vs Batting Order Win Rate
  - Top 3 Teams with Highest Win Rate When Chasing (Min 50 Matches)
  - Highest Target Chased by Each Team
  - Top 10 Stadiums by Average Runs Scored

### 5. **Power BI Dashboard Integration**
- Connected Power BI to Databricks using ODBC
- Created interactive dashboards on:
  - Match Summary (Matches Played, Matches by Venue using filled map)
  - Venue-wise Comparision (RPO per innings, Wickets Fallen per innings, Toss Decision)
  - Team-wise Analysis

---
## 📊 Key Skills Demonstrated
- **Techniques Used**: Live data ingestion from web ZIPs, JSON parsing in memory, cricket-specific logic for overs and innings, SQL analytics in Databricks, and Power BI dashboards with DAX and drillthrough
- **Python**: Data extraction, transformation, cricket-specific logic
- **SQL**: CTEs, window functions, Joins, Aggregates
- **Azure Databricks**: Sandbox tables, notebook workflows
- **Power BI**: Dynamic dashboards, drill-throughs, DAX , slicers

---
## 📁 Files Description
- **`odi_data_extract.py`** – Python script to download, extract, and clean ODI match data from Cricsheet.
- **`odi_summary.csv`** – Cleaned match-level data generated from the extraction script.
- **`stadiums.csv`** – Stadium-to-city and country mapping for location analysis.
- **`ODI Summary Analysis.py`** – SQL notebook used in Azure Databricks for match analysis.
- **`ODI Dashboard.pbix`** – Power BI dashboard file containing all interactive visuals.
 

