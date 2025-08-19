# -----------------------------------------------
# ArogyaLite-UHR: Windows Install Script (PowerShell)
# Ensures all dependencies install using prebuilt wheels
# -----------------------------------------------

# Step 1: Upgrade pip, setuptools, wheel
Write-Host "Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

# Step 2: Clean pip cache to avoid old builds
Write-Host "Cleaning pip cache..."
pip cache purge

# Step 3: Install core packages using wheels only
Write-Host "Installing core packages with prebuilt wheels..."
pip install --only-binary=:all: pandas==2.2.2 numpy==1.26.4 scipy==1.11.1 scikit-learn==1.4.2 matplotlib==3.8.0 seaborn==0.13.2

# Step 4: Install FastAPI backend
Write-Host "Installing FastAPI and related backend packages..."
pip install fastapi==0.110.0 uvicorn==0.29.0 gradio==4.29.0 pydantic==2.7.1 python-dotenv==1.0.1 python-multipart==0.0.9 bcrypt==4.1.2 pyjwt==2.8.0 requests==2.31.0 aiofiles==23.2.1

# Step 5: Optional AI / NLP packages (comment if not needed)
Write-Host "Installing optional AI/NLP packages..."
pip install --only-binary=:all: torch==2.2.1 transformers==4.41.0 sentence-transformers==2.7.0 spacy==3.7.4

# Step 6: Optional Speech packages
Write-Host "Installing optional speech packages..."
pip install SpeechRecognition==3.10.1 pydub==0.25.1 pyaudio==0.2.14

# Step 7: Dev tools (optional)
Write-Host "Installing dev/testing tools..."
pip install pytest==8.2.0 black==24.3.0 isort==5.13.2

Write-Host "-----------------------------------------"
Write-Host "✅ Installation completed. Your environment is ready!"
Write-Host "Run 'python -m spacy download en_core_web_sm' if using spacy."
Write-Host "-----------------------------------------"
