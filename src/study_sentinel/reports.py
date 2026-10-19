"""Safe aggregate report export with atomic replacement."""
from pathlib import Path
import json,os,tempfile
from .errors import ValidationError

def write_report(report:dict,output:str|Path)->tuple[Path,Path]:
    target=Path(output)
    target.mkdir(parents=True,exist_ok=True)
    raw=json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    sections=["# Study Sentinel audit","",f"**Study:** {report['study']['name']}",
              f"**Participants:** {report['quality']['participants']}",
              f"**Input SHA-256:** `{report['input_sha256']}`","",
              "## Reproducibility","The exact CSV bytes are referenced by SHA-256. No participant rows are exported.","",
              "## Results"]
    for name in ("correlation","ols","permutation"):
        sections.extend([f"### {name}", "```json",json.dumps(report[name],indent=2,allow_nan=False),"```",""])
    sections.extend(["## Limitations","This report is descriptive/observational, not clinical or causal evidence.",""])
    md="\n".join(sections)
    def atomic(dest:Path,content:str):
        with tempfile.NamedTemporaryFile("w",encoding="utf8",dir=target,delete=False) as tmp:
            tmp.write(content);name=tmp.name
        os.replace(name,dest)
    js=target/"report.json"
    txt=target/"report.md"
    atomic(js,raw);atomic(txt,md)
    return js,txt
