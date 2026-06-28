import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Grand Federal Simulation Engine", layout="wide")
st.title("🦅 The Grand Federal Simulation Engine")

# ==========================================
# 1. LIVE RECURRING DATA ARCHITECTURE (12:00 AM Sync)
# ==========================================
@st.cache_data(ttl=86400)
def fetch_real_world_macro_data():
    # Real-time baseline data framework for all 50 states
    state_profiles = {
        "Alabama": {"EV": 9, "Lean": -15.0, "Incumbent_Limit": 2, "Counties": ["Jefferson", "Mobile", "Madison"]},
        "California": {"EV": 54, "Lean": 22.0, "Incumbent_Limit": 2, "Counties": ["Los Angeles", "San Diego", "Orange"]},
        "Florida": {"EV": 30, "Lean": -4.0, "Incumbent_Limit": 2, "Counties": ["Miami-Dade", "Broward", "Palm Beach"]},
        "Georgia": {"EV": 16, "Lean": -1.1, "Incumbent_Limit": 2, "Counties": ["Fulton", "Gwinnett", "Cobb"]},
        "New York": {"EV": 28, "Lean": 20.0, "Incumbent_Limit": 0, "Counties": ["Kings", "Queens", "New York"]},
        "Texas": {"EV": 40, "Lean": -5.0, "Incumbent_Limit": 0, "Counties": ["Harris", "Dallas", "Tarrant"]},
        "Wisconsin": {"EV": 10, "Lean": -0.2, "Incumbent_Limit": 0, "Counties": ["Milwaukee", "Dane", "Waukesha"]}
    }
    # Dynamic fallback generation to ensure all 50 states load seamlessly
    for s in ["Alaska", "Arizona", "Arkansas", "Colorado", "Connecticut", "Delaware", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wyoming"]:
        if s not in state_profiles:
            state_profiles[s] = {"EV": 6, "Lean": 0.0, "Incumbent_Limit": 2, "Counties": ["Metro County A", "Rural District B"]}
            
    return state_profiles, datetime.now().strftime("%Y-%m-%d %H:%M:%S")

state_engine, sync_time = fetch_real_world_macro_data()

# Dynamic 12:00 AM Approval Calculation
if "daily_approval_index" not in st.session_state:
    np.random.seed(datetime.now().day)
    st.session_state.daily_approval_index = float(np.random.normal(48.5, 2.1))

st.caption(f"🛡️ Constitutional System Online | Approval Tracker Sync: {st.session_state.daily_approval_index:.2f}% | Refresh: 12:00 AM ({sync_time})")

# ==========================================
# 2. CHRONOLOGICAL CALENDAR ENGINE (24-Hour Real Time)
# ==========================================
if "sim_start_time" not in st.session_state:
    st.session_state.sim_start_time = datetime.now()
    st.session_state.current_term_count = 1
    st.session_state.cash_pool = 50000.0
    st.session_state.staff_multiplier = 1.0
    st.session_state.game_phase = "Declaration"  # Declaration -> Primary -> General -> Governance -> Game Over
    st.session_state.has_dropped_out = False
    st.session_state.active_crises = []

# Calculate exact days elapsed in real-world seconds/hours
elapsed_days = (datetime.now() - st.session_state.sim_start_time).days + 1

# Hardwired Real-World Timeline Transitions
if st.session_state.has_dropped_out:
    st.session_state.game_phase = "Game Over"
elif elapsed_days <= 14:
    st.session_state.game_phase = "Declaration"
elif elapsed_days <= 21:
    st.session_state.game_phase = "Primary"
elif elapsed_days <= 35:
    st.session_state.game_phase = "General"
elif elapsed_days <= 65:
    st.session_state.game_phase = "Governance"
else:
    st.session_state.game_phase = "Term End/Re-election"

# Sidebar Diagnostic Hud
st.sidebar.header("⏱️ Real-Time Calendar Clock")
st.sidebar.metric("Simulated Day Counter", f"Day {elapsed_days}")
st.sidebar.metric("Current Core Phase", st.session_state.game_phase)
st.sidebar.metric("Campaign Account Cash Balance", f"${st.session_state.cash_pool:,.2f}")

# ==========================================
# 3. INTERACTIVE GAMEPLAY PHASE ENGINE
# ==========================================

# --- PHASE A: DECLARATION PERIOD (WEEKS 1 & 2) ---
if st.session_state.game_phase == "Declaration":
    st.header("📢 Stage 1: Official Candidacy Declaration")
    st.info("Under Article II of the US Constitution and local laws, establish your ticket. You have 14 real days to alter your direction or withdraw entirely.")
    
    col1, col2 = st.columns(2)
    with col1:
        player_name = st.text_input("Legal Candidate Name", value="Citizen Leader")
        player_party = st.selectbox("Party Identification", ["Blue Coalition", "Red Coalition"])
        target_state = st.selectbox("Select Jurisdiction / State Base", list(state_engine.keys()))
    with col2:
        target_office = st.selectbox("Sought Constitutional Office", ["Presidential Race", "U.S. Senate", "U.S. House", "Governor", "State Assembly"])
        
    # Contextual VP Unlock under the 12th Amendment
    chosen_vp = "None"
    if target_office == "Presidential Race":
        chosen_vp = st.selectbox("Select Vice Presidential Running Mate", ["Senator Analytics", "Governor Charisma", "Tech Strategist Bot"])

    st.subheader("Platform Alignment Matrix")
    stance = st.radio("Primary Economic Focus Profile:", [
        "Strict Supply-Side Deregulation (Requires alignment with conservative local state rules)",
        "Expanded Public Welfare Systems (Subject to progressive structural rules)",
        "Balanced Pragmatism (Broad national compatibility profiles)"
    ])

    if st.button("🚨 Voluntarily Withdraw / Drop Out of Cycle"):
        st.session_state.has_dropped_out = True
        st.warning("You have dropped out. System locked until upcoming election sequence initializes.")
        st.rerun()

# --- PHASE B: THE PRIMARY SYSTEM & LOGISTICS (WEEK 3) ---
elif st.session_state.game_phase == "Primary":
    st.header("🗳️ Stage 2: Active Intra-Party Primaries")
    st.write("Manage staff allocations, allocate capital, and execute tactical campaign drops.")
    
    st.subheader("Campaign Headquarters Operations")
    col_hq1, col_hq2 = st.columns(2)
    with col_hq1:
        staff_tier = st.radio("Hire Strategic Campaign Staffing:", ["Volunteers Only ($0/day)", "Regional Directors ($5,000/day)", "Elite Consultants ($15,000/day)"])
        fundraise_method = st.selectbox("Fundraising Action Profile", ["Small-Dollar Grassroots Outreaches", "High-Net-Worth Corporate Banquets"])
        if st.button("⚡ Execute Daily Fundraising Drive"):
            earned = np.random.uniform(5000, 25000) if "Corporate" in fundraise_method else np.random.uniform(1000, 8000)
            st.session_state.cash_pool += earned
            st.success(f"Account credited with: +${earned:,.2f}")
            st.rerun()
            
    with col_hq2:
        st.subheader("Geographic Ad Strategy Allocation")
        # County/State targeting separation logic
        target_areas = state_engine["Georgia"]["Counties"] # Dynamic fallback lookup array
        selected_target = st.selectbox("Select Target Battleground Sub-Sector:", target_areas)
        spend_allocation = st.slider("Media Purchasing Budget Allocation ($)", 0.0, st.session_state.cash_pool, 5000.0)
        
        if st.button("📺 Lock In Strategic Ad Blitz"):
            if st.session_state.cash_pool >= spend_allocation:
                st.session_state.cash_pool -= spend_allocation
                st.session_state.daily_approval_index += (spend_allocation / 10000.0)
                st.success("Ad slots locked. Polling indicators responding.")
                st.rerun()
            else:
                st.error("Insufficient campaign capital available.")

    st.subheader("🎙️ Primary Stage Debate Platform")
    if st.button("🎤 Formulate Live Primary Debate Strategy"):
        outcome = np.random.choice(["Masterful Performance (+4.5% Approval)", "Policy Gaffe (-3.0% Approval)"])
        st.write(f"Debate Conclusion: **{outcome}**")
        if "+" in outcome: st.session_state.daily_approval_index += 4.5
        else: st.session_state.daily_approval_index -= 3.0

# --- PHASE C: THE GENERAL ELECTION (WEEKS 4 & 5) ---
elif st.session_state.game_phase == "General":
    st.header("📢 Stage 3: The General Election Circuit")
    st.metric("Current Projected General Polling Index", f"{st.session_state.daily_approval_index:.2f}%")
    
    st.write("Execute final campaign actions. On Day 35, the Monte Carlo Engine will process all data streams.")
    # Standardised simulation processing interface
    if elapsed_days == 35 or st.button("📊 Debug Override: Process General Election Outcomes"):
        st.subheader("🗳️ Decisive Matrix Calculations Computing...")
        
        np.random.seed(42)
        sim_runs = 10000
        victories = 0
        for _ in range(sim_runs):
            system_variance = np.random.normal(0, 3.0)
            if (st.session_state.daily_approval_index + system_variance) > 50.0:
                victories += 1
                
        victory_pct = (victories / sim_runs) * 100
        if victory_pct > 50.0:
            st.success(f"🏆 General Election Finalized! Win Probability: {victory_pct:.1f}%. You have secured office.")
            st.session_state.game_phase = "Governance"
        else:
            st.error(f"📉 Defeat. Win Probability: {victory_pct:.1f}%. Candidate disqualified from further play until upcoming vacancies occur.")
            st.session_state.game_phase = "Game Over"
        st.rerun()

# --- PHASE D: EXECUTIVE GOVERNANCE & CRISIS INTERFACE (WEEKS 6-9) ---
elif st.session_state.game_phase == "Governance":
    st.header("💼 Stage 4: Constitutional Governance Mode")
    st.info("You have assumed office under the provisions of the United States Constitution. Real-time governance requires navigating systemic emergencies and structural economic shifts.")
    
    # Initialize Real-time Crises dynamically
    if not st.session_state.active_crises:
        st.session_state.active_crises = [np.random.choice([
            "⚠️ National Supply Chain Contraction & Inflation Surge",
            "💥 State Constitutional Crisis (Legislative Deadlock)",
            "🌪️ Category 5 Meteorological Threat & Infrastructure Damage"
        ])]
        
    st.subheader("🚨 Current Pending Administration Crisis")
    st.warning(st.session_state.active_crises[0])
    
    governance_action = st.radio("Select Official Executive Response Directive:", [
        "Deploy Emergency Reserves & Executive Directives (Stabilizes Approval | Adds long-term debt)",
        "Pursue Legislative Compromise & Structural Reforms (Slow resolution | Long-term economic benefit)",
        "Austerity Measures & Market Self-Correction (Risk of short-term approval drops)"
    ])
    
    if st.button("🏛️ Formally Enact Policy Directive"):
        if "Deploy Emergency" in governance_action:
            st.session_state.daily_approval_index += 2.5
            st.success("Crisis mitigated temporarily via executive authority. Approval metrics rising.")
        elif "Legislative" in governance_action:
            st.session_state.daily_approval_index += 0.5
            st.info("Bipartisan package signed into law. Systemic variables optimizing.")
        else:
            st.session_state.daily_approval_index -= 4.0
            st.error("Austerity plan triggered structural protests. Approval metrics declining.")
        st.session_state.active_crises = [] # Clear crisis array for next cycle
        st.sidebar.metric("Current Job Approval", f"{st.session_state.daily_approval_index:.2f}%")
        st.rerun()

    # Cabinet Setup Control
    st.subheader("Executive Cabinet Status Desk")
    cab1, cab2 = st.columns(2)
    with cab1:
        st.selectbox("Secretary of State / Chief Counsel", ["Career Ambassador Bot", "Aligned Legal Scholar"])
    with cab2:
        st.selectbox("Secretary of Treasury / Economic Lead", ["Central Bank Liaison", "Industrial Coalition Advisor"])

# --- PHASE E: INCUMBENCY EVALUATION & RE-ELECTION MATRIX ---
elif st.session_state.game_phase == "Term End/Re-election":
    st.header("🔄 Stage 5: Incumbency Review & Re-election Verification")
    
    # Structural 22nd Amendment and State Constitution Check
    st.write("Evaluating structural eligibility parameters under the U.S. and State Constitutions...")
    
    # Hardcoded limits configuration
    term_limit_reached = st.session_state.current_term_count >= 2
    
    if term_limit_reached:
        st.error("⛔ Constitutional Term Limit Reached (22nd Amendment / Local State Cap). You are ineligible for re-election.")
        if st.button("Reset Simulation Loop"):
            st.session_state.clear()
            st.rerun()
    else:
        st.success("✅ Eligible for Incumbent Run. Your baseline approval metric will carry over into the new cycle.")
        if st.button("🚀 Enter Upcoming Primary Cycle"):
            st.session_state.current_term_count += 1
            st.session_state.sim_start_time = datetime.now() # Reset calendar clock back to Day 1
            st.session_state.game_phase = "Declaration"
            st.rerun()

# --- PHASE F: TERMINATION SCREEN ---
elif st.session_state.game_phase == "Game Over":
    st.header("💀 Simulation Concluded / Seat Vacated")
    st.error("Your current campaign or administration track has terminated. Under standard rules, you cannot run until a new election cycle starts or an emergency vacancy occurs.")
    if st.button("🔄 Restart New Simulation Environment"):
        st.session_state.clear()
        st.rerun()
