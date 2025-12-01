# SynCode — Real-Time Pair Programming Prototype

## Overview
SynCode is a small prototype demonstrating a real-time pair-programming experience:
- Backend: FastAPI + WebSockets + Postgres (async)
- Frontend: React + TypeScript + Redux Toolkit (minimal)
- Mocked /autocomplete endpoint for AI-style suggestions

## File Structure
```bash
SynCode/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── rooms.py
│   │   │   └── autocomplete.py
│   │   ├── services/
│   │   │   └── room_service.py
│   │   └── websockets.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── store.ts
│       ├── features/
│       │   └── editorSlice.ts
│       ├── components/
│       │   └── Editor.tsx
│       └── styles/
│           └── global.css
│
├── README.md
└── .gitignore
```

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

## Notes

1. WebSocket endpoint: ws://localhost:8000/ws/{roomId}
2. Create a room: POST http://localhost:8000/rooms (returns JSON { "roomId": "<uuid>" })
3. Autocomplete endpoint: POST http://localhost:8000/autocomplete

## What to improve

1. Use Monaco/CodeMirror for editor ergonomics
2. Implement OT/CRDT for robust concurrency
3. Add user presence, cursors, nicknames
4. Add migrations (Alembic) and tests
