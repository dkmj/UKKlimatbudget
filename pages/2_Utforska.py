"""Utforska — Sök och filtrera bland alla klimatåtgärder."""

import json

import pandas as pd
import streamlit as st

from lib.auth import check_password
from lib.favorites import (
    MAX_FAVORITES,
    add_favorite,
    is_favorite,
    remove_favorite,
    render_sidebar_favorites,
)
from lib.feedback import thumbs_feedback
from lib.style import inject_custom_css

st.set_page_config(page_title="Utforska — Klimatbudget", page_icon="🔍", layout="wide")

if not check_password():
    st.stop()

inject_custom_css()
render_sidebar_favorites()

with open("data/klimatbudget.json", encoding="utf-8") as f:
    data = json.load(f)

with open("data/abbreviations.json", encoding="utf-8") as f:
    abbrevs = json.load(f)

områden = data["områden"]

st.title("🔍 Utforska klimatåtgärder")
st.markdown("Sök, filtrera och jämför alla 72 klimatåtgärder i budgeten.")

# Cross-reference navigation button
st.markdown(
    '<a href="#korsreferens" '
    'style="display:inline-block;padding:8px 20px;background:#5B2D8E;color:#F0EDE8;'
    "border-radius:8px;text-decoration:none;font-weight:500;font-size:0.9em;"
    'border:1px solid #7B2D8E;margin-bottom:1rem;">'
    "📋 Gå till korsreferens per organisation ⬇️</a>",
    unsafe_allow_html=True,
)

# Build flat dataframe
rows = []
for o in områden:
    for a in o["åtgärder"]:
        rows.append(
            {
                "Nr": a["nr"],
                "Område": o["namn"],
                "Åtgärd": a["åtgärd"],
                "Ansvariga": ", ".join(a["ansvariga"]),
                "Ansvariga_list": a["ansvariga"],
            }
        )
df = pd.DataFrame(rows)

# --- Filters ---
col1, col2, col3 = st.columns(3)

with col1:
    selected_area = st.multiselect(
        "Filtrera efter område",
        options=[o["namn"] for o in områden],
        default=[],
        placeholder="Alla områden",
    )

with col2:
    all_orgs = sorted(
        set(
            r
            for row in rows
            for r in row["Ansvariga_list"]
            if r != "Alla nämnder och bolag"
        )
    )
    selected_org = st.multiselect(
        "Filtrera efter ansvarig",
        options=all_orgs,
        default=[],
        format_func=lambda x: f"{x} ({abbrevs.get(x, x)})",
        placeholder="Alla organisationer",
    )

with col3:
    search_text = st.text_input(
        "Sök i åtgärdstext", placeholder="t.ex. cykel, energi, plast..."
    )

# Apply filters
filtered = df.copy()

if selected_area:
    filtered = filtered[filtered["Område"].isin(selected_area)]

if selected_org:
    filtered = filtered[
        filtered["Ansvariga_list"].apply(
            lambda orgs: any(o in orgs for o in selected_org)
        )
    ]

if search_text:
    filtered = filtered[
        filtered["Åtgärd"].str.contains(search_text, case=False, na=False)
    ]

# --- Results ---
st.markdown(f"**{len(filtered)} åtgärder** matchar dina filter")

# Display as expandable cards
for _, row in filtered.iterrows():
    with st.expander(f"**{row['Nr']}** — {row['Åtgärd'][:80]}..."):
        st.markdown(f"**Område:** {row['Område']}")
        st.markdown(f"**Åtgärd:** {row['Åtgärd']}")

        # Show responsible parties with full names
        ansvariga_full = []
        for org in row["Ansvariga_list"]:
            full_name = abbrevs.get(org, org)
            if full_name != org:
                ansvariga_full.append(f"**{org}** ({full_name})")
            else:
                ansvariga_full.append(f"**{org}**")
        st.markdown(f"**Ansvariga:** {', '.join(ansvariga_full)}")

        # Star/favorite toggle (replaces thumbs up/down)
        if is_favorite(row["Nr"]):
            if st.button("★ Ta bort favorit", key=f"unfav_{row['Nr']}"):
                remove_favorite(row["Nr"])
                st.rerun()
        else:
            favs = len([f for f in st.session_state.get("favorites", [])])
            if favs >= MAX_FAVORITES:
                st.caption(
                    f"☆ Favoritlistan är full ({MAX_FAVORITES}/{MAX_FAVORITES}). Ta bort en först."
                )
            else:
                if st.button("☆ Lägg till favorit", key=f"fav_{row['Nr']}"):
                    add_favorite(row["Nr"], row["Åtgärd"], row["Område"])
                    st.rerun()

st.markdown("---")

# --- Cross-reference view ---
st.markdown('<div id="korsreferens"></div>', unsafe_allow_html=True)
st.subheader("Korsreferens: Åtgärder per organisation")
st.markdown("Välj en organisation för att se alla dess åtgärder samlade.")

selected_cross_org = st.selectbox(
    "Välj organisation",
    options=[""] + all_orgs,
    format_func=lambda x: f"{x} — {abbrevs.get(x, x)}" if x else "Välj...",
)

if selected_cross_org:
    org_actions = df[
        df["Ansvariga_list"].apply(lambda orgs: selected_cross_org in orgs)
    ]
    st.markdown(
        f"**{abbrevs.get(selected_cross_org, selected_cross_org)}** "
        f"ansvarar för **{len(org_actions)} åtgärder** inom följande områden:"
    )

    for area_name in org_actions["Område"].unique():
        area_subset = org_actions[org_actions["Område"] == area_name]
        st.markdown(f"### {area_name}")
        for _, row in area_subset.iterrows():
            st.markdown(f"- **{row['Nr']}**: {row['Åtgärd']}")

    thumbs_feedback(
        "korsreferens",
        f"Organisation: {selected_cross_org}",
        key_suffix=f"cross_{selected_cross_org}",
    )
