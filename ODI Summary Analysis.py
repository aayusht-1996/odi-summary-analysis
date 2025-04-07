# Databricks notebook source
# MAGIC %md
# MAGIC ### **1. Top 5 Most Dominant Wins by Margin (All Time)**

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT winner, 
# MAGIC        batting_first_team, 
# MAGIC        batting_second_team,
# MAGIC        won_by_runs, 
# MAGIC        date
# MAGIC FROM odi_summary
# MAGIC WHERE won_by_runs IS NOT NULL 
# MAGIC ORDER BY 
# MAGIC     COALESCE(won_by_runs, 0) DESC
# MAGIC LIMIT 5;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### **2. Toss Impact vs Batting Order Win Rate**

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH toss_context AS (
# MAGIC   SELECT *,
# MAGIC          CASE WHEN toss_winner = batting_first_team THEN 'Toss & Bat First'
# MAGIC               WHEN toss_winner = batting_second_team THEN 'Toss & Field First'
# MAGIC          END AS toss_strategy
# MAGIC   FROM odi_summary
# MAGIC   WHERE winner IS NOT NULL
# MAGIC )
# MAGIC SELECT toss_strategy,
# MAGIC        COUNT(*) AS total_matches,
# MAGIC        SUM(CASE WHEN winner = batting_first_team THEN 1 ELSE 0 END) AS batting_first_wins,
# MAGIC        ROUND(SUM(CASE WHEN winner = batting_first_team THEN 1 ELSE 0 END)*1.0/COUNT(*), 2)*100 AS batting_first_win_rate_percent
# MAGIC FROM toss_context
# MAGIC GROUP BY toss_strategy;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### **3.  Top 3 Teams with Highest Win Rate When Chasing (Min 50 Matches)**
# MAGIC ### 
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT batting_second_team AS team,
# MAGIC        COUNT(*) AS matches,
# MAGIC        SUM(CASE WHEN batting_second_team = winner THEN 1 ELSE 0 END) AS wins,
# MAGIC        ROUND(SUM(CASE WHEN batting_second_team = winner THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS win_rate
# MAGIC FROM odi_summary
# MAGIC WHERE batting_second_team IS NOT NULL
# MAGIC GROUP BY batting_second_team
# MAGIC HAVING COUNT(*) >= 50
# MAGIC ORDER BY win_rate DESC
# MAGIC LIMIT 3;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. Highest Target Chased by Each Team
# MAGIC ### 

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH chases AS (
# MAGIC   SELECT 
# MAGIC     batting_second_team AS team,
# MAGIC     target_runs,
# MAGIC     winner,
# MAGIC     date,
# MAGIC     ROW_NUMBER() OVER (PARTITION BY batting_second_team ORDER BY target_runs DESC) AS rn
# MAGIC   FROM odi_summary
# MAGIC   WHERE target_runs IS NOT NULL AND batting_second_team = winner
# MAGIC )
# MAGIC SELECT team, target_runs, winner, date
# MAGIC FROM chases
# MAGIC WHERE rn = 1
# MAGIC ORDER BY target_runs DESC;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5. Top 10 Stadiums by Average Runs Scored 

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH stadium_avg_runs AS (
# MAGIC     SELECT
# MAGIC         s.venue,
# MAGIC         s.city,
# MAGIC         s.country,
# MAGIC         ROUND(AVG(CAST(o.batting_first_runs AS DOUBLE) + CAST(o.batting_second_runs AS DOUBLE)), 2) AS avg_total_runs
# MAGIC     FROM
# MAGIC         odi_summary o
# MAGIC     JOIN
# MAGIC         stadiums s ON o.stadium = s.venue
# MAGIC     WHERE
# MAGIC         o.batting_first_runs IS NOT NULL AND o.batting_second_runs IS NOT NULL
# MAGIC     GROUP BY
# MAGIC         s.venue, s.city, s.country
# MAGIC ),
# MAGIC ranked_stadiums AS (
# MAGIC     SELECT *,
# MAGIC            RANK() OVER (ORDER BY avg_total_runs DESC) AS run_rank
# MAGIC     FROM stadium_avg_runs
# MAGIC )
# MAGIC SELECT *
# MAGIC FROM ranked_stadiums
# MAGIC WHERE run_rank <= 10
# MAGIC ORDER BY run_rank;
# MAGIC