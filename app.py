import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="ROAD//SAFE — Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Design system: editorial / cyberpunk road-safety product ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --bg: #070b12;
  --panel: #0d1521;
  --panel2: #111d2b;
  --line: #24394b;
  --muted: #91a5b9;
  --text: #eef6ff;
  --mint: #63f5d2;
  --acid: #d5ff62;
  --blue: #73b8ff;
  --orange: #ff865e;
}
html, body, [class*="css"] { font-family: 'Manrope', sans-serif; }
.stApp {
  background:
    radial-gradient(ellipse at 84% 0%, rgba(30, 176, 159, .13), transparent 32%),
    radial-gradient(ellipse at 2% 35%, rgba(60, 107, 191, .10), transparent 30%),
    linear-gradient(145deg, #070b12 0%, #080f19 52%, #070b12 100%);
  color: var(--text);
}
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0c1420 0%, #080e18 100%);
  border-right: 1px solid #24394b;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.4rem; }
.block-container { max-width: 1500px; padding-top: 1.1rem; padding-bottom: 3rem; }
h1, h2, h3, h4 {
  font-family: 'Barlow Condensed', sans-serif !important;
  letter-spacing: -.025em !important;
  font-weight: 800 !important;
}
h1 { font-size: clamp(3rem, 5vw, 5.4rem) !important; line-height: .94 !important; }
h2 { font-size: 2.25rem !important; }
h3 { font-size: 1.55rem !important; }
p, label, .stMarkdown { color: #dbe8f5; }
[data-testid="stSidebar"] h2 {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 2.5rem !important;
  font-weight: 900 !important;
  letter-spacing: -.04em !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  font-family: 'Manrope', sans-serif !important;
  font-weight: 800 !important;
  font-size: 1.02rem !important;
  color: #e8f4ff !important;
  padding: .55rem .7rem !important;
  border: 1px solid transparent;
  border-radius: 10px;
  margin: .12rem 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(99,245,210,.08);
  border-color: rgba(99,245,210,.24);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p { font-weight: 800 !important; }
[data-testid="stSidebar"] hr { border-color: #26394c; }
.block-container hr { border-color: transparent !important; margin: .5rem 0 !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stToolbar"] { right: 1rem; }
.eyebrow {
  color: var(--mint); font: 500 .74rem 'DM Mono', monospace;
  letter-spacing: .18em; text-transform: uppercase; margin-bottom: .7rem;
}
.hero {
  padding: clamp(1.6rem, 4vw, 3.3rem); border: 1px solid #28545c; border-radius: 4px 22px 4px 22px;
  background:
    linear-gradient(110deg, rgba(14, 35, 48, .98), rgba(12, 39, 43, .9)),
    repeating-linear-gradient(135deg, transparent 0 8px, rgba(99,245,210,.03) 8px 9px);
  position: relative; overflow: hidden; margin-bottom: 1.7rem;
  box-shadow: 0 22px 70px rgba(0,0,0,.16);
}
.hero:before {
  content: ''; position: absolute; inset: 0 0 0 auto; width: 33%;
  background: repeating-linear-gradient(135deg, transparent 0 17px, rgba(99,245,210,.055) 17px 18px);
  mask-image: linear-gradient(90deg, transparent, #000); pointer-events: none;
}
.hero:after {
  content: 'RS/'; position: absolute; right: 3%; bottom: -3.6rem;
  color: rgba(99,245,210,.055); font: 900 15rem 'Barlow Condensed', sans-serif;
  transform: skewX(-10deg); pointer-events: none;
}
.hero-content { position: relative; z-index: 1; }
.pill {
  display: inline-flex; align-items: center; gap: .5rem; border: 1px solid #39766e;
  padding: .48rem .78rem; color: var(--mint); font: 500 .72rem 'DM Mono', monospace;
  letter-spacing: .13em; text-transform: uppercase; margin-bottom: 1.4rem;
  background: rgba(99,245,210,.035);
}
.pill-dot { display:inline-block; width:7px; height:7px; background:var(--acid); border-radius:50%; box-shadow:0 0 12px var(--acid); }
.hero h1 { margin: 0 0 1rem 0; color: #f5f9ff; max-width: 850px; }
.hero p { color: #b5cbd9; max-width: 680px; font-size: 1rem; line-height: 1.8; }
.metric {
  border: 1px solid #263d50; border-radius: 3px 16px 3px 16px; padding: 1.25rem;
  background: linear-gradient(145deg, #111e2c, #0b1420); min-height: 125px;
  position: relative; overflow: hidden;
}
.metric:after { content:''; position:absolute; left:0; top:0; width:3px; height:100%; background:var(--mint); }
.metric-label { color: #93aabd; font: 500 .72rem 'DM Mono', monospace; letter-spacing: .09em; text-transform: uppercase; }
.metric-value { color: #f4f9ff; font: 800 2.3rem 'Barlow Condensed', sans-serif; margin-top: .45rem; }
.metric-note { color: var(--mint); font: 500 .7rem 'DM Mono', monospace; margin-top: .2rem; }
.info-card {
  padding: 1.35rem; border: 1px solid #26394b; background: rgba(14,23,36,.8);
  border-radius: 3px 16px 3px 16px; height: 100%;
}
.info-card h3 { margin: .1rem 0 .45rem; color: #f0f7ff; }
.info-card p { color: #9eb3c6; font-size: .92rem; line-height: 1.7; }
.stButton button, [data-testid="stFormSubmitButton"] button {
  background: var(--mint) !important; color: #061b1a !important; border: none !important;
  border-radius: 3px 11px 3px 11px !important; font-weight: 900 !important;
  min-height: 2.9rem; padding: .7rem 1.2rem; text-transform: uppercase;
  letter-spacing: .06em; box-shadow: 0 8px 25px rgba(99,245,210,.12);
}
.stButton button:hover, [data-testid="stFormSubmitButton"] button:hover { background: var(--acid) !important; transform: translateY(-1px); }
.stButton button p, [data-testid="stFormSubmitButton"] button p,
.stButton button span, [data-testid="stFormSubmitButton"] button span {
  color: #041512 !important; opacity: 1 !important; font-weight: 900 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [data-testid="stRadio"] label p {
  color: #f2f7ff !important; opacity: 1 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] {
  background: rgba(99,245,210,.12) !important;
  border-color: rgba(99,245,210,.5) !important;
}
div[data-baseweb="select"] > div, input, textarea {
  background-color: #101c2a !important; border-color: #2a4055 !important; border-radius: 8px !important;
}
[data-testid="stSelectbox"] label, [data-testid="stNumberInput"] label, [data-testid="stTextInput"] label {
  font-weight: 800 !important; color: #cfe0ef !important; letter-spacing: .015em;
}
.result-card {
  padding: 1.6rem; border: 1px solid #398c7d; border-radius: 3px 18px 3px 18px;
  background: linear-gradient(125deg, #102b32, #0d1d29); margin: .6rem 0 1rem;
  box-shadow: 0 18px 45px rgba(0,0,0,.18);
}
.result-label { color: #a5c9cf; font: 500 .72rem 'DM Mono', monospace; letter-spacing: .14em; text-transform: uppercase; }
.result-value { color: var(--mint); font: 900 3rem 'Barlow Condensed', sans-serif; margin-top: .4rem; text-transform: uppercase; }
.section-head { display:flex; align-items:center; gap:.8rem; margin: 1.2rem 0 .8rem; }
.section-index { color:var(--mint); font:500 .8rem 'DM Mono', monospace; }
.stTabs [data-baseweb="tab-list"] { gap: .4rem; border-bottom: 1px solid #26374b; }
.stTabs [data-baseweb="tab"] { background: #101927; border-radius: 7px 7px 0 0; padding: .65rem 1rem; font-weight:800; }
.stCaption, [data-testid="stCaptionContainer"] { color: #8097ad !important; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_artifact():
    return joblib.load("road_accident_severity_classifier.joblib")

@st.cache_data
def load_dataset():
    path = Path("Road.csv")
    return pd.read_csv(path) if path.exists() else None

artifact_path = Path("road_accident_severity_classifier.joblib")
if not artifact_path.exists():
    st.error("Model file missing. Place road_accident_severity_classifier.joblib in the same folder as app.py.")
    st.stop()

artifact = load_artifact()
model = artifact["model"]
model_name = artifact.get("model_name", "RoadSafe classifier")
features = artifact["features"]
target = artifact.get("target", "Accident_severity")
feature_options = artifact.get("feature_options", {})
data = load_dataset()

with st.sidebar:
    st.markdown("### ◈ ROAD//SAFE")
    st.caption("FIELD INTELLIGENCE SYSTEM")
    st.markdown("---")
    st.markdown('<div class="eyebrow">Navigation / 01—04</div>', unsafe_allow_html=True)
    page = st.radio(
        "GO TO",
        ["Home", "Classify Severity", "Road Safety Insights", "About"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown('<div class="eyebrow">SYSTEM STATUS</div>', unsafe_allow_html=True)
    st.caption("● MODEL LOADED" if artifact_path.exists() else "○ MODEL OFFLINE")
    st.caption("Educational use • Historical records")

st.markdown("""
<div class="hero">
 <div class="hero-content">
  <div class="pill"><span class="pill-dot"></span> ROAD SAFETY / MACHINE INTELLIGENCE</div>
  <h1>SEE THE SIGNAL.<br>READ THE ROAD.</h1>
  <p>Explore historical road-accident patterns and classify the severity category associated with a recorded accident scenario.</p>
 </div>
</div>
""", unsafe_allow_html=True)

if page == "Home":
    st.markdown('<div class="eyebrow">01 / Command overview</div>', unsafe_allow_html=True)
    st.header("Designed for people who use the road.")
    st.write("A sharp, accessible interface for exploring historical road conditions and understanding the severity category predicted by a machine-learning model.")
    total_records = len(data) if data is not None else None
    total_features = len(features)
    severity_count = data[target].nunique() if data is not None and target in data.columns else len(artifact.get("class_labels", []))
    m1, m2, m3 = st.columns(3)
    with m1:
        val = f"{total_records:,}" if total_records is not None else "—"
        note = "HISTORICAL DATASET" if total_records is not None else "ROAD.CSV NOT FOUND"
        st.markdown(f'<div class="metric"><div class="metric-label">Records indexed</div><div class="metric-value">{val}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric"><div class="metric-label">Input signals</div><div class="metric-value">{total_features:02d}</div><div class="metric-note">ROAD / VEHICLE / DRIVER</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric"><div class="metric-label">Severity classes</div><div class="metric-value">{severity_count:02d}</div><div class="metric-note">TARGET CATEGORIES</div></div>', unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.05, 1])
    with left:
        st.markdown('<div class="eyebrow">Platform / capabilities</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-card">
          <h3>01 — Classify a scenario</h3>
          <p>Enter road, weather, vehicle and driver conditions to receive a severity classification.</p>
          <h3>02 — Explore the context</h3>
          <p>Review patterns across historical records with simple, interactive charts.</p>
          <h3>03 — Read responsibly</h3>
          <p>Understand what a model can indicate—and where its predictions should not be used.</p>
        </div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown('<div class="eyebrow">Dataset / class distribution</div>', unsafe_allow_html=True)
        if data is not None and target in data.columns:
            st.bar_chart(data[target].astype(str).value_counts(), use_container_width=True)
        else:
            st.info("Place Road.csv beside app.py to enable the severity chart.")
    st.write("")
    if st.button("OPEN CLASSIFICATION →", use_container_width=True):
        st.session_state["road_safe_page"] = "Classify Severity"
        st.rerun()

elif page == "Classify Severity":
    st.markdown('<div class="eyebrow">02 / Classification console</div>', unsafe_allow_html=True)
    st.header("Describe the scenario.")
    st.write("Select the closest matching conditions from the dataset. RoadSafe will classify the recorded severity category.")
    st.info("This tool classifies the severity label of a scenario; it does not predict whether an accident will happen.")
    with st.form("severity_form"):
        input_values = {}
        if data is not None:
            left, right = st.columns(2)
            for i, feature in enumerate(features):
                with (left if i % 2 == 0 else right):
                    series = data[feature] if feature in data.columns else pd.Series(dtype="object")
                    # Use category dropdowns for categorical inputs so users do not have to guess encoded IDs.
                    categorical_features = {
                        "Day_of_week", "Age_band_of_driver", "Sex_of_driver",
                        "Educational_level", "Vehicle_driver_relation",
                        "Driving_experience", "Type_of_vehicle", "Owner_of_vehicle",
                        "Service_year_of_vehicle", "Defect_of_vehicle",
                        "Area_accident_occured", "Lanes_or_Medians", "Road_allignment",
                        "Types_of_Junction", "Road_surface_type",
                        "Road_surface_conditions", "Light_conditions",
                        "Weather_conditions", "Type_of_collision",
                        "Vehicle_movement", "Pedestrian_movement", "Cause_of_accident"
                    }
                    if feature.lower() == "time":
                        choices = [
                            "00:00:00", "03:00:00", "06:00:00", "09:00:00",
                            "12:00:00", "15:00:00", "17:00:00", "18:00:00",
                            "20:00:00", "22:00:00", "23:00:00"
                        ]
                    elif feature in feature_options and feature_options[feature]:
                        choices = [str(x) for x in feature_options[feature]]
                    elif feature in categorical_features or series.dtype == "object" or str(series.dtype) == "category":
                        choices = series.dropna().astype(str).value_counts().index.tolist()
                        choices = sorted(choices, key=lambda x: x.lower())
                    else:
                        choices = []

                    if choices:
                        input_values[feature] = st.selectbox(
                            "Time of day" if feature.lower() == "time" else feature.replace("_", " ").title(),
                            choices,
                            key=f"scenario_{feature}"
                        )
                    else:
                        num = pd.to_numeric(series, errors="coerce").dropna()
                        default = float(num.median()) if not num.empty else 1.0
                        minimum = float(num.min()) if not num.empty else 0.0
                        maximum = float(num.max()) if not num.empty else 100.0
                        input_values[feature] = st.number_input(
                            feature.replace("_", " ").title(),
                            min_value=minimum,
                            max_value=maximum,
                            value=min(max(default, minimum), maximum),
                            step=1.0,
                            key=f"scenario_{feature}"
                        )
        else:
            st.warning("Road.csv is needed to populate valid dropdown choices. Put it beside app.py.")
            for feature in features:
                input_values[feature] = st.text_input(feature.replace("_", " ").title(), value="Unknown")
        submitted = st.form_submit_button("RUN CLASSIFICATION  ↗", use_container_width=True)

    if submitted:
        input_df = pd.DataFrame([input_values], columns=features)
        try:
            prediction = model.predict(input_df)[0]
            st.markdown(
                f'<div class="result-card"><div class="result-label">CLASSIFICATION OUTPUT / {model_name}</div><div class="result-value">{prediction}</div><p>Predicted severity category for the supplied record.</p></div>',
                unsafe_allow_html=True
            )
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(input_df)[0]
                prob_df = pd.DataFrame({
                    "Severity category": model.classes_,
                    "Estimated probability (%)": (probs * 100).round(1)
                }).sort_values("Estimated probability (%)", ascending=False)
                st.markdown('<div class="eyebrow">Model confidence / estimated probabilities</div>', unsafe_allow_html=True)
                st.bar_chart(prob_df.set_index("Severity category"))
                st.dataframe(prob_df, hide_index=True, use_container_width=True)
            st.caption("Probabilities are model estimates and may not be calibrated. Educational use only.")
        except Exception as exc:
            st.error(f"Could not classify this input. Ensure values match the training data format. Details: {exc}")

elif page == "Road Safety Insights":
    st.markdown('<div class="eyebrow">03 / Historical patterns</div>', unsafe_allow_html=True)
    st.header("Signals in the data.")
    if data is None:
        st.warning("Place Road.csv beside app.py to enable insights.")
    else:
        if target in data.columns:
            options = sorted(data[target].dropna().astype(str).unique())
            selected = st.multiselect("Severity categories", options, default=options)
            filtered = data[data[target].astype(str).isin(selected)]
        else:
            filtered = data.copy()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Records by severity")
            if target in filtered.columns:
                st.bar_chart(filtered[target].astype(str).value_counts())
        with c2:
            candidates = ["Weather_conditions", "Road_surface_conditions", "Light_conditions", "Day_of_week", "Types_of_Junction"]
            available = [c for c in candidates if c in filtered.columns]
            if available:
                selected_feature = st.selectbox("Explore a condition", available)
                st.markdown(f"### {selected_feature.replace('_', ' ').title()}")
                st.bar_chart(filtered[selected_feature].astype(str).value_counts().head(15))
        st.markdown("### Sample records")
        st.dataframe(filtered.head(100), use_container_width=True, hide_index=True)

elif page == "About":
    st.markdown('<div class="eyebrow">04 / Project profile</div>', unsafe_allow_html=True)
    st.header("Built to explore—not overclaim.")
    st.markdown("""
    <div class="info-card">
      <h3>Project scope</h3>
      <p>RoadSafe combines a web-scraping demonstration, statistical analysis and multiclass classification using a historical road-accident dataset.</p>
      <h3>What the model does</h3>
      <p>Classifies the severity label for an input record using patterns learned from the supplied data.</p>
      <h3>What it does not do</h3>
      <p>It does not predict whether an accident will occur, guarantee real-world outcomes, or establish that a road or weather condition caused an accident.</p>
      <h3>Data note</h3>
      <p>Road.csv is the analysis dataset. The official public data catalogue is used separately to demonstrate web scraping and is not represented as the source of each CSV row.</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Active model: {model_name}  •  Target: {target}")
