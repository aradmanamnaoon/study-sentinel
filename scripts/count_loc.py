"""Count nonblank, noncomment first-party implementation lines only."""
from pathlib import Path
from collections import defaultdict
root=Path(__file__).resolve().parents[1]
counts=defaultdict(int)
for base,extensions in (("src",{".py",".ts",".tsx",".js"}),):
    for p in (root/base).rglob("*"):
        if not p.is_file() or p.suffix not in extensions:continue
        lines=p.read_text(encoding="utf-8").splitlines()
        counts[p.suffix]+=sum(bool(line.strip()) and not line.lstrip().startswith(("#","//")) for line in lines)
print({"by_extension":dict(counts),"total":sum(counts.values()),"excludes":"tests, docs, scripts, fixtures, blank/comment-only"})
