import os
import json
from typing import Dict, List, Optional
import requests
from .medical_ner import extract_entities as local_extract_entities
from .prescription_ai import suggest_prescription as local_suggest


def _hf_headers() -> Dict[str, str]:
    token = os.getenv("HUGGINGFACE_API_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
    return {"Authorization": f"Bearer {token}"} if token else {}


def _hf_ner(note: str) -> Optional[List[Dict]]:
    url = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
    headers = _hf_headers()
    if not headers:
        return None
    try:
        r = requests.post(url, headers=headers, json={"inputs": note}, timeout=15)
        r.raise_for_status()
        data = r.json()
        # HF may return list[list[entities]] or list[entities]
        entities = data[0] if (isinstance(data, list) and data and isinstance(data[0], list)) else data
        out = []
        if isinstance(entities, list):
            for e in entities:
                if isinstance(e, dict):
                    out.append({
                        "entity": e.get("entity_group") or e.get("entity") or "ENT",
                        "text": e.get("word") or e.get("text") or "",
                        "score": float(e.get("score", 0))
                    })
        return out
    except Exception:
        return None


def _hf_suggest(note: str) -> Optional[str]:
    url = "https://api-inference.huggingface.co/models/google/flan-t5-small"
    headers = _hf_headers()
    if not headers:
        return None
    prompt = f"Provide concise non-diagnostic care advice for this clinical note: {note}"
    try:
        r = requests.post(url, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 64}}, timeout=20)
        r.raise_for_status()
        data = r.json()
        # Typical format: [{"generated_text": "..."}] or dict variants
        if isinstance(data, list) and data and isinstance(data[0], dict):
            gen = data[0].get("generated_text") or data[0].get("summary_text")
            if isinstance(gen, str):
                return gen.strip()
        if isinstance(data, dict):
            gen = data.get("generated_text") or data.get("summary_text")
            if isinstance(gen, str):
                return gen.strip()
        return None
    except Exception:
        return None


def analyze_note(note: str) -> Dict:
    """Analyze a clinical note using configured provider.

    Provider selection via env:
    - AI_PROVIDER=hf uses Hugging Face Inference API (requires HUGGINGFACE_API_TOKEN)
    - default: local heuristic/transformers-on-device fallback
    """
    provider = (os.getenv("AI_PROVIDER") or "local").strip().lower()
    if provider == "hf":
        ents = _hf_ner(note) or []
        rx = _hf_suggest(note) or None
        if ents or rx:
            return {"provider": "hf", "entities": ents, "suggestion": rx or "No suggestion"}
        # fall through to local on failures

    # Local provider: try on-device transformers via free_models, then regex + rule-based advice
    ents_local = local_extract_entities(note) or []
    rx_local = local_suggest(note) or "No suggestion"
    return {"provider": "local", "entities": ents_local, "suggestion": rx_local}

