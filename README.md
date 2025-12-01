# SynCode — Real-Time Pair Programming Prototype

## Overview
SynCode is a small prototype demonstrating a real-time pair-programming experience:
- Backend: FastAPI + WebSockets + Postgres (async)
- Frontend: React + TypeScript + Redux Toolkit (minimal)
- Mocked /autocomplete endpoint for AI-style suggestions

## Run (quick)
1. Start backend + db (docker):
   ```bash
   cd SynCode/backend
   docker-compose up --build
   ```

Backend will be at http://localhost:8000

2. Start frontend:

```bash
cd SynCode/frontend
npm install
npm run dev
```

Frontend (Vite) default port is 3000 -> http://localhost:3000
