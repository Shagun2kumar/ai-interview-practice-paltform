import speech_recognition as sr

def analyze_voice():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak your introduction...")
        audio = r.listen(source, phrase_time_limit=5)

    try:
        text = r.recognize_google(audio)

        words = len(text.split())

        # simple confidence logic
        if words > 20:
            return 80, "Fluent speaking"
        elif words > 10:
            return 65, "Average speaking"
        else:
            return 50, "Speak more clearly and confidently"

    except:
        return 50, "Could not understand voice"
