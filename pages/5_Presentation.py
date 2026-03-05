# -*- coding: utf-8 -*-
"""Presentation & Tankekarta — Bildspel och interaktiv tankekarta."""

import json
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from lib.auth import check_password
from lib.feedback import thumbs_feedback
from lib.style import inject_custom_css

st.set_page_config(page_title="Presentation — Klimatbudget", page_icon="📑", layout="wide")

if not check_password():
    st.stop()

inject_custom_css()

st.title("📑 Presentation: Klimatbudgeten")
st.markdown("AI-genererad presentation och tankekarta för möten och workshops.")

# --- Slides ---
slides_dir = Path("assets/generated")
slide_files = list(slides_dir.glob("slides*.pdf")) + list(slides_dir.glob("slides*.pptx"))

if slide_files:
    for slide_file in sorted(slide_files):
        st.subheader("Slides")

        with open(slide_file, "rb") as f:
            pdf_bytes = f.read()

        size_mb = len(pdf_bytes) / (1024 * 1024)
        st.download_button(
            label=f"📥 Ladda ner presentation (PDF, {size_mb:.1f} MB)",
            data=pdf_bytes,
            file_name=slide_file.name,
            mime="application/pdf",
        )

        # Embed PDF using object tag (works better than iframe with data URIs)
        import base64
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_html = f'''
        <object
            data="data:application/pdf;base64,{b64}"
            type="application/pdf"
            width="100%"
            height="700px"
            style="border: 1px solid #ddd; border-radius: 8px;">
            <p>Din webbläsare kan inte visa PDF direkt.
            <a href="data:application/pdf;base64,{b64}" download="{slide_file.name}">Ladda ner PDF</a></p>
        </object>
        '''
        components.html(pdf_html, height=720)

        thumbs_feedback("presentation", slide_file.stem, key_suffix=slide_file.stem)
else:
    st.info("Ingen presentation har genererats ännu.")

# --- Mind Map ---
st.markdown("---")
st.subheader("🧠 Tankekarta")

mind_map_file = slides_dir / "mind_map.json"
if mind_map_file.exists():
    with open(mind_map_file, "r", encoding="utf-8") as f:
        mind_map_data = json.load(f)

    # Build interactive D3.js collapsible tree
    mind_map_json = json.dumps(mind_map_data, ensure_ascii=False)
    tree_html = f'''<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; overflow: hidden; }}
svg {{ width: 100%; height: 100%; }}
.node circle {{ fill: #fff; stroke: #2E7D32; stroke-width: 2.5px; cursor: pointer; transition: all 0.2s; }}
.node circle:hover {{ fill: #E8F5E9; stroke-width: 3px; r: 7; }}
.node circle.has-children {{ fill: #E8F5E9; }}
.node circle.collapsed {{ fill: #FFF3E0; stroke: #F57C00; }}
.node text {{ font-size: 13px; fill: #333; }}
.node--root text {{ font-size: 15px; font-weight: 700; fill: #1B5E20; }}
.link {{ fill: none; stroke: #C8E6C9; stroke-width: 1.5px; }}
.tooltip {{ position: absolute; background: #333; color: #fff; padding: 6px 10px; border-radius: 4px;
  font-size: 12px; pointer-events: none; opacity: 0; transition: opacity 0.2s; }}
</style>
</head><body>
<div class="tooltip" id="tooltip"></div>
<svg></svg>
<script>
const data = {mind_map_json};
const width = document.body.clientWidth;
const height = 650;
const margin = {{top: 20, right: 200, bottom: 20, left: 120}};

const svg = d3.select("svg")
  .attr("viewBox", [0, 0, width, height])
  .append("g")
  .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

const treeLayout = d3.tree().size([height - margin.top - margin.bottom, width - margin.left - margin.right - 100]);

const root = d3.hierarchy(data);
root.x0 = (height - margin.top - margin.bottom) / 2;
root.y0 = 0;

// Start with first level expanded
root.children && root.children.forEach(c => {{
  if (c.children) {{
    c._children = c.children;
    c.children = null;
  }}
}});
// But expand root children
root.children = root.data.children ? root.children || d3.hierarchy(data).children : null;
// Reset — just expand all
const rootFresh = d3.hierarchy(data);
rootFresh.x0 = (height - margin.top - margin.bottom) / 2;
rootFresh.y0 = 0;

function collapse(d) {{
  if (d.children) {{
    d._children = d.children;
    d._children.forEach(collapse);
    d.children = null;
  }}
}}
// Collapse after level 1
rootFresh.children && rootFresh.children.forEach(collapse);

update(rootFresh);

function update(source) {{
  const treeData = treeLayout(rootFresh);
  const nodes = treeData.descendants();
  const links = treeData.links();

  // Horizontal spacing
  nodes.forEach(d => {{ d.y = d.depth * 180; }});

  // --- Nodes ---
  const node = svg.selectAll("g.node")
    .data(nodes, d => d.data.name);

  const nodeEnter = node.enter().append("g")
    .attr("class", d => "node" + (d.depth === 0 ? " node--root" : ""))
    .attr("transform", d => `translate(${{source.y0}},${{source.x0}})`)
    .on("click", (event, d) => {{
      if (d.children) {{
        d._children = d.children;
        d.children = null;
      }} else if (d._children) {{
        d.children = d._children;
        d._children = null;
      }}
      update(d);
    }});

  nodeEnter.append("circle")
    .attr("r", 5)
    .attr("class", d => d._children ? "collapsed" : (d.children ? "has-children" : ""));

  nodeEnter.append("text")
    .attr("dy", "0.35em")
    .attr("x", d => d.children || d._children ? -12 : 12)
    .attr("text-anchor", d => d.children || d._children ? "end" : "start")
    .text(d => d.data.name);

  // Update
  const nodeUpdate = nodeEnter.merge(node);
  nodeUpdate.transition().duration(400)
    .attr("transform", d => `translate(${{d.y}},${{d.x}})`);

  nodeUpdate.select("circle")
    .attr("class", d => d._children ? "collapsed" : (d.children ? "has-children" : ""));

  // Exit
  const nodeExit = node.exit().transition().duration(400)
    .attr("transform", d => `translate(${{source.y}},${{source.x}})`)
    .remove();
  nodeExit.select("circle").attr("r", 0);
  nodeExit.select("text").style("fill-opacity", 0);

  // --- Links ---
  const link = svg.selectAll("path.link")
    .data(links, d => d.target.data.name);

  const linkEnter = link.enter().insert("path", "g")
    .attr("class", "link")
    .attr("d", d => {{
      const o = {{x: source.x0, y: source.y0}};
      return diagonal(o, o);
    }});

  linkEnter.merge(link).transition().duration(400)
    .attr("d", d => diagonal(d.source, d.target));

  link.exit().transition().duration(400)
    .attr("d", d => {{
      const o = {{x: source.x, y: source.y}};
      return diagonal(o, o);
    }}).remove();

  // Store positions
  nodes.forEach(d => {{ d.x0 = d.x; d.y0 = d.y; }});
}}

function diagonal(s, d) {{
  return `M ${{s.y}} ${{s.x}}
          C ${{(s.y + d.y) / 2}} ${{s.x}},
            ${{(s.y + d.y) / 2}} ${{d.x}},
            ${{d.y}} ${{d.x}}`;
}}
</script></body></html>'''

    components.html(tree_html, height=680, scrolling=False)
    st.caption("💡 Klicka på en nod för att expandera/fälla ihop grenar.")

    # Download raw data
    with open(mind_map_file, "rb") as f:
        st.download_button(
            label="📥 Ladda ner tankekarta (JSON)",
            data=f.read(),
            file_name="tankekarta_klimatbudget.json",
            mime="application/json",
        )

    thumbs_feedback("mind_map", "tankekarta", key_suffix="mind_map")
else:
    # Check for old HTML format
    old_html = slides_dir / "mind_map.html"
    if old_html.exists():
        with open(old_html, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=700, scrolling=True)
        thumbs_feedback("mind_map", "tankekarta_html", key_suffix="mind_map_html")
    else:
        st.info("Ingen tankekarta har genererats ännu.")

# --- Flashcards ---
flashcards_file = slides_dir / "flashcards.json"
if flashcards_file.exists():
    st.markdown("---")
    st.subheader("🃏 Flashkort")

    with open(flashcards_file, "r", encoding="utf-8") as f:
        fc_data = json.load(f)

    cards = fc_data.get("cards", [])
    if cards:
        st.markdown(f"**{len(cards)} flashkort** — klicka för att visa svaret.")

        # Pagination
        if "fc_index" not in st.session_state:
            st.session_state.fc_index = 0

        card_idx = st.session_state.fc_index
        card = cards[card_idx]

        st.progress((card_idx + 1) / len(cards), text=f"Kort {card_idx + 1} av {len(cards)}")

        # Strip LaTeX from flashcard text
        import re
        def strip_latex(text):
            text = re.sub(r"\$([^$]+)\$", r"\1", text)
            return text.replace("\\%", "%").replace("\\", "")

        st.markdown(f"### {strip_latex(card['front'])}")

        if st.button("Visa svar", key=f"fc_reveal_{card_idx}"):
            st.info(strip_latex(card["back"]))

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("⬅️ Föregående", disabled=card_idx == 0, key=f"fc_prev_{card_idx}"):
                st.session_state.fc_index -= 1
                st.rerun()
        with col3:
            if st.button("Nästa ➡️", disabled=card_idx >= len(cards) - 1, key=f"fc_next_{card_idx}"):
                st.session_state.fc_index += 1
                st.rerun()

        thumbs_feedback("flashcards", f"kort_{card_idx}", key_suffix=f"fc_{card_idx}")
