"""
AI-Powered Employee Dashboard Prototype
A high-performance fintech-inspired personal performance command center
Built with Streamlit + Plotly + Mock Data
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Tuple
import random

# ============================================================================
# PAGE CONFIG & THEME
# ============================================================================

st.set_page_config(
    page_title="Employee Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark mode theme via CSS
st.markdown("""
    <style>
        :root {
            --primary: #00d4ff;
            --success: #00ff88;
            --warning: #ffa500;
            --danger: #ff4757;
            --dark-bg: #0f1419;
            --card-bg: #1a1f2e;
            --text-primary: #ffffff;
            --text-secondary: #a0aec0;
        }
        
        body {
            background-color: var(--dark-bg);
            color: var(--text-primary);
        }
        
        .kpi-card {
            background: linear-gradient(135deg, var(--card-bg) 0%, #252d3d 100%);
            padding: 24px;
            border-radius: 12px;
            border-left: 4px solid var(--primary);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            margin-bottom: 16px;
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
        }
        
        .kpi-value {
            font-size: 32px;
            font-weight: 700;
            color: var(--primary);
            margin: 8px 0;
            line-height: 1.2;
        }
        
        .kpi-label {
            font-size: 13px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
            line-height: 1.3;
        }
        
        .kpi-subtitle {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 8px;
            line-height: 1.3;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }
        
        .status-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            margin-right: 8px;
        }
        
        .status-green {
            background-color: rgba(0, 255, 136, 0.15);
            color: var(--success);
            border: 1px solid var(--success);
        }
        
        .status-yellow {
            background-color: rgba(255, 165, 0, 0.15);
            color: var(--warning);
            border: 1px solid var(--warning);
        }
        
        .status-red {
            background-color: rgba(255, 71, 87, 0.15);
            color: var(--danger);
            border: 1px solid var(--danger);
        }
        
        .risk-banner {
            background: rgba(255, 71, 87, 0.1);
            border-left: 3px solid var(--danger);
            padding: 12px 16px;
            border-radius: 4px;
            margin-bottom: 16px;
            color: var(--danger);
            font-size: 13px;
        }
        
        .success-banner {
            background: rgba(0, 255, 136, 0.1);
            border-left: 3px solid var(--success);
            padding: 12px 16px;
            border-radius: 4px;
            margin-bottom: 16px;
            color: var(--success);
            font-size: 13px;
        }
        
        .section-header {
            font-size: 24px;
            font-weight: 700;
            color: var(--text-primary);
            margin: 24px 0 16px 0;
            border-bottom: 2px solid rgba(0, 212, 255, 0.2);
            padding-bottom: 12px;
        }
        
        .ai-recommendation-card {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 255, 136, 0.05) 100%);
            border: 1px solid rgba(0, 212, 255, 0.3);
            padding: 20px;
            border-radius: 12px;
            margin: 16px 0;
        }
        
        .promotion-readiness {
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 212, 255, 0.05) 100%);
        }
        
        .burnout-warning {
            background: linear-gradient(135deg, rgba(255, 165, 0, 0.1) 0%, rgba(255, 71, 87, 0.05) 100%);
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# MOCK DATA GENERATION
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables"""
    if "employee_name" not in st.session_state:
        st.session_state.employee_name = "Alex Morgan"
    if "employee_id" not in st.session_state:
        st.session_state.employee_id = "EMP-2024-5847"
    if "department" not in st.session_state:
        st.session_state.department = "Quantitative Trading"
    if "health_entries" not in st.session_state:
        st.session_state.health_entries = generate_mock_health_history()
    if "feedback_received" not in st.session_state:
        st.session_state.feedback_received = generate_mock_feedback()
    if "performance_data" not in st.session_state:
        st.session_state.performance_data = generate_mock_performance()
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Overview"

def generate_mock_performance() -> Dict:
    """Generate mock performance data"""
    months = pd.date_range(start="2025-09-01", end="2026-02-01", freq="M")
    
    aop_targets = [95, 98, 102, 105, 108, 110]
    actuals = [92, 101, 100, 108, 112, 115]
    
    return {
        "months": months.strftime("%b").tolist(),
        "aop": aop_targets,
        "actual": actuals,
        "kras": [
            {"name": "Revenue Generation", "target": 100, "actual": 115, "owner": "Self"},
            {"name": "Client Retention", "target": 98, "actual": 102, "owner": "Self"},
            {"name": "Risk Management", "target": 95, "actual": 94, "owner": "Team"},
            {"name": "Model Accuracy", "target": 99, "actual": 101, "owner": "Self"},
        ],
        "projects": [
            {"name": "ML Model Upgrade v2.1", "status": "Open", "progress": 72, "start_date": "2025-11-15", "end_date": "2026-03-31", "update": "On track"},
            {"name": "Client Dashboard Migration", "status": "Closed", "progress": 100, "start_date": "2025-08-01", "end_date": "2026-01-31", "update": "Completed"},
            {"name": "Risk Profiling AI", "status": "Open", "progress": 58, "start_date": "2025-12-01", "end_date": "2026-04-15", "update": "Minor delays"},
        ],
        "initiatives": [
            {"name": "Mentorship Program", "status": "Active", "contribution": "High"},
            {"name": "Process Automation", "status": "Planning", "contribution": "Medium"},
        ]
    }

def generate_mock_health_history() -> List[Dict]:
    """Generate mock health status history"""
    entries = []
    for i in range(8, 0, -1):
        date = datetime.now() - timedelta(weeks=i)
        entries.append({
            "date": date.strftime("%b %d"),
            "stress": random.randint(4, 8),
            "sleep": random.randint(6, 9),
            "energy": random.randint(5, 8),
            "satisfaction": random.randint(6, 9),
            "note": random.choice([
                "Busy week, but managed well",
                "Good progress on projects",
                "Tired from deliverables push",
                "Great mentorship session",
                ""
            ])
        })
    return entries

def generate_mock_feedback() -> List[Dict]:
    """Generate mock 360 feedback"""
    return [
        {
            "from": "Sarah Chen",
            "role": "Manager",
            "sentiment": 0.87,
            "text": "Strong execution and ownership. Delivered Q4 targets ahead of schedule."
        },
        {
            "from": "James Wilson",
            "role": "Peer",
            "sentiment": 0.79,
            "text": "Great collaboration on the ML project. Could improve documentation."
        },
        {
            "from": "Maria Rodriguez",
            "role": "Direct Report",
            "sentiment": 0.92,
            "text": "Excellent mentor. Provided clear guidance and supported my growth."
        },
        {
            "from": "David Park",
            "role": "Peer",
            "sentiment": 0.81,
            "text": "Good insights in meetings. Sometimes moves fast on decisions."
        },
        {
            "from": "Lisa Tan",
            "role": "Manager",
            "sentiment": 0.88,
            "text": "Drives innovation and team culture. Strong contributor."
        },
    ]

def generate_mock_social_score() -> Dict:
    """Generate mock social score components"""
    return {
        "email_response_time": random.randint(85, 95),
        "meeting_participation": random.randint(80, 92),
        "collaboration_score": random.randint(82, 94),
        "mentorship_score": random.randint(75, 88),
    }

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_status_color(value: float, thresholds: Tuple[float, float] = (70, 85)) -> str:
    """Determine status color based on thresholds"""
    if value >= thresholds[1]:
        return "#00ff88"  # Green
    elif value >= thresholds[0]:
        return "#ffa500"  # Yellow
    else:
        return "#ff4757"  # Red

def get_status_badge_class(value: float, thresholds: Tuple[float, float] = (70, 85)) -> str:
    """Get status badge CSS class"""
    if value >= thresholds[1]:
        return "status-green"
    elif value >= thresholds[0]:
        return "status-yellow"
    else:
        return "status-red"

def get_status_text(value: float, thresholds: Tuple[float, float] = (70, 85)) -> str:
    """Get status text"""
    if value >= thresholds[1]:
        return "On Track"
    elif value >= thresholds[0]:
        return "Moderate Risk"
    else:
        return "Attention Needed"

def kpi_card(label: str, value: str, subtitle: str = "", status_color: str = "#00d4ff") -> str:
    """Generate KPI card HTML"""
    return f"""
    <div class="kpi-card" style="border-left-color: {status_color}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color: {status_color}">{value}</div>
        <div class="kpi-subtitle">{subtitle}</div>
    </div>
    """

# ============================================================================
# PAGE: OVERVIEW
# ============================================================================

def page_overview():
    """Overview dashboard with KPI cards and trends"""
    
    # Calculate metrics
    perf_data = st.session_state.performance_data
    latest_actual = perf_data["actual"][-1]
    latest_aop = perf_data["aop"][-1]
    performance_score = (latest_actual / latest_aop) * 100
    
    health_data = st.session_state.health_entries[-1]
    health_index = np.mean([
        health_data["stress"] / 10 * 100,
        health_data["sleep"] / 10 * 100,
        health_data["energy"] / 10 * 100,
        health_data["satisfaction"] / 10 * 100,
    ])
    
    social_score_data = generate_mock_social_score()
    social_score = np.mean(list(social_score_data.values()))
    
    feedback_sentiments = [f["sentiment"] for f in st.session_state.feedback_received]
    feedback_score = np.mean(feedback_sentiments) * 100
    
    # Top KPI Section
    st.markdown('<div class="section-header">📊 Performance Command Center</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(kpi_card(
            "Actual vs AOP",
            f"{performance_score:.0f}%",
            f"{latest_actual}% of {latest_aop}%",
            get_status_color(performance_score, (90, 100))
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(kpi_card(
            "Performance Score",
            f"{performance_score:.0f}",
            "0–100 scale",
            get_status_color(performance_score, (70, 85))
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(kpi_card(
            "Health Index",
            f"{health_index:.0f}",
            "Weekly avg",
            get_status_color(health_index, (70, 85))
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(kpi_card(
            "Social Score",
            f"{social_score:.0f}",
            "Team collaboration",
            get_status_color(social_score, (75, 88))
        ), unsafe_allow_html=True)
    
    with col5:
        st.markdown(kpi_card(
            "360 Sentiment",
            f"{feedback_score:.0f}",
            f"{len(feedback_sentiments)} reviews",
            get_status_color(feedback_score, (75, 90))
        ), unsafe_allow_html=True)
    
    # Risk indicator
    if health_index < 60:
        st.markdown(
            '<div class="risk-banner">⚠️ Health Alert: Consider workload adjustment</div>',
            unsafe_allow_html=True
        )
    
    # Charts section
    st.markdown('<div class="section-header">📈 Trends & Performance</div>', unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Monthly Actual vs AOP
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=perf_data["months"],
            y=perf_data["aop"],
            name="AOP Target",
            mode="lines+markers",
            line=dict(color="#ffa500", width=2),
            marker=dict(size=6)
        ))
        fig_trend.add_trace(go.Scatter(
            x=perf_data["months"],
            y=perf_data["actual"],
            name="Actual Performance",
            mode="lines+markers",
            line=dict(color="#00ff88", width=3),
            marker=dict(size=8),
            fill="tozeroy",
            fillcolor="rgba(0, 255, 136, 0.1)"
        ))
        fig_trend.update_layout(
            title="Monthly Performance vs AOP",
            xaxis_title="Month",
            yaxis_title="% Achievement",
            template="plotly_dark",
            hovermode="x unified",
            height=380,
            margin=dict(l=40, r=40, t=40, b=60),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with chart_col2:
        # KRAs Performance
        kras_df = pd.DataFrame(perf_data["kras"])
        fig_kra = go.Figure(data=[
            go.Bar(
                x=kras_df["name"],
                y=kras_df["actual"],
                name="Actual",
                marker_color="#00ff88"
            ),
            go.Bar(
                x=kras_df["name"],
                y=kras_df["target"],
                name="Target",
                marker_color="#a0aec0",
                opacity=0.5
            )
        ])
        fig_kra.update_layout(
            title="KRA Performance",
            xaxis_title="",
            yaxis_title="% Achievement",
            template="plotly_dark",
            barmode="group",
            height=380,
            margin=dict(l=40, r=40, t=40, b=80),
        )
        st.plotly_chart(fig_kra, use_container_width=True)

# ============================================================================
# PAGE: HEALTH STATUS
# ============================================================================

def page_health_status():
    """Health status tracking and wellness insights"""
    
    st.markdown('<div class="section-header">💚 Health & Wellness Tracker</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("### Weekly Self-Assessment")
        
        stress = st.slider("Stress Level", 1, 10, 5, help="1 = Low stress, 10 = High stress")
        sleep = st.slider("Sleep Quality", 1, 10, 7, help="1 = Poor, 10 = Excellent")
        energy = st.slider("Energy Level", 1, 10, 6, help="1 = Exhausted, 10 = Peak energy")
        satisfaction = st.slider("Work Satisfaction", 1, 10, 7, help="1 = Very low, 10 = Very high")
        
        note = st.text_area("Optional Note", placeholder="How are you feeling this week?", height=80)
        
        if st.button("Save Health Entry", use_container_width=True):
            new_entry = {
                "date": datetime.now().strftime("%b %d"),
                "stress": stress,
                "sleep": sleep,
                "energy": energy,
                "satisfaction": satisfaction,
                "note": note
            }
            st.session_state.health_entries.append(new_entry)
            st.success("✅ Health entry saved!")
    
    with col2:
        # Current health index
        latest = st.session_state.health_entries[-1]
        health_index = np.mean([
            (10 - latest["stress"]) / 10 * 100,
            latest["sleep"] / 10 * 100,
            latest["energy"] / 10 * 100,
            latest["satisfaction"] / 10 * 100,
        ])
        
        # Gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_index,
            title={"text": "Health Index"},
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#00d4ff"},
                "steps": [
                    {"range": [0, 50], "color": "rgba(255, 71, 87, 0.3)"},
                    {"range": [50, 75], "color": "rgba(255, 165, 0, 0.3)"},
                    {"range": [75, 100], "color": "rgba(0, 255, 136, 0.3)"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 90
                }
            }
        ))
        fig_gauge.update_layout(
            template="plotly_dark",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Health trend
    st.markdown('<div class="section-header">📊 Wellness Trend</div>', unsafe_allow_html=True)
    
    health_df = pd.DataFrame(st.session_state.health_entries)
    health_df["health_index"] = (
        (10 - health_df["stress"]) / 10 * 100 +
        health_df["sleep"] / 10 * 100 +
        health_df["energy"] / 10 * 100 +
        health_df["satisfaction"] / 10 * 100
    ) / 4
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=health_df["date"],
        y=health_df["health_index"],
        name="Health Index",
        mode="lines+markers",
        line=dict(color="#00d4ff", width=2),
        marker=dict(size=8),
        fill="tozeroy",
        fillcolor="rgba(0, 212, 255, 0.1)"
    ))
    fig_trend.add_hline(y=75, line_dash="dash", line_color="#00ff88", annotation_text="Healthy Threshold")
    fig_trend.add_hline(y=60, line_dash="dash", line_color="#ffa500", annotation_text="At Risk Threshold")
    
    fig_trend.update_layout(
        title="8-Week Health Trend",
        xaxis_title="Week",
        yaxis_title="Health Index",
        template="plotly_dark",
        height=400,
        hovermode="x unified"
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # AI Insight
    if health_index < 70:
        st.markdown(
            f'<div class="risk-banner">🤖 AI Insight: Your wellness metrics suggest you could benefit from a workload review. Consider discussing with your manager.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="success-banner">🤖 AI Insight: Your wellness metrics are strong. Keep maintaining this pace!</div>',
            unsafe_allow_html=True
        )

# ============================================================================
# PAGE: PERFORMANCE
# ============================================================================

def page_performance():
    """Performance tracking and MIS generation"""
    
    st.markdown('<div class="section-header">📈 Performance & MIS</div>', unsafe_allow_html=True)
    
    perf_data = st.session_state.performance_data
    
    # ========== Edit Monthly Performance ==========
    st.markdown('<div class="section-header">📊 Edit Monthly Performance (Actual vs AOP)</div>', unsafe_allow_html=True)
    
    st.write("**Current Data:**")
    monthly_display = pd.DataFrame({
        "Month": perf_data["months"],
        "AOP Target": perf_data["aop"],
        "Actual": perf_data["actual"]
    })
    st.dataframe(monthly_display, use_container_width=True, hide_index=True)
    
    st.write("\n**📝 Update Monthly Data**")
    
    edit_col1, edit_col2, edit_col3 = st.columns(3)
    
    with edit_col1:
        month_idx = st.selectbox(
            "Select Month",
            range(len(perf_data["months"])),
            format_func=lambda i: perf_data["months"][i],
            key="month_select_perf"
        )
    
    with edit_col2:
        new_aop = st.number_input(
            "AOP Target %",
            min_value=0,
            max_value=200,
            value=perf_data["aop"][month_idx],
            step=1,
            key="aop_input"
        )
    
    with edit_col3:
        new_actual = st.number_input(
            "Actual %",
            min_value=0,
            max_value=200,
            value=perf_data["actual"][month_idx],
            step=1,
            key="actual_input"
        )
    
    if st.button("✅ Update Month Data", use_container_width=True):
        perf_data["aop"][month_idx] = new_aop
        perf_data["actual"][month_idx] = new_actual
        st.success(f"✅ Updated {perf_data['months'][month_idx]}")
        st.rerun()
    
    st.markdown("---")
    
    # ========== Edit KRA Data ==========
    st.markdown('<div class="section-header">🎯 Edit KRA Data</div>', unsafe_allow_html=True)
    
    kras_df = pd.DataFrame(perf_data["kras"])
    st.write("**Current KRAs:**")
    st.dataframe(kras_df, use_container_width=True, hide_index=True)
    
    st.write("\n**📝 Update KRA**")
    
    kra_col1, kra_col2, kra_col3 = st.columns(3)
    
    with kra_col1:
        kra_idx = st.selectbox(
            "Select KRA",
            range(len(perf_data["kras"])),
            format_func=lambda i: perf_data["kras"][i]["name"],
            key="kra_select"
        )
    
    with kra_col2:
        new_kra_target = st.number_input(
            "Target %",
            min_value=0,
            max_value=200,
            value=perf_data["kras"][kra_idx]["target"],
            step=1,
            key="kra_target_input"
        )
    
    with kra_col3:
        new_kra_actual = st.number_input(
            "Actual %",
            min_value=0,
            max_value=200,
            value=perf_data["kras"][kra_idx]["actual"],
            step=1,
            key="kra_actual_input"
        )
    
    if st.button("✅ Update KRA", use_container_width=True):
        perf_data["kras"][kra_idx]["target"] = new_kra_target
        perf_data["kras"][kra_idx]["actual"] = new_kra_actual
        st.success(f"✅ Updated {perf_data['kras'][kra_idx]['name']}")
        st.rerun()
    
    st.write("\n**➕ Add New KRA**")
    
    add_kra_col1, add_kra_col2, add_kra_col3 = st.columns(3)
    
    with add_kra_col1:
        new_kra_name = st.text_input("KRA Name", placeholder="Enter KRA", key="new_kra_name")
    
    with add_kra_col2:
        new_kra_tgt = st.number_input("Target %", min_value=0, max_value=200, value=100, key="new_kra_tgt")
    
    with add_kra_col3:
        new_kra_act = st.number_input("Actual %", min_value=0, max_value=200, value=100, key="new_kra_act")
    
    if st.button("➕ Add KRA", use_container_width=True):
        if new_kra_name:
            perf_data["kras"].append({
                "name": new_kra_name,
                "target": new_kra_tgt,
                "actual": new_kra_act
            })
            st.success(f"✅ Added KRA: {new_kra_name}")
            st.rerun()
        else:
            st.warning("Please enter a KRA name")
    
    st.markdown("---")
    
    # ========== Projects and Initiatives Management ==========
    st.markdown('<div class="section-header">🚀 Projects & Initiatives Management</div>', unsafe_allow_html=True)
    
    proj_col1, proj_col2 = st.columns(2)
    
    with proj_col1:
        st.write("**Active Projects**")
        for proj in perf_data["projects"]:
            status_color = "#00ff88" if proj["progress"] == 100 else "#00d4ff"
            st.markdown(f"""
            <div style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>{proj['name']}</span>
                    <span style="color: {status_color}; font-weight: 600;">{proj['progress']}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(proj["progress"] / 100)
        
        # Projects table
        st.write("\n")
        st.write("**Project Details**")
        projects_df = pd.DataFrame([
            {
                "Project": proj["name"],
                "Start Date": proj["start_date"],
                "Target End": proj["end_date"],
                "Status": proj["status"],
                "Progress": f"{proj['progress']}%",
                "Update": proj["update"]
            }
            for proj in perf_data["projects"]
        ])
        st.dataframe(projects_df, use_container_width=True, hide_index=True)
        
        # Update Project Section
        st.write("\n---\n")
        st.write("**📝 Update Project Status**")
        
        update_col1, update_col2, update_col3 = st.columns(3)
        
        with update_col1:
            project_to_update = st.selectbox(
                "Select Project",
                [p["name"] for p in perf_data["projects"]],
                key="project_select"
            )
        
        with update_col2:
            new_progress = st.number_input(
                "Progress %",
                min_value=0,
                max_value=100,
                value=50,
                step=5,
                key="progress_input"
            )
        
        with update_col3:
            new_status = st.selectbox(
                "Status",
                ["Open", "Closed", "On Hold"],
                key="status_select"
            )
        
        update_col_a, update_col_b = st.columns(2)
        
        with update_col_a:
            new_update_text = st.text_input(
                "Status Update",
                placeholder="e.g., On track, Minor delays, Blocked",
                key="update_text"
            )
        
        with update_col_b:
            if st.button("✅ Update Project", use_container_width=True):
                # Find and update project
                for proj in perf_data["projects"]:
                    if proj["name"] == project_to_update:
                        proj["progress"] = new_progress
                        proj["status"] = new_status
                        if new_update_text:
                            proj["update"] = new_update_text
                st.success(f"✅ Updated {project_to_update}!")
                st.rerun()
        
        # Add New Project
        st.write("\n**➕ Add New Project**")
        
        new_proj_col1, new_proj_col2 = st.columns(2)
        
        with new_proj_col1:
            new_project_name = st.text_input(
                "Project Name",
                placeholder="Enter project name",
                key="new_proj_name"
            )
            new_start_date = st.date_input(
                "Start Date",
                key="new_start_date"
            )
        
        with new_proj_col2:
            new_proj_progress = st.number_input(
                "Initial Progress %",
                min_value=0,
                max_value=100,
                value=0,
                step=5,
                key="new_proj_progress"
            )
            new_end_date = st.date_input(
                "Target End Date",
                key="new_end_date"
            )
        
        if st.button("➕ Add Project", use_container_width=True):
            if new_project_name and new_start_date and new_end_date:
                new_project = {
                    "name": new_project_name,
                    "status": "Open",
                    "progress": new_proj_progress,
                    "start_date": new_start_date.strftime("%Y-%m-%d"),
                    "end_date": new_end_date.strftime("%Y-%m-%d"),
                    "update": "Just added"
                }
                perf_data["projects"].append(new_project)
                st.success(f"✅ Added project: {new_project_name}")
                st.rerun()
            else:
                st.warning("Please fill in all fields")
    
    with proj_col2:
        st.write("**Key Initiatives**")
        for init in perf_data["initiatives"]:
            status_color = "#00ff88" if init["status"] == "Active" else "#ffa500"
            st.markdown(f"""
            <span class="status-badge {get_status_badge_class(80 if init['status'] == 'Active' else 50)}">
                {init['status']}
            </span> {init['name']} — {init['contribution']}
            """, unsafe_allow_html=True)
        
        # Update Initiative Section
        st.write("\n---\n")
        st.write("**📝 Update Initiative**")
        
        init_update_col1, init_update_col2 = st.columns(2)
        
        with init_update_col1:
            initiative_to_update = st.selectbox(
                "Select Initiative",
                [i["name"] for i in perf_data["initiatives"]],
                key="init_select"
            )
        
        with init_update_col2:
            new_init_status = st.selectbox(
                "Status",
                ["Active", "Planning", "Paused", "Completed"],
                key="init_status_select"
            )
        
        init_contrib_col1, init_contrib_col2 = st.columns(2)
        
        with init_contrib_col1:
            new_init_contrib = st.selectbox(
                "Contribution Level",
                ["High", "Medium", "Low"],
                key="init_contrib_select"
            )
        
        with init_contrib_col2:
            if st.button("✅ Update Initiative", use_container_width=True):
                for init in perf_data["initiatives"]:
                    if init["name"] == initiative_to_update:
                        init["status"] = new_init_status
                        init["contribution"] = new_init_contrib
                st.success(f"✅ Updated {initiative_to_update}!")
                st.rerun()
        
        # Add New Initiative
        st.write("\n**➕ Add New Initiative**")
        
        new_init_col1, new_init_col2 = st.columns(2)
        
        with new_init_col1:
            new_initiative_name = st.text_input(
                "Initiative Name",
                placeholder="Enter initiative name",
                key="new_init_name"
            )
        
        with new_init_col2:
            new_initiative_contrib = st.selectbox(
                "Your Contribution",
                ["High", "Medium", "Low"],
                key="new_init_contrib"
            )
        
        if st.button("➕ Add Initiative", use_container_width=True):
            if new_initiative_name:
                new_initiative = {
                    "name": new_initiative_name,
                    "status": "Active",
                    "contribution": new_initiative_contrib
                }
                perf_data["initiatives"].append(new_initiative)
                st.success(f"✅ Added initiative: {new_initiative_name}")
                st.rerun()
            else:
                st.warning("Please enter an initiative name")
    
    # ========== MIS Generation ==========
    st.markdown('<div class="section-header">📋 Generate MIS Report</div>', unsafe_allow_html=True)
    
    st.write("Generate Monthly Intelligence Sheet based on all 4 inputs:")
    st.write("1. ✅ Monthly Performance (Actual vs AOP)")
    st.write("2. ✅ KRA Data")
    st.write("3. ✅ Project Updates")
    st.write("4. ✅ Initiatives")
    
    if st.button("📊 Generate MIS Report", use_container_width=True):
        # Generate MIS from all 4 sources
        kras_df = pd.DataFrame(perf_data["kras"])
        kras_df["Achievement %"] = (kras_df["actual"] / kras_df["target"] * 100).round(1)
        
        mis_report = f"""
        ═══════════════════════════════════════════════════════════════════════════════
        MONTHLY INTELLIGENCE SHEET (MIS)
        ═══════════════════════════════════════════════════════════════════════════════
        
        Employee: {st.session_state.employee_name}
        Department: {st.session_state.department}
        Date: {datetime.now().strftime("%B %d, %Y")}
        
        ───────────────────────────────────────────────────────────────────────────────
        1. MONTHLY PERFORMANCE OVERVIEW
        ───────────────────────────────────────────────────────────────────────────────
        Latest Month: {perf_data["months"][-1]}
        AOP Target: {perf_data["aop"][-1]}%
        Actual Achievement: {perf_data["actual"][-1]}%
        Performance vs Target: {((perf_data["actual"][-1] / perf_data["aop"][-1]) * 100):.1f}%
        
        ───────────────────────────────────────────────────────────────────────────────
        2. KEY RESULT AREAS (KRAs) PERFORMANCE
        ───────────────────────────────────────────────────────────────────────────────
        """
        
        for idx, row in kras_df.iterrows():
            mis_report += f"\n{row['name']:<35} Target: {row['target']:>5}%  Actual: {row['actual']:>5}%  Achievement: {row['Achievement %']:>6.1f}%"
        
        avg_achievement = kras_df["Achievement %"].mean()
        mis_report += f"\n{'─' * 80}\nAverage KRA Achievement: {avg_achievement:.1f}%\n"
        
        mis_report += """
        ───────────────────────────────────────────────────────────────────────────────
        3. ACTIVE PROJECTS
        ───────────────────────────────────────────────────────────────────────────────
        """
        
        for proj in perf_data["projects"]:
            mis_report += f"\n{proj['name']:<40} Status: {proj['status']:<10} Progress: {proj['progress']:>3}%  Update: {proj['update']}"
        
        mis_report += """
        
        ───────────────────────────────────────────────────────────────────────────────
        4. KEY INITIATIVES
        ───────────────────────────────────────────────────────────────────────────────
        """
        
        for init in perf_data["initiatives"]:
            mis_report += f"\n{init['name']:<40} Status: {init['status']:<12} Contribution: {init['contribution']}"
        
        mis_report += f"""
        
        ═══════════════════════════════════════════════════════════════════════════════
        """
        
        st.success("✅ MIS Report Generated!")
        st.text_area("📋 MIS Report", value=mis_report, height=400, disabled=True)
        
        # Download button
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download MIS (Text)",
                data=mis_report,
                file_name=f"MIS_{st.session_state.employee_name}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        
        with col2:
            if st.button("📧 Share with Manager", use_container_width=True):
                st.success("✅ MIS Report shared with your manager!")

# ============================================================================
# PAGE: 360 FEEDBACK
# ============================================================================

def page_360_feedback():
    """360 feedback and sentiment analysis"""
    
    st.markdown('<div class="section-header">🤝 360 Feedback & Sentiment</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Submit Feedback for a Colleague")
        
        colleague_name = st.text_input("Colleague Name")
        colleague_role = st.selectbox("Relationship", ["Manager", "Peer", "Direct Report"])
        feedback_text = st.text_area("Feedback", placeholder="Share constructive feedback...", height=120)
        
        if st.button("Submit Feedback", use_container_width=True):
            if colleague_name and feedback_text:
                # Simulate sentiment analysis
                sentiment_score = random.uniform(0.65, 0.98)
                new_feedback = {
                    "from": colleague_name,
                    "role": colleague_role,
                    "sentiment": sentiment_score,
                    "text": feedback_text
                }
                st.session_state.feedback_received.append(new_feedback)
                st.success(f"✅ Feedback submitted! Sentiment: {sentiment_score:.2f}")
            else:
                st.warning("Please fill in all fields")
    
    with col2:
        st.write("### Sentiment Overview")
        
        feedback_list = st.session_state.feedback_received
        sentiments = [f["sentiment"] for f in feedback_list]
        avg_sentiment = np.mean(sentiments)
        
        st.metric("Average Sentiment Score", f"{avg_sentiment:.2f}/1.0", f"+{random.uniform(0.01, 0.05):.2f}")
        
        # Sentiment distribution
        sentiment_bins = np.array([0, 0.3, 0.6, 0.8, 1.0])
        sentiment_labels = ["Poor", "Fair", "Good", "Excellent"]
        
        fig_sentiment = go.Figure(data=[
            go.Pie(
                labels=sentiment_labels,
                values=[
                    len([s for s in sentiments if s < 0.3]),
                    len([s for s in sentiments if 0.3 <= s < 0.6]),
                    len([s for s in sentiments if 0.6 <= s < 0.8]),
                    len([s for s in sentiments if s >= 0.8]),
                ],
                marker=dict(colors=["#ff4757", "#ffa500", "#00d4ff", "#00ff88"])
            )
        ])
        fig_sentiment.update_layout(
            template="plotly_dark",
            height=300,
            showlegend=True
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    # Feedback Received
    st.markdown('<div class="section-header">📥 Feedback Received</div>', unsafe_allow_html=True)
    
    for feedback in st.session_state.feedback_received[-5:]:  # Show last 5
        sentiment = feedback["sentiment"]
        sentiment_text = "Excellent" if sentiment >= 0.8 else "Good" if sentiment >= 0.6 else "Fair"
        sentiment_color = "#00ff88" if sentiment >= 0.8 else "#00d4ff" if sentiment >= 0.6 else "#ffa500"
        
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.05); padding: 16px; border-radius: 8px; margin-bottom: 12px; border-left: 3px solid {sentiment_color};">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <strong>{feedback['from']}</strong> <span style="color: #a0aec0; font-size: 12px;">({feedback['role']})</span><br>
                    <span style="color: #a0aec0; font-size: 12px;">{feedback['text'][:80]}...</span>
                </div>
                <div style="color: {sentiment_color}; font-weight: 600; text-align: right;">
                    {sentiment:.2f}<br>
                    <span style="font-size: 12px;">{sentiment_text}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE: SOCIAL SCORE
# ============================================================================

def page_social_score():
    """Social score and collaboration metrics"""
    
    st.markdown('<div class="section-header">👥 Social Score & Collaboration</div>', unsafe_allow_html=True)
    
    social_data = generate_mock_social_score()
    social_score = np.mean(list(social_data.values()))
    
    # KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(kpi_card(
            "Social Score",
            f"{social_score:.0f}",
            "Composite metric",
            get_status_color(social_score, (75, 88))
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(kpi_card(
            "Email Response",
            f"{social_data['email_response_time']:.0f}%",
            "Within SLA",
            get_status_color(social_data['email_response_time'], (80, 90))
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(kpi_card(
            "Meeting Engagement",
            f"{social_data['meeting_participation']:.0f}%",
            "Active participation",
            get_status_color(social_data['meeting_participation'], (75, 88))
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(kpi_card(
            "Collaboration",
            f"{social_data['collaboration_score']:.0f}%",
            "Cross-team work",
            get_status_color(social_data['collaboration_score'], (75, 88))
        ), unsafe_allow_html=True)
    
    with col5:
        st.markdown(kpi_card(
            "Mentorship",
            f"{social_data['mentorship_score']:.0f}%",
            "Team development",
            get_status_color(social_data['mentorship_score'], (70, 85))
        ), unsafe_allow_html=True)
    
    # Radar Chart
    st.markdown('<div class="section-header">🎯 Collaboration Profile</div>', unsafe_allow_html=True)
    
    categories = list(social_data.keys())
    values = list(social_data.values())
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=[cat.replace('_', ' ').title() for cat in categories],
        fill='toself',
        name='Score',
        line=dict(color='#00d4ff'),
        fillcolor='rgba(0, 212, 255, 0.3)'
    ))
    
    fig_radar.update_layout(
        template="plotly_dark",
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        height=400,
        margin=dict(l=80, r=80, t=40, b=40)
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Insights
    st.markdown('<div class="section-header">💡 Social Insights</div>', unsafe_allow_html=True)
    
    if social_data['collaboration_score'] < 75:
        st.markdown(
            '<div class="risk-banner">Collaboration score is below team average. Consider engaging with cross-functional projects.</div>',
            unsafe_allow_html=True
        )
    
    if social_data['mentorship_score'] > 80:
        st.markdown(
            '<div class="success-banner">Great mentorship contributions! You\'re making a positive impact on team growth.</div>',
            unsafe_allow_html=True
        )

# ============================================================================
# PAGE: AI APPRAISAL ASSISTANT
# ============================================================================

def calculate_ai_appraisal() -> Dict:
    """Calculate AI-powered appraisal recommendations"""
    
    perf_data = st.session_state.performance_data
    latest_actual = perf_data["actual"][-1]
    latest_aop = perf_data["aop"][-1]
    performance_score = (latest_actual / latest_aop) * 100
    
    health_data = st.session_state.health_entries[-1]
    health_index = np.mean([
        (10 - health_data["stress"]) / 10 * 100,
        health_data["sleep"] / 10 * 100,
        health_data["energy"] / 10 * 100,
        health_data["satisfaction"] / 10 * 100,
    ])
    
    social_data = generate_mock_social_score()
    social_score = np.mean(list(social_data.values()))
    
    feedback_sentiments = [f["sentiment"] for f in st.session_state.feedback_received]
    feedback_score = np.mean(feedback_sentiments) * 100
    
    # AI Logic
    appraisal = {
        "performance": performance_score,
        "health": health_index,
        "social": social_score,
        "feedback": feedback_score,
        "strengths": [],
        "risks": [],
        "promotion_readiness": 0,
        "increment_band": "Standard",
        "trajectory": "",
    }
    
    # Strengths analysis
    if performance_score > 105:
        appraisal["strengths"].append("✅ Exceeding performance targets consistently")
    
    if feedback_score > 85:
        appraisal["strengths"].append("✅ Highly positive peer and manager feedback")
    
    if social_score > 85:
        appraisal["strengths"].append("✅ Strong collaboration and team engagement")
    
    if health_index > 75 and performance_score > 95:
        appraisal["strengths"].append("✅ Maintaining strong wellness while delivering results")
    
    # Risk analysis
    if performance_score < 90:
        appraisal["risks"].append("⚠️ Performance below target—review priorities")
    
    if health_index < 60:
        appraisal["risks"].append("⚠️ Wellness concerns detected—burnout risk")
    
    if social_score < 70:
        appraisal["risks"].append("⚠️ Low collaboration metrics—needs team engagement focus")
    
    if performance_score > 100 and health_index < 65:
        appraisal["risks"].append("🔴 High burnout risk—strong output masking fatigue")
    
    # Promotion Readiness
    if performance_score > 105 and health_index > 75 and social_score > 85 and feedback_score > 85:
        appraisal["promotion_readiness"] = 95
        appraisal["trajectory"] = "Senior/Lead Track"
        appraisal["increment_band"] = "Exceptional (A+)"
    elif performance_score > 100 and health_index > 70 and social_score > 80:
        appraisal["promotion_readiness"] = 75
        appraisal["trajectory"] = "Specialist/Senior Track"
        appraisal["increment_band"] = "High Performer (A)"
    elif performance_score > 95:
        appraisal["promotion_readiness"] = 55
        appraisal["trajectory"] = "Individual Contributor Track"
        appraisal["increment_band"] = "Strong (B+)"
    else:
        appraisal["promotion_readiness"] = 35
        appraisal["trajectory"] = "Development Focus"
        appraisal["increment_band"] = "Standard (B)"
    
    return appraisal

def page_ai_appraisal():
    """AI-powered quarterly appraisal assistant"""
    
    st.markdown('<div class="section-header">🤖 AI Quarterly Appraisal Assistant</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("Generate AI-powered quarterly review based on your performance data.")
    
    with col2:
        if st.button("🚀 Generate Quarterly AI Review", use_container_width=True):
            st.session_state.appraisal_generated = True
    
    if st.session_state.get("appraisal_generated", False):
        appraisal = calculate_ai_appraisal()
        
        # Promotion Readiness Gauge
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=appraisal["promotion_readiness"],
                title={"text": "Promotion Readiness"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#00d4ff"},
                    "steps": [
                        {"range": [0, 50], "color": "rgba(255, 71, 87, 0.3)"},
                        {"range": [50, 75], "color": "rgba(255, 165, 0, 0.3)"},
                        {"range": [75, 100], "color": "rgba(0, 255, 136, 0.3)"}
                    ],
                }
            ))
            fig_gauge.update_layout(
                template="plotly_dark",
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            st.markdown(f"""
            <div class="ai-recommendation-card">
                <h3>📊 Performance Score</h3>
                <div class="kpi-value" style="color: {get_status_color(appraisal['performance'], (90, 105))};">{appraisal['performance']:.0f}%</div>
                <div style="color: #a0aec0; font-size: 12px; margin-top: 8px;">vs AOP Target</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="ai-recommendation-card">
                <h3>💚 Health Index</h3>
                <div class="kpi-value" style="color: {get_status_color(appraisal['health'], (70, 85))};">{appraisal['health']:.0f}</div>
                <div style="color: #a0aec0; font-size: 12px; margin-top: 8px;">Wellness Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Increment Band
        st.markdown('<div class="section-header">💰 Compensation & Trajectory</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            increment_colors = {
                "Exceptional (A+)": "#00ff88",
                "High Performer (A)": "#00d4ff",
                "Strong (B+)": "#ffa500",
                "Standard (B)": "#a0aec0",
            }
            
            increment_bands = {
                "Exceptional (A+)": "10-12%",
                "High Performer (A)": "8-10%",
                "Strong (B+)": "5-8%",
                "Standard (B)": "3-5%"
            }
            
            recommended_raise = increment_bands.get(appraisal['increment_band'], '3-5%')
            
            st.markdown(f"""
            <div class="ai-recommendation-card promotion-readiness">
                <h3>Increment Band</h3>
                <div class="kpi-value" style="color: {increment_colors.get(appraisal['increment_band'], '#00d4ff')};">
                    {appraisal['increment_band']}
                </div>
                <div style="color: #a0aec0; font-size: 12px; margin-top: 8px;">
                    Recommended raise: 
                    <span style="color: {increment_colors.get(appraisal['increment_band'], '#00d4ff')}; font-weight: 600;">
                        {recommended_raise}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="ai-recommendation-card">
                <h3>Role Trajectory</h3>
                <div style="font-size: 18px; color: #00d4ff; font-weight: 600; margin: 12px 0;">
                    {appraisal['trajectory']}
                </div>
                <div style="color: #a0aec0; font-size: 12px;">
                    Recommended path based on performance & engagement
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Strengths
        if appraisal["strengths"]:
            st.markdown('<div class="section-header">💪 Identified Strengths</div>', unsafe_allow_html=True)
            
            for strength in appraisal["strengths"]:
                st.markdown(f"""
                <div style="background: rgba(0, 255, 136, 0.05); padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #00ff88;">
                    {strength}
                </div>
                """, unsafe_allow_html=True)
        
        # Risk Areas
        if appraisal["risks"]:
            st.markdown('<div class="section-header">🚨 Risk Areas & Development Focus</div>', unsafe_allow_html=True)
            
            for risk in appraisal["risks"]:
                risk_color = "#ff4757" if "🔴" in risk else "#ffa500"
                st.markdown(f"""
                <div style="background: rgba(255, 71, 87, 0.05); padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid {risk_color};">
                    {risk}
                </div>
                """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown('<div class="section-header">📋 Recommendations</div>', unsafe_allow_html=True)
        
        recommendations = []
        
        if appraisal["promotion_readiness"] > 85:
            recommendations.append("🎯 **Promotion-Ready**: Consider advancement to next level in 1-2 quarters")
        elif appraisal["promotion_readiness"] > 70:
            recommendations.append("📈 **Development Plan**: Target specific gaps to reach senior level")
        
        if appraisal["health"] < 65:
            recommendations.append("💚 **Wellness Focus**: Schedule check-in with manager on workload")
        
        if appraisal["social"] < 75:
            recommendations.append("👥 **Engagement**: Increase cross-team collaboration initiatives")
        
        if not recommendations:
            recommendations.append("✅ **Continue Momentum**: Current trajectory is strong—maintain focus")
        
        for rec in recommendations:
            st.write(f"• {rec}")
        
        # Export option
        st.markdown('<div class="section-header">📥 Share Review</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📧 Send to Manager", use_container_width=True):
                st.success("✅ Appraisal sent to manager for review")
        
        with col2:
            if st.button("📥 Download PDF Report", use_container_width=True):
                st.success("✅ Report downloaded")

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application"""
    
    # Initialize
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        # Profile picture
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=AlexMorgan" style="width: 120px; height: 120px; border-radius: 50%; border: 3px solid #00d4ff; display: block; margin: 0 auto;">
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"### {st.session_state.employee_name}")
        st.write(f"*{st.session_state.department}*")
        st.write(f"ID: {st.session_state.employee_id}")
        
        st.markdown("---")
        
        pages = {
            "📊 Overview": "Overview",
            "💚 Health Status": "Health",
            "📈 Performance": "Performance",
            "🤝 360 Feedback": "Feedback",
            "👥 Social Score": "Social",
            "🤖 AI Appraisal": "Appraisal",
        }
        
        selected = st.radio("Navigation", list(pages.keys()))
        st.session_state.current_page = pages[selected]
        
        st.markdown("---")
        st.caption("📅 Last Updated: Today")
        st.caption("🔐 Data is mocked for prototype")
    
    # Page Router
    if st.session_state.current_page == "Overview":
        page_overview()
    elif st.session_state.current_page == "Health":
        page_health_status()
    elif st.session_state.current_page == "Performance":
        page_performance()
    elif st.session_state.current_page == "Feedback":
        page_360_feedback()
    elif st.session_state.current_page == "Social":
        page_social_score()
    elif st.session_state.current_page == "Appraisal":
        page_ai_appraisal()

if __name__ == "__main__":
    main()
