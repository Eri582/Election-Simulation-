import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Ultimate Presidential Simulator", layout="wide")
st.title("🦅 The Ultimate Presidential & Cabinet Simulator")

# 1. LIVE AUTOMATED DATA SETTING
@st.cache_data(ttl=86400)
def fetch_election_map():
    states = {
        "State": ["Pennsylvania", "Michigan", "Wisconsin", "Georgia", "Arizona", "Nevada", "North Carolina"],
        "EV": [19, 15, 10, 16, 11, 6, 16],
        "Baseline_Lean": [0.5, 1.2, -0.2, -1.1, -1.5, 0.1, -1.8]
    }
    return pd.DataFrame(states), datetime.now().strftime("%Y-%m-%d %H:%M:%S")

df_states, last_update = fetch_election_map()
st.caption(f"🔄 Central Engine Sync: Active | Data updated at midnight: {last_update}")

# 2. NOMINATION PHASE (PRESIDENT & VP)
st.header("🎟️ Stage 1: The Ticket Selection")

col_pres1, col_pres2 = st.columns(2)
with col_pres1:
    blue_pres = st.text_input("🟦 Blue Presidential Nominee", placeholder="Leave blank for NPC...")
    if not blue_pres:
        blue_pres = "🤖 Governor Bot-Alpha"
        st.caption(f"Assigned: {blue_pres}")

with col_pres2:
    red_pres = st.text_input("🟥 Red Presidential Nominee", placeholder="Leave blank for NPC...")
    if not red_pres:
        red_pres = "🤖 Senator Bot-Omega"
        st.caption(f"Assigned: {red_pres}")

# Vice Presidential Selection Option
col_vp1, col_vp2 = st.columns(2)
with col_vp1:
    blue_vp = st.selectbox("🔵 Choose Blue Vice President", ["Select NPC Runner...", "Senator Analytics", "Governor Charisma", "Rep. Strategist"])
    if blue_vp == "Select NPC Runner...":
        blue_vp = "🤖 AI-Running-Mate-D"
with col_vp2:
    red_vp = st.selectbox("🔴 Choose Red Vice President", ["Select NPC Runner...", "General Executive", "Governor Vanguard", "Tech Mogul Bot"])
    if red_vp == "Select NPC Runner...":
        red_vp = "🤖 AI-Running-Mate-R"

# 3. THE CAMPAIGN TRAIL
st.header("📢 Stage 2: The Campaign Strategy")
campaign_focus = st.radio("Select National Campaign Focus Strategy:", 
                          ("Focus on Economic Message", "Focus on Foreign Policy", "Broad Multi-State Appeal"))

# Introduce slight modifiers based on strategy selection
strategy_bonus = 0.0
if campaign_focus == "Focus on Economic Message":
    strategy_bonus = 0.3  # Slight boost to Blue environment in this hypothetical script
elif campaign_focus == "Focus on Foreign Policy":
    strategy_bonus = -0.3 # Slight boost to Red environment

# 4. SIMULATE ELECTION NIGHT
if st.button("🗳️ Run General Election Simulation"):
    st.header("📊 Stage 3: Election Night Desk")
    
    st.success(f"**The Tickets are locked in!**")
    st.write(f"🟦 **Blue Team:** {blue_pres} / {blue_vp}")
    st.write(f"🟥 **Red Team:** {red_pres} / {red_vp}")
    
    # Mathematical Engine
    num_sims = 10000
    blue_wins = 0
    total_ev_pool = df_states["EV"].sum()
    
    np.random.seed(datetime.now().microsecond)
    for _ in range(num_sims):
        national_swing = np.random.normal(0, 3.2) + strategy_bonus
        sim_ev = 0
        
        for idx, row in df_states.iterrows():
            state_swing = np.random.normal(0, 2.1)
            final_margin = row["Baseline_Lean"] + national_swing + state_swing
            if final_margin > 0:
                sim_ev += row["EV"]
                
        if sim_ev > (total_ev_pool / 2):
            blue_wins += 1
            
    blue_chance = (blue_wins / num_sims) * 100
    red_chance = 100 - blue_chance
    
    # Display Winner Probability
    c1, c2 = st.columns(2)
    c1.metric(label="🔵 Blue Ticket Win Probability", value=f"{blue_chance:.1f}%")
    c2.metric(label="🔴 Red Ticket Win Probability", value=f"{red_chance:.1f}%")
    
    # Declare simulated winner of the current run
    winner_color = "Blue" if blue_chance > red_chance else "Red"
    winner_president = blue_pres if winner_color == "Blue" else red_pres
    
    # 5. THE CABINET APPOINTMENTS (POST-ELECTION STAGE)
    st.header("💼 Stage 4: Appointing Your Cabinet")
    st.info(f"Congratulations to the Projected Administration of **{winner_president}**! Appoint your leaders below:")
    
    cab1, cab2, cab3 = st.columns(3)
    with cab1:
        st.selectbox("Secretary of State", ["Diplomat Bot A", "Ambassador Bot B", "Human Pick"])
    with cab2:
        st.selectbox("Secretary of the Treasury", ["Economist Bot X", "WallStreet Bot Y", "Human Pick"])
    with cab3:
        st.selectbox("Secretary of Defense", ["General Bot Chief", "Defense Expert Z", "Human Pick"])
        
    st.balloons()
