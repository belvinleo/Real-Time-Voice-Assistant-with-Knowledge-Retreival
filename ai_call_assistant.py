import speech_recognition as sr
import pyttsx3
from transformers import pipeline

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 220)  # Faster speaking speed
engine.setProperty('volume', 1.0)  # Max volume

# Load AI chatbot model
chatbot = pipeline("text2text-generation", model="facebook/blenderbot-400M-distill")


def speak(text):
    """Convert text to speech and speak it immediately."""
    engine.say(text)
    engine.runAndWait()


def recognize_speech():
    """Capture speech input quickly and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)  # Minimal noise adjustment
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)  # Short listening window
            text = recognizer.recognize_google(audio).lower()
            print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            print("Couldn't understand, please repeat.")
            return None
        except sr.RequestError:
            print("Speech Recognition service unavailable.")
            return None
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None


def chat_with_ai(user_input):
    """Generate AI response with a quick reply limit."""
    response = chatbot(user_input, max_length=30)[0]['generated_text']  # Shorter responses for speed
    return response


if __name__ == "__main__":
    print("📞 AI Customer Support Active. Start speaking!")

    while True:
        text = recognize_speech()
        if text:
            if "bye" in text:
                print("AI: Goodbye! Have a great day!")
                speak("Goodbye! Have a great day!")
                break  # Exit loop on "bye"

            response = chat_with_ai(text)
            print(f"AI: {response}")
            speak(response)