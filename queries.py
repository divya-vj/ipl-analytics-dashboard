import sqlite3
import pandas as pd

def run_query(sql):
    """Execute any SQL query and return result as DataFrame."""
    conn = sqlite3.connect("database/ipl.db")
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

q1 = run_query("""
    SELECT season,
           COUNT(*) AS total_matches
    FROM matches
    GROUP BY season
    ORDER BY season ASC
""")
print("Q1 - Matches Per Season")
print(q1)
print()

q2 = run_query("""
    SELECT batter,
           SUM(batsman_runs) AS total_runs,
           COUNT(DISTINCT match_id) AS matches_played,
           ROUND(SUM(batsman_runs) * 1.0 / COUNT(DISTINCT match_id), 2) AS avg_per_match
    FROM deliveries
    GROUP BY batter
    ORDER BY total_runs DESC
    LIMIT 10
""")
print("Q2 - Top 10 Run Scorers")
print(q2)
print()

q3 = run_query("""
    SELECT
        COUNT(*) AS total_matches,
        SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS toss_winner_won,
        ROUND(
            SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
            1
        ) AS win_percentage
    FROM matches
    WHERE winner IS NOT NULL
""")
print("Q3 - Toss Impact on Match Result")
print(q3)
print()

q4 = run_query("""
    SELECT bowler,
           COUNT(DISTINCT match_id) AS matches,
           SUM(total_runs) AS runs_conceded,
           ROUND(COUNT(*) / 6.0, 1) AS overs_bowled,
           ROUND(SUM(total_runs) * 6.0 / COUNT(*), 2) AS economy_rate
    FROM deliveries
    WHERE extras_type NOT IN ('wides', 'noballs')
       OR extras_type IS NULL
    GROUP BY bowler
    HAVING COUNT(*) >= 300
    ORDER BY economy_rate ASC
    LIMIT 10
""")
print("Q4 - Best Bowlers by Economy")
print(q4)
print()

q5 = run_query("""
    SELECT venue,
           COUNT(*) AS total_matches,
           SUM(CASE WHEN result = 'runs' THEN 1 ELSE 0 END) AS batting_first_wins,
           SUM(CASE WHEN result = 'wickets' THEN 1 ELSE 0 END) AS batting_second_wins,
           ROUND(SUM(CASE WHEN result = 'runs' THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS bat_first_win_pct
    FROM matches
    WHERE winner IS NOT NULL
    GROUP BY venue
    HAVING COUNT(*) >= 10
    ORDER BY bat_first_win_pct DESC
    LIMIT 10
""")
print("Q5 - Venue Analysis")
print(q5)
print()

q6 = run_query("""
    SELECT m.season,
           ROUND(AVG(innings_total), 0) AS avg_first_innings_score
    FROM matches m
    JOIN (
        SELECT match_id,
               SUM(total_runs) AS innings_total
        FROM deliveries
        WHERE inning = 1
        GROUP BY match_id
    ) AS first_innings ON m.id = first_innings.match_id
    GROUP BY m.season
    ORDER BY m.season
""")
print("Q6 - Average First Innings Score Per Season")
print(q6)
print()

q7 = run_query("""
    SELECT player_of_match,
           COUNT(*) AS potm_awards,
           COUNT(DISTINCT season) AS seasons_active
    FROM matches
    WHERE player_of_match IS NOT NULL
    GROUP BY player_of_match
    ORDER BY potm_awards DESC
    LIMIT 10
""")
print("Q7 - Most Player of the Match Awards")
print(q7)
print()

q8 = run_query("""
    SELECT batter,
           SUM(CASE WHEN batsman_runs = 6 THEN 1 ELSE 0 END) AS total_sixes,
           COUNT(DISTINCT match_id) AS matches,
           ROUND(
               SUM(CASE WHEN batsman_runs = 6 THEN 1 ELSE 0 END) * 1.0 /
               COUNT(DISTINCT match_id),
               2
           ) AS sixes_per_match
    FROM deliveries
    GROUP BY batter
    ORDER BY total_sixes DESC
    LIMIT 10
""")
print("Q8 - Most Sixes")
print(q8)
print()

q9 = run_query("""
    SELECT winner AS team,
           season,
           COUNT(*) AS wins
    FROM matches
    WHERE winner IS NOT NULL
    GROUP BY winner, season
    ORDER BY wins DESC
    LIMIT 10
""")
print("Q9 - Most Wins Per Team Per Season")
print(q9)
print()

q10 = run_query("""
    SELECT season, batter, season_runs
    FROM (
        SELECT m.season,
               d.batter,
               SUM(d.batsman_runs) AS season_runs,
               ROW_NUMBER() OVER (
                   PARTITION BY m.season
                   ORDER BY SUM(d.batsman_runs) DESC
               ) AS rank_in_season
        FROM deliveries d
        JOIN matches m ON d.match_id = m.id
        GROUP BY m.season, d.batter
    ) ranked
    WHERE rank_in_season = 1
    ORDER BY season
""")
print("Q10 - Top Scorer Per Season (Window Function)")
print(q10)
print()

if __name__ == "__main__":
    print("Running all 10 queries...\n")
