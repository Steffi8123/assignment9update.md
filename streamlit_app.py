# app.py
import streamlit as st
import pandas as pd
import random

# ---------- BASIC PAGE CONFIG ----------
st.set_page_config(
    page_title="PenTrust – Healthcare Content Clarity Analyzer",
    layout="wide",
)

PRIMARY = "#F9D342"   # yellow
SECONDARY = "#F59E0B" # warm orange
ACCENT = "#2563EB"    # blue

# ---------- GLOBAL STYLES ----------
st.markdown(
    f"""
    <style>
    /* Page background */
    .stApp {{
        background-color: #0F172A;
    }}

    /* Main container */
    .main-block {{
        background-color: #F9FAFB;
        border-radius: 18px;
        padding: 18px 22px;
        margin: 0;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] > div:first-child {{
        background-color: {PRIMARY};
        padding-top: 20px;
        border-right: 1px solid rgba(15,23,42,0.08);
    }}
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] li {{
        color: #111827 !important;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}

    /* Nav buttons */
    .nav-pill {{
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 14px;
        border-radius: 999px;
        background-color: #FEFCE8;
        border: 1px solid rgba(15,23,42,0.08);
        font-weight: 600;
        margin-bottom: 10px;
    }}

    .nav-pill span.icon {{
        font-size: 16px;
    }}

    /* Cards */
    .metric-card {{
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 10px 30px rgba(15,23,42,0.08);
        border: 1px solid rgba(15,23,42,0.05);
    }}
    .metric-label {{
        font-size: 14px;
        color: #4B5563;
        margin-bottom: 4px;
    }}
    .metric-value {{
        font-size: 28px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0;
    }}
    .metric-delta {{
        font-size: 12px;
        color: #16A34A;
    }}

    /* Section titles */
    .section-title {{
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 4px;
        color: #111827;
    }}
    .section-sub {{
        font-size: 13px;
        color: #6B7280;
        margin-bottom: 12px;
    }}

    /* Pill chips */
    .pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 12px;
        background-color: #EFF6FF;
        color: #1D4ED8;
        margin-right: 6px;
        margin-bottom: 4px;
    }}

    /* Problem / success lists */
    .issue-item {{
        font-size: 13px;
        margin-bottom: 4px;
        color: #B45309;
    }}
    .success-item {{
        font-size: 13px;
        margin-bottom: 4px;
        color: #166534;
    }}

    .roi-card {{
        background-color: #ECFDF3;
        border-radius: 14px;
        padding: 10px 12px;
        border: 1px solid #22C55E33;
        font-size: 13px;
        color: #166534;
    }}

    /* Text blocks */
    .content-box {{
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 12px 14px;
        border: 1px solid rgba(15,23,42,0.06);
        font-size: 13px;
        color: #111827;
        line-height: 1.5;
    }}
    .content-box.bad {{
        border-left: 4px solid {SECONDARY};
    }}
    .content-box.good {{
        border-left: 4px solid #16A34A;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("### 🩺 PenTrust")
    st.caption("Healthcare Content Clarity Analyzer")
    st.markdown(
        f"""
        <div class="nav-pill">
            <span class="icon">📊</span> <span>Dashboard</span>
        </div>
        <div class="nav-pill" style="background:#FFFBEB;">
            <span class="icon">🧪</span> <span>Analysis</span>
        </div>
        <div style="margin-top:18px;font-size:12px;color:#4B5563;">
            Designed for UX & content teams auditing<br/>
            healthcare portals, apps, and messages.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- INPUT PANEL ----------
st.markdown('<div class="main-block">', unsafe_allow_html=True)

top_cols = st.columns([2, 1])

with top_cols[0]:
    st.markdown(
        f"<div class='section-title'>Dashboard</div>"
        f"<div class='section-sub'>Paste a few URLs or page labels and run a demo content audit.</div>",
        unsafe_allow_html=True,
    )

with top_cols[1]:
    st.markdown(
        f"<div style='text-align:right;font-size:12px;color:#6B7280;'>Today</div>",
        unsafe_allow_html=True,
    )

input_col, summary_col = st.columns([2, 1])

with input_col:
    urls_text = st.text_area(
        "Pages to review",
        placeholder="Example:\nhttps://hospital-portal.com/patient-login\nhttps://hospital-portal.com/medication-refill\nDischarge summary SMS copy",
        height=120,
    )
    run_demo = st.button("Run PenTrust demo")

with summary_col:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Today’s analyses</div>
            <div class="metric-value">128</div>
            <div class="metric-delta">+11.0% vs. last week</div>
        </div>
        <br/>
        <div class="metric-card">
            <div class="metric-label">Avg. Clarity Score</div>
            <div class="metric-value">82</div>
            <div class="metric-delta">↑ after tone & safety fixes</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- FAKE ANALYSIS ENGINE ----------
def fake_analyze(url_label: str):
    """Very simple demo logic to simulate issues & fixes."""
    # You can replace this with real NLP later
    issues = [
        "Confusing next-step instructions",
        "Dense paragraph in a high-stress moment",
        "Jargon that may be hard for patients to understand",
    ]
    successes = [
        "Clear step-by-step guidance",
        "Shorter, scannable paragraphs",
        "Plain language aligned with health literacy guidance",
    ]
    clarity = random.randint(55, 88)
    improved = min(clarity + random.randint(8, 15), 98)

    roi_points = [
        "Fewer calls to nurses and front-desk teams",
        "Higher completion of portal tasks without help",
        "Less time spent rewriting content before go-live",
    ]

    return {
        "label": url_label,
        "clarity": clarity,
        "improved": improved,
        "issues": issues,
        "successes": successes,
        "roi": roi_points,
        "bad_example": (
            "To proceed, you must strictly adhere to the following complex "
            "requirements. Failure to do so may result in delays or denial of service. "
            "Please carefully review all sections before taking any action."
        ),
        "good_example": (
            "To book your appointment:\n"
            "1. Choose a date and time.\n"
            "2. Confirm your contact details.\n"
            "3. Tap **Book appointment**.\n\n"
            "If you need help, call us or send a secure message from the portal."
        ),
    }

# ---------- BUILD DATAFRAME FOR TABLE ----------
pages = []
if run_demo and urls_text.strip():
    for line in urls_text.split("\n"):
        label = line.strip()
        if not label:
            continue
        pages.append(fake_analyze(label))

if pages:
    df = pd.DataFrame(
        [
            {
                "Page / Message": p["label"],
                "Clarity score": p["clarity"],
                "Projected score after fixes": p["improved"],
            }
            for p in pages
        ]
    )

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-title'>Pages in this audit</div>"
        "<div class='section-sub'>Select a row to inspect issues, suggested copy, and ROI impact.</div>",
        unsafe_allow_html=True,
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

    # -------- DETAIL PANEL FOR ONE PAGE --------
    st.markdown("<br/>", unsafe_allow_html=True)
    labels = [p["label"] for p in pages]
    selected_label = st.selectbox("Inspect details for:", labels)
    selected = next(p for p in pages if p["label"] == selected_label)

    left, right = st.columns([1.3, 1])

    # LEFT: Problematic vs optimized copy
    with left:
        st.markdown(
            "<div class='section-title'>Customer’s problematic input → Optimized content</div>"
            "<div class='section-sub'>How PenTrust helps designers move from friction to clarity.</div>",
            unsafe_allow_html=True,
        )

        sub_cols = st.columns(2)

        with sub_cols[0]:
            st.markdown("**⚠️ Original copy (high friction)**")
            st.markdown(
                f"<div class='content-box bad'>{selected['bad_example']}</div>",
                unsafe_allow_html=True,
            )
            st.markdown("**Detected issues**")
            for issue in selected["issues"]:
                st.markdown(f"<div class='issue-item'>⚠️ {issue}</div>", unsafe_allow_html=True)

        with sub_cols[1]:
            st.markdown("**✅ Optimized copy (PenTrust-guided)**")
            st.markdown(
                f"<div class='content-box good'>{selected['good_example'].replace(chr(10), '<br/>')}</div>",
                unsafe_allow_html=True,
            )
            st.markdown("**Success metrics this supports**")
            for s in selected["successes"]:
                st.markdown(f"<div class='success-item'>✅ {s}</div>", unsafe_allow_html=True)

    # RIGHT: Metrics + ROI
    with right:
        st.markdown(
            "<div class='section-title'>Impact & ROI signals</div>"
            "<div class='section-sub'>How this content change moves business and safety metrics.</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Clarity score</div>
                <div class="metric-value">{selected['clarity']}</div>
                <div class="metric-delta" style="color:#DC2626;">Before fixes</div>
            </div>
            <br/>
            <div class="metric-card">
                <div class="metric-label">Projected clarity after fixes</div>
                <div class="metric-value" style="color:{ACCENT};">{selected['improved']}</div>
                <div class="metric-delta">Modeled from similar content changes</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("<div class='roi-card'><b>ROI levers this change influences:</b></div>", unsafe_allow_html=True)
        for r in selected["roi"]:
            st.markdown(f"<div class='success-item'>📈 {r}</div>", unsafe_allow_html=True)

else:
    st.markdown(
        "<br/><div class='section-sub'>Paste at least one URL or page label above and click "
        "<b>Run PenTrust demo</b> to populate the dashboard.</div>",
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)
