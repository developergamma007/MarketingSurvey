# Survey Application - Complete Setup Documentation

This document explains every command and step used to set up this full-stack survey application with Next.js frontend and Python FastAPI backend.

---

## Project Structure

```
Survey/
├── frontend/          # Next.js application (React + TypeScript)
├── backend/           # Python FastAPI application
└── README.md          # Quick start guide
```

---

## 1. Initial Project Setup

### 1.1 Create Next.js Frontend Application

**Command:**
```bash
cd /Users/gamma/Desktop/Survey
npx create-next-app@latest frontend --typescript --eslint --tailwind --src-dir --app --no-experimental-app --use-npm --yes
```

**What it does:**
- Creates a new Next.js application in the `frontend` folder
- Uses TypeScript for type safety
- Includes ESLint for code linting
- Sets up Tailwind CSS for styling
- Uses `src/` directory structure
- Uses App Router (modern Next.js routing)
- Uses npm as package manager
- `--yes` flag auto-accepts all prompts

**Result:** A fully configured Next.js project with all dependencies installed.

---

### 1.2 Create Python Backend Structure

**Commands:**
```bash
cd /Users/gamma/Desktop/Survey
mkdir -p backend
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

**What each command does:**
- `mkdir -p backend` - Creates the backend directory
- `python3 -m venv .venv` - Creates a Python virtual environment named `.venv`
- `source .venv/bin/activate` - Activates the virtual environment (on macOS/Linux)
  - On Windows: `.venv\Scripts\activate`
- `pip install --upgrade pip` - Upgrades pip to the latest version

**Result:** A Python virtual environment ready for package installation.

---

### 1.3 Install Backend Dependencies

**Commands:**
```bash
cd backend
source .venv/bin/activate
pip install fastapi uvicorn
pip install sqlalchemy psycopg2-binary python-dotenv
```

**What each package does:**
- `fastapi` - Modern Python web framework for building APIs
- `uvicorn` - ASGI server to run FastAPI applications
- `sqlalchemy` - SQL toolkit and ORM for database operations
- `psycopg2-binary` - PostgreSQL adapter for Python
- `python-dotenv` - Loads environment variables from `.env` file

**Result:** All backend dependencies installed in the virtual environment.

---

### 1.4 Install Frontend Dependencies

**Command:**
```bash
cd frontend
npm install -D tailwindcss @tailwindcss/postcss
```

**What it does:**
- Installs Tailwind CSS and PostCSS plugin required by the Next.js configuration
- `-D` flag installs as dev dependencies

**Result:** Tailwind CSS properly configured for styling.

---

## 2. Database Setup

### 2.1 Install PostgreSQL

**If PostgreSQL is not installed:**

**On macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**On Windows:**
Download and install from: https://www.postgresql.org/download/windows/

---

### 2.2 Create Database

**Commands:**
```bash
# Connect to PostgreSQL
psql -U postgres

# Inside psql prompt:
CREATE DATABASE surveydb;
\q
```

**What it does:**
- Creates a new PostgreSQL database named `surveydb`

---

### 2.3 Configure Database Connection

**Create `.env` file in `backend/` directory:**

**Command:**
```bash
cd backend
touch .env
```

**Add to `.env` file:**
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/surveydb
```

**What it does:**
- Sets the database connection string
- Format: `postgresql://username:password@host:port/database`
- Adjust username, password, host, and port as needed

**Note:** The `.env` file is gitignored for security. Never commit database credentials.

---

## 3. Running the Application

### 3.1 Start Backend Server

**Commands:**
```bash
cd backend
source .venv/bin/activate  # Activate virtual environment
uvicorn main:app --reload --port 8000
```

**What it does:**
- `uvicorn` - Runs the ASGI server
- `main:app` - Points to the `app` object in `main.py`
- `--reload` - Enables auto-reload on code changes (development mode)
- `--port 8000` - Runs server on port 8000

**Result:** Backend API available at `http://localhost:8000`

**API Endpoints:**
- `GET http://localhost:8000/health` - Health check endpoint
- `POST http://localhost:8000/surveys` - Submit survey data

---

### 3.2 Start Frontend Development Server

**Commands:**
```bash
cd frontend
npm run dev
```

**What it does:**
- Starts Next.js development server with Turbopack
- Enables hot module replacement (HMR) for instant updates
- Runs on port 3000 by default (or next available port)

**Result:** Frontend available at `http://localhost:3000`

---

## 4. Checking the Database

### 4.1 Using psql (PostgreSQL Command Line)

**Connect to database:**
```bash
psql -U postgres -d surveydb
```

**Inside psql, useful commands:**
```sql
-- List all tables
\dt

-- View table structure
\d survey_responses

-- View all survey responses
SELECT * FROM survey_responses;

-- Count total surveys
SELECT COUNT(*) FROM survey_responses;

-- View recent surveys (last 10)
SELECT id, assembly, gba_ward, polling_station_name, created_at 
FROM survey_responses 
ORDER BY created_at DESC 
LIMIT 10;

-- View surveys with location data
SELECT id, assembly, latitude, longitude, created_at 
FROM survey_responses 
WHERE latitude IS NOT NULL AND longitude IS NOT NULL;

-- Exit psql
\q
```

---

### 4.2 Using pgAdmin (GUI Tool)

1. Install pgAdmin from: https://www.pgadmin.org/download/
2. Open pgAdmin and connect to your PostgreSQL server
3. Navigate to: Servers → PostgreSQL → Databases → surveydb → Schemas → public → Tables → survey_responses
4. Right-click on `survey_responses` → View/Edit Data → All Rows

---

### 4.3 Using Python Script to Query Database

**Create a script `backend/check_db.py`:**
```python
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/surveydb",
)

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM survey_responses"))
    count = result.scalar()
    print(f"Total surveys: {count}")
    
    result = conn.execute(text("SELECT * FROM survey_responses ORDER BY created_at DESC LIMIT 5"))
    for row in result:
        print(row)
```

**Run it:**
```bash
cd backend
source .venv/bin/activate
python check_db.py
```

---

### 4.4 Using FastAPI Interactive Docs

1. Start the backend server: `uvicorn main:app --reload --port 8000`
2. Open browser: `http://localhost:8000/docs`
3. Use the interactive Swagger UI to test endpoints
4. Note: This shows API endpoints, not direct database access

---

## 5. Troubleshooting Commands

### 5.1 Fix Port Already in Use

**Find process using port 3000:**
```bash
lsof -ti:3000
```

**Kill the process:**
```bash
kill -9 $(lsof -ti:3000)
```

**Or for port 8000:**
```bash
kill -9 $(lsof -ti:8000)
```

---

### 5.2 Reset Database Tables

**Drop and recreate tables:**
```python
# In Python shell or script
from backend.main import Base, engine
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
```

---

### 5.3 Check Virtual Environment

**Verify virtual environment is active:**
```bash
which python  # Should show path to .venv/bin/python
```

**Reinstall dependencies:**
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
```

---

### 5.4 Clear Next.js Cache

**If build errors occur:**
```bash
cd frontend
rm -rf .next
npm run dev
```

---

## 6. File Structure Explained

### Backend Files:
- `main.py` - FastAPI application, database models, and API endpoints
- `requirements.txt` - Python package dependencies
- `.env` - Database connection string (not in git)
- `.venv/` - Python virtual environment (not in git)

### Frontend Files:
- `src/app/page.tsx` - Main survey form component
- `src/app/layout.tsx` - Root layout component
- `src/app/globals.css` - Global styles with Tailwind
- `package.json` - Node.js dependencies
- `.next/` - Next.js build cache (not in git)

---

## 7. Common Workflows

### Submit a Survey:
1. Start backend: `cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser: `http://localhost:3000`
4. Fill out the form and submit
5. Check database: `psql -U postgres -d surveydb` then `SELECT * FROM survey_responses;`

### View Survey Data:
```bash
psql -U postgres -d surveydb -c "SELECT id, assembly, gba_ward, interviewer_name, created_at FROM survey_responses ORDER BY created_at DESC LIMIT 10;"
```

---

## 8. Environment Variables

### Backend `.env` file:
```
DATABASE_URL=postgresql://username:password@localhost:5432/surveydb
```

**Change these values based on your PostgreSQL setup:**
- `username` - Your PostgreSQL username (default: `postgres`)
- `password` - Your PostgreSQL password
- `localhost` - Database host (use `127.0.0.1` if `localhost` doesn't work)
- `5432` - PostgreSQL port (default: `5432`)
- `surveydb` - Database name

---

## 9. Production Deployment Notes

### Backend:
- Remove `--reload` flag in production
- Use environment variables for sensitive data
- Set up proper CORS origins
- Use production-grade ASGI server (Gunicorn + Uvicorn workers)

### Frontend:
- Run `npm run build` to create production build
- Run `npm start` to serve production build
- Configure environment variables for API URL

---

## Summary

This project uses:
- **Frontend:** Next.js 16 with TypeScript, Tailwind CSS, App Router
- **Backend:** FastAPI with SQLAlchemy ORM
- **Database:** PostgreSQL
- **Development:** Hot reload enabled for both frontend and backend

All commands are documented above. The database can be checked using psql, pgAdmin, or custom Python scripts.

---

## 10. Recent Changes & Fixes

### [2026-02-13] Database Connection Fix
- **Issue**: Backend failed to connect as default `postgres` user (role did not exist).
- **Fix**: Created `backend/.env` configuration to use local system user `gamma`.
- **Change**: Added `DATABASE_URL="postgresql://gamma@localhost:5432/surveydb"` to `.env`.
- **Verify**: Confirmed `survey_responses` table creation with `verify_fix.py`.

### [2026-02-13] Authentication & Responses View
- **Feature**: Added JWT-based authentication.
- **Backend**:
    - Installed `passlib`, `python-jose`, `python-multipart`.
    - Added `POST /token` for login.
    - Added protected `GET /api/responses` endpoint.
    - Default user: `admin` / `admin`.
- **Frontend**:
    - Added Login page at `/login`.
    - Added Protected Responses Dashboard at `/responses`.

### [2026-02-13] UI Enhancements & Logic Updates
- **Feature**: Comprehensive Responses View & Audio Handling.
- **Backend**: Updated `SurveyRead` model to include `audio_base64`.
- **Frontend**:
    -   **Submission**: Added automatic stop recording trigger on form submission.
    -   **Responses**: Expanded table to show all fields (demographics, location, questions).
    -   **Audio**: Added in-browser audio player for listening to response recordings.
    -   **Analytics**: Added `recharts` and `lucide-react` for data visualization.
    -   **Dashboard**: Implemented tabbed interface with summary cards and charts (Party Preference, Gender, Top Candidates).
- **Mobile App**:
    -   Initialized Expo project at `/mobile-app`.
    -   Implemented Login Screen with JWT storage.
    -   Implemented Survey Submission with **Audio Recording** and **GPS Location**.
    -   Implemented Responses List View.
    -   **Native Build**: Ejected to bare workflow (`prebuild`).
        -   `ios/` and `android/` directories generated.
        -   Ready for Xcode / Android Studio usage.
