import os
import gradio as gr
from dotenv import load_dotenv
from backend.database.sqlite_manager import SQLiteManager
from backend.ai.medical_ner import extract_entities
from backend.ai.prescription_ai import suggest_prescription

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "./data/health.db")
db = SQLiteManager(DB_PATH)
db.init_db()

def register_patient(name, age, gender, contact):
    pid = db.add_patient({"name": name, "age": age, "gender": gender, "contact": contact})
    return f"Patient registered with ID: {pid}"

def list_patients():
    rows = db.list_patients()
    if not rows:
        return "No patients yet."
    return "\n".join([f"{r['id']}: {r['name']} ({r['gender']}, {r['age']})" for r in rows])

def save_record(patient_id, note_text):
    rid = db.add_record({"patient_id": int(patient_id), "note": note_text})
    entities = extract_entities(note_text) or []
    rx = suggest_prescription(note_text) or "No suggestion"
    return f"Record saved with ID: {rid}\nEntities: {entities}\nAI Suggestion: {rx}"

def create_health_interface():
    with gr.Blocks(title="ArogyaLite-UHR") as demo:
        gr.Markdown("# 🏥 ArogyaLite-UHR — Free Unified Health Record")
        with gr.Tab("Patient Registration"):
            name = gr.Textbox(label="Name")
            age = gr.Number(value=30, label="Age")
            gender = gr.Dropdown(choices=["Male","Female","Other"], value="Male", label="Gender")
            contact = gr.Textbox(label="Contact")
            out = gr.Textbox(label="Output")
            btn = gr.Button("Register")
            btn.click(fn=register_patient, inputs=[name, age, gender, contact], outputs=out)

        with gr.Tab("Patients"):
            refresh = gr.Button("List Patients")
            out2 = gr.Textbox(label="Patients", lines=10)
            refresh.click(fn=list_patients, outputs=out2)

        with gr.Tab("Add Clinical Note"):
            pid = gr.Number(value=1, label="Patient ID")
            note = gr.Textbox(lines=6, label="Clinical Note")
            out3 = gr.Textbox(label="Result", lines=8)
            btn2 = gr.Button("Save")
            btn2.click(fn=save_record, inputs=[pid, note], outputs=out3)

    return demo

if __name__ == "__main__":
    app = create_health_interface()
    app.launch(server_name="0.0.0.0", server_port=7860)
