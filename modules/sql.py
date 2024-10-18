import sqlite3
import os
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(f"{os.path.abspath(os.getcwd())}/databases/Assistent.db")
        self.c = self.conn.cursor()
        self.create()
    def create(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS gpt
                    (id INTEGER PRIMARY KEY, prompt TEXT, answer TEXT)''')
    def insert(self, prompt, answer):
        self.c.execute(f"INSERT INTO gpt (prompt, answer) VALUES ('{prompt}', '{answer}')")
        self.conn.commit()
    def get_answers(self):
        answers = self.c.execute(f"SELECT * FROM gpt")
        return answers
    def close_conn(self):
        self.conn.close()