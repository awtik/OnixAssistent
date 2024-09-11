from g4f.client import Client
from modules.sql import Database
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # Remove warning message in console

client = Client() # Initialization lib g4f
db = Database() # Initialization db
        
def get_answer(prompt):
    """Generation answer from prompt"""
    try:
        if prompt != '':
            out = ''
            word_list = prompt.split() # Create a list from string
            ind = 0
            for word in word_list:
                if word == 'оникс': # Check for search key in command
                    del word_list[ind] # Removing it from string
                    ind -= 1
                ind += 1
            out = ' '.join(word_list) # Compilate prompt list

            print('Start genereation')
            # Selecting model, setting chat properties
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": out+'. Пиши на русском'}],
                language='ru'
            )
            db.create() # Create table if its not exists
            db.insert(out, response.choices[0].message.content) # Insert data in DB
            return response.choices[0].message.content # Return generated answer
    except Exception as e: # If error - programm wont close
        print(e)

def show_answers():
    output = ''
    for answ in db.get_answers():
        output += f'\n{answ[0]}) Text: {answ[1]}\nAnswer: \n{answ[2]}'
    print(output)