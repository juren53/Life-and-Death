#!/usr/bin/env python3
"""
Build docs/cover-letter.html from submissions/LAT-cover-letter.md.
The MD file is the source of truth for the letter text, but the public
page redacts direct contact info (phone/email) — the source file keeps
the real values for actual email submission.
"""

import subprocess
from pathlib import Path

MD  = "submissions/LAT-cover-letter.md"
OUT = "docs/cover-letter.html"

# ── Read source ──────────────────────────────────────────────────────────────
text = Path(MD).read_text(encoding="utf-8")

# Redact direct contact info for the public page
text = text.replace(
    "310-614-7844\njim.uren@gmail.com",
    "(contact information available on request)"
)

# ── Convert to HTML via pandoc ───────────────────────────────────────────────
result = subprocess.run(
    ['pandoc', '--from', 'markdown+smart', '--to', 'html'],
    input=text.encode('utf-8'), capture_output=True, check=True
)
body_html = result.stdout.decode('utf-8').strip()

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
  <title>LA Times Op-Ed Submission Letter — Learning the Meaning of Life and Death</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container">

  <h1>LA Times Op-Ed Submission</h1>
  <p class="subtitle">Cover letter and manuscript for &ldquo;Learning the Meaning of Life and Death&rdquo;</p>
  <p class="byline">by Jim U&#39;Ren</p>

{body_html}

  <p class="timestamp"><a href="index.html">&larr; Back to the full essay</a></p>

</div>
</body>
</html>
'''

Path(OUT).write_text(html, encoding="utf-8")
print(f"HTML written to {OUT}")
