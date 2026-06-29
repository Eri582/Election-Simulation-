import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- CONFIGURATION & LAYOUT ---
st.set_page_config(page_title="Statecraft Grand Strategy", layout="wide", initial_sidebar_state="expanded")

# --- 1. THE 50-STATE & REGIONAL GEOGRAPHY DATA DESK ---
@st.cache_data
def load_geopolitical_database():
    states = {
        "Alabama": [-15.0, 9], "Alaska": [-8.0, 3], "Arizona": [-1.5, 11], "Arkansas": [-18.0, 6],
        "California": [22.0, 54], "Colorado": [8.0, 10], "Connecticut": [15.0, 7], "Delaware": [14.0, 3],
        "Florida": [-4.0, 30], "Georgia": [-1.1, 16], "Hawaii": [20.0, 4], "Idaho": [-22.0, 4],
        "Illinois": [12.0, 19], "Indiana": [-11.0, 11], "Iowa": [-8.0, 6], "Kansas": [-12.0, 6],
        "Kentucky": [-16.0, 8], "Louisiana": [-14.0, 8], "Maine": [6.0, 4], "Maryland": [25.0, 10],
        "Massachusetts": [26.0, 11], "Michigan": [1.2, 15], "Minnesota": [6.0, 10], "Mississippi": [-12.0, 6],
        "Missouri": [-10.0, 10], "Montana": [-12.0, 4], "Nebraska": [-13.0, 5], "Nevada": [0.1, 6],
        "New Hampshire": [5.0, 4], "New Jersey": [14.0, 14], "New Mexico": [5.0, 5], "New York": [20.0, 28],
        "North Carolina": [-1.8, 16], "North Dakota": [-25.0, 3], "Ohio": [-6.0, 17], "Oklahoma": [-22.0, 7],
        "Oregon": [10.0, 8], "Pennsylvania": [0.5, 19], "Rhode Island": [18.0, 4], "South Carolina": [-10.0, 9],
        "South Dakota": [-20.0, 3], "Tennessee": [-15.0, 11], "Texas": [-5.0, 40], "Utah": [-18.0, 6],
        "Vermont": [28.0, 3], "Virginia": [6.0, 13], "Washington": [14.0, 12], "West Virginia": [-28.0, 4],
        "Wisconsin": [-0.2, 10], "Wyoming": [-30.0, 3]
    }
    return pd.DataFrame.from_dict(states, orient='index', columns=['Lean', 'EV']).reset_index().rename(columns={'index': 'State'})

df_states = load_geopolitical_database()

# --- 2. ENGINE INITIALIZATION & INITIAL MEMORY CACHE ---
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.day = 1
    st.session_state.player_alive = True
    st.session_state.submitted = False
    
    # Player Stats
    st.session_state.approval = 50.0
    st.session_state.cash = 12000.0
    st.session_state.momentum = 0.0
    st.session_state.primary_won = False
    
    # Multi-Bot System Cache (Guarantees at least 3 active competitors per primary)
    st.session_state.primary_bots = []
    st.session_state.general_opponent = {}

# --- 3. FLOATING DASHBOARD MONITOR ---
st.sidebar.markdown("### 📊 CAMPAIGN HEADQUARTERS")
st.sidebar.metric("Your Core Approval", f"{st.session_state.approval:.1f}%")
st.sidebar.metric("Campaign Account Liquidity", f"${st.session_state.cash:,.2f}")
st.sidebar.metric("Campaign Momentum Mod", f"+{st.session_state.momentum:.2f}")

st.sidebar.markdown("---")
st.sidebar.markdown(f"🗓️ **Calendar Cycle:** Day {st.session_state.day} / 30")

if st.sidebar.button("⏩ Move Campaign Clock Forward 24h"):
    if st.session_state.day < 30:
        st.session_state.day += 1
        # Dynamic AI Bot activity updates out of view
        if st.session_state.submitted:
            for bot in st.session_state.primary_bots:
                bot["cash"] += np.random.randint(1500, 4500)
                bot["polls"] += np.random.normal(0.2, 0.5)
    else:
        st.session_state.day = 1
        st.session_state.submitted = False
        st.session_state.primary_won = False
    st.rerun()

if st.sidebar.button("🗑️ Wipe Campaign Data Logs"):
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

if not st.session_state.player_alive:
    st.error("❌ Campaign Terminated: Your operation was unable to clear the structural requirements to remain viable on the ballot.")
    st.stop()

# --- 4. TOP ENGINE METRICS BANNER ---
st.title("🏛️ STATECRAFT: The Grand Competitive Political RPG")

# Map exact stages around the calendar
if st.session_state.day <= 14:
    phase_str = "Phase 1: Exploratory Announcement & Early Stump Campaigns (Weeks 1 & 2)"
elif st.session_state.day <= 21:
    phase_str = "Phase 2: Closed Party Primary Battles (Week 3 - Top 4 Elimination)"
elif st.session_state.day <= 28:
    phase_str = "Phase 3: General Election Strategic Offensive (Week 4)"
else:
    phase_str = "Phase 4: Executive Governance & Crisis Management"

st.info(f"🛰️ **Active Chrono-Phase:** {phase_str}")

# --- 5. WORKBENCH GRAPHICS TABS ---
tab_setup, tab_trail, tab_map_desk = st.tabs(["👤 Core Character Profiling", "📢 Ground Campaign Trail", "🗺️ Dynamic Polling Ledger Map"])

# TAB 1: FILING FOR OFFICE & SELECTING TICKETS
with tab_setup:
    st.subheader("Filing Office: Register Candidacy & Ticket Configuration")
    if not st.session_state.submitted:
        c1, c2 = st.columns(2)
        with c1:
            p_name = st.text_input("Register Candidate Legal Name", "Patriot One")
            p_party = st.selectbox("Select Your Faction Alignment", ["Blue Faction", "Red Faction"])
            p_office = st.selectbox("Target Public Office Tier", ["Presidential Campaign", "Governor", "U.S. Senate", "U.S. House", "State Legislature"])
        with c2:
            p_state = st.selectbox("Select Core Base Jurisdiction State", df_states["State"].tolist())
            
            # Recruitable Running Mates inside the game universe
            vp_roster = ["Senator Analytics (Boosts Media Actions)", "Governor Charisma (Boosts Townhall Actions)", "Tech Mogul Bot (Boosts Funding Drives)"]
            chosen_vp = st.selectbox("Select Your Running Mate / VP Pick", vp_roster)
            
        if st.button("📝 Formally Submit Registration & Lock Ticket"):
            st.session_state.submitted = True
            st.session_state.p_name = p_name
            st.session_state.p_party = p_party
            st.session_state.p_office = p_office
            st.session_state.p_state = p_state
            st.session_state.chosen_vp = chosen_vp
            
            # GUARANTEE 3 DISTINCT PRIMARY BOTS AT LEAST NO MATTER THE RACE
            st.session_state.primary_bots = [
                {"name": f"🤖 Challenger_Bot_Alpha", "cash": 8000.0, "polls": 20.0, "stance": "Moderate Realism Approach"},
                {"name": f"🤖 Challenger_Bot_Beta", "cash": 11000.0, "polls": 22.0, "stance": "Aggressive Faction Populism"},
                {"name": f"🤖 Challenger_Bot_Gamma", "cash": 9500.0, "polls": 18.0, "stance": "Systemic Policy Technocrat"}
            ]
            st.success("Filing completed! 3 competitive AI Primary Challengers generated instantly.")
            st.rerun()
    else:
        st.success(f"🔒 Balloting Locked: **{st.session_state.p_name}** running for **{st.session_state.p_office}** across **{st.session_state.p_state}**.")

# TAB 2: ACTIVE GAMEPLAY ACTION DESK
with tab_trail:
    if not st.session_state.submitted:
        st.warning("Register your candidate profile in Tab 1 to unlock strategic field deployment options.")
    else:
        # TIMELINE STAGE OPERATIONS
        if st.session_state.day <= 14:
            st.subheader("📢 Stage 1: Announcement & Early Target Selection")
            st.write("You are free to build foundational awareness. Select your targeted geography and action types below:")
            
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                if st.session_state.p_office == "Presidential Campaign":
                    target_zone = st.selectbox("Select Target Campaign State Strategy", df_states["State"].tolist())
                else:
                    target_zone = st.selectbox("Select Target Regional County Zone", ["Metro Urban Center", "Suburban Growth Ring", "Rural Farm Outskirts"])
            with col_g2:
                action_type = st.selectbox("Select Action Type", ["Grassroots Door-to-Door", "Local High-School Townhall", "Regional Media Advertising Blitz"])
                
            pitch_text = st.text_input("Type your core platform talking point for this demographic:")
            
            if st.button("⚡ Execute Field Strategy"):
                if len(pitch_text) > 3:
                    cost = 1500 if "Blitz" in action_type else 500
                    if st.session_state.cash >= cost:
                        st.session_state.cash -= cost
                        boost = np.random.choice([1.2, 2.8, 3.5])
                        st.session_state.approval += boost
                        st.session_state.momentum += (boost * 0.1)
                        st.success(f"Campaign action completed across {target_zone}! Core Approval adjusted by +{boost:.2f}%")
                    else: st.error("Insufficient Funding reserves to execute.")

        elif st.session_state.day <= 21:
            st.subheader("🗳️ Stage 2: Direct Party Primary Battle Arena")
            st.write("Review your standing against the 3 guaranteed primary bots. You must execute fundraising and debates to win the nomination.")
            
            # Display Side-by-Side Competitive Standing
            st.markdown("#### Primary Election Leaderboard Index")
            player_primary_poll = 40.0 + (st.session_state.momentum * 2)
            
            # Simple clean dataframe tracking the 3 primary bots vs you
            lead_data = {
                "Candidate Name": [f"👤 {st.session_state.p_name} (You)"] + [b["name"] for b in st.session_state.primary_bots],
                "Current Primary Polling Share": [f"{player_primary_poll:.1f}%"] + [f"{b['polls']:.1f}%" for b in st.session_state.primary_bots],
                "Campaign Funds": [f"${st.session_state.cash:,.2f}"] + [f"${b['cash']:,.2f}" for b in st.session_state.primary_bots],
                "Declared Agenda": ["Player Platform Selection"] + [b["stance"] for b in st.session_state.primary_bots]
            }
            st.dataframe(pd.DataFrame(lead_data), use_container_width=True)
            
            st.markdown("---")
            st.markdown("##### Execute Daily Primary Operations")
            if st.button("💰 Organize Small-Dollar Fundraising Event"):
                gain = np.random.randint(4000, 8500)
                st.session_state.cash += gain
                st.success(f"Acquired +${gain:,} from grassroots networks.")
                
            if st.button("⚔️ Participate in Televised Primary Debate Panel"):
                perf = np.random.choice([-4.0, 1.5, 6.0])
                st.session_state.momentum += (perf * 0.1)
                st.write(f"Debate completed. Momentum shift adjustment: {perf:+.2f}")
                
            if st.session_state.day == 21:
                st.markdown("### 🔔 POLLS CLOSING: Computing Primary Tallies")
                if player_primary_poll > 30.0: # Simplistic requirement to beat out 3 split bots
                    st.session_state.primary_won = True
                    st.success("🏆 CONGRATULATIONS: You won the nomination! Advancing past the primary window to the general campaign grid.")
                else:
                    st.error("❌ DEFEATED IN PRIMARY: You failed to clear the required margin against the 3 rival bots. Game Over.")
                    st.session_state.player_alive = False

        elif st.session_state.day <= 28:
            st.subheader("📢 Stage 3: General Election Offensive Grid")
            if not st.session_state.primary_won:
                st.warning("You did not secure the nomination forms. Disqualified from General Election access.")
            else:
                st.write(f"The party tickets are set! You and your ticketmate **{st.session_state.chosen_vp}** are facing the opposition's general election infrastructure.")
                
                # Campaign Action Row
                g_target = st.selectbox("Select Key Swing Corridor to Spend Resources On", ["Urban Hub", "Suburban Collars", "Rural Outposts"])
                if st.button("🎤 Deliver High-Impact Policy Speech"):
                    g_boost = np.random.choice([-1.0, 4.0]) + (st.session_state.momentum * 0.5)
                    st.session_state.approval += g_boost
                    st.success(f"Stump delivery completed. Feedback adjustments: {g_boost:+.2f}%")

        elif st.session_state.day == 29:
            st.subheader("📊 Stage 4: Decision Desk Mainframe Processing")
            state_lean = df_states[df_states["State"] == st.session_state.p_state]["Lean"].values[0]
            
            sims = 10000
            wins = 0
            for _ in range(sims):
                noise = np.random.normal(0, 3.2)
                if st.session_state.p_party.startswith("Blue"):
                    score = state_lean + noise + (st.session_state.approval - 50.0) + st.session_state.momentum
                    if score > 0: wins += 1
                else:
                    score = state_lean + noise - (st.session_state.approval - 50.0) - st.session_state.momentum
                    if score < 0: wins += 1
                    
            prob = (wins / sims) * 100
            st.metric("Your Consolidated Win Probability Output", f"{prob:.1f}%")
            
            if prob >= 50.0:
                st.balloons()
                st.success("🏆 VICTORY DECLARED: Your organization has successfully cleared the path to secure public office.")
                if st.button("🛡️ Assume Office & Enact Mandates"):
                    st.session_state.day = 30
                    st.rerun()
            else:
                st.error("❌ DEFEAT: Projections indicate your strategy was unable to pierce the structural limits of the district lean.")
                st.session_state.player_alive = False

        else:
            st.subheader("💼 Stage 5: Executive Governance Chambers")
            st.write("You are the sitting authority. Balance regional interests to maintain steady approval scores.")
            if st.button("🔄 File Intent to Seek Re-election next Term"):
                st.session_state.day = 1
                st.session_state.submitted = False
                st.session_state.primary_won = False
                st.rerun()

# TAB 3: DYNAMIC LEDGER & GRAPHICS MAPPING
with tab_map_desk:
    if st.session_state.submitted and st.session_state.p_office != "Presidential Campaign":
        st.subheader(f"🗺️ Regional County Poll Mapping Matrix: {st.session_state.p_state}")
        st.write("Tracking the localized county-level battleground margins inside your running jurisdiction:")
        
        # Calculate localized county fluctuations
        base_lean = df_states[df_states["State"] == st.session_state.p_state]["Lean"].values[0]
        
        county_data = {
            "County/District Belt": ["Metro Core Urban Grid", "Suburban Residential Ring", "Rural Frontier Corridors"],
            "Electoral/Turnout Weight": ["45% of Population", "35% of Population", "20% of Population"],
            "Base Lean Profile": ["Leans Blue (+12.0)", "Highly Competitive (Swing)", "Leans Red (-18.0)"],
            "Your Active Polling Margin vs Opponent": [
                f"{50.0 + base_lean + st.session_state.approval - 50.0:.1f}% vs {50.0 - base_lean:.1f}%",
                f"{st.session_state.approval:.1f}% vs {100.0 - st.session_state.approval:.1f}%",
                f"{50.0 + base_lean + (st.session_state.approval - 60.0):.1f}% vs {50.0 - base_lean + 10.0:.1f}%"
            ]
        }
        st.table(pd.DataFrame(county_data))
    else:
        st.subheader("🗺️ National Electoral Map Overview (Presidential Level)")
        st.write("Tracking all 50 structural state configurations and baseline lean indicators read by the simulation engine processing modules:")
        st.dataframe(df_states, use_container_width=True)
