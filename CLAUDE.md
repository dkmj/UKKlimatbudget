# UKKlimatbudget - Project Guide

## What This Is
AI-powered interactive explorer for Uppsala kommun's klimatbudget (climate budget).
Streamlit web app that makes the klimatbudget accessible, interactive, and inspiring
for municipal staff who currently work with Word documents.

## Language
- ALL user-facing text is in **Swedish**
- ALL code comments, variable names, and file names are in **English**
- Always use UTF-8 encoding. Ensure Swedish characters (å, ä, ö, Å, Ä, Ö) work
  correctly through the entire pipeline.

## Tech Stack
- **Python 3.13** managed with `uv`
- **Streamlit** for web UI
- **Plotly** for interactive charts
- **notebooklm-py** (pipx-installed) for generating supporting materials
- **Gemini Flash** (optional) for live chat
- Hosted on **Streamlit Community Cloud**

## Project Structure
```
├── CLAUDE.md              # This file
├── plan.md                # Full specification
├── pyproject.toml         # uv project config
├── app.py                 # Streamlit app entry point
├── pages/                 # Streamlit multi-page app
│   ├── 1_Oversikt.py      # Dashboard overview
│   ├── 2_Utforska.py      # Explore actions by area/responsible party
│   ├── 3_Quiz.py          # Interactive quiz
│   ├── 4_Podcast.py       # Audio player
│   ├── 5_Presentation.py  # Slide deck viewer
│   └── 6_Chatt.py         # Live chat (optional Gemini)
├── data/
│   ├── klimatbudget.json   # Structured data: all 72 actions
│   └── abbreviations.json  # KS → Kommunstyrelsen mappings
├── assets/
│   └── generated/          # NotebookLM outputs (podcast, quiz, slides, etc.)
├── lib/
│   ├── auth.py             # Simple password authentication
│   ├── feedback.py         # Thumbs up/down feedback collection
│   └── chat.py             # Gemini Flash chat integration
├── scripts/
│   ├── setup_notebook.sh   # Create NotebookLM notebook + add sources
│   └── generate_content.sh # Generate all NotebookLM assets
└── .streamlit/
    └── config.toml         # Streamlit configuration
```

## Commands
- `uv run streamlit run app.py` — run the app locally
- `uv pip compile pyproject.toml -o requirements.txt` — generate requirements.txt for Streamlit Cloud

## Key Conventions
- Keep components modular — each page is independent and can be added/removed
- All pre-generated content goes in `assets/generated/`
- Source document: `mal-och-budget-2026.pdf` pages 37-44
- Feedback data is stored in `feedback/` directory as JSON files
- The app must work fully offline (without API keys) using pre-generated content
- When API key is available, chat feature activates automatically

## Abbreviations (Ansvariga)
These are the responsible parties referenced in the klimatbudget actions.
Full mapping in `data/abbreviations.json`. User will provide complete list.
Known so far: KS = Kommunstyrelsen

## Source Material
- Primary: `mal-och-budget-2026.pdf` pp. 37-44
- Web: https://www.uppsala.se/kommun-och-politik/kommunens-mal-och-budget/mal-och-budget/klimatbudget/
- Additional material may be added over time
