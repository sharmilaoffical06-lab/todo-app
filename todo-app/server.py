from flask import Flask, jsonify, request, send_from_directory
import sqlite3, os

app = Flask(__name__, static_folder='public', static_url_path='')

DB_PATH = os.path.join(os.path.dirname(__file__), 'todos.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                text      TEXT    NOT NULL,
                done      INTEGER NOT NULL DEFAULT 0,
                priority  TEXT    NOT NULL DEFAULT "low",
                created_at TEXT   NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


@app.route('/')
def index():
    return send_from_directory('public', 'index.html')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    with get_db() as conn:
        rows = conn.execute(
            'SELECT * FROM tasks ORDER BY created_at DESC'
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    text = (data.get('text') or '').strip()
    priority = data.get('priority', 'low')
    if priority not in ('low', 'med', 'high'):
        priority = 'low'
    if not text:
        return jsonify({'error': 'text required'}), 400
    with get_db() as conn:
        cur = conn.execute(
            'INSERT INTO tasks (text, priority) VALUES (?, ?)',
            (text, priority)
        )
        conn.commit()
        row = conn.execute('SELECT * FROM tasks WHERE id = ?', (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201


@app.route('/api/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    data = request.get_json()
    with get_db() as conn:
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if not task:
            return jsonify({'error': 'not found'}), 404

        done     = int(data['done'])     if 'done'     in data else task['done']
        text     = data['text'].strip()  if 'text'     in data else task['text']
        priority = data['priority']      if 'priority' in data else task['priority']

        conn.execute(
            'UPDATE tasks SET done=?, text=?, priority=? WHERE id=?',
            (done, text, priority, task_id)
        )
        conn.commit()
        row = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    return jsonify(dict(row))


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with get_db() as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
    return jsonify({'deleted': task_id})


@app.route('/api/tasks/clear-done', methods=['DELETE'])
def clear_done():
    with get_db() as conn:
        conn.execute('DELETE FROM tasks WHERE done = 1')
        conn.commit()
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    init_db()
    print('\n  🟡  DO IT server running → http://localhost:5000\n')
    app.run(debug=True, port=5000)
