import sqlite3
import os
class DatabaseTask:
    def __init__(self):
        "Initialization method"
        folder_path = "C:/Onix/databases" # Path to folder
        os.makedirs(folder_path, exist_ok=True) # Create a folder
        self.conn = sqlite3.connect(f"C:/Onix/databases/Assistent.db", check_same_thread=False) # Connect to DB
        self.c = self.conn.cursor() # Create cursor
        self.create() # create db if not exists
    def create(self):
        "Create db if not exists"
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (id INTEGER PRIMARY KEY, text TEXT)''') # Creating db
    def insert(self, text):
        "Insert new task into db"
        self.c.execute(f"INSERT INTO tasks (text) VALUES ('{text}')")
        self.conn.commit()
    def get_tasks(self):
        "Get all tasks from db"
        tasks = self.c.execute(f"SELECT * FROM tasks")
        return tasks
    def del_task(self, tid):
        "Delete task from db"
        self.c.execute(f"DELETE FROM tasks WHERE id = '{tid}'")
        self.conn.commit()
    def close_conn(self):
        "close conn method"
        self.conn.close()