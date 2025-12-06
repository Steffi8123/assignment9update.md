import streamlit as st
import pandas as pd
import random
import hashlib
from datetime import datetime

# -----------------------------
# Brand tokens
# -----------------------------
PRIMARY = "#F9D342"
SECONDARY = "#F59E0B"
ACCENT = "#2563EB"
BG = "#F7F8FB"
CARD_BG = "#FFFFFF"
TEXT = "#0F172A"
MUTED = "#6B7280"
BORDER = "#E5E7EB"

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="PenTrust – Healthcare Content Clarity Analyzer",
    page_icon="✏️",
    layout="wide"
)

# -----------------------------
# CSS (light, clean, card-based)
# -----------------------------
st.markdown(
    f"""
    <style>
        .stApp {{
            background: {BG};
            color: {TEXT};
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {PRIMARY} 0%, #FCE57A 100%);
            border-right: 1px solid rgba(0,0,0,0.04);
        }}
        section[data-testid="stSidebar"] * {{
            color: {TEXT} !important;
        }}

        /* Input outline clarity */
        textarea {{
            border: 1.5px solid {BORDER} !important;
            border-radius: 12px !important;
        }}

        /* Button styling */
        .stButton>button {{
            background: {TEXT};
            color: white;
            border-radius: 12px;
            padding: 0.6rem 1rem;
            border: none;
            font-weight: 600;
        }}
        .stButton>button:hover {{
            background: #111827;
        }}

        /* Card styles */
        .pt-card {{
            background: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 18px;
            padding: 18px 20px;
            box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
        }}

        .pt-metric {{
            border-radius: 18px;
            padding: 22px 22px;
            border: 1px solid {BORDER};
            background: {CARD_BG};
            box-shadow: 0 6px 18px rgba(2, 6, 23, 0.06);
            min-height: 140px;
        }}
        .pt-metric.primary {{
            background: linear-gradient(135deg, {PRIMARY} 0%, #FFECA0 100%);
        }}
        .pt-metric.blue {{
            background: linear-gradient(135deg, #DBEAFE 0%, #C7D2FE 100%);
        }}
        .pt-metric.soft {{
            background: #FFF7E6;
        }}

        .pt-metric-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: {TEXT};
            margin-bottom: 6px;
        }}
        .pt-metric-value {{
            font-size: 2.4rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin: 0;
            color: {TEXT};
        }}
        .pt-metric-sub {{
            font-size: 0.95rem;
            color: {MUTED};
            margin-top: 6px;
        }}

        .pt-section-title {{
            font-size: 1.6rem;
            font-weight: 800;
            margin-bottom: 6px;
        }}

        .pt-caption {{
            color: {MUTED};
            font-size: 0.98rem;
        }}

        .pt-pill {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            background: #EEF2FF;
            color: {TEXT};
            border: 1px solid {BORDER};
        }}

        /* Reduce default top padding feel */
        .block-container {{
            padding-top: 1.4rem;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Utilities
# -----------------------------
def normalize_urls(raw: str):
    if not raw:
        return []
    lines = [l.strip() for l in raw.splitlines()]
    lines = [l for l in lines if l]
    # Allow simple labels too, but treat as "pages"
    return lines

def stable_seed(text: str) -> int:
    h = hashlib.md5(text.encode("utf-8")).hexdigest()
    return int(h[:8], 16)

def mock_analysis_for_url(url: str):
    rnd = random.Random(stable_seed(url))

    # Scores intentionally not all perfect (so you can demo problems)
    clarity = rnd.randint(58, 82)
    next_steps = rnd.randint(52, 80)
    trust = rnd.randint(55, 85)
    accessibility = rnd.randint(48, 78)

    # Pick 2 primary issues to show on dashboard
    issue_pool = [
        ("Dense instructions", "Long paragraphs reduce scanability in critical flows."),
        ("Unclear next steps", "Confirmation copy doesn’t specify the user's next action."),
        ("Weak micro trust", "Lack of brief reassurance near sensitive content."),
        ("Readability mismatch", "Reading level may be high for broad patient audiences."),
        ("Accessibility gaps", "Content structure may not support assistive scanning.")
    ]
    rnd.shuffle(issue_pool)
    top_issues = issue_pool[:2]

    # Trend data for clarity chart
    trend = [max(40, min(90, clarity + rnd.randint(-8, 8))) for _ in range(8)]

    return {
        "scores": {
            "Clarity": clarity,
            "Next-step guidance": next_steps,
            "Trust signals": trust,
            "Accessibility-aware writing": accessibility
        },
        "top_issues": top_issues,
        "trend": trend
    }

def build_detailed_table(analyses: dict):
    rows = []
    for url, a in analyses.items():
        s = a["scores"]
        issues = ", ".join([i[0] for i in a["top_issues"]])
        # Simple risk label for presentation clarity
        risk = "High" if min(s.values()) < 55 else ("Medium" if min(s.values()) < 65 else "Low")

        rows.append({
            "Page / label": url,
            "Clarity score": s["Clarity"],
            "Next-step score": s["Next-step guidance"],
            "Trust score": s["Trust signals"],
            "Accessibility-aware score": s["Accessibility-aware writing"],
            "Top risk signals": issues,
            "Risk level": risk
        })
    if not rows:
        return pd.DataFrame(columns=[
            "Page / label", "Clarity score", "Next-step score", "Trust score",
            "Accessibility-aware score", "Top risk signals", "Risk level"
        ])
    return pd.DataFrame(rows)

def render_metric_card(title, value, sub, style_class=""):
    st.markdown(
        f"""
        <div class="pt-metric {style_class}">
            <div class="pt-metric-title">{title}</div>
            <div class="pt-metric-value">{value}</div>
            <div class="pt-metric-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_issue_list(issues):
    for title, desc in issues:
        st.markdown(
            f"""
            <div class="pt-card" style="margin-bottom: 10px;">
                <span class="pt-pill">Issue</span>
                <div style="font-weight: 700; font-size: 1.05rem; margin-top: 6px;">⚠️ {title}</div>
                <div class="pt-caption" style="margin-top: 2px;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# Session state
# -----------------------------
if "analyses" not in st.session_state:
    st.session_state.analyses = {}  # url -> analysis dict

if "urls" not in st.session_state:
    st.session_state.urls = []

if "selected_url" not in st.session_state:
    st.session_state.selected_url = None

# -----------------------------
# Sidebar nav (ONLY 2)
# -----------------------------
st.sidebar.markdown("## ✏️ PenTrust")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Deep Analysis"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "PenTrust is a presentation-friendly interface for an AI-assisted content clarity analyzer "
    "for healthcare UX and content teams."
)

# -----------------------------
# Header (top area)
# -----------------------------
st.markdown(
    """
    <div class="pt-card">
        <div class="pt-section-title">PenTrust – Healthcare Content Clarity Analyzer</div>
        <div class="pt-caption">
            Paste multiple URLs or page labels to simulate how an AI content audit could surface clarity,
            next-step, trust, and accessibility-aware writing risks.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# -----------------------------
# Input block (shared)
# -----------------------------
with st.container():
    left, right = st.columns([3, 1])

    with left:
        raw = st.text_area(
            "Pages to review",
            value="",
            height=110,
            placeholder="Paste the link(s) here — one per line",
            label_visibility="visible"
        )

    with right:
        st.write("")
        run = st.button("Run analysis", use_container_width=True)
        st.caption("Demo logic generates realistic signals for presentation use.")

    if run:
        urls = normalize_urls(raw)
        st.session_state.urls = urls

        analyses = {}
        for u in urls:
            analyses[u] = mock_analysis_for_url(u)

        st.session_state.analyses = analyses
        st.session_state.selected_url = urls[0] if urls else None

# If we already have urls but the user didn't press run this time
if not st.session_state.selected_url and st.session_state.urls:
    st.session_state.selected_url = st.session_state.urls[0]

analyses = st.session_state.analyses
urls = st.session_state.urls

# -----------------------------
# URL selector
# -----------------------------
if urls:
    st.markdown("##### Select a page")
    selected = st.selectbox(
        "Select a page",
        options=urls,
        index=urls.index(st.session_state.selected_url) if st.session_state.selected_url in urls else 0,
        label_visibility="collapsed"
    )
    st.session_state.selected_url = selected

selected_url = st.session_state.selected_url
selected_analysis = analyses.get(selected_url) if selected_url else None

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
if page == "Dashboard":
    if not urls:
        st.info("Add pages in **Pages to review** and click **Run analysis** to generate the dashboard.")
    else:
        # Layout similar to your reference:
        # left main area + right notifications/activities
        main, side = st.columns([3.2, 1.2])

        with main:
            st.markdown(
                f"""
                <div style="display:flex; justify-content: space-between; align-items:center; margin-bottom: 8px;">
                    <div class="pt-section-title">Dashboard</div>
                    <div class="pt-caption">Today</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Metric cards (2x2)
            c1, c2 = st.columns(2)
            c3, c4 = st.columns(2)

            s = selected_analysis["scores"]

            with c1:
                render_metric_card(
                    "Clarity risk signals found",
                    f"{max(2, 6 - (s['Clarity'] // 15))}",
                    "High-impact copy friction surfaced",
                    "primary"
                )
            with c2:
                render_metric_card(
                    "Next-step gaps flagged",
                    f"{max(1, 5 - (s['Next-step guidance'] // 18))}",
                    "Missing microcopy patterns",
                    "blue"
                )
            with c3:
                render_metric_card(
                    "Trust cues needing reinforcement",
                    f"{max(1, 5 - (s['Trust signals'] // 18))}",
                    "Sensitive moments identified",
                    "soft"
                )
            with c4:
                render_metric_card(
                    "Accessibility-aware writing risks",
                    f"{max(1, 6 - (s['Accessibility-aware writing'] // 16))}",
                    "Structure & readability warnings",
                    "blue"
                )

            st.write("")

            # Clarity score trend chart
            st.markdown("#### Clarity Score Trend")
            trend_df = pd.DataFrame({"Clarity score": selected_analysis["trend"]})
            st.bar_chart(trend_df)

            st.write("")

            # "Problems" area (explicitly for your presentation)
            st.markdown("#### Key problems detected on this page")
            render_issue_list(selected_analysis["top_issues"])

        with side:
            st.markdown(
                """
                <div class="pt-card">
                    <div class="pt-section-title" style="font-size:1.3rem;">Notifications</div>
                    <div style="margin-top:12px;">
                        <div style="font-weight:600;">⚠️ Clarity alert detected</div>
                        <div class="pt-caption">Just now</div>
                    </div>
                    <div style="margin-top:14px;">
                        <div style="font-weight:600;">👥 New page added to review</div>
                        <div class="pt-caption">A few minutes ago</div>
                    </div>
                    <div style="margin-top:14px;">
                        <div style="font-weight:600;">✅ Analysis complete</div>
                        <div class="pt-caption">Moments ago</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            st.markdown(
                """
                <div class="pt-card">
                    <div class="pt-section-title" style="font-size:1.3rem;">Activities</div>
                    <div style="margin-top:12px;">
                        <div style="font-weight:600;">📄 Report previewed</div>
                        <div class="pt-caption">Just now</div>
                    </div>
                    <div style="margin-top:14px;">
                        <div style="font-weight:600;">🧭 Page switched</div>
                        <div class="pt-caption">Live selection enabled</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")
        st.markdown("### Detailed audit table")
        st.caption("This is your big table for grading + screenshots.")
        st.dataframe(
            build_detailed_table(analyses),
            use_container_width=True,
            hide_index=True
        )

# -----------------------------
# DEEP ANALYSIS PAGE (Solutions)
# -----------------------------
elif page == "Deep Analysis":
    if not urls:
        st.info("Add pages in **Pages to review** and click **Run analysis** to generate deep analysis.")
    else:
        st.markdown(
            f"""
            <div style="display:flex; justify-content: space-between; align-items:center; margin-bottom: 8px;">
                <div class="pt-section-title">Deep Analysis</div>
                <div class="pt-caption">Solutions & rewrite guidance</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="pt-card">
                <div style="font-weight:700;">Page under review</div>
                <div class="pt-caption">{selected_url}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        # We show solutions that map to the dashboard issues,
        # without any HTML/code snippets.
        issues = selected_analysis["top_issues"]
        issue_titles = [i[0] for i in issues]

        # 1) Dense instructions
        if "Dense instructions" in issue_titles:
            st.markdown("### 1. Instructions are too dense for quick scanning")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**⚠️ Problem signal**")
                st.info("Actions are embedded in long paragraphs, lowering scan and completion rates.")
            with col2:
                st.markdown("**✅ Suggested fix**")
                st.success("Lead with a 1-line summary, then 2–3 short steps. Add headings and whitespace.")

            st.markdown("**Before (sample copy)**")
            st.write(
                "To complete your appointment request, please review the following detailed instructions, "
                "ensure you have your insurance information ready, and confirm your provider preference before proceeding."
            )

            st.markdown("**After (clearer version)**")
            st.write(
                "**Book in 3 steps:** 1) Choose a date  2) Select a provider  3) Confirm your details. "
                "Have your insurance card ready for step 3."
            )
            st.markdown("---")

        # 2) Unclear next steps
        if "Unclear next steps" in issue_titles:
            st.markdown("### 2. Next steps are unclear after key actions")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**⚠️ Problem signal**")
                st.info("Users receive acknowledgment without instructions for what to do next.")
            with col2:
                st.markdown("**✅ Suggested fix**")
                st.success("Add explicit next-step microcopy + one primary CTA + time expectation.")

            st.markdown("**Before (sample copy)**")
            st.write("Your request was received. We’ll review it.")

            st.markdown("**After (clearer version)**")
            st.write("Request received. **Next:** Upload your insurance card to continue. You’ll get an update within 24 hours.")
            st.markdown("---")

        # 3) Weak micro trust
        if "Weak micro trust" in issue_titles:
            st.markdown("### 3. Trust signals need reinforcement near sensitive moments")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**⚠️ Problem signal**")
                st.info("Sensitive information appears without brief reassurance or ownership cues.")
            with col2:
                st.markdown("**✅ Suggested fix**")
                st.success("Add micro trust cues: “Reviewed by…”, “Last updated…”, and 1-line data reassurance.")

            st.markdown("**Before (sample copy)**")
            st.write("This information will be used to support your care.")

            st.markdown("**After (clearer version)**")
            st.write(
                "This information supports your care. **We use it only for your treatment and service updates.** "
                "Reviewed by the care team • Last updated this month."
            )
            st.markdown("---")

        # 4) Readability mismatch
        if "Readability mismatch" in issue_titles:
            st.markdown("### 4. Readability may be too complex for broad patient use")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**⚠️ Problem signal**")
                st.info("Medical or administrative language may increase confusion and support dependence.")
            with col2:
                st.markdown("**✅ Suggested fix**")
                st.success("Swap jargon for plain language and add short examples.")

            st.markdown("**Before (sample copy)**")
            st.write("Please submit the required documentation to facilitate claim adjudication.")

            st.markdown("**After (clearer version)**")
            st.write("Please upload your documents so we can process your insurance claim.")
            st.markdown("---")

        # 5) Accessibility-aware writing
        if "Accessibility gaps" in issue_titles:
            st.markdown("### 5. Accessibility-aware writing structure is inconsistent")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**⚠️ Problem signal**")
                st.info("Headings, lists, and chunking may not support quick assistive scanning.")
            with col2:
                st.markdown("**✅ Suggested fix**")
                st.success("Use descriptive headings, short paragraphs, and consistent list patterns.")

            st.markdown("**Writer checklist**")
            st.write(
                "• One idea per paragraph\n"
                "• Use numbered steps for tasks\n"
                "• Put critical warnings first\n"
                "• Keep labels consistent across pages\n"
                "• Avoid multi-clause instruction sentences"
            )
            st.markdown("---")

        st.markdown("### Detailed audit table (for your screenshots)")
        st.dataframe(
            build_detailed_table(analyses),
            use_container_width=True,
            hide_index=True
        )
