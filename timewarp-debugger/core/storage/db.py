import sqlite3
import json

class StorageEngine:
    def __init__(self, db_path="timewarp.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_db()
        
    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                thread_id INTEGER,
                event_type TEXT,
                function TEXT,
                line_no INTEGER,
                source_code TEXT,
                stack_depth INTEGER,
                locals_json TEXT
            )
        ''')
        self.conn.commit()
        
    def save_events(self, events):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM events") # Clear old events for thin implementation
        for e in events:
            cursor.execute('''
                INSERT INTO events (timestamp, thread_id, event_type, function, line_no, source_code, stack_depth, locals_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                e.get('time'),
                e.get('thread_id', 0),
                e.get('event'),
                e.get('function'),
                e.get('line'),
                e.get('source', ''),
                e.get('depth', 0),
                json.dumps(e.get('locals', {}))
            ))
        self.conn.commit()

    def get_all_events(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM events ORDER BY id ASC")
        rows = cursor.fetchall()
        
        events = []
        for r in rows:
            events.append({
                "id": r[0],
                "time": r[1],
                "thread_id": r[2],
                "event": r[3],
                "function": r[4],
                "line": r[5],
                "source": r[6],
                "depth": r[7],
                "locals": json.loads(r[8])
            })
        return events
