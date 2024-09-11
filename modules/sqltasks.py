import sqlite3
class DatabaseTask:
    def __init__(self):
        self.conn = sqlite3.connect("E:\projects\VoiceAssistent\databases\Assistent1.db")
        self.c = self.conn.cursor()
        self.create()
    def create(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (id INTEGER PRIMARY KEY, text TEXT)''')
    def insert(self, text):
        self.c.execute(f"INSERT INTO tasks (text) VALUES ('{text}')")
        self.conn.commit()
    def get_tasks(self):
        tasks = self.c.execute(f"SELECT * FROM tasks")
        return tasks
    def del_task(self, tid):
        self.c.execute(f"DELETE FROM tasks WHERE id = '{tid}'")
        self.conn.commit()
    def close_conn(self):
        self.conn.close()