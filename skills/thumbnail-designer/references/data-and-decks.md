# Data and Decks — infographics, charts, presentations, reports

Everything in this file carries numbers, and a number on a graphic is a claim. The design
job is to make the claim legible; it is never to make the claim stronger than the data.

---

## 1. The sourcing rule

**Every figure comes from the user or a named source, and the source appears on the
artefact.** Not in the chat message — on the graphic, where it travels with the image.

- No invented statistics, not even as placeholder "example" numbers that could be mistaken
  for real ones. If a layout needs filling, label the values visibly as placeholders.
- No chart presented as a screenshot of a real dashboard.
- `infographic.html` renders a red **NO SOURCE SUPPLIED — do not publish** badge when
  figures are present and `SOURCE` is empty. `make_deck.py` refuses to pass a `bars` or
  `stat` slide that has no `source`. Both are deliberate: the gap is made visible rather
  than quietly shipped.
- Rounding is fine; rounding that changes the conclusion is not.

See also `glow-and-light.md §6` on *stylised* data — an oversized glowing candlestick as
a visual device is honest because nobody reads it as a measurement. A realistic chart with
invented numbers is not.

---

## 2. Charts that do not mislead

- **Bars start at zero.** A truncated axis is the standard way a chart lies. Neither
  template offers the option.
- **Bars for comparison, lines for time, nothing for two numbers** — two numbers are a
  sentence, not a chart.
- **No pie chart past three slices**, and never for values that do not sum to a whole.
- **Label the bars directly.** A legend forces the eye to shuttle; a direct label does not.
- **One accent colour carries the point**; everything else is neutral. Colouring every bar
  differently means none of them is emphasised.
- **Never use 3D, perspective or drop shadows on data.** They distort the quantity they
  are drawing.
- Include units. "71" is not a number anyone can use.

---

## 3. Infographics

```
python scripts/render_html.py assets/templates/infographic.html out.png --size 1080x1350 \
  --var TITLE="..." --var STATS="38%|Housing;19%|Transport" \
  --var BARS="2021,42;2022,51" --var BAR_UNIT="%" --var SOURCE="..."
```

- **One argument per graphic.** An infographic that makes four points makes none.
- Two to six statistics. Past that nobody reads, they scroll.
- The headline states the finding, not the topic: "Housing takes 38% of everything"
  beats "Household spending".
- Put the biggest number first and largest — that is the whole hierarchy.
- Canvas: 1080×1350 for feed, 1080×1920 for story, 1200×630 for OG. For print, use
  `make_pdf.py` instead so the page has a physical size.
- Dense is right here — the stats fit pass shrinks the block rather than letting it
  overlap the chart — but white space between rows is what makes it readable.

---

## 4. Presentations

```
python scripts/make_deck.py --example > deck.json     # then edit it
python scripts/make_deck.py deck.json --pdf deck.pdf --png-dir slides/
```

**Be honest about the format.** This produces a **PDF deck plus slide PNGs**. Nothing here
can write a genuine `.pptx`. If the user needs an editable PowerPoint, say so and hand
over the PDF plus the JSON, which regenerates the whole deck after any edit — that is the
real editable source in this environment.

Design rules the template enforces or checks:

- **One idea per slide.** `make_deck.py` flags more than six bullets and any bullet over
  18 words — both mean the slide is a document.
- Slide size is 16:9 at its true physical size (338.667×190.5 mm), so it prints and
  projects correctly.
- Consistency beats variety: one accent, one type family, one footer, page numbers.
- Body text large. A deck is read from the back of a room — if it needs 14 pt, it needs
  to be a document instead.
- Structure: title → problem → evidence → what changes → ask. Section dividers for
  anything over about ten slides.
- A quote slide and a single-statistic slide are the two highest-impact layouts; use them
  where the argument turns.

---

## 5. Reports and long documents

This skill designs **covers, pull-quote pages, data pages and section openers** well. It
is not a page-layout engine: there is no text reflow across pages, no automatic
pagination, no table of contents generation.

For a long report, the honest split is: build the cover and the key spreads here, and say
plainly that the running text belongs in a word processor or a layout application. Do not
attempt a 40-page document one page at a time and call it a report.

---

## 6. Checks

- [ ] Every number traceable to the user or a named source, and the source is **on** the graphic
- [ ] Axis starts at zero; bar heights proportional to the values (look at them)
- [ ] Units present; labels direct, not in a legend
- [ ] Deck: page count in the PDF matches the slide count in the spec (the script compares)
- [ ] Opened the rendered output and re-read every figure against the source data
- [ ] Said which format was produced, and which was not

Related: `deliverables.md`, `niche-guide.md`, `glow-and-light.md §6`, `composition-type.md`,
`qa-export.md`.
