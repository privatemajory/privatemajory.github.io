import re
import pathlib

root = pathlib.Path("_site")
missing = []
checked = 0
for f in root.rglob("*.html"):
    html = f.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r'(?:href|src)="(/[^"#?]*)"', html):
        url = m.group(1)
        target = root / url.lstrip("/")
        if url.endswith("/"):
            target = target / "index.html"
        checked += 1
        if not target.exists():
            missing.append(url)

print("checked", checked, "| unique missing:", len(set(missing)))
for url in sorted(set(missing))[:15]:
    print("MISSING", url)
