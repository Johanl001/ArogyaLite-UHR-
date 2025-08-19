# Quick Start (Local)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-free.txt
python scripts/init_free_db.py

# Run API
uvicorn backend.main:app --reload --port 8000

# (Optional) Run Gradio demo
python app.py
```

## Frontend
```bash
cd frontend
npm install
npm run dev
# Set VITE_API_URL=http://localhost:8000 for local dev
```

## Docker
```bash
docker compose -f deployment/docker-compose.free.yml up --build
```
