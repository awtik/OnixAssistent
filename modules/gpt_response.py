from g4f.client import Client
import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

client = Client()

def get_answer(prompt):
    if not prompt:
        return "Empty prompt provided."

    cleaned_prompt = ' '.join(word for word in prompt.split() if word.lower() != 'оникс')

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": cleaned_prompt}],
            language='ru'
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)