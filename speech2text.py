import speech_recognition as sr
from googletrans import Translator

def translate_tamil_to_english(text):
    translator = Translator()
    translated_text = translator.translate(text, src='ta', dest='en')
    return translated_text.text

def tamil_speech_to_text():
    text=""
    while(text==""):

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak something in Tamil...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)


        try:
            print("Transcribing...")
            # Using Google Speech Recognition for Tamil
            text = recognizer.recognize_google(audio, language="ta-IN")
            print("You said:", text)
            text = translate_tamil_to_english(text)
            print(text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            text= ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            text= ""

def english_speech_to_text():
    text=""
    while text=="":
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak something ")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Transcribing...")
            # Using Google Speech Recognition for Tamil
            text = recognizer.recognize_google(audio, language="en")
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            text=""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            text=""


def voice2text(ln):
    if ln=="ta":
        text = tamil_speech_to_text()
    else:
        text = english_speech_to_text()
    return text


