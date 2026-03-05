# -*- coding: utf-8 -*-
"""Översikt — Dashboard med nyckeltal och visualiseringar."""

import json
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from lib.auth import check_password
from lib.feedback import thumbs_feedback

st.set_page_config(page_title="Översikt — Klimatbudget", page_icon="📊", layout="wide")

if not check_password():
    st.stop()

# Load data
with open("data/klimatbudget.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("data/abbreviations.json", "r", encoding="utf-8") as f:
    abbrevs = json.load(f)

meta = data["meta"]
områden = data["områden"]

st.title("📊 Översikt")
st.markdown("Nyckeltal och visualiseringar från Uppsala kommuns klimatbudget.")

# --- Key metrics ---
st.subheader("Nyckeltal")
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Utsläpp kommungeografiskt",
    f"{meta['utsläpp_2023_kton']} kton",
    delta=f"{meta['utsläpp_2023_kton'] - meta['utsläpp_2022_kton']:+d} kton vs 2022",
    delta_color="inverse",
)
c2.metric(
    "Årlig minskning krävs",
    f"{meta['årlig_minskning_procent']}%",
    delta="per år till 2030",
    delta_color="off",
)
c3.metric(
    "Gång/cykel/kollektivt",
    f"{meta['andel_gang_cykel_kollektiv_2024_procent']}%",
    delta=f"Mål 2028: {meta['andel_gang_cykel_kollektiv_mål_2028_procent']}%",
    delta_color="off",
)
c4.metric(
    "Materialåtervinning",
    f"{meta['materialåtervinning_2024_procent']}%",
    delta=f"Mål 2028: {meta['materialåtervinning_mål_2028_procent']}%",
    delta_color="off",
)

st.markdown("---")

# --- Actions per area ---
st.subheader("Antal åtgärder per område")
area_counts = []
for o in områden:
    area_counts.append({"Område": o["namn"], "Antal åtgärder": len(o["åtgärder"])})

df_areas = pd.DataFrame(area_counts)
fig_areas = px.bar(
    df_areas,
    x="Område",
    y="Antal åtgärder",
    color="Område",
    color_discrete_sequence=px.colors.qualitative.Set2,
    text="Antal åtgärder",
)
fig_areas.update_layout(showlegend=False, yaxis_title="", xaxis_title="")
fig_areas.update_traces(textposition="outside")
st.plotly_chart(fig_areas, use_container_width=True)

thumbs_feedback("oversikt_area_chart", "Diagram: åtgärder per område", key_suffix="areas")

# --- Responsibility distribution ---
st.subheader("Ansvar — vilka organisationer bär flest åtgärder?")

resp_count: dict[str, int] = {}
for o in områden:
    for a in o["åtgärder"]:
        for r in a["ansvariga"]:
            if r != "Alla nämnder och bolag":
                resp_count[r] = resp_count.get(r, 0) + 1

df_resp = pd.DataFrame(
    [
        {"Organisation": abbrevs.get(k, k), "Förkortning": k, "Antal åtgärder": v}
        for k, v in sorted(resp_count.items(), key=lambda x: -x[1])
    ]
)

fig_resp = px.bar(
    df_resp,
    x="Antal åtgärder",
    y="Organisation",
    orientation="h",
    color="Antal åtgärder",
    color_continuous_scale="Greens",
    text="Antal åtgärder",
    hover_data=["Förkortning"],
)
fig_resp.update_layout(
    yaxis={"categoryorder": "total ascending"},
    showlegend=False,
    coloraxis_showscale=False,
    xaxis_title="",
    yaxis_title="",
    height=500,
)
fig_resp.update_traces(textposition="outside")
st.plotly_chart(fig_resp, use_container_width=True)

thumbs_feedback("oversikt_resp_chart", "Diagram: ansvar per organisation", key_suffix="resp")

# --- Emissions trajectory (simplified) ---
st.subheader("Utsläppsbana — kommungeografiskt")
st.info(
    "Utsläppen av växthusgaser inom Uppsalas kommungeografiska område ska minska med "
    "18–22 procent per år för att utsläppsutrymmet inte ska överskridas. "
    "Målet är klimatneutralitet 2030 och klimatpositivitet 2050."
)

# Simple projection based on known data points
years = list(range(2015, 2051))
historical = {2015: 1050, 2016: 1020, 2017: 1000, 2018: 980, 2019: 950, 2020: 880, 2022: 807, 2023: 816}

hist_years = sorted(historical.keys())
hist_values = [historical[y] for y in hist_years]

# Budget trajectory: 20% reduction per year from 2023
budget_years = list(range(2023, 2051))
budget_values = [816]
for i in range(1, len(budget_years)):
    budget_values.append(budget_values[-1] * 0.80)

fig_emissions = go.Figure()
fig_emissions.add_trace(
    go.Scatter(
        x=hist_years,
        y=hist_values,
        mode="lines+markers",
        name="Historiska utsläpp",
        line=dict(color="#1976D2", width=3),
    )
)
fig_emissions.add_trace(
    go.Scatter(
        x=budget_years,
        y=budget_values,
        mode="lines",
        name="Utsläppsbudget (20%/år)",
        line=dict(color="#2E7D32", width=2, dash="dash"),
        fill="tozeroy",
        fillcolor="rgba(46, 125, 50, 0.1)",
    )
)
fig_emissions.update_layout(
    yaxis_title="kton CO₂e",
    xaxis_title="År",
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    height=400,
)
st.plotly_chart(fig_emissions, use_container_width=True)

thumbs_feedback("oversikt_emissions", "Graf: utsläppsbana", key_suffix="emissions")

st.markdown("---")
st.caption("Källa: Mål och budget 2026, Uppsala kommun, sidorna 37–44")
