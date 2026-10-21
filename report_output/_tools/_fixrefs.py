# -*- coding: utf-8 -*-
"""Repair the split reference literals produced by the content generator.

Pattern: a line ending with  \",", "   opens a string that the following
line's leading quote accidentally closes.  Rebuild such lines as
   ...\",", "<rest of next line>"
so the tuple stays balanced.
"""
import re
import sys

PATH = "report_output/_tools/content_part3.py"

with open(PATH, encoding="utf-8") as fh:
    src = fh.read()

lines = src.split("\n")
out = []
i = 0
fixed = 0
while i < len(lines):
    line = lines[i]
    if re.search(r'\\",", "$', line) and i + 1 < len(lines):
        nxt = lines[i + 1]
        m = re.match(r'^\s*"(.*)",\s*(None|True|False)\),\s*$', nxt)
        if m:
            body, tail = m.group(1), m.group(2)
            # strip trailing comma inside the quoted body
            body = body.rstrip()
            if body.endswith(","):
                body = body[:-1]
            new = line + body + '", ' + tail + "),"
            out.append(new)
            fixed += 1
            i += 2
            continue
    out.append(line)
    i += 1

with open(PATH, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out))

print("fixed", fixed)
