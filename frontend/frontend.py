import os, requests
import gradio as gr
from backend.main import app  # Optional: if you want to call FastAPI functions directly

# Example functions to call your backend API
# Replace these with your actual endpoints and logic

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def get_status():
    """Check API status"""
    response = requests.get(f"{BASE_URL}/")
    return response.json()

def add_patient(name, age, email):
    """Send a new patient record to backend"""
    payload = {"name": name, "age": age, "email": email}
    response = requests.post(f"{BASE_URL}/patients/create", json=payload)
    return response.json()

def get_patient_records(patient_id):
    """Retrieve patient records"""
    response = requests.get(f"{BASE_URL}/patients/{patient_id}/records")
    return response.json()


# --- Gradio Interface ---
with gr.Blocks() as demo:
    gr.Markdown("# ArogyaLite-UHR Dashboard")
    
    with gr.Tab("Status"):
        status_btn = gr.Button("Check API Status")
        status_output = gr.JSON()
        status_btn.click(get_status, inputs=None, outputs=status_output)
    
    with gr.Tab("Add Patient"):
        name = gr.Textbox(label="Name")
        age = gr.Number(label="Age")
        email = gr.Textbox(label="Email")
        add_btn = gr.Button("Add Patient")
        add_output = gr.JSON()
        add_btn.click(add_patient, inputs=[name, age, email], outputs=add_output)
    
    with gr.Tab("Get Records"):
        patient_id = gr.Textbox(label="Patient ID")
        get_btn = gr.Button("Get Records")
        get_output = gr.JSON()
        get_btn.click(get_patient_records, inputs=patient_id, outputs=get_output)

demo.launch()
