# -*- coding: utf-8 -*-
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
P = "report_output/_tools/content_part3.py"
s = open(P, encoding="utf-8").read()
old = 'Google\\",\\"and the Firebase'
new = 'Google\\", \\"and the Firebase'
print("found:", old in s)
if old in s:
    s = s.replace(old, new)
    open(P, "w", encoding="utf-8").write(s)
    print("patched")
