#!/usr/bin/env python3
"""
Build docs/index.html from the essay Markdown file.
The MD file is the single source of truth for essay text and the timestamp.
Run this after any text edits, then commit docs/index.html.
"""

import subprocess
import re
from pathlib import Path

MD  = "Life-and-Death.md"
OUT = "docs/index.html"

# ── Read source ──────────────────────────────────────────────────────────────
text = Path(MD).read_text(encoding="utf-8")

# Extract "Last updated" timestamp from MD
ts_match = re.search(r'Last updated: ([\d-]+ · [\d:]+)', text)
timestamp = ts_match.group(1) if ts_match else ""

# ── Extract essay body ───────────────────────────────────────────────────────
# Collect lines between the opening header block and "## Archival Materials".
# Skip: headings, byline, date line, and the *Last updated* line.
# Keep: all paragraphs and --- section-break lines (pandoc renders them as <hr>).
lines = text.split('\n')
body_lines = []
in_body = False
for line in lines:
    if re.match(r'^## Archival', line):       # stop at archival section
        break
    if re.match(r'^#{1,6}\s', line):          # skip all headings
        continue
    if re.match(r'^by ', line, re.I):         # skip byline
        continue
    if re.match(r'^\d{4}-\d{2}-\d{2}', line): # skip date line
        continue
    if re.match(r'^\*Last updated', line):    # skip timestamp line
        continue
    if not in_body and line.strip() == '':    # skip leading blank lines
        continue
    in_body = True
    body_lines.append(line)

body_md = '\n'.join(body_lines).rstrip()

# ── Convert essay body to HTML via pandoc ────────────────────────────────────
result = subprocess.run(
    ['pandoc', '--from', 'markdown+smart', '--to', 'html'],
    input=body_md.encode('utf-8'), capture_output=True, check=True
)
body_html = result.stdout.decode('utf-8').strip()

# Remove any trailing <hr> that pandoc generates from the --- before ## Archival
body_html = re.sub(r'\s*<hr\s*/?>\s*$', '', body_html)

# Indent every line by two spaces to match the rest of the HTML
body_html = '\n'.join(
    ('  ' + line) if line else ''
    for line in body_html.split('\n')
)

# ── Assemble full HTML ───────────────────────────────────────────────────────
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Learning the Meaning of Life and Death</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container">

  <h1>Learning the Meaning of Life and Death</h1>
  <p class="subtitle">Recollections of September 17, 1966, North Hollywood, California</p>
  <p class="byline">by Jim U&#39;Ren &nbsp;&middot;&nbsp; March 15, 2026</p>

{body_html}

  <p class="timestamp"><em>Last updated: {timestamp}</em></p>

  <hr>

  <div class="archival">
    <h2>Archival Materials</h2>

    <div class="gallery">
      <figure>
        <img src="MAP_Last-Flight-of-N9143Z.jpg" alt="Route map of the final flight of AJ-1 Savage N9143Z">
        <figcaption>Route map of the final flight of AJ-1 Savage N9143Z from Burbank Airport, September 17, 1966</figcaption>
      </figure>
      <figure>
        <img src="PHOTO_North-American-AJ-1-that-crashed-on-Goodland-Ave-C.jpg" alt="The AJ-1 Savage N9143Z after the crash on Goodland Avenue">
        <figcaption>The AJ-1 Savage N9143Z at the crash site on Goodland Avenue, North Hollywood, September 17, 1966</figcaption>
      </figure>
      <figure>
        <img src="PHOTO_NA-AJ-1-0000100586.jpg" alt="North American AJ-1 Savage in fire-tanker configuration">
        <figcaption>North American AJ-1 Savage in aerial fire-tanker configuration</figcaption>
      </figure>
      <figure>
        <img src="AJ-77-tanker-crew-on-ramp.jpeg" alt="AJ Savage tanker No. 77 with crew on the ramp">
        <figcaption>AJ Savage tanker No. 77 &mdash; the aircraft flown by Major Hennessy &mdash; with crew on the ramp</figcaption>
      </figure>
      <figure>
        <img src="Savage-N9143Z-77-side-KOM.jpg" alt="Side view of N9143Z, tanker No. 77">
        <figcaption>Side view of N9143Z, tanker No. 77</figcaption>
      </figure>
      <figure>
        <img src="Savage-N9143Z-engine-running-KOM.jpg" alt="N9143Z with engine running, pre-flight">
        <figcaption>N9143Z with engine running, pre-flight</figcaption>
      </figure>
      <figure>
        <img src="Newspaper-youngsters-examine-wreckage.jpeg" alt="Neighborhood youngsters examine wreckage in a North Hollywood yard">
        <figcaption>Neighborhood youngsters examine wreckage in a North Hollywood yard after the crash</figcaption>
      </figure>
      <figure>
        <img src="Newspaper-fire-crews-search-wreckage.jpeg" alt="Fire crews searching scattered wreckage in North Hollywood">
        <figcaption>City fire crews search scattered wreckage in a North Hollywood backyard. One engine lies at right; automobiles were destroyed in the crash.</figcaption>
      </figure>
      <figure>
        <img src="Newspaper-body-of-pilot-recovered.jpeg" alt="Body of pilot Jack Hennessy recovered from wreckage">
        <figcaption>Body of pilot Jack Hennessy, of Long Beach, covered on a stretcher after being recovered from the wreckage of AJ-77</figcaption>
      </figure>
      <figure>
        <img src="73807626_1450910410.jpg" alt="Headstone of Major John F. Hennessy, Forest Lawn Memorial Park, Glendale">
        <figcaption>Headstone of Major John F. Hennessy, Forest Lawn Memorial Park, Glendale, California &mdash; <em>Major, 729 Bomb Sq AF, World War II, Korea</em></figcaption>
      </figure>
      <figure>
        <img src="Screenshot-JAUs-msg-post-2024-01-09.png" alt="Online forum discussion about the Goodland Avenue crash, 2009">
        <figcaption>Online forum discussion about the Goodland Avenue crash, January 2009, including the author&#39;s recollection</figcaption>
      </figure>
    </div>

    <div class="documents-section">
      <h3>Documents</h3>
      <ul>
        <li><a href="LA-Times-9-17-66-Goodland-Plane-Crash.pdf" target="_blank">Los Angeles Times &mdash; news report on the crash, September 17, 1966 (PDF)</a></li>
        <li><a href="Accident-North-American-AJ-1-Savage-N9143Z.pdf" target="_blank">Official accident report for N9143Z (PDF)</a></li>
        <li><a href="NTSB-Accident-Report-Tanker-Crash-North-Hollywood-2008-09-17.htm" target="_blank">NTSB accident report documentation (HTM)</a></li>
        <li><a href="INFO_North-American-AJ-1-Bomber.htm" target="_blank">Background on the North American AJ-1 Savage aircraft type (HTM)</a></li>
        <li><a href="North-American-AJ-Savage-bomber.pdf" target="_blank">Technical reference: North American AJ Savage bomber (PDF)</a></li>
        <li><a href="EMAIL-thread_RE-Goodland-Crash.txt" target="_blank">Email exchange between the author and Roger LaPlante (2010), a neighbor who remembered the crash (TXT)</a></li>
      </ul>
    </div>

  </div>

</div>
</body>
</html>
'''

Path(OUT).write_text(html, encoding="utf-8")
print(f"HTML written to {OUT}")
