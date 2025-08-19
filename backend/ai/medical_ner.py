import re
from typing import List, Dict, Optional
from .free_models import ner

FALLBACK_TERMS = ["fever", "cough", "headache", "diabetes", "hypertension"]

def extract_entities(text: str) -> Optional[List[Dict]]:
    # Try transformer NER first
    out = ner(text)
    if out:
        return [{"entity": e.get("entity_group","ENT"), "text": e.get("word",""), "score": float(e.get("score",0))} for e in out]

    # Fallback naive extraction
    res = []
    for term in FALLBACK_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", text, flags=re.I):
            res.append({"entity": "TERM", "text": term, "score": 0.5})
    return res
