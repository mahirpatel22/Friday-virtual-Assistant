import os
import threading
import webbrowser
import eel
import pyttsx3
import requests
import speech_recognition as sr
import musicLibrary
from google import genai

# ------------------------------------------------------------------
# 1. EEL & API SETUP
# ------------------------------------------------------------------
eel.init('web')

NEWS_API_KEY = ""
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# ------------------------------------------------------------------
# 2. TTS FUNCTION
# ------------------------------------------------------------------
def speak(text):
    """Local, offline speech synthesis."""
    engine = pyttsx3.init()
    engine.setProperty("rate", 180)
    engine.say(str(text))
    engine.runAndWait()
    engine.stop()

# ------------------------------------------------------------------
# 3. FIXED REAL-TIME NEWS FETCHING
# ------------------------------------------------------------------
def fetch_latest_news():
    """Fetches real-time news headlines using NewsData API."""
    url = f"https://newsdata.io/api/1/latest?apikey={NEWS_API_KEY}&language=en"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if results:
                headlines = [article["title"] for article in results[:3]]
                return headlines
            else:
                print("News API returned 0 articles.")
                return None
        else:
            print(f"News API Error Code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"Failed to fetch news: {e}")
        return None

# ------------------------------------------------------------------
# 4. GEMINI FALLBACK
# ------------------------------------------------------------------
def aiProcess(command):
    prompt = f"You are Friday, a helpful AI assistant. Answer briefly in 1-2 sentences.\nUser: {command}\nAssistant:"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()

# ------------------------------------------------------------------
# 5. COMMAND PROCESSOR
# ------------------------------------------------------------------
def processCommand(c):
    c_clean = c.lower()

    if "open google" in c_clean:
        webbrowser.open("https://google.com")
        eel.updateUI('idle', c, "Opening Google...")()
        speak("Opening Google.")
        
    elif "open youtube" in c_clean:
        webbrowser.open("https://youtube.com")
        eel.updateUI('idle', c, "Opening YouTube...")()
        speak("Opening YouTube.")
        
    elif c_clean.startswith("play"):
        parts = c_clean.split(" ")
        if len(parts) > 1 and parts[1] in musicLibrary.music:
            song = parts[1]
            webbrowser.open(musicLibrary.music[song])
            eel.updateUI('idle', c, f"Playing {song}...")()
            speak(f"Playing {song}.")
            
    elif "news" in c_clean:
        eel.updateUI('speaking', c, "Fetching real-time news headlines...")()
        speak("Fetching latest news headlines.")
        
        headlines = fetch_latest_news()
        if headlines:
            for idx, headline in enumerate(headlines, 1):
                eel.updateUI('speaking', f"Headline {idx}", headline)()
                speak(headline)
            eel.updateUI('idle', "", "Finished reading news.")()
        else:
            eel.updateUI('idle', c, "Sorry, I couldn't fetch live news right now.")()
            speak("Sorry, I was unable to fetch the news at this moment.")
            
    else:
        output = aiProcess(c)
        eel.updateUI('speaking', c, output)()
        speak(output)
        eel.updateUI('idle', "", output)()

# ------------------------------------------------------------------
# 6. ASSISTANT LOOP
# ------------------------------------------------------------------
def assistant_loop():
    recognizer = sr.Recognizer()
    
    eel.sleep(1)
    eel.updateUI('idle', "", "Initializing Friday...")()
    speak("Initializing Friday.")

    while True:
        try:
            with sr.Microphone() as source:
                eel.updateUI('idle', "", "Listening for 'Friday'...")()
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=3)

            word = recognizer.recognize_google(audio).lower()

            if "friday" in word:
                eel.updateUI('speaking', 'Friday', 'Yes sir, how can I help you?')()
                speak("Yes sir, how can I help you?")

                eel.updateUI('listening', 'Listening for your command...', '')()

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    command_audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
                    command = recognizer.recognize_google(command_audio)

                    processCommand(command)

        except sr.UnknownValueError:
            pass
        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print(f"Error: {e}")

# ------------------------------------------------------------------
# 7. LAUNCH GUI
# ------------------------------------------------------------------
if __name__ == "__main__":
    threading.Thread(target=assistant_loop, daemon=True).start()
    eel.start('index.html', size=(600, 700))