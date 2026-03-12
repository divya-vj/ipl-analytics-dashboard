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

# ── Custom CSS Styling ─────────────────────────────────────────────────────
st.markdown("""
<style>

/* ── Main background ── */
.main {
    background-color: #0E1117;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1A56A8, #0D2B5E);
    border-radius: 10px;
    padding: 15px 20px;
    border: 1px solid #2A5FC8;
}
[data-testid="metric-container"] label {
    color: #A0C4FF !important;
    font-size: 13px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* ── Sidebar styling ── */
[data-testid="stSidebar"] {
    background-color: #0D2B5E;
    border-right: 2px solid #1A56A8;
}
[data-testid="stSidebar"] * {
    color: #DCE8FA !important;
}

/* ── Page title ── */
h1 {
    color: #1A56A8 !important;
    border-bottom: 2px solid #1A56A8;
    padding-bottom: 10px;
}

/* ── Subheaders ── */
h2, h3 {
    color: #2A6ED4 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1A56A8;
    border-radius: 8px;
}

/* ── Buttons ── */
.stButton button {
    background-color: #1A56A8;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 8px 24px;
    font-weight: 600;
    transition: background-color 0.3s;
}
.stButton button:hover {
    background-color: #0D2B5E;
    color: white;
}

/* ── Success message ── */
.stSuccess {
    background-color: #0A4A25 !important;
    border-left: 4px solid #1A7A42 !important;
}

/* ── Error message ── */
.stError {
    background-color: #4A0A0A !important;
    border-left: 4px solid #C04A00 !important;
}

/* ── Text area ── */
.stTextArea textarea {
    background-color: #1A1A2E;
    color: #CDD6F4;
    border: 1px solid #1A56A8;
    font-family: 'Courier New', monospace;
    font-size: 13px;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background-color: #1A1A2E;
    border: 1px solid #1A56A8;
    color: white;
}

/* ── Horizontal rule ── */
hr {
    border-color: #1A56A8;
}

</style>
""", unsafe_allow_html=True)

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
    # ── Key Insights Box ──────────────────────────────────────────────────
    st.subheader("🔑 Key Insights From The Data")
    ins1, ins2, ins3 = st.columns(3)

    with ins1:
        st.markdown("""
        <div style='background:#0A4A25; border-left:4px solid #1A7A42;
                    padding:15px; border-radius:8px;'>
            <b style='color:#6FCF97'>📈 Scores Are Rising</b><br>
            <span style='color:#ccc; font-size:13px'>
            Average first innings score jumped from 150 in 2009 to 190 in 2024.
            IPL has become significantly more aggressive over 17 seasons.
            </span>
        </div>
        """, unsafe_allow_html=True)

    with ins2:
        st.markdown("""
        <div style='background:#0D2B5E; border-left:4px solid #1A56A8;
                    padding:15px; border-radius:8px;'>
            <b style='color:#A0C4FF'>🪙 Toss Barely Matters</b><br>
            <span style='color:#ccc; font-size:13px'>
            Toss winner wins only 50.8% of matches — essentially a coin flip.
            Team quality matters far more than winning the toss.
            </span>
        </div>
        """, unsafe_allow_html=True)

    with ins3:
        st.markdown("""
        <div style='background:#3B1560; border-left:4px solid #7B3FA0;
                    padding:15px; border-radius:8px;'>
            <b style='color:#D4A0FF'>🏆 Most Dominant Team</b><br>
            <span style='color:#ccc; font-size:13px'>
            Mumbai Indians won 13 matches in 2013 — the most wins by any
            team in a single IPL season in history.
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

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

    # ── Top Scorer Per Season ─────────────────────────────────────────────
    st.subheader("🏆 Top Scorer Each Season — Window Function Analysis")
    q_top = run_query("""
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
    fig_top = px.bar(
        q_top,
        x="season", y="season_runs",
        text="batter",
        title="Top Run Scorer Per Season",
        labels={"season":"Season","season_runs":"Runs","batter":"Batsman"},
        color="season_runs",
        color_continuous_scale="Viridis"
    )
    fig_top.update_traces(textposition="outside", textfont_size=10)
    fig_top.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_top, use_container_width=True)
    # ── Player Comparison Feature ─────────────────────────────────────────
    st.subheader("⚔️ Compare Two Batsmen")
    all_batters = run_query("""
        SELECT DISTINCT batter FROM deliveries
        ORDER BY batter
    """)["batter"].tolist()

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        player1 = st.selectbox("Select Player 1:", all_batters,
                               index=all_batters.index("V Kohli")
                               if "V Kohli" in all_batters else 0)
    with col_p2:
        player2 = st.selectbox("Select Player 2:", all_batters,
                               index=all_batters.index("RG Sharma")
                               if "RG Sharma" in all_batters else 1)

    def get_player_stats(name):
        return run_query(f"""
            SELECT
                SUM(batsman_runs)                                           AS total_runs,
                COUNT(DISTINCT match_id)                                    AS matches,
                ROUND(SUM(batsman_runs)*1.0/COUNT(DISTINCT match_id),1)    AS avg_per_match,
                SUM(CASE WHEN batsman_runs=6 THEN 1 ELSE 0 END)            AS sixes,
                SUM(CASE WHEN batsman_runs=4 THEN 1 ELSE 0 END)            AS fours,
                MAX(batsman_runs)                                           AS highest_in_delivery
            FROM deliveries
            WHERE batter = '{name}'
        """)

    s1 = get_player_stats(player1).iloc[0]
    s2 = get_player_stats(player2).iloc[0]

    comp_data = {
        "Stat":         ["Total Runs","Matches","Avg Per Match","Sixes","Fours"],
        player1:        [s1.total_runs, s1.matches, s1.avg_per_match,
                         s1.sixes, s1.fours],
        player2:        [s2.total_runs, s2.matches, s2.avg_per_match,
                         s2.sixes, s2.fours],
    }
    import pandas as pd
    comp_df = pd.DataFrame(comp_data)
    st.dataframe(comp_df, use_container_width=True)

    fig_comp = px.bar(
        comp_df.melt(id_vars="Stat", var_name="Player", value_name="Value"),
        x="Stat", y="Value", color="Player", barmode="group",
        title=f"{player1} vs {player2} — Career Comparison",
        color_discrete_sequence=["#1A56A8","#C04A00"]
    )
    st.plotly_chart(fig_comp, use_container_width=True)

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



# ── Footer ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; color:#555; font-size:12px; padding:10px'>
        IPL Analytics Dashboard · Built with Python, SQLite, Streamlit & Plotly ·
        Data: IPL 2007–2024 · 1095 Matches · 260,920 Deliveries
    </div>
    """,
    unsafe_allow_html=True
)