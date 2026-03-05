# Uppsala Klimatbudget App — Specifikation & Plan

## Vision
En interaktiv webbapp som gör Uppsala kommuns klimatbudget tillgänglig, inspirerande
och användbar för kommunens medarbetare. Appen ersätter statiska Word-dokument med
AI-genererat innehåll, interaktiv utforskning och möjlighet till dialog.

## Målgrupp
- Förvaltningschefer ansvariga för klimatåtgärder (de "Ansvariga" i tabellerna)
- Klimat- och hållbarhetsmedarbetare
- Alla som arbetar med klimatomställningen inom Uppsala kommun

## Källa
Klimatbudgeten från "Mål och budget 2026 med plan för 2027–2028", sidorna 37–44.
Innehåller 72 numrerade klimatåtgärder inom 6 områden.

---

## Appens Komponenter

### 1. Översikt (Dashboard)
- Nyckeltal: 816 kton CO2e (2023), mål 18–22% minskning/år
- Interaktiv version av utsläppsgrafen (historik + budget 2021–2050)
- Fördelning av åtgärder per område (stapel/cirkeldiagram)
- Fördelning av ansvar per organisation

### 2. Utforska (Explorer)
- Sökbar/filtrerbar tabell med alla 72 åtgärder
- Filter: område, ansvarig organisation, fritext
- Klickbar detalj per åtgärd
- Korsreferens: "Visa allt som KS ansvarar för"
- Jämförelse mellan områden

### 3. Quiz
- Genererat via NotebookLM
- Interaktivt flervalformat i Streamlit
- Visar rätt svar + förklaring
- Poängräkning per session

### 4. Podcast
- Genererad via NotebookLM (audio overview)
- Inbäddad ljudspelare i appen
- Svenskspråkig djupdykning i klimatbudgeten

### 5. Presentation
- Genererad via NotebookLM (slide deck)
- Visas som PDF eller bild-karusell i appen
- Kan laddas ner för användning i möten

### 6. Chatt (valfri)
- AI-driven fråga/svar om klimatbudgeten
- Brainstorming kring prioritering av åtgärder
- Jämförelseanalys mellan områden
- Kräver Gemini API-nyckel (gratis tier räcker)
- Fungerar utan nyckel — visar meddelande om att aktivera

---

## Feedback-system
- Tumme upp/ner på:
  - Chattsvar
  - Varje komponent/sektion
  - Quiz-frågor
- Feedback sparas lokalt som JSON
- Ägaren (du) kan granska feedback innan release

---

## Innehållspipeline (uppdaterbar)

### Steg 1: Förbered källor
```bash
notebooklm create "Uppsala Klimatbudget"
notebooklm source add --type url "https://www.uppsala.se/.../klimatbudget/"
notebooklm source add --type file mal-och-budget-2026.pdf
# Lägg till fler källor vid behov
```

### Steg 2: Generera innehåll
```bash
notebooklm generate audio "djupdykning i klimatbudgeten på svenska"
notebooklm generate quiz "frågor om klimatbudgetens åtgärder och mål"
notebooklm generate slide-deck "presentation av klimatbudgeten"
notebooklm generate mind-map "kopplingar mellan områden och åtgärder"
```

### Steg 3: Ladda ner
```bash
notebooklm download audio -o assets/generated/podcast.wav
notebooklm download quiz -o assets/generated/quiz.json
notebooklm download slide-deck -o assets/generated/slides.pdf
notebooklm download mind-map -o assets/generated/mindmap.json
```

### Steg 4: Uppdatera appen
Appen läser automatiskt från `assets/generated/` — nya filer syns direkt.

---

## Autentisering
- Enkel delad lösenordsskärm vid start
- Konfigureras via Streamlit secrets eller miljövariabel
- Enkel loggning av sessioner (tidpunkt, varaktighet)

---

## Teknik
- Python 3.13, uv
- Streamlit (multi-page app)
- Plotly för interaktiva grafer
- notebooklm-py för innehållsgenerering
- google-generativeai (Gemini Flash) för chatt
- Hosting: Streamlit Community Cloud

---

## Iterativ Utveckling
1. ✅ Fas 0: Spec & projektuppsättning (denna fil)
2. 🔲 Fas 1: Grundapp med Översikt + Utforska (strukturerad data)
3. 🔲 Fas 2: NotebookLM-genererat innehåll (podcast, quiz, slides)
4. 🔲 Fas 3: Chatt + feedback-system
5. 🔲 Fas 4: Design, polering, iteration med dig
6. 🔲 Fas 5: Deploy till Streamlit Cloud

Varje fas avslutas med din granskning innan vi går vidare.

---

## Öppna Frågor
- [ ] Fullständig mappning av förkortningar (KS, GSN, UHEM, etc.)
- [ ] Eventuellt ytterligare källmaterial
- [ ] Önskad lösenordsfras för appen
- [ ] Gemini API-nyckel (om/när chatt aktiveras)
- [ ] Streamlit Cloud-konto kopplat till GitHub
