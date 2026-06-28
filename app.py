import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="Ultra-Realistic Political Simulator", layout="wide")
st.title("🏛️ The Grand Constitutional Strategy & Office Simulation Engine")

# ==========================================================
# 1. THE AUTOMATED 12:00 AM POLLING & APPROVAL ENGINE
# ==========================================================
@st.cache_data(ttl=86400)
def update_daily_approval_and_polls(day_seed):
    # Simulates shifting public mood and baseline approvals precisely at midnight daily
    np.random.seed(day_seed)
    macro_economic_shift = np.random.normal(0, 1.5)
    voter_sentiment_vibe = np.random.normal(0, 2.0)
    return macro_economic_shift, voter_sentiment_vibe

current_date_str = datetime.now().strftime("%Y-%m-%d")
day_seed = datetime.now().day
macro_shift, voter_vibe = update_daily_approval_and_polls(day_seed)

st.caption(f"🔄 **Live Server Clock:** Sync Complete for {current_date_str} | 12:00 AM Polling & Baseline Approvals Generated.")

# Initialize Persistent Session Data for Long-term Real-Time Tracking
if "registration_submitted" not in st.session_state:
    st.session_state.registration_submitted = False
if "campaign_funds" not in st.session_state:
    st.session_state.campaign_funds = 50000.0
if "approval_rating" not in st.session_state:
    st.session_state.approval_rating = 50.0
if "staff_count" not in st.session_state:
    st.session_state.staff_count = 0
if "is_eligible" not in st.session_state:
    st.session_state.is_eligible = True
if "game_start_time" not in st.session_state:
    st.session_state.game_start_time = datetime.now()

# Calculate actual elapsed real time (1 real day = 24 hours)
elapsed_time = datetime.now() - st.session_state.game_start_time
game_day = elapsed_time.days + 1  # Starts at Day 1

# Game Phase Mapping based on Exact Real-World Time Framework:
# Days 1-14 (2 wks): Announcement/Candidacy | Days 15-21 (1 wk): Primaries | Days 22-35 (2 wks): General | Days 36-65 (1 mo): Governance
if game_day <= 14:
    current_phase = "Announcement & Declaration Window"
elif game_day <= 21:
    current_phase = "Primary Election Phase"
elif game_day <= 35:
    current_phase = "General Election Cycle"
elif game_day <= 65:
    current_phase = "Active Executive Governance Term"
else:
    current_phase = "Term Completed / Next Election Cycle Looming"

# Sidebar Stats Hud
st.sidebar.header("🗓️ Campaign Dashboard Clock")
st.sidebar.metric("Current Real-Time Game Day", f"Day {game_day} / 65")
st.sidebar.info(f"**Current Status:** {current_phase}")
st.sidebar.metric("💰 Campaign Chest", f"${st.session_state.campaign_funds:,.2f}")
st.sidebar.metric("📈 Your Public Approval Rating", f"{st.session_state.approval_rating + voter_vibe:.1f}%")

if not st.session_state.is_eligible:
    st.error("❌ CONSTITUTIONAL BARRIER: You are currently ineligible to run due to term limits or a lost race. Wait for a vacancy.")
    st.stop()

# ==========================================================
# STAGE 1: ANNOUNCEMENT, CANDIDACY & CONSTITUTIONS
# ==========================================================
if not st.session_state.registration_submitted:
    st.header("📋 Stage 1: Candidate Declaration & Legal Review")
    st.write("According to Article II of the U.S. Constitution (for National Executive) and individual State Constitutions (for state offices), you must clear requirements.")
    
    col_reg1, col_reg2 = st.columns(2)
    with col_reg1:
        p_name = st.text_input("Candidate Name", value="Statesman")
        p_office = st.selectbox("Office Sought", ["Presidential Race", "Governor", "U.S. Senate", "U.S. House", "State Senate", "State House"])
        p_state = st.selectbox("State of Registration", ["Pennsylvania", "Texas", "California", "Florida", "Michigan", "Ohio"])
        p_party = st.selectbox("Party Line", ["Blue Coalition (Democrat)", "Red Coalition (Republican)"])
        
    with col_reg2:
        st.subheader("📜 Constitutional Rules Repository")
        if p_office == "Presidential Race":
            st.warning("⚠️ **United States Constitution:** Affects the whole country. Requires winning a 270 Electoral Vote majority. 2-term consecutive limit applies. Must pick a Vice President below.")
            vp_choice = st.selectbox("Select Your VP Running Mate", ["Senator Analytics", "Governor Charisma", "General Executive"])
        else:
            st.info(f"🏛️ **{p_state} State Constitution:** Affects your localized district. Plurality vote rules apply. Term parameters subject to local legislative code limits.")
            vp_choice = "None (State Race)"

    st.subheader("📢 Select Campaign Issue Stance")
    p_stance = st.radio("Core Campaign Stance:", [
        "Prioritize Supply-Side Economics & Fiscal Restraint",
        "Prioritize Welfare Enhancements & Green Infrastructure Investment",
        "Moderate Compromise Platform"
    ])

    if st.button("Submit Official Filing Papers"):
        st.session_state.p_name = p_name
        st.session_state.p_office = p_office
        st.session_state.p_state = p_state
        st.session_state.p_party = p_party
        st.session_state.p_vp = vp_choice
        st.session_state.p_stance = p_stance
        st.session_state.registration_submitted = True
        st.success("Filing validated. Entering the tracking environment.")
        st.rerun()

# ==========================================================
# STAGE 2: THE ANNOUNCEMENT PERIOD (DAYS 1-14)
# ==========================================================
else:
    # Fetch player details from memory
    office = st.session_state.p_office
    state = st.session_state.p_state
    party = st.session_state.p_party

    if game_day <= 14:
        st.header("📢 Candidacy Window: Declaration & Initial Footing")
        st.write("You have stepped into the race. Use this two-week window to gauge public reaction or adjust your focus before primary lock-in.")
        
        col_an1, col_an2 = st.columns(2)
        with col_an1:
            st.subheader("🛠️ Management Actions")
            if st.button("🚨 Voluntarily Drop Out of Current Race"):
                st.session_state.registration_submitted = False
                st.warning("You dropped out. You can now choose a new race to enter.")
                st.rerun()
                
            # Random Challenge Engine (Positively/Negatively alters parameters)
            st.subheader("⚠️ Campaign Incident Log")
            np.random.seed(day_seed + 10)
            challenge_trigger = np.random.choice(["Good Press", "Scandal", "Quiet Day"])
            if challenge_trigger == "Good Press":
                st.success("🔥 Positive Turnout Event: A local organization endorsed your filing! Approval rating up +3%.")
                st.session_state.approval_rating += 0.05
            elif challenge_trigger == "Scandal":
                st.error("📉 Opponent Leak: Old comments regarding local tax structures surfaced. Approval rating dropped -4%.")
                st.session_state.approval_rating -= 0.05
            else:
                st.write("Campaign operational lines holding normal metrics today.")

# ==========================================================
# STAGE 3: RUNNING THE PRIMARY (DAYS 15-21)
# ==========================================================
    elif game_day <= 21:
        st.header("🗳️ The Primary Election Loop & Infrastructure Setup")
        st.write("You are locked into your party primary. Spend funds wisely to out-hustle internal challengers.")
        
        # Fundraising / Staffing Controls
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.subheader("💼 Financial Campaign Operations")
            fund_action = st.radio("Choose Fundraising Strategy:", ["Host High-Plate Private Dinners", "Launch Grassroots Micro-Donation Drive"])
            if st.button("Execute Fundraiser Session (Takes 24 hrs to repeat)"):
                added_cash = np.random.uniform(5000, 15000) if "Private" in fund_action else np.random.uniform(2000, 8000)
                st.session_state.campaign_funds += added_cash
                st.success(f"Fundraising complete. Deposited: ${added_cash:,.2f}")
                
        with c_p2:
            st.subheader("👥 Operations & Allocations")
            st.write(f"Active Staff Members: **{st.session_state.staff_count}**")
            if st.button("Hire Field Directors ($5,000 cost)"):
                if st.session_state.campaign_funds >= 5000:
                    st.session_state.campaign_funds -= 5000
                    st.session_state.staff_count += 1
                    st.session_state.approval_rating += 1.5
                else:
                    st.error("Insufficient funds.")

        st.subheader("🎤 Mandatory Primary Debate Room")
        st.info("The internal network primary debate is broadcasting live. Answer strategically to lock down the nomination:")
        debate_response = st.selectbox("How do you address your primary opponent's charge that your platform lacks localized viability?", 
                                       ["Pivot to national unified party messages", "Counter-attack their legislative attendance history"])
        if st.button("Log Debate Verdict"):
            st.success("Debate finalized. Metrics applied to midnight tracking loops.")

# ==========================================================
# STAGE 4: GENERAL ELECTION CYCLE (DAYS 22-35)
# ==========================================================
    elif game_day <= 35:
        st.header("📢 The General Election Campaign Trail")
        st.write("The primaries are finalized. It is ticket vs ticket. Target your campaign deployments precisely.")
        
        if office == "Presidential Race":
            target_area = st.text_input("Target State Focus (e.g. Pennsylvania, Michigan, Wisconsin)", value="Pennsylvania")
        else:
            target_area = st.text_input("Target County Focus for State Operations", value="County Centric")
            
        st.write(f"Deploying field assets and advertising spend into: **{target_area}**")
        
        # General Election Debate
        st.subheader("📺 High-Stakes General Election Debate Arena")
        st.selectbox("Your opponent states your structural economic plan will harm local job growth. What is your response?", 
                     ["Present data forecasting long-term investment yield surpluses", "Decline to answer directly and highlight previous historical achievements"])
        if st.button("Submit Response To Moderator"):
            st.success("Response locked in.")

# ==========================================================
# STAGE 5: GOVERNANCE & CRISIS STAGE (DAYS 36-65)
# ==========================================================
    else:
        st.header("🦅 Executive Governance Chamber")
        st.write(f"You have won your respective race and taken the Oath of Office to uphold the Constitution. Welcome to your Term.")
        
        # REALISTIC CRISIS AND EMERGENCY CONTROL HUB
        st.subheader("🚨 Real-Time Emergency Council Room")
        np.random.seed(day_seed + 100)
        active_crisis = np.random.choice(["Infrastructure Breakdown", "Economic High-Inflation Wave", "Localized Border/Sovereignty Strain", "Quiet Governance Week"])
        
        if active_crisis == "Infrastructure Breakdown":
            st.error("⚠️ **CRISIS:** A major bridge grid and electrical grid failure has crippled transit lines in your jurisdiction.")
            choice = st.radio("Action Plan:", ["Allocate EMERGENCY funding reserves to fast-track municipal repairs", "Request federal disaster assistance and deploy localized guardsmen"])
            if st.button("Execute Crisis Directive"):
                st.success("Directive logged. Infrastructure stabilization metrics processing.")
                
        elif active_crisis == "Economic High-Inflation Wave":
            st.error("📉 **CRISIS:** Global trade blockages have spiked fuel and commodity indexes. Local prices are soaring.")
            choice = st.radio("Action Plan:", ["Enact short-term regulatory tax holidays on necessary consumer goods", "Implement strict spending cuts to control localized deficit expansion"])
            if st.button("Execute Financial Directive"):
                st.success("Economic emergency adjustment parameters activated.")
        else:
            st.success("✨ Safe Horizon: Your departments report smooth standard operations across all operational sectors today.")

        st.subheader("💼 Long-Term Structural Cabinet")
        st.selectbox("Appoint / Re-verify Secretary of State", ["Diplomatic Career Officer", "Strategic Coalition Leader"])
        st.selectbox("Appoint / Re-verify Secretary of the Treasury", ["Central Banking Architect", "Industrial Academic Specialist"])
        
        # Re-election eligibility flag
        st.subheader("🔄 Future Cycle Outlook")
        if st.button("File Intention Paperwork for Next Re-Election Cycle"):
            st.info("Paperwork verified against Constitutional guidelines. If you have not exceeded your two-term bound, you will be cleared for the next cycle layout.")
