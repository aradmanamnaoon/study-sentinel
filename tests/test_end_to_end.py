import json
import pytest
from study_sentinel.cli import main
from study_sentinel.contracts import Study
from study_sentinel.pipeline import run
from study_sentinel.io import read_study
from study_sentinel.errors import ValidationError

def test_demo_analysis(tmp_path):
    folder=tmp_path/"demo"
    report=tmp_path/"result"
    assert main(["demo","--out",str(folder),"--n","100","--seed","5"])==0
    assert main(["analyze","--manifest",str(folder/"study.json"),"--csv",str(folder/"synthetic_study.csv"),
                 "--out",str(report),"--permutations","50"])==0
    payload=json.loads((report/"report.json").read_text())
    assert payload["quality"]["participants"]==100
    assert len(payload["input_sha256"])==64
    assert payload["permutation"]["repeats"]==50
    assert (report/"report.md").exists()
    assert "participant_id" not in json.dumps(payload["quality"])
def test_duplicate_participants_rejected(tmp_path):
    folder=tmp_path/"demo"
    main(["demo","--out",str(folder),"--n","20"])
    csv=folder/"synthetic_study.csv"
    lines=csv.read_text().splitlines()
    lines[2]=lines[1]
    csv.write_text("\n".join(lines)+"\n")
    with pytest.raises(ValidationError): read_study(csv,Study.load(folder/"study.json"))
