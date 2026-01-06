import requests
import pyttsx3

def fetch_news(api_key, source):
    url = f"https://newsapi.org/v2/top-headlines?sources={source}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def main():
    api_key = "NEWS_API" #Replace 'NEWS_API' with your own API

    # Enter the news source you want to fetch news from
    news_source = "the-hindu"  # Example: "bbc-news", "cnn", "the-verge", etc.

    # Fetch news
    news_data = fetch_news(api_key, news_source)

    # Check if news fetching was successful
    if news_data['status'] == 'ok':
        articles = news_data['articles']
        if articles:
            speak("Here are the latest headlines.")
            for index, article in enumerate(articles, 1):
                title = article['title']
                description = article['description']
                speak(f"Headline {index}: {title}. {description}")
        else:
            speak("No news articles found.")
    else:
        speak("Sorry, I couldn't fetch the news at the moment.")

if __name__ == "__main__":
    main()
