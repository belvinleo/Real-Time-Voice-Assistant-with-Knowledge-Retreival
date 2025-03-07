import requests
import speech_recognition as sr
import pyttsx3

# Initialize Text-to-Speech (TTS)
engine = pyttsx3.init()
engine.setProperty('rate', 200)
engine.setProperty('volume', 1.0)

# Define Ollama API endpoint
OLLAMA_API_URL = "http://localhost:12345/api/generate"  # Ensure Ollama is running


def speak(text):
    """Convert text to speech and speak it."""
    engine.say(text)
    engine.runAndWait()


def recognize_speech():
    """Capture speech input quickly and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)  # Short listening window
            text = recognizer.recognize_google(audio).lower()
            print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            print("Couldn't understand, please repeat.")
        except sr.RequestError:
            print("Speech Recognition service unavailable.")
        except sr.WaitTimeoutError:
            print("No speech detected.")
    return None


def chat_with_ai(user_input):
    """Generate AI response using Ollama (LLaMA model)."""
    payload = {
        "model": "llama2",  # Ensure LLaMA model is installed in Ollama
        "prompt": user_input,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response_json = response.json()
        return response_json["response"].strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"


if __name__ == "__main__":
    print("📞 AI Call Assistant is active. Say 'end call' to exit.")

    while True:
        text = recognize_speech()
        if text:
            if "end call" in text:
                print("AI: Ending the call. Have a great day!")
                speak("Ending the call. Have a great day!")
                break  # Exit loop

            response = chat_with_ai(text)
            print(f"AI: {response}")
            speak(response)
