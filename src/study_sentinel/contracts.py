"""Typed study manifest contracts."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json
from .errors import ValidationError

@dataclass(frozen=True)
class Scale:
    name: str
    items: tuple[str, ...]
    reverse: tuple[str, ...] = ()
    minimum: float = 1.0
    maximum: float = 5.0
    min_answered: int = 2
    def __post_init__(self):
        if not self.name or len(self.items) < 2 or len(set(self.items)) != len(self.items):
            raise ValidationError("scale needs a name and at least two distinct items")
        if not set(self.reverse).issubset(self.items): raise ValidationError("reverse items not in scale")
        if self.minimum >= self.maximum: raise ValidationError("invalid scale range")
        if not 2 <= self.min_answered <= len(self.items): raise ValidationError("invalid min_answered")

@dataclass(frozen=True)
class Study:
    name: str
    id_column: str
    outcome: str
    exposure: str
    covariates: tuple[str, ...] = ()
    scales: tuple[Scale, ...] = ()
    seed: int = 42
    missing_tokens: tuple[str, ...] = ("", "NA", "N/A", "null")
    privacy_min_group: int = 10
    def __post_init__(self):
        if not all((self.name,self.id_column,self.outcome,self.exposure)):
            raise ValidationError("study name/id/outcome/exposure required")
        if len({self.id_column,self.outcome,self.exposure})!=3: raise ValidationError("id/outcome/exposure distinct")
        if len(set(self.covariates))!=len(self.covariates): raise ValidationError("duplicate covariate")
        if self.privacy_min_group<2: raise ValidationError("privacy_min_group >= 2")
        if not 0 <= self.seed < 2**32: raise ValidationError("invalid random seed")
    def required_columns(self) -> set[str]:
        return {self.id_column,self.outcome,self.exposure,*self.covariates,*[i for s in self.scales for i in s.items]}
    def as_dict(self) -> dict:
        return asdict(self)
    @classmethod
    def load(cls, path: str | Path) -> "Study":
        try:
            obj=json.loads(Path(path).read_text(encoding="utf-8"))
            if not isinstance(obj,dict): raise ValidationError("manifest must be an object")
            scales=tuple(Scale(**{**d,"items":tuple(d["items"]),"reverse":tuple(d.get("reverse",()))}) for d in obj.pop("scales",()))
            for key in ("covariates","missing_tokens"):
                if key in obj: obj[key]=tuple(obj[key])
            return cls(**obj,scales=scales)
        except (OSError,TypeError,KeyError,ValueError) as exc:
            raise ValidationError(f"invalid manifest: {exc}") from exc
