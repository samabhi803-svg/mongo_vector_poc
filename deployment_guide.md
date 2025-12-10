# Deployment Guide to Render.com

## 1. Preparation
Ensure your repository contains:
- `backend/`
- `frontend/`
- `requirements.txt`
- `build.sh` (Created in root)

## 2. Create Service on Render
1.  Log in to [Render.com](https://render.com).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.

## 3. Usage Configuration
Configure the following settings:

| Setting | Value |
| :--- | :--- |
| **Name** | `mongo-vector-agent` |
| **Runtime** | **Python 3** |
| **Build Command** | `bash build.sh` |
| **Start Command** | `uvicorn backend.server:app --host 0.0.0.0 --port $PORT` |

## 4. Environment Variables
Add these in Render Dashboard:

| Key | Value |
| :--- | :--- |
| `MONGO_URI` | Your MongoDB Connection String |
| `DB_NAME` | `vector_poc_db` |
| `COLLECTION_NAME` | `documents` |
| `GOOGLE_API_KEY` | Your Google Gemini API Key |
| `PYTHON_VERSION` | `3.11.0` |

## 5. Deploy
Click **Create Web Service**. 
Your App will be live at `https://<your-service>.onrender.com`!
