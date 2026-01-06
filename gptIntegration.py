import openai
import speech2text as s2t

openai.api_key = 'API_KEY' #replace 'API_KEY' with your own OpenAI API key

def chat():
    print("\nSay 'stop listening' to stop")
    while True:
        text = input("You: ")

        if not text:
            continue

        if text.lower() == 'stop listening':
            break

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Your name is Jarvis and you're a virtual assistant."},
                {"role": "user", "content": text},
            ]
        )

        print(response['choices'][0]['message']['content'])

