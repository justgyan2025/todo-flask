import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
DATABASE = 'todo.db'


# ✅ Persistent Database Connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Close the database connection at the end of the request."""
    if 'db' in g:
        g.db.close()


# ✅ Initialize Database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS todos (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          title TEXT NOT NULL,
                          completed INTEGER NOT NULL DEFAULT 0
                        )''')
        conn.commit()

init_db()  # Create table at startup


# ✅ Home Route - Display Todos
@app.route('/')
def index():
    conn = get_db()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    return render_template('index.html', todos=todos)


# ✅ Add New Todo (Prevents Empty Submissions)
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title'].strip()
    if title:
        conn = get_db()
        conn.execute('INSERT INTO todos (title, completed) VALUES (?, ?)', (title, 0))
        conn.commit()
    return redirect(url_for('index'))


# ✅ Mark Todo as Completed
@app.route('/complete/<int:id>')
def complete(id):
    conn = get_db()
    conn.execute('UPDATE todos SET completed = 1 WHERE id = ?', (id,))
    conn.commit()
    return redirect(url_for('index'))


# ✅ Delete Todo
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    return redirect(url_for('index'))


# ✅ Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
