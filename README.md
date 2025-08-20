# ArogyaLite-UHR — Free Unified Digital Health Record (UHR) System

---
title: ArogyaLite-UHR
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
pinned: false
---

A fully free, open-source starter kit for a **Unified Digital Health Record** with an **offline-first** mindset.
Focuses on local processing, privacy, and zero-cost stack choices.

## Highlights
- FastAPI backend with SQLite (local-first)
- Gradio demo app for Hugging Face Spaces
- React + Vite frontend with offline PWA skeleton
- JWT auth (no external auth dependency)
- Optional local AI hooks (Hugging Face transformers)
- Minimal, auditable codebase

See `docs/FREE_SETUP.md` and `docs/API_DOCUMENTATION.md` for quick start and endpoints.

## .env template
Copy `.env.example` to `.env` and fill in values as needed. For a free AI option, set `AI_PROVIDER=hf` and create a free token at `https://huggingface.co/settings/tokens` (Read scope). Put it in `HUGGINGFACE_API_TOKEN`.
