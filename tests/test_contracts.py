import json
import pytest
from study_sentinel.contracts import Study,Scale
from study_sentinel.errors import ValidationError

def test_reverse_not_in_items():
    with pytest.raises(ValidationError): Scale("x",("a","b"),("c",))
def test_duplicate_items():
    with pytest.raises(ValidationError): Scale("x",("a","a"))
def test_study_requires_unique_roles():
    with pytest.raises(ValidationError): Study("bad","pid","x","x")
def test_manifest_roundtrip(tmp_path):
    s=Study("test","pid","y","x",scales=(Scale("s",("a","b")),))
    p=tmp_path/"study.json"
    p.write_text(json.dumps(s.as_dict()))
    assert Study.load(p)==s
