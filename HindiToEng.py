from mtranslate import translate
import speech_recognition as sr

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio,language='en-in')
        print(f"user: {query}")
        return query.lower()

    except Exception as e:
        #print("Sorry,I could not understand audio.")
        return "none"

hinglish = take_command()

eng = translate(hinglish, "en", "auto")
print(f"Translated: {eng}")