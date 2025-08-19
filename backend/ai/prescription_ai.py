from typing import Optional

def suggest_prescription(clinical_note: str) -> Optional[str]:
    t = clinical_note.lower()
    if "fever" in t:
        return "Paracetamol 500mg, hydration, rest. If persists >48h, consult physician."
    if "cough" in t:
        return "Warm fluids, throat lozenges; if productive >7d or blood, seek evaluation."
    return "General advice: balanced diet, hydration, sleep 7-8h."
