# -*- coding: utf-8 -*-
"""Presentation & Begreppsträd — Bildspel och interaktivt begreppsträd."""

import json
import base64
import re
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from lib.auth import check_password
from lib.feedback import thumbs_feedback
from lib.favorites import render_sidebar_favorites
from lib.style import inject_custom_css

st.set_page_config(page_title="Presentation — Klimatbudget", page_icon="📑", layout="wide")

if not check_password():
    st.stop()

inject_custom_css()
render_sidebar_favorites()

st.title("📑 Presentation: Klimatbudgeten")
st.markdown("AI-genererad presentation och begreppsträd för möten och workshops.")

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

        # Render PDF using pdf.js for reliable cross-browser display
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_html = f'''<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<style>
body {{ margin: 0; background: #1A0A2E; padding: 10px; }}
.page-canvas {{
    display: block;
    margin: 0 auto 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.4);
    border-radius: 4px;
    max-width: 100%;
}}
.page-label {{
    text-align: center;
    color: #E8E0D8;
    font-family: sans-serif;
    font-size: 12px;
    margin-bottom: 8px;
    opacity: 0.7;
}}
</style>
</head><body>
<div id="pages"></div>
<script>
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
const pdfData = atob('{b64}');
const loadingTask = pdfjsLib.getDocument({{data: pdfData}});
loadingTask.promise.then(pdf => {{
    const container = document.getElementById('pages');
    for (let i = 1; i <= pdf.numPages; i++) {{
        pdf.getPage(i).then(page => {{
            const scale = 1.5;
            const viewport = page.getViewport({{scale}});
            const label = document.createElement('div');
            label.className = 'page-label';
            label.textContent = 'Sida ' + i + ' av ' + pdf.numPages;
            const canvas = document.createElement('canvas');
            canvas.className = 'page-canvas';
            canvas.width = viewport.width;
            canvas.height = viewport.height;
            container.appendChild(label);
            container.appendChild(canvas);
            page.render({{canvasContext: canvas.getContext('2d'), viewport}});
        }});
    }}
}});
</script>
</body></html>'''
        components.html(pdf_html, height=800, scrolling=True)

        thumbs_feedback("presentation", slide_file.stem, key_suffix=slide_file.stem)
else:
    st.info("Ingen presentation har genererats ännu.")

# --- Begreppsträd (formerly Tankekarta / Mind Map) ---
st.markdown("---")
st.subheader("🌳 Begreppsträd")

mind_map_file = slides_dir / "mind_map.json"
if mind_map_file.exists():
    with open(mind_map_file, "r", encoding="utf-8") as f:
        mind_map_data = json.load(f)

    # Build interactive D3.js collapsible tree with dark theme
    mind_map_json = json.dumps(mind_map_data, ensure_ascii=False)
    tree_html = f'''<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
       overflow: hidden; background: #1A0A2E; }}
svg {{ width: 100%; height: 100%; }}
.node circle {{
    fill: #2D1B4E; stroke: #7B2D8E; stroke-width: 2.5px;
    cursor: pointer; transition: all 0.2s;
}}
.node circle:hover {{ fill: #5B2D8E; stroke-width: 3px; r: 7; }}
.node circle.has-children {{ fill: #3D2560; stroke: #D94F7A; }}
.node circle.collapsed {{ fill: #D4A843; stroke: #D4A843; }}
.node text {{
    font-size: 13px; fill: #F0EDE8;
    text-shadow: 0 1px 3px rgba(0,0,0,0.8);
}}
.node--root text {{
    font-size: 15px; font-weight: 700; fill: #D94F7A;
    text-shadow: 0 1px 4px rgba(0,0,0,0.9);
}}
.link {{ fill: none; stroke: rgba(123, 45, 142, 0.5); stroke-width: 1.5px; }}
.download-btn {{
    position: absolute; top: 10px; right: 10px;
    background: #5B2D8E; color: #F0EDE8; border: 1px solid #7B2D8E;
    padding: 8px 16px; border-radius: 8px; cursor: pointer;
    font-size: 13px; font-family: sans-serif;
    transition: background 0.2s;
}}
.download-btn:hover {{ background: #7B2D8E; }}
</style>
</head><body>
<button class="download-btn" onclick="downloadAsImage()">📥 Ladda ner som bild</button>
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

let treeLayout = d3.tree().size([height - margin.top - margin.bottom, width - margin.left - margin.right - 100]);

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

function expandAll(d) {{
  if (d._children) {{
    d.children = d._children;
    d._children = null;
  }}
  if (d.children) d.children.forEach(expandAll);
}}

function downloadAsImage() {{
  // Expand all nodes for the screenshot
  expandAll(rootFresh);

  // Calculate the needed height based on total nodes
  const allNodes = rootFresh.descendants();
  const nodeCount = allNodes.length;
  const fullHeight = Math.max(800, nodeCount * 28);
  const fullWidth = Math.max(width, 1200);

  // Temporarily resize the tree layout
  treeLayout = d3.tree().size([fullHeight - 40, fullWidth - margin.left - margin.right - 100]);
  update(rootFresh);

  // Wait for transitions
  setTimeout(() => {{
    const svgEl = document.querySelector('svg');
    const gEl = svgEl.querySelector('g');

    // Update viewBox for full size
    svgEl.setAttribute('viewBox', `0 0 ${{fullWidth}} ${{fullHeight}}`);
    svgEl.setAttribute('width', fullWidth);
    svgEl.setAttribute('height', fullHeight);

    const svgData = new XMLSerializer().serializeToString(svgEl);
    const svgBlob = new Blob([svgData], {{type: 'image/svg+xml;charset=utf-8'}});
    const url = URL.createObjectURL(svgBlob);

    const img = new Image();
    img.onload = () => {{
      const scale = 2;
      const canvas = document.createElement('canvas');
      canvas.width = fullWidth * scale;
      canvas.height = fullHeight * scale;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#1A0A2E';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.scale(scale, scale);
      ctx.drawImage(img, 0, 0, fullWidth, fullHeight);

      canvas.toBlob(blob => {{
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'begreppsträd_klimatbudget.jpg';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        // Restore the original size
        svgEl.setAttribute('viewBox', `0 0 ${{width}} ${{height}}`);
        svgEl.removeAttribute('width');
        svgEl.removeAttribute('height');
        treeLayout = d3.tree().size([height - margin.top - margin.bottom, width - margin.left - margin.right - 100]);
        // Re-collapse to level 1
        rootFresh.children && rootFresh.children.forEach(collapse);
        update(rootFresh);
      }}, 'image/jpeg', 0.95);
    }};
    img.src = url;
  }}, 800);
}}

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

    components.html(tree_html, height=700, scrolling=False)
    st.caption("💡 Klicka på en nod för att expandera/fälla ihop grenar. "
               "Använd knappen \"Ladda ner som bild\" för en fullständig JPG.")

    thumbs_feedback("begreppsträd", "begreppsträd", key_suffix="mind_map")
else:
    # Check for old HTML format
    old_html = slides_dir / "mind_map.html"
    if old_html.exists():
        with open(old_html, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=700, scrolling=True)
        thumbs_feedback("begreppsträd", "begreppsträd_html", key_suffix="mind_map_html")
    else:
        st.info("Inget begreppsträd har genererats ännu.")

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
