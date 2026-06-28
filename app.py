import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Grand Strategy Simulator", layout="wide", page_icon="🏛️")
st.title("🏛️ The Constitutional Multi-Office Simulator")

# ==========================================
# 1. LIVE AUTOMATED DATA & MIDNIGHT DESK SYNC
# ==========================================
@st.cache_data(ttl=86400)
def generate_daily_market_and_approval_shifts():
    # Changes every single calendar day at 12:00 AM outside of the game speed
    np.random.seed(datetime.now().day)
    base_national_mood = np.random.normal(0, 1.5)
    market_index = 10000 + int(np.random.normal(0, 200))
    return base_national_mood, market_index

midnight_mood, dow_index = generate_daily_market_and_approval_shifts()
st.caption(f"🔄 Real-Time Core Feed: Active | Midnight Polling Shift: {midnight_mood:+.2f} | Economic Index: {dow_index} pts")

@st.cache_data
def load_all_50_states():
    state_baselines = {
        "Alabama": [-15.0], "Alaska": [-8.0], "Arizona": [-1.5], "Arkansas": [-18.0], "California": [22.0],
        "Colorado": [8.0], "Connecticut": [15.0], "Delaware": [14.0], "Florida": [-4.0], "Georgia": [-1.1],
        "Hawaii": [20.0], "Idaho": [-22.0], "Illinois": [12.0], "Indiana": [-11.0], "Iowa": [-8.0],
        "Kansas": [-12.0], "Kentucky": [-16.0], "Louisiana": [-14.0], "Maine": [6.0], "Maryland": [25.0],
        "Massachusetts": [26.0], "Michigan": [1.2], "Minnesota": [6.0], "Mississippi": [-12.0], "Missouri": [-10.0],
        "Montana": [-12.0], "Nebraska": [-13.0], "Nevada": [0.1], "New Hampshire": [5.0], "New Jersey": [14.0],
        "New Mexico": [5.0], "New York": [20.0], "North Carolina": [-1.8], "North Dakota": [-25.0], "Ohio": [-6.0],
        "Oklahoma": [-22.0], "Oregon": [10.0], "Pennsylvania": [0.5], "Rhode Island": [18.0], "South Carolina": [-10.0],
        "South Dakota": [-20.0], "Tennessee": [-15.0], "Texas": [-5.0], "Utah": [-18.0], "Vermont": [28.0],
        "Virginia": [6.0], "Washington": [14.0], "West Virginia": [-28.0], "Wisconsin": [-0.2], "Wyoming": [-30.0]
    }
    return pd.DataFrame(list(state_baselines.items()), columns=["State", "Baseline_Lean"])

df_all_states = load_all_50_states()

# ==========================================
# 2. STATE PERSISTENT SYSTEM (SESSION STATE)
# ==========================================
if "game_day" not in st.session_state:
    st.session_state.game_day = 1
if "campaign_momentum" not in st.session_state:
    st.session_state.campaign_momentum = 0.0
if "approval_rating" not in st.session_state:
    st.session_state.approval_rating = 50.0
if "is_disqualified" not in st.session_state:
    st.session_state.is_disqualified = False
if "terms_served" not in st.session_state:
    st.session_state.terms_served = 0
if "has_won_election" not in st.session_state:
    st.session_state.has_won_election = False
if "crisis_event" not in st.session_state:
    st.session_state.crisis_event = None

# ==========================================
# 3. CONSTITUTIONAL CHECK & CORE TRACKER
# ==========================================
st.sidebar.header("⚖️ Constitutional Rules Desk")
st.sidebar.markdown("""
* **Art. II, Sec. 1 / 22nd Amendment:** Max 2 Terms allowed for Presidential Office execution.
* **Art. I Eligibility:** Minimum tenure requirements mapped automatically based on target chamber.
* **Defeat Clause:** If you lose the Primary or General Election, your campaign is bricked until the next month cycle starts.
""")

st.sidebar.divider()
st.sidebar.subheader("📅 Executive Calendar")

# Phase Calendar Calculations
day = st.session_state.game_day
if st.session_state.is_disqualified:
    phase_title = "❌ DISQUALIFIED / LOCKOUT PHASE"
elif day <= 14:
    phase_title = "📢 Weeks 1-2: Exploration & Candidate Announcement"
elif day <= 21:
    phase_title = "🗳️ Week 3: Party Primaries"
elif day <= 35:
    phase_title = "📣 Weeks 4-5: General Campaign Window"
elif day == 36:
    phase_title = "📊 ELECTION NIGHT DESK"
else:
    phase_title = "🦅 Phase 5: Active Office Governance Term"

st.sidebar.info(f"**Day:** {day} / 60\n\n**Status:** {phase_title}")

# Calculate current approval rating combining active efforts and natural midnight shifts
current_approval = np.clip(st.session_state.approval_rating + midnight_mood + (st.session_state.campaign_momentum * 0.1), 0.0, 100.0)
st.sidebar.metric("Your Real-Time Approval Rating", f"{current_approval:.1f}%")

if st.sidebar.button("⏩ Advance Calendar 1 Day"):
    if st.session_state.game_day < 60:
        st.session_state.game_day += 1
        # Randomly trigger realistic domestic crises during governance phase
        if st.session_state.game_day > 36 and st.session_state.has_won_election and np.random.rand() > 0.6:
            crises = [
                {"name": "Supply Chain / Inflation Surge", "impact": -5.0, "desc": "Energy prices spike nationwide, raising manufacturing costs."},
                {"name": "Cyber Breach on Utility Grid", "impact": -8.0, "desc": "Critical financial systems encounter targeted hostile infrastructure attacks."},
                {"name": "Severe Interstate Flood Crisis", "impact": -3.0, "desc": "Logistical nodes compromised due to catastrophic regional storms."}
            ]
            st.session_state.crisis_event = np.random.choice(crises)
    else:
        # Month End Reset Term Loop
        st.session_state.game_day = 1
        st.session_state.campaign_momentum = 0.0
        st.session_state.crisis_event = None
        if not st.session_state.has_won_election:
            st.session_state.is_disqualified = False
    st.rerun()

if st.sidebar.button("🔄 Full Reset Simulator"):
    st.session_state.clear()
    st.rerun()

# ==========================================
# GAME SCREENS BASED ON THE TIMELINE
# ==========================================
if st.session_state.is_disqualified:
    st.error("❌ **Access Denied:** Your campaign platform failed to secure the required votes. Under Constitutional Rules, you are locked out of executive management until the current office terms expire and a fresh cycle opens next month.")
    st.stop()

# ------------------------------------------
# STAGE 1: ANNOUNCEMENT WINDOW (DAYS 1-14)
# ------------------------------------------
if day <= 14:
    st.header("📢 Stage 1: Candidate Announcement & Strategy Setup")
    st.write("You are inside the exploratory phase. You can safely change races, shift offices, or choose to drop out.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        player_name = st.text_input("Register Name", value="Statesman")
        player_party = st.selectbox("Party Alignment", ["Blue Faction (Democrat)", "Red Faction (Republican)"])
    with col2:
        player_state = st.selectbox("Select Target Jurisdiction", df_all_states["State"].tolist())
        player_office = st.selectbox("Select Target Seat", ["Presidential Race", "Governor", "U.S. Senate", "U.S. House"])
    with col3:
        chosen_vp = st.selectbox("Select Running Mate / Lieutenant", ["Senator Analytics", "Governor Charisma", "Rep. Strategist", "General Executive"])

    # Term Limit Validity Checks
    if player_office == "Presidential Race" and st.session_state.terms_served >= 2:
        st.error("⛔ **CONSTITUTIONAL BAR:** Under the 22nd Amendment, you have hit your maximum term limit for the Presidency and cannot announce your candidacy.")
    else:
        st.success(f"✔️ Ready: You are exploring an announcement for **{player_state} {player_office}**.")
        
    st.markdown("### Choose Core Stance Platform")
    stance = st.radio("Primary Structural Policy:", [
        "Pro-Growth Deregulation (Boosts baseline performance in Red-leaning districts)",
        "Social Infrastructure Mandates (Boosts baseline performance in Blue-leaning districts)",
        "Centrist Deficit Management (Appeals evenly across split margins)"
    ])
    
    if st.button("🛑 Drop Out of Race Immediately"):
        st.session_state.is_disqualified = True
        st.rerun()

# ------------------------------------------
# STAGE 2: PARTY PRIMARIES (DAYS 15-21)
# ------------------------------------------
elif day <= 21:
    st.header("🗳️ Stage 2: Closed Party Primaries")
    st.write("Your announcement window has slammed shut. Your race is locked. If no other player entered, active NPC bots have auto-filled the opposing tickets.")
    
    # Simple primary math to simulate getting through the base faction hurdle
    primary_roll = np.random.normal(52, 5) + (midnight_mood * 2)
    st.info(f"Current internal tracking shows you securing roughly **{primary_roll:.1f}%** of early caucus projections.")
    
    if day == 21:
        if primary_roll < 50.0:
            st.error("💥 You lost the primary race to an intra-party NPC challenger!")
            st.session_state.is_disqualified = True
        else:
            st.success("🎉 You secured the official party nomination! Advancing to the General Ballot.")

# ------------------------------------------
# STAGE 3: THE CAMPAIGN TRAIL (DAYS 22-35)
# ------------------------------------------
elif day <= 35:
    st.header("📣 Stage 3: The General Campaign Window")
    st.write("All nationwide seats have been populated with competitive AI Bots. Run your platform to shape real-time approvals.")
    
    campaign_action = st.radio("Choose Daily Campaign Operation:", [
        "Purchase Local Broadcast Advertisements (+0.4 Momentum)",
        "Deploy Ground Staff for Voter Turnout Operation (+0.6 State Momentum)"
    ])
    
    if st.button("⚡ Execute Campaign Push"):
        st.session_state.campaign_momentum += 0.5
        st.session_state.approval_rating = np.clip(st.session_state.approval_rating + 1.2, 0.0, 100.0)
        st.success("Campaign data updated! Review your new approval rating tracking on the sidebar menu.")

# ------------------------------------------
# STAGE 4: ELECTION NIGHT (DAY 36)
# ------------------------------------------
elif day == 36:
    st.header("📊 Stage 4: Election Night Data Command")
    st.write("The 10,000-iteration Monte Carlo engine is running the voter models right now...")
    
    # Compute simulation incorporating the user inputs
    sims = 10000
    success_runs = 0
    np.random.seed(1776)
    
    for _ in range(sims):
        voter_noise = np.random.normal(0, 3.0)
        # Combine midnight tracking data with player actions
        final_score = 0.0 + midnight_mood + st.session_state.campaign_momentum + voter_noise
        if final_score > -1.0:
            success_runs += 1
            
    win_chance = (success_runs / sims) * 100
    st.metric("Your Final Projected Chance of Victory", f"{win_chance:.1f}%")
    
    if win_chance >= 50.0:
        st.balloons()
        st.success("🏆 VICTORY CONGRUENT. You have cleared the constitutional hurdle and won your election!")
        st.session_state.has_won_election = True
        st.session_state.terms_served += 1
    else:
        st.error("📉 DEFEAT. Your campaign team was unable to secure the target margins.")
        st.session_state.is_disqualified = True

# ------------------------------------------
# STAGE 5: GOVERNANCE & CRISIS (DAYS 37-60)
# ------------------------------------------
else:
    st.header("🦅 Stage 5: Active Governance & Crisis Center")
    st.write("You are officially executing the functions of your office. Real-world structural tracking will test your approvals.")
    
    # Display the cabinet appointment options
    st.subheader("Manage Your Cabinet Teams")
    c_a, c_b = st.columns(2)
    with c_a:
        st.selectbox("Appoint Chief of Staff", ["Strategic Agent AI", "Veteran Policy Bot"])
    with c_b:
        st.selectbox("Appoint Secretary of State", ["Diplomatic Unit Alpha", "International Trade Expert"])
        
    # Crisis Event Engine Trigger
    if st.session_state.crisis_event:
        st.warning(f"⚠️ **REAL-TIME EMERGENCY:** {st.session_state.crisis_event['name']}")
        st.write(st.session_state.crisis_event['desc'])
        
        choice = st.radio("Select Emergency Resolution Directive:", [
            "Authorize Emergency Funding Drops (Stabilizes approval, risks future inflation)",
            "Enact Regulatory Executive Action (Strong partisan match, alienates center)"
        ])
        
        if st.button("📜 Sign Crisis Directive"):
            st.session_state.approval_rating = np.clip(st.session_state.approval_rating + st.session_state.crisis_event['impact'] + 4.0, 0.0, 100.0)
            st.session_state.crisis_event = None
            st.success("Directive implemented. Check your updated approval data.")
            st.rerun()
    else:
        st.info("☀️ Current Domestic Status: Stable. No active emergency events reported in your jurisdiction today.")
        
    st.divider()
    if st.session_state.game_day >= 55:
        st.subheader("🔁 Constitutional Re-Election Evaluation")
        st.write("The current term is concluding. If eligible, you can run for re-election or choose to step aside.")
        if st.session_state.terms_served >= 2:
            st.error("🚫 You have hit your maximum structural term limits and must retire at the end of the month.")
        else:
            if st.button("🗳️ File for Re-Election Next Cycle"):
                st.session_state.game_day = 1
                st.session_state.campaign_momentum = 0.0
                st.session_state.has_won_election = False
                st.success("Candidacy filed! The simulator calendar will reset shortly.")
                st.rerun()
