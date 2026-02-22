# DO IT — Todo App

A sleek, brutalist-themed todo app powered by **Python + Flask + SQLite**.

## Setup

### Requirements
- Python 3.8+

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the server
```bash
python server.py
```

Then open **http://localhost:5000** in your browser.

## Features
- ✅ Add, complete, and delete tasks
- 🔴 Priority levels: Low / Med / High
- 🔍 Filter: All / Active / Done / High Priority
- 📊 Progress bar + stats
- 🗄️ SQLite database — data persists forever
- ⚡ REST API (Flask)

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create a task `{ text, priority }` |
| PATCH | `/api/tasks/:id` | Update a task `{ done, text, priority }` |
| DELETE | `/api/tasks/:id` | Delete a task |
| DELETE | `/api/tasks/clear-done` | Remove all completed tasks |

## File Structure
```
todo-app/
├── server.py        ← Flask backend + SQLite
├── requirements.txt ← Python dependencies
├── todos.db         ← SQLite database (auto-created on first run)
├── README.md
└── public/
    └── index.html   ← Frontend (HTML/CSS/JS)
```
