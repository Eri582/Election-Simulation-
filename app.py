import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Decision Desk Simulator", layout="wide", initial_sidebar_state="expanded")

# --- 1. DATABASES & DYNAMIC OPPONENT GENERATION ---
@st.cache_data(ttl=86400)
def fetch_live_midnight_polls():
    np.random.seed(datetime.now().day)
    return np.random.normal(0, 1.4)

midnight_poll_shift = fetch_live_midnight_polls()

@st.cache_data
def load_constitutional_map():
    states = {
        "Alabama": [-15.0, 9], "Alaska": [-8.0, 3], "Arizona": [-1.5, 11], "California": [22.0, 54],
        "Colorado": [8.0, 10], "Florida": [-4.0, 30], "Georgia": [-1.1, 16], "Michigan": [1.2, 15],
        "Nevada": [0.1, 6], "North Carolina": [-1.8, 16], "Ohio": [-6.0, 17], "Pennsylvania": [0.5, 19],
        "Texas": [-5.0, 40], "Wisconsin": [-0.2, 10]
    }
    return pd.DataFrame.from_dict(states, orient='index', columns=['Lean', 'EV']).reset_index().rename(columns={'index': 'State'})

df_map = load_constitutional_map()

# --- 2. GAME STATE MEMORY INITIALIZATION ---
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.player_alive = True
    st.session_state.day = 1
    st.session_state.approval = 50.0  
    st.session_state.cash = 10000.0
    st.session_state.staff = 0
    st.session_state.submitted = False
    st.session_state.campaign_boost = 0.0
    
    # NEW: Opponent Logic Trackers
    st.session_state.opponent_name = ""
    st.session_state.opponent_cash = 10000.0
    st.session_state.opponent_policy = ""
    st.session_state.opponent_boost = 0.0

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.markdown("### 📊 DECISION MONITOR")
st.sidebar.metric("Your Approval Rating", f"{st.session_state.approval:.1f}%")
st.sidebar.metric("Your Campaign Wallet", f"${st.session_state.cash:,.2f}")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Calendar Tracker:** Day {st.session_state.day} / 30")
if st.sidebar.button("⏩ Advance Clock (24-Hour Cycle)"):
    if st.session_state.day < 30:
        st.session_state.day += 1
        # Simulated NPC AI Logic: Opponent funds and adjustments grow over time
        if st.session_state.submitted and st.session_state.day > 14:
            st.session_state.opponent_cash += np.random.randint(2000, 7000)
            st.session_state.opponent_boost += np.random.choice([0.1, 0.3, 0.5])
    else:
        st.session_state.day = 1
        st.session_state.campaign_boost = 0.0
        st.session_state.opponent_boost = 0.0
    st.rerun()

if st.sidebar.button("🗑️ Reset Engine Data"):
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

if not st.session_state.player_alive:
    st.error("❌ Disqualified: Campaign failed to secure office.")
    st.stop()

# --- 4. TOP DISPLAY BANNER ---
st.title("🗳️ Election Prediction Office Simulation")

if st.session_state.day <= 14:
    current_phase = "1. Announcement Window (Weeks 1 & 2)"
elif st.session_state.day <= 21:
    current_phase = "2. Party Nominations & Primaries (Week 3)"
elif st.session_state.day <= 28:
    current_phase = "3. General Election Offensive (Week 4)"
elif st.session_state.day == 29:
    current_phase = "4. ELECTION NIGHT COMPILING"
else:
    current_phase = "5. Executive Governance Term"

st.info(f"**Active Timeline Environment:** {current_phase}")

# --- 5. MODULAR TABS ---
tab_profile, tab_actions, tab_head_to_head = st.tabs(["👤 Candidate Setup", "📢 Active Campaign Matrix", "📊 Head-to-Head Intelligence"])

# TAB 1: CHARACTER CREATION (With Dynamic Bot Generation)
with tab_profile:
    st.subheader("Step 1: File Candidate Declaration Forms")
    if not st.session_state.submitted:
        col1, col2 = st.columns(2)
        with col1:
            p_name = st.text_input("Enter Your Candidate Name", "Patriot One")
            p_party = st.selectbox("Select Your Party", ["Blue Coalition", "Red Coalition"])
            p_office = st.selectbox("Target Seat Selection", ["Governor", "U.S. Senate", "U.S. House"])
        with col2:
            p_state = st.selectbox("Select State", df_map["State"].tolist())
                
        if st.button("📝 Submit Official Filings"):
            st.session_state.submitted = True
            st.session_state.p_name = p_name
            st.session_state.p_party = p_party
            st.session_state.p_office = p_office
            st.session_state.p_state = p_state
            
            # GENERATE OPPONENT DATA DYNAMICALLY BASED ON CHOICE
            if p_party == "Blue Coalition":
                st.session_state.opponent_name = f"🤖 Rep_Bot_{p_state[:3].upper()}"
                st.session_state.opponent_policy = "Aggressive Tax Cuts & Supply-Side Balance"
            else:
                st.session_state.opponent_name = f"🤖 Dem_Bot_{p_state[:3].upper()}"
                st.session_state.opponent_policy = "Increased Social Spending & Green Energy Mandates"
                
            st.success("Candidacy verified. Opponent generated.")
            st.rerun()
    else:
        st.info(f"Registered Profile: **{st.session_state.p_name}** vs **{st.session_state.opponent_name}**.")

# TAB 2: ACTIONS
with tab_actions:
    if not st.session_state.submitted:
        st.warning("Please complete Step 1 and register your profile to unlock tracking operations.")
    else:
        if st.session_state.day <= 14:
            st.subheader("📢 Announcement Window Options")
            explore_topic = st.text_input("Type your core exploratory platform message:")
            if st.button("🚀 Push Message to Wire Streams"):
                st.session_state.approval += np.random.choice([-1.5, 2.5]) + midnight_poll_shift
                st.success("Message pushed.")

        elif st.session_state.day <= 21:
            st.subheader("🗳️ Primary Election Week Operations")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Hire Local Field Directors (-$2,500)"):
                    if st.session_state.cash >= 2500:
                        st.session_state.cash -= 2500
                        st.session_state.staff += 1
                        st.session_state.approval += 2.0
                    else: st.error("Insufficient Funds.")
            with col_b:
                if st.button("Run Daily Fundraising Drive"):
                    gain = np.random.randint(3000, 7000)
                    st.session_state.cash += gain
                    st.success(f"Acquired +${gain:,}")

        elif st.session_state.day <= 28:
            st.subheader("📢 General Election Campaign Offensive")
            policy_speech = st.text_input("Type exactly what issue you are pitching to voters:")
            if st.button("🎤 Deliver Stump Speech"):
                modifier = np.random.choice([-2.0, 3.5]) + (st.session_state.staff * 0.1)
                st.session_state.approval += modifier
                st.session_state.campaign_boost += max(0.0, modifier * 0.1)
                st.write(f"Voter feedback logged: {modifier:+.2f}%")

        elif st.session_state.day == 29:
            st.subheader("📊 Decision Desk: Running Projections")
            target_state_lean = df_map[df_map["State"] == st.session_state.p_state]["Lean"].values[0]
            
            sims = 10000
            wins = 0
            for _ in range(sims):
                noise = np.random.normal(0, 3.0)
                if st.session_state.p_party == "Blue Coalition":
                    score = target_state_lean + midnight_poll_shift + noise + st.session_state.campaign_boost - st.session_state.opponent_boost
                    if score > 0: wins += 1
                else:
                    score = target_state_lean + midnight_poll_shift + noise - st.session_state.campaign_boost + st.session_state.opponent_boost
                    if score < 0: wins += 1
            
            prob = (wins / sims) * 100
            st.metric("Your Calculated Win Probability", f"{prob:.1f}%")
            
            if prob >= 50.0:
                st.balloons()
                st.success("🏆 VICTORY PROJECTED!")
                if st.button("🛡️ Assume Governance"):
                    st.session_state.day = 30
                    st.rerun()
            else:
                st.error("❌ DEFEAT PROJECTED.")
                st.session_state.player_alive = False
                st.rerun()
        else:
            st.subheader("💼 Constitutional Governance Room")
            st.write("You are handling executive issues. Enact mandates to govern.")
            if st.button("🔄 File Papers for Next Re-election Term"):
                st.session_state.day = 1
                st.session_state.submitted = False
                st.rerun()

# TAB 3: NEW HEAD-TO-HEAD DISPLAY (ANSWERING YOUR QUESTION)
with tab_head_to_head:
    if not st.session_state.submitted:
        st.warning("Register your candidate in Tab 1 to unlock the Intelligence Ledger.")
    else:
        st.subheader("🕵️ Live Campaign Intelligence Matrix")
        st.write("Real-time comparison between your operation and the opponent bot.")
        
        # 1. SIDE-BY-SIDE PROFILE CARDS
        card1, card2 = st.columns(2)
        with card1:
            st.info(f"""
            ### 👤 YOUR CAMPAIGN
            * **Candidate Name:** {st.session_state.p_name}
            * **Party Alignment:** {st.session_state.p_party}
            * **Available Funds:** ${st.session_state.cash:,.2f}
            * **Campaign Momentum Mod:** +{st.session_state.campaign_boost:.2f}
            """)
        with card2:
            st.error(f"""
            ### {st.session_state.opponent_name} (NPC)
            * **Candidate Name:** Opposition Challenger Unit
            * **Party Alignment:** {"Red Coalition" if st.session_state.p_party == "Blue Coalition" else "Blue Coalition"}
            * **Available Funds:** ${st.session_state.opponent_cash:,.2f}
            * **Campaign Momentum Mod:** +{st.session_state.opponent_boost:.2f}
            * **Core Policy Agenda:** {st.session_state.opponent_policy}
            """)
            
        st.markdown("---")
        
        # 2. HEAD-TO-HEAD POLLING MONITOR
        st.subheader("📊 Dynamic Head-to-Head Polling Index")
        
        # Base math calculating the current poll line
        base_lean = df_map[df_map["State"] == st.session_state.p_state]["Lean"].values[0]
        
        # Calculate your raw position vs opponent position
        if st.session_state.p_party == "Blue Coalition":
            your_poll = 50.0 + base_lean + midnight_poll_shift + st.session_state.campaign_boost - st.session_state.opponent_boost
        else:
            your_poll = 50.0 - base_lean + midnight_poll_shift + st.session_state.campaign_boost - st.session_state.opponent_boost
            
        # Bound cleanly between 0-100
        your_poll = max(5.0, min(95.0, your_poll))
        opponent_poll = 100.0 - your_poll
        
        # Visual Progress Bars representing real polls
        st.write(f"**{st.session_state.p_name} (You):** {your_poll:.1f}%")
        st.progress(int(your_poll))
        
        st.write(f"**{st.session_state.opponent_name} (Opponent):** {opponent_poll:.1f}%")
        st.progress(int(opponent_poll))
