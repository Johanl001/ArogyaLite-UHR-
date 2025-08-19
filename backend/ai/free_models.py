from typing import Optional

_pipe = None

def _lazy_load():
    global _pipe
    if _pipe is not None:
        return _pipe
    try:
        from transformers import pipeline
        _pipe = pipeline("token-classification", model="dslim/bert-base-NER", grouped_entities=True)
        return _pipe
    except Exception:
        return None

def ner(text: str) -> Optional[list]:
    pipe = _lazy_load()
    if not pipe:
        return None
    try:
        return pipe(text)
    except Exception:
        return None
