import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# ── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Database Helper ────────────────────────────────────────────────────────
@st.cache_data
def run_query(sql):
    conn = sqlite3.connect("database/ipl.db")
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

# ── Sidebar ────────────────────────────────────────────────────────────────
st.sidebar.title("🏏 IPL Analytics")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate to:",
    [
        "📊 Season Overview",
        "🏏 Batting Analysis",
        "🎯 Bowling Analysis",
        "🏟️ Venue Insights",
        "🔍 Custom SQL Query"
    ]
)

# ══════════════════════════════════════════════════════════════════════════
# PAGE 1 — SEASON OVERVIEW
# ══════════════════════════════════════════════════════════════════════════
if page == "📊 Season Overview":

    st.title("📊 IPL Season Overview")
    st.markdown("*Analysing 17 seasons of IPL cricket data*")

    # ── Metric Cards ──────────────────────────────────────────────────────
    total_matches  = run_query("SELECT COUNT(*) as cnt FROM matches").iloc[0][0]
    total_seasons  = run_query("SELECT COUNT(DISTINCT season) as cnt FROM matches").iloc[0][0]
    total_teams    = run_query("SELECT COUNT(DISTINCT team1) as cnt FROM matches").iloc[0][0]
    total_players  = run_query("SELECT COUNT(DISTINCT batter) as cnt FROM deliveries").iloc[0][0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Matches",  total_matches)
    col2.metric("Seasons",        total_seasons)
    col3.metric("Teams",          total_teams)
    col4.metric("Batters",        total_players)

    st.markdown("---")

    # ── Chart 1: Matches Per Season ───────────────────────────────────────
    st.subheader("📅 Matches Per Season")
    q1 = run_query("""
        SELECT season, COUNT(*) AS total_matches
        FROM matches
        GROUP BY season
        ORDER BY season
    """)
    fig1 = px.bar(
        q1,
        x="season", y="total_matches",
        title="Number of Matches Per IPL Season",
        labels={"season": "Season", "total_matches": "Total Matches"},
        color="total_matches",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ── Chart 2: Average First Innings Score ──────────────────────────────
    st.subheader("📈 Has IPL Become More Aggressive Over The Years?")
    q2 = run_query("""
        SELECT m.season,
               ROUND(AVG(innings_total), 0) AS avg_score
        FROM matches m
        JOIN (
            SELECT match_id, SUM(total_runs) AS innings_total
            FROM deliveries
            WHERE inning = 1
            GROUP BY match_id
        ) t ON m.id = t.match_id
        GROUP BY m.season
        ORDER BY m.season
    """)
    fig2 = px.line(
        q2,
        x="season", y="avg_score",
        title="Average First Innings Score Per Season",
        markers=True,
        labels={"season": "Season", "avg_score": "Avg Score"}
    )
    fig2.update_traces(line_color="#1A56A8", marker_size=8)
    st.plotly_chart(fig2, use_container_width=True)

    # ── Chart 3: Toss Impact ──────────────────────────────────────────────
    st.subheader("🪙 Does Winning The Toss Help?")
    q3 = run_query("""
        SELECT
            SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS toss_winner_won,
            SUM(CASE WHEN toss_winner != winner THEN 1 ELSE 0 END) AS toss_winner_lost
        FROM matches
        WHERE winner IS NOT NULL
    """)
    fig3 = px.pie(
        values=[q3["toss_winner_won"].iloc[0], q3["toss_winner_lost"].iloc[0]],
        names=["Toss Winner Won", "Toss Winner Lost"],
        title="Toss Winner vs Match Winner",
        color_discrete_sequence=["#1A7A42", "#C04A00"]
    )
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════
# PAGE 2 — BATTING ANALYSIS
# ══════════════════════════════════════════════════════════════════════════
elif page == "🏏 Batting Analysis":

    st.title("🏏 Batting Analysis")

    # Season filter
    seasons = run_query(
        "SELECT DISTINCT season FROM matches ORDER BY season"
    )["season"].tolist()
    seasons.insert(0, "All Seasons")
    selected = st.selectbox("Filter by Season:", seasons)

    if selected == "All Seasons":
        season_filter = ""
    else:
        season_filter = f"AND m.season = '{selected}'"

    batting_sql = f"""
        SELECT d.batter,
               SUM(d.batsman_runs)                                        AS total_runs,
               COUNT(DISTINCT d.match_id)                                 AS matches,
               ROUND(SUM(d.batsman_runs)*1.0/COUNT(DISTINCT d.match_id), 1) AS avg_per_match,
               SUM(CASE WHEN d.batsman_runs = 6 THEN 1 ELSE 0 END)       AS sixes,
               SUM(CASE WHEN d.batsman_runs = 4 THEN 1 ELSE 0 END)       AS fours
        FROM deliveries d
        JOIN matches m ON d.match_id = m.id
        WHERE 1=1 {season_filter}
        GROUP BY d.batter
        HAVING COUNT(DISTINCT d.match_id) >= 5
        ORDER BY total_runs DESC
        LIMIT 15
    """
    df_bat = run_query(batting_sql)

    fig_bat = px.bar(
        df_bat, x="batter", y="total_runs",
        title=f"Top 15 Run Scorers — {selected}",
        color="avg_per_match",
        color_continuous_scale="Viridis",
        hover_data=["matches", "sixes", "fours"],
        labels={"batter": "Batsman", "total_runs": "Total Runs"}
    )
    fig_bat.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bat, use_container_width=True)

    st.subheader("Most Sixes in IPL History")
    q_six = run_query("""
        SELECT batter,
               SUM(CASE WHEN batsman_runs = 6 THEN 1 ELSE 0 END) AS sixes,
               COUNT(DISTINCT match_id) AS matches,
               ROUND(SUM(CASE WHEN batsman_runs=6 THEN 1.0 ELSE 0 END)
                     / COUNT(DISTINCT match_id), 2) AS sixes_per_match
        FROM deliveries
        GROUP BY batter
        ORDER BY sixes DESC
        LIMIT 10
    """)
    fig_six = px.bar(
        q_six, x="batter", y="sixes",
        title="Most Sixes in IPL History",
        color="sixes_per_match",
        color_continuous_scale="Reds",
        hover_data=["matches", "sixes_per_match"]
    )
    fig_six.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_six, use_container_width=True)

    st.subheader("Full Data Table")
    st.dataframe(df_bat, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════
# PAGE 3 — BOWLING ANALYSIS
# ══════════════════════════════════════════════════════════════════════════
elif page == "🎯 Bowling Analysis":

    st.title("🎯 Bowling Analysis")

    bowling_sql = """
        SELECT bowler,
               COUNT(DISTINCT match_id)                                        AS matches,
               SUM(CASE WHEN dismissal_kind NOT IN
                   ('run out','retired hurt','obstructing the field')
                   AND dismissal_kind IS NOT NULL THEN 1 ELSE 0 END)           AS wickets,
               ROUND(SUM(total_runs) * 6.0 / COUNT(*), 2)                     AS economy,
               ROUND(COUNT(*) * 1.0 /
                     NULLIF(SUM(CASE WHEN dismissal_kind NOT IN
                     ('run out','retired hurt') AND dismissal_kind IS NOT NULL
                     THEN 1 ELSE 0 END), 0), 1)                                AS strike_rate
        FROM deliveries
        WHERE extras_type NOT IN ('wides','noballs')
           OR extras_type IS NULL
        GROUP BY bowler
        HAVING COUNT(*) >= 300 AND wickets >= 20
        ORDER BY wickets DESC
        LIMIT 15
    """
    df_bowl = run_query(bowling_sql)

    col1, col2 = st.columns(2)
    with col1:
        fig_w = px.bar(
            df_bowl, x="bowler", y="wickets",
            title="Top Wicket Takers",
            color="economy",
            color_continuous_scale="Reds_r"
        )
        fig_w.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_w, use_container_width=True)

    with col2:
        fig_e = px.scatter(
            df_bowl, x="economy", y="wickets",
            text="bowler",
            title="Economy vs Wickets",
            size="matches",
            labels={"economy": "Economy Rate", "wickets": "Total Wickets"}
        )
        st.plotly_chart(fig_e, use_container_width=True)

    st.subheader("Full Bowling Data")
    st.dataframe(df_bowl, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════
# PAGE 4 — VENUE INSIGHTS
# ══════════════════════════════════════════════════════════════════════════
elif page == "🏟️ Venue Insights":

    st.title("🏟️ Venue Insights")

    venue_sql = """
        SELECT venue, city,
               COUNT(*) AS total_matches,
               ROUND(SUM(CASE WHEN result='runs' THEN 1.0 ELSE 0 END)
                     / COUNT(*) * 100, 1) AS bat_first_win_pct
        FROM matches
        WHERE winner IS NOT NULL
        GROUP BY venue, city
        HAVING COUNT(*) >= 8
        ORDER BY total_matches DESC
    """
    df_venue = run_query(venue_sql)

    fig_v = px.scatter(
        df_venue,
        x="total_matches", y="bat_first_win_pct",
        size="total_matches", text="city",
        title="Venues: Matches Hosted vs Batting First Win %",
        labels={
            "total_matches":    "Matches Hosted",
            "bat_first_win_pct":"Batting First Win %"
        }
    )
    fig_v.add_hline(
        y=50, line_dash="dash",
        annotation_text="50% — Equal Advantage Line"
    )
    st.plotly_chart(fig_v, use_container_width=True)

    st.subheader("Venue Data Table")
    st.dataframe(df_venue, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════
# PAGE 5 — CUSTOM SQL QUERY
# ══════════════════════════════════════════════════════════════════════════
elif page == "🔍 Custom SQL Query":

    st.title("🔍 Write Your Own SQL Query")
    st.markdown("**Tables available:** `matches` &nbsp;|&nbsp; `deliveries`")

    with st.expander("📋 See available columns"):
        c1, c2 = st.columns(2)
        with c1:
            st.write("**matches columns:**")
            st.write(run_query("PRAGMA table_info(matches)")["name"].tolist())
        with c2:
            st.write("**deliveries columns:**")
            st.write(run_query("PRAGMA table_info(deliveries)")["name"].tolist())

    default_sql = """SELECT season, COUNT(*) AS matches
FROM matches
GROUP BY season
ORDER BY season"""

    user_sql = st.text_area("Write SQL Query:", value=default_sql, height=150)

    if st.button("▶ Run Query"):
        try:
            result = run_query(user_sql)
            st.success(f"✅ Query returned {len(result)} rows")
            st.dataframe(result, use_container_width=True)
            numeric_cols = result.select_dtypes("number").columns.tolist()
            if len(numeric_cols) >= 1 and len(result.columns) >= 2:
                st.bar_chart(
                    result.set_index(result.columns[0])[numeric_cols[0]]
                )
        except Exception as e:
            st.error(f"❌ SQL Error: {str(e)}")