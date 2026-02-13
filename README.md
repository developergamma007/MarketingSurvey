## Full-stack setup (Next.js + Python)

This project has:

- `frontend`: Next.js (TypeScript, Tailwind, App Router)
- `backend`: Python FastAPI app

### Frontend (Next.js)

From the `frontend` folder:

```bash
cd frontend
npm install         # already run once by the generator, but safe to re-run
npm run dev
```

The app will start by default on `http://localhost:3000`.

### Backend (FastAPI)

From the `backend` folder:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`.

