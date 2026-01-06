from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import winsearch as ws
import pandas as pd
import spacy
import text2speech as t2s
import speech2text as s2t
import string
import Email
import WeatherUpdates
import utubeVideoDownloader
import gptIntegration
import ScheduleGmeet
import pyttsx3
import searchFile
import os


ln = "en"

def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc if not token.is_stop and token.text not in string.punctuation]
    processed_text = " ".join(tokens)
    return processed_text

def predict_label(input_text, df, vectorizer):
    preprocessed_input_text = preprocess_text(input_text)
    print(preprocessed_input_text)
    input_vector = vectorizer.transform([preprocessed_input_text])
    similarities = cosine_similarity(input_vector, vectorizer.transform(df['text']))
    max_index = similarities.argmax()
    max_similarity = similarities[0, max_index]
    return df['label'][max_index], max_similarity

engine = pyttsx3.init()
nlp = spacy.load('en_core_web_sm')
df = pd.read_csv('os_dataset.csv')
df.dropna(subset=['text'], inplace=True)
df.reset_index(drop=True, inplace=True)
vectorizer = CountVectorizer().fit(df['text'])
while(True):

    input_text=s2t.voice2text(ln)
    input_text=input_text.lower()


    if "send email" in input_text:
        print("Recipient's Email:")

        t2s.text2speech(engine, "tell Recipient's Email address")
        receiver_email = s2t.voice2text(ln).lower().replace(" ", "")
        while not receiver_email:
            receiver_email = s2t.voice2text(ln).lower().replace(" ", "")
        print("Receiver:", receiver_email)
        print("Subject:")
        t2s.text2speech(engine, "Subject of the email")
        subject = s2t.voice2text(ln)
        while not subject:
            subject = s2t.voice2text(ln)
        print("Body:")
        t2s.text2speech(engine, "Body of the Email")
        body = s2t.voice2text(ln)
        while not body:
            body = s2t.voice2text(ln)
        Email.send_email(receiver_email, subject, body)

        t2s.text2speech(engine, "Email Sent successufully")


    elif "check weather" in input_text:
        print("Which city do you want to check weather for?")
        t2s.text2speech(engine, "Which city do you want to check weather for?")
        city_name = s2t.voice2text(ln)
        while not city_name:
            print("Which city do you want to check weather for?")
            t2s.text2speech(engine, "Which city do you want to check weather for?")
            city_name = s2t.voice2text(ln)
            city_name.strip()
        if city_name.lower() == 'exit':
            break
        else:
            weather=WeatherUpdates.get_weather(city_name)
            t2s.text2speech(engine, f"Todays weather in {city_name} is {weather} degree celcius")

    elif "download youtube video" in input_text:

        t2s.text2speech(engine, "Enter the URL of the video: ")
        url = input("Enter the URL of the video: ")
        username = os.environ['USERNAME']
        # save_path = r"C:\Users\{username}\Downloads"
        t2s.text2speech(engine, "Enter the path to save the video ")
        save_path=input("Enter the path")
        utubeVideoDownloader.download_video(url, save_path)
        t2s.text2speech(engine, "The video is saved to your downloads")

    elif "go to interactive mode" in input_text:
        t2s.text2speech(engine, "Interactive mode activated")
        gptIntegration.chat()

    elif "schedule meeting" in input_text:
        ScheduleGmeet.main()
        t2s.text2speech(engine, "Yes sir")

    elif "search file" in input_text:
        t2s.text2speech(engine, "What the name of the file do you want to search")
        name = s2t.voice2text(ln)
        searchFile.open_windows_search(name)

    elif "change to tamil" in input_text:
        ln="ta"
        t2s.text2speech(engine, "neengal ippoludhu tamilaum pesalam")
    elif "change to english" in input_text:
        ln="en"
        t2s.text2speech(engine, "You can speak in english")


    elif "switch to jarvis" in input_text:
        t2s.switch_voice(engine,'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')

    elif "switch to friday" in input_text:
        t2s.switch_voice(engine, 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

    elif input_text=="stop listening":
        t2s.text2speech(engine, "Sure")
        break

    else:
        predicted_label, max_similarity = predict_label(input_text, df, vectorizer)
        print("Predicted label:", predicted_label)
        print("Maximum similarity score:", max_similarity)

        if(max_similarity > 0.5):
            if "open" in predicted_label :
                app = predicted_label.replace("open ","")
                ws.os_open(app)
                t2s.text2speech(engine, "Yes sir")
            elif "close" in predicted_label:
                app = predicted_label.replace("close ","")
                ws.close_application(app)
                t2s.text2speech(engine, "Yes sir")


