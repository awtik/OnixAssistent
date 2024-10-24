from modules.sqltasks import DatabaseTask
from text_to_num import text2num
class Tasks:
    def __init__(self):
        self.db = DatabaseTask() # Initialization db class
        self.db.create()

    def task_create(self, text):
        prompt = ''
        word_list = text.split() # Create a list from string
        ind = 0
        for word in word_list:
            if word in ['создай', 'добавь', 'оникс', 'задачу', 'задачку']: # Check for search key in command
                del word_list[ind] # Removing it from string
                ind -= 1
            ind += 1
        prompt = ' '.join(word_list) # Compilate prompt list
        self.db.insert(prompt)

    def task_remove(self, text):
        for word in text.split():
            try:
                id = text2num(word, 'ru') # Try to find num in the command
                break
            except:
                pass
        self.db.del_task(id) # Del task
    
    def show_tasks(self):
        output = ''
        tasks = self.db.get_tasks()
        for task in tasks:
            output += f'\n{task[0]}) Task: {task[1]}' # 1) Task: test
        return output