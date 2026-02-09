# Pantry Business Dashboard

A data visualization tool for tracking pantry business performance. This project serves as both a **Streamlit Dashboard** and a **Full-Stack Web App (React + FastAPI)**.

## 🚀 Quick Deployment
Deploy the **Streamlit Version** (easiest):
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

Deploy the **Backend API** (for Web App):
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

---

## 🌟 Features
- **Monthly Analysis**: November 2025 - January 2026.
- **Key Metrics**: Customer Retention, New vs Old, Gross Profit.
- **Visuals**: Interactive Line Charts, Pie Charts, and Bar Graphs.

## 🛠️ Project Structure
- `app.py`: Original Streamlit application.
- `web_app/`:
    - `backend/`: FastAPI Python Server.
    - `frontend/`: React + Vite Application.

## 💻 Local Setup

### Option 1: Run Streamlit App
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Option 2: Run Full Web App
Double-click **`run_web_app.bat`** on Windows.
*Or manually:*
1. **Backend**: `cd web_app/backend && uvicorn main:app --reload`
2. **Frontend**: `cd web_app/frontend && npm run dev`

## 🌐 Full Web App Deployment
- **Frontend**: Hosted on [Firebase Hosting](https://firebase.google.com/docs/hosting).
- **Backend**: Hosted on [Render](https://render.com/).

See [DEPLOYMENT_GUIDE_WEB_APP.md](DEPLOYMENT_GUIDE_WEB_APP.md) for details.
