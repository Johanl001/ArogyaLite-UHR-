"""Optional helper to pre-download a lightweight NER model for offline use."""
try:
    from transformers import pipeline
    print("Downloading dslim/bert-base-NER ...")
    _ = pipeline("token-classification", model="dslim/bert-base-NER")
    print("Done.")
except Exception as e:
    print("Failed to download model:", e)
