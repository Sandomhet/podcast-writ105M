#!/usr/bin/env python3
"""Inject script.md content into index.html script-body. Uses exact text from script."""
import re
import html as htmlmod

with open("script.md", "r", encoding="utf-8") as f:
    script = f.read()

with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

lines = script.strip().split("\n")
body_parts = []
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    if not stripped:
        i += 1
        continue
    if re.match(r"^\d{1,2}:\d{2}[–\-]\d{1,2}:\d{2}\s+.+", stripped):
        body_parts.append(f'              <p class="script-head">{htmlmod.escape(stripped)}</p>')
        i += 1
        continue
    if stripped.startswith("[") and stripped.endswith("]"):
        body_parts.append(f'              <p class="script-sfx">{htmlmod.escape(stripped)}</p>')
        i += 1
        continue
    # Speaker: must be single word + colon (Jelena:, Felicia:, Samuel:, James:)
    if re.match(r"^[A-Za-z]+:\s*$", stripped):
        speaker = stripped[:-1].strip()
        i += 1
        block = []
        while i < len(lines):
            L = lines[i]
            s = L.strip()
            if not s:
                i += 1
                continue
            if re.match(r"^[A-Za-z]+:\s*$", s):
                break
            if s.startswith("[") and s.endswith("]"):
                break
            if re.match(r"^\d{1,2}:\d{2}[–\-]\d{1,2}:\d{2}\s+", s):
                break
            block.append(s)
            i += 1
        if block:
            text = "<br>\n              ".join(htmlmod.escape(ln) for ln in block)
            body_parts.append(f'              <p class="speaker">{htmlmod.escape(speaker)}</p>')
            body_parts.append(f'              <p>{text}</p>')
        continue
    # Standalone narrative (opening music lines)
    body_parts.append(f'              <p>{htmlmod.escape(stripped)}</p>')
    i += 1

body_html = "\n\n".join(body_parts)

# Replace content between <div class="script-body"> and </div> (the closing of that div)
pattern = r'(<div class="script-body">)\s*.*?\s*(</div>\s*</details>)'
replacement = r'\1\n' + body_html + r'\n            \2'
new_html = re.sub(pattern, replacement, html_content, count=1, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("Done. Script body injected.")
