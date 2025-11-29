import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Web Clarity & Empathy Analyzer",
    page_icon="✏️",
    layout="wide",
)

# ---------- GLOBAL STYLES ----------
st.markdown("""
<style>
:root {
  --primary-yellow: #F9D342;
  --primary-amber: #F59E0B;
  --accent-blue:  #2563EB;
}

/* Page background + base */
body, .stApp {
  font-family: "Georgia", "Times New Roman", serif;
  background-color: #F7F7FB;
}

/* Buttons */
.stButton>button {
  background-color: var(--accent-blue);
  color: white;
  border-radius: 999px;
  padding: 0.45rem 1.5rem;
  border: none;
  font-weight: 600;
}
.stButton>button:hover {
  background-color: #1E48A8;
}

/* Section title underline */
.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0 0 0.4rem 0;
}
.section-title span {
  border-bottom: 4px solid var(--primary-amber);
  padding-bottom: 4px;
}

/* Cards */
.card {
  background: white;
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
  margin-bottom: 1.0rem;
}
.card-border-amber {
  border-left: 6px solid var(--primary-amber);
}
.soft-card {
  background: #FFF8E5;
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 1.0rem;
}

/* Small pill labels if you want later */
.pill {
  display: inline-block;
  padding: 3px 9px;
  border-radius: 999px;
  background: rgba(37,99,235,0.08);
  font-size: 0.75rem;
}

/* Reduce padding around dataframe */
.block-container {
  padding-top: 1.6rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE / HERO ----------
col_title, col_side = st.columns([2.5, 1])

with col_title:
    st.markdown(
        '<div class="section-title"><span>✏️ Web Clarity & Empathy Analyzer</span></div>',
        unsafe_allow_html=True,
    )
    st.write(
        "First Madison-based UI that checks how **clear, empathetic and accessible** a web page feels. "
        "Paste URLs and get a quick UX snapshot inspired by healthcare communication."
    )

with col_side:
    st.markdown(
        """
        <div class="soft-card">
        <b>Quick steps</b><br><br>
        1. Paste one or more URLs<br>
        2. Click <b>Run analysis</b><br>
        3. Review the dashboard + deep-dive cards<br>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")

# ---------- INPUT + TOOL INFO ----------
left, right = st.columns([2, 1])

with left:
    st.markdown('<div class="section-title"><span>Input</span></div>', unsafe_allow_html=True)
    with st.container():
        urls_text = st.text_area(
            "",
            placeholder="https://example.com/page-1\nhttps://example.com/page-2",
            height=150,
        )
        run_button = st.button("Run analysis")

with right:
    st.markdown('<div class="section-title"><span>What this tool checks</span></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card">
        • 🧠 <b>Clarity</b> – is the content easy to understand?<br>
        • 💬 <b>Empathy</b> – does the tone feel supportive, not harsh?<br>
        • ♿ <b>Accessibility</b> – simple WCAG-inspired checks (demo).<br>
        • 🩺 <b>Healthcare-inspired UX</b> (non-clinical):<br>
        &nbsp;&nbsp;&nbsp;– Low-literacy friendliness<br>
        &nbsp;&nbsp;&nbsp;– Emotionally safe tone (no scary language)<br>
        &nbsp;&nbsp;&nbsp;– Clear information hierarchy<br>
        &nbsp;&nbsp;&nbsp;– Visual stress from dense blocks of text
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "For this assignment, the analysis is mocked so you can explore the interface. "
        "In a real deployment, this would call my Madison/n8n workflow and log results to a Google Sheet."
    )

# ---------- DUMMY ANALYSIS (REPLACE WITH REAL API LATER) ----------
def analyze_url_dummy(url: str) -> dict:
    """Demo analysis so the UI works even without a backend."""
    return {
        "url": url,
        # Core analysis
        "empathy_score": "Medium",
        "clarity_score": "High",
        "wcag_status": "Pass (AA demo)",
        "visual_schema": "Content-heavy layout",
        "summary": (
            "Demo summary: content is generally clear but could be simplified "
            "for low-literacy readers."
        ),
        "rewrite_suggestion": (
            "Shorten long sentences, reduce jargon, and add headings and "
            "bullet points for key actions."
        ),
        # Healthcare-inspired UX checks (non-clinical)
        "low_literacy_note": (
            "Contains a few long sentences; consider simpler language and "
            "shorter paragraphs."
        ),
        "tone_safety_note": (
            "Tone is mostly calm and neutral. Avoid phrases that sound "
            "alarming or judgmental."
        ),
        "hierarchy_note": (
            "Main message appears, but headings and bullets could be used "
            "more consistently."
        ),
        "visual_stress_note": (
            "Text blocks are a bit dense. Adding spacing and subheadings "
            "would reduce visual fatigue."
        ),
        "recommendations": [
            "Break long paragraphs into 2–3 shorter ones.",
            "Use headings for key sections like ‘What this means’ and ‘What to do next’.",
            "Replace medical jargon with patient-friendly words where possible.",
        ],
    }

# ---------- MAIN ACTION ----------
results = []
df = None

if run_button:
    urls = []
    if urls_text.strip():
        urls = [u.strip() for u in urls_text.splitlines() if u.strip()]

    if not urls:
        st.warning("Please paste at least one URL.")
    else:
        st.success(f"Running demo analysis for {len(urls)} URL(s)…")

        for url in urls:
            data = analyze_url_dummy(url)
            results.append(data)

        # Build summary df
        df_rows = []
        for item in results:
            df_rows.append({
                "URL": item.get("url", ""),
                "Empathy": item.get("empathy_score", ""),
                "Clarity": item.get("clarity_score", ""),
                "WCAG": item.get("wcag_status", ""),
                "Visual schema": item.get("visual_schema", ""),
            })
        df = pd.DataFrame(df_rows)

# ---------- RESULTS UI (ONLY IF WE HAVE RESULTS) ----------
if results and df is not None:

    st.markdown("---")
    st.markdown('<div class="section-title"><span>📊 Analysis snapshot</span></div>', unsafe_allow_html=True)

    # High-level metrics
    total_urls = len(df)
    score_map = {"Low": 1, "Medium": 2, "High": 3}

    high_clarity = (df["Clarity"] == "High").sum()
    good_empathy = df["Empathy"].isin(["Medium", "High"]).sum()
    wcag_pass = df["WCAG"].str.contains("Pass").sum()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("URLs analyzed", total_urls)
    m2.metric("High clarity pages", f"{high_clarity}/{total_urls}")
    m3.metric("Supportive tone (Med/High)", f"{good_empathy}/{total_urls}")
    m4.metric("WCAG pass (demo)", f"{wcag_pass}/{total_urls}")

    # Summary table in a card
    with st.expander("View summary table"):
        st.dataframe(df, use_container_width=True)

    # Clarity vs Empathy chart
    st.markdown('<div class="section-title"><span>🧠 Clarity vs Empathy</span></div>', unsafe_allow_html=True)

    chart_df = df.copy()
    chart_df["Clarity score"] = chart_df["Clarity"].map(score_map)
    chart_df["Empathy score"] = chart_df["Empathy"].map(score_map)
    chart_df = chart_df.set_index("URL")[["Clarity score", "Empathy score"]]

    st.bar_chart(chart_df)

    # ---------- PAGE DEEP-DIVE ----------
    st.markdown("---")
    st.markdown('<div class="section-title"><span>🔍 Page deep-dive</span></div>', unsafe_allow_html=True)

    selected_url = st.selectbox(
        "Select a URL to view detailed insights:",
        df["URL"].tolist()
    )

    selected_item = next(item for item in results if item["url"] == selected_url)

    colA, colB = st.columns(2)

    with colA:
        st.markdown(
            f"""
            <div class="card card-border-amber">
            <h4>Core metrics</h4>
            <b>URL:</b> {selected_item["url"]}<br><br>
            <b>Empathy:</b> {selected_item["empathy_score"]}<br>
            <b>Clarity:</b> {selected_item["clarity_score"]}<br>
            <b>WCAG status:</b> {selected_item["wcag_status"]}<br>
            <b>Visual layout:</b> {selected_item["visual_schema"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="soft-card">
            <h4>Summary</h4>
            {selected_item["summary"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    with colB:
        st.markdown(
            f"""
            <div class="card">
            <h4>AI rewrite suggestion</h4>
            {selected_item["rewrite_suggestion"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="card">
        <h4>🩺 Healthcare-inspired UX indicators</h4>
        <b>Low-literacy friendliness:</b> {selected_item["low_literacy_note"]}<br><br>
        <b>Tone safety:</b> {selected_item["tone_safety_note"]}<br><br>
        <b>Information hierarchy:</b> {selected_item["hierarchy_note"]}<br><br>
        <b>Visual stress:</b> {selected_item["visual_stress_note"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ Recommendations")
    for r in selected_item.get("recommendations", []):
        st.markdown(f"- {r}")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "Back to my portfolio: [steffimanhalli.com](https://steffimanhalli.com)"
)
