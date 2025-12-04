import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="PenTrust · Healthcare Content Clarity Analyzer",
    page_icon="✏️",
    layout="wide",
)

# ---------- GLOBAL STYLES ----------
st.markdown("""
<style>
:root {
  --primary-yellow: #F9D342;  /* Primary */
  --primary-amber:  #F59E0B;  /* Secondary */
  --accent-blue:    #2563EB;  /* Tertiary / Accent */
}

/* Page background + base */
body, .stApp {
  font-family: "Georgia", "Times New Roman", serif;
  background-color: #F7F7FB;
}

/* Main container padding */
.block-container {
  padding-top: 1.4rem;
}

/* Buttons */
.stButton>button {
  background-color: var(--accent-blue);
  color: white;
  border-radius: 999px;
  padding: 0.45rem 1.5rem;
  border: none;
  font-weight: 600;
  font-size: 0.95rem;
}
.stButton>button:hover {
  background-color: #1E48A8;
}

/* Section title underline */
.section-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0 0 0.4rem 0;
  letter-spacing: 0.02em;
}
.section-title span {
  border-bottom: 4px solid var(--primary-amber);
  padding-bottom: 4px;
}

/* Sub label (small overlines) */
.overline {
  text-transform: uppercase;
  font-size: 0.7rem;
  letter-spacing: 0.14em;
  color: #6B7280;
}

/* Cards */
.card {
  background: white;
  border-radius: 16px;
  padding: 18px 20px;
  box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
  margin-bottom: 1.0rem;
}
.card-border-amber {
  border-left: 5px solid var(--primary-amber);
}
.soft-card {
  background: #FFF8E2;
  border-radius: 16px;
  padding: 16px 18px;
  margin-bottom: 1.0rem;
  border: 1px solid rgba(245,158,11,0.2);
}

/* Pills / tags */
.pill {
  display: inline-block;
  padding: 3px 9px;
  border-radius: 999px;
  background: rgba(37,99,235,0.08);
  font-size: 0.75rem;
  color: #1F2937;
}

/* Tiny badge top right */
.badge-top-right {
  position: absolute;
  top: 12px;
  right: 18px;
  background: rgba(37,99,235,0.10);
  color: #1E40AF;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.7rem;
}

/* Metric cards tweak */
[data-testid="stMetric"] {
  background: white;
  border-radius: 14px;
  padding: 12px 14px;
  box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

/* Small helper text */
.helper-text {
  font-size: 0.8rem;
  color: #6B7280;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE / HERO ----------
hero_col1, hero_col2 = st.columns([2.6, 1.4])

with hero_col1:
    st.markdown(
        '<div class="overline">Madison · Branding & AI Prototype</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-title"><span>✏️ PenTrust – Healthcare Content Clarity Analyzer</span></div>',
        unsafe_allow_html=True,
    )
    st.write(
        "PenTrust is a demo interface for an AI-assisted text analyzer that helps UX and "
        "healthcare teams review content for **clarity, tone safety, readability, and trust signals**. "
        "Paste a few URLs or page labels to simulate how a content audit dashboard could look."
    )

with hero_col2:
    st.markdown(
        """
        <div class="card" style="position:relative;">
          <div class="badge-top-right">AI-assisted · Demo only</div>
          <b>Who this helps</b><br><br>
          • UX & product designers<br>
          • Content / UX writers<br>
          • Clinicians & care teams<br>
          • Ops / compliance leaders<br><br>
          <span class="helper-text">
          Manually reviewing thousands of lines of text is unrealistic. PenTrust imagines
          how AI text analysis could surface clarity issues early, before they become
          support calls, safety risks, or rework.
          </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")

# ---------- INPUT + TOOL INFO ----------
left, right = st.columns([1.8, 1.2])

with left:
    st.markdown('<div class="section-title"><span>Input content</span></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="helper-text">'
        'For this prototype, you can paste one or more URLs or short page labels '
        '(e.g., “Billing portal”, “Discharge instructions”, “Alert screen – ICU”). '
        'The analysis is mocked so you can focus on the UX and storytelling.'
        '</div>',
        unsafe_allow_html=True,
    )
    urls_text = st.text_area(
        "",
        placeholder="https://example.com/billing\nTest results page\nOnboarding – older adults",
        height=150,
    )
    run_button = st.button("Run PenTrust analysis")

with right:
    st.markdown('<div class="section-title"><span>What PenTrust checks</span></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card">
        <b>1. Pain points & friction</b><br>
        • Confusing instructions or missing next steps<br>
        • Overloaded alerts and dense paragraphs<br><br>

        <b>2. Clinical & safety context</b><br>
        • High-risk wording in critical flows<br>
        • Signals of alert fatigue in copy<br><br>

        <b>3. Trust & engagement</b><br>
        • Jargon vs. plain language<br>
        • Tone for patients vs. clinicians<br>
        • Transparency & explanation cues
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "In a real deployment, this UI would call an AI text analysis backend (e.g., "
        "Madison + n8n + LLM) and log results to a sheet or database. "
        "Here, the results are demo data to support your case study."
    )

# ---------- DUMMY ANALYSIS (REPLACE WITH REAL API LATER) ----------
def analyze_url_dummy(url: str) -> dict:
    """Demo analysis so the UI works even without a backend."""
    # Simple rules to vary things a bit by URL label
    url_lower = url.lower()
    if "alert" in url_lower or "icu" in url_lower:
        risk = "High"
        category = "Alert fatigue / safety"
        empathy = "Medium"
        clarity = "Medium"
    elif "billing" in url_lower or "payment" in url_lower:
        risk = "Medium"
        category = "Readability & trust"
        empathy = "Medium"
        clarity = "High"
    elif "results" in url_lower or "discharge" in url_lower:
        risk = "High"
        category = "Patient comprehension"
        empathy = "High"
        clarity = "Medium"
    else:
        risk = "Low"
        category = "General readability"
        empathy = "Medium"
        clarity = "High"

    return {
        "url": url,
        "risk_level": risk,
        "issue_category": category,
        # Core analysis
        "empathy_score": empathy,
        "clarity_score": clarity,
        "wcag_status": "Pass (AA demo)",
        "visual_schema": "Content-heavy layout",
        "summary": (
            "Demo summary: content is generally understandable, but key concepts could be "
            "surfaced more clearly for busy clinicians and patients with lower health literacy."
        ),
        "rewrite_suggestion": (
            "Shorten long sentences, remove jargon, and add a short 'What this means for you' "
            "section with bullet-point next steps."
        ),
        # Healthcare-inspired UX checks (non-clinical)
        "low_literacy_note": (
            "Contains a few long, complex sentences. Consider breaking them up and using "
            "simpler vocabulary."
        ),
        "tone_safety_note": (
            "Tone is mostly neutral. Review for phrases that may sound alarming in sensitive contexts."
        ),
        "hierarchy_note": (
            "Key actions could be surfaced more clearly using headings, bullets, or step-by-step structure."
        ),
        "visual_stress_note": (
            "Several dense blocks of text. Extra spacing and subheadings would reduce visual fatigue."
        ),
        "recommendations": [
            "Break long paragraphs into 2–3 shorter ones with clear headings.",
            "Replace medical jargon with patient- and clinician-friendly terms where possible.",
            "Add explicit 'What to do next' sections for critical flows (billing, results, follow-up).",
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
        st.warning("Please paste at least one URL or page label.")
    else:
        st.success(f"Running demo PenTrust analysis for {len(urls)} item(s)…")

        for url in urls:
            data = analyze_url_dummy(url)
            results.append(data)

        # Build summary df
        df_rows = []
        for item in results:
            df_rows.append({
                "Page / URL": item.get("url", ""),
                "Risk level": item.get("risk_level", ""),
                "Issue category": item.get("issue_category", ""),
                "Empathy": item.get("empathy_score", ""),
                "Clarity": item.get("clarity_score", ""),
                "WCAG": item.get("wcag_status", ""),
                "Visual schema": item.get("visual_schema", ""),
            })
        df = pd.DataFrame(df_rows)

# ---------- RESULTS UI (ONLY IF WE HAVE RESULTS) ----------
if results and df is not None:

    st.markdown("---")
    st.markdown('<div class="section-title"><span>📊 PenTrust snapshot</span></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="helper-text">High-level view of where your biggest content risks and UX opportunities are (demo data).</div>',
        unsafe_allow_html=True,
    )

    # High-level metrics
    total_urls = len(df)
    score_map = {"Low": 1, "Medium": 2, "High": 3}

    high_clarity = (df["Clarity"] == "High").sum()
    good_empathy = df["Empathy"].isin(["Medium", "High"]).sum()
    wcag_pass = df["WCAG"].str.contains("Pass").sum()
    high_risk = (df["Risk level"] == "High").sum()

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Pages analyzed", total_urls)
    m2.metric("High-risk items", high_risk)
    m3.metric("High clarity", f"{high_clarity}/{total_urls}")
    m4.metric("Supportive tone (Med/High)", f"{good_empathy}/{total_urls}")
    m5.metric("WCAG pass (demo)", f"{wcag_pass}/{total_urls}")

    # Summary table in a card
    with st.expander("View summary table"):
        st.dataframe(df, use_container_width=True)

    # Issue categories chart
    st.markdown('<div class="section-title"><span>🧩 Issues by category</span></div>', unsafe_allow_html=True)
    cat_counts = df["Issue category"].value_counts().reset_index()
    cat_counts.columns = ["Issue category", "Count"]
    st.bar_chart(cat_counts.set_index("Issue category"))

    # Clarity vs Empathy chart
    st.markdown('<div class="section-title"><span>🧠 Clarity vs tone safety</span></div>', unsafe_allow_html=True)

    chart_df = df.copy()
    chart_df["Clarity score"] = chart_df["Clarity"].map(score_map)
    chart_df["Empathy score"] = chart_df["Empathy"].map(score_map)
    chart_df = chart_df.set_index("Page / URL")[["Clarity score", "Empathy score"]]

    st.bar_chart(chart_df)
    # ---------- PAGE DEEP-DIVE ----------
    st.markdown("---")
    st.markdown('<div class="section-title"><span>🔍 Page deep-dive</span></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="helper-text">Select one item to see the kind of AI guidance PenTrust could provide to designers, writers, and clinical teams.</div>',
        unsafe_allow_html=True,
    )

    # dropdown uses exactly what is in the table
    selected_url = st.selectbox(
        "Select a page / URL to view detailed insights:",
        df["Page / URL"].tolist()
    )

    # make sure we match cleanly (strip spaces)
    safe_selected = selected_url.strip()

    # find the matching result
    selected_item = None
    for item in results:
        if item["url"].strip() == safe_selected:
            selected_item = item
            break

    # fallback: if something weird happens, default to first
    if selected_item is None and results:
        selected_item = results[0]

    colA, colB = st.columns(2)

    with colA:
        st.markdown(
            f"""
            <div class="card card-border-amber">
            <h4>Core metrics</h4>
            <b>Page / URL:</b> {selected_item["url"]}<br><br>
            <b>Risk level:</b> {selected_item["risk_level"]}<br>
            <b>Issue category:</b> {selected_item["issue_category"]}<br><br>
            <b>Empathy / tone:</b> {selected_item["empathy_score"]}<br>
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
            <h4>Summary (UX + clinical context)</h4>
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
            <p class="helper-text">
            In a real system, this could feed into UX writing, design tickets, or a CMS workflow
            so teams can iterate quickly.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="card">
        <h4>🩺 Healthcare & UX indicators</h4>
        <b>Low-literacy friendliness:</b> {selected_item["low_literacy_note"]}<br><br>
        <b>Tone safety:</b> {selected_item["tone_safety_note"]}<br><br>
        <b>Information hierarchy:</b> {selected_item["hierarchy_note"]}<br><br>
        <b>Visual stress:</b> {selected_item["visual_stress_note"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ Recommendations for the team")
    for r in selected_item.get("recommendations", []):
        st.markdown(f"- {r}")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "Made as part of my Branding & AI course · PenTrust demo UI · "
    "Back to my portfolio: [steffimanhalli.com](https://steffimanhalli.com)"
)
