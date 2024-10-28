from g4f.client import Client
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # Remove warning message in console

client = Client() # Initialization lib g4f
        
async def get_answer(prompt):
    """Generation answer from prompt"""
    try:
        if not prompt:
            return "Empty prompt provided."
        
        # Убираем слово "оникс" из prompt
        out = ' '.join(word for word in prompt.split() if word.lower() != 'оникс')
        # Selecting model, setting chat properties
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": out}],
            language='ru'
        )
        return response.choices[0].message.content # Return generated answer
    except Exception as e: # If error - programm wont close
        return e