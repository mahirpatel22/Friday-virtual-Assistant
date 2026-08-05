# ============================================================
#  FRIDAY VOICE ASSISTANT - Explained in VERY SIMPLE English
# ============================================================

# --- BRINGING IN TOOLS (LIBRARIES) ---
# Think of these like apps you install before you can use them.

import speech_recognition as sr
# This tool listens to the mic and turns speech into text.

import webbrowser
# This tool opens websites, like Google or YouTube.

import pyttsx3
# This tool makes the computer talk. It is old and sounds robotic.
# It works without internet.

import musicLibrary
# This is your own file. It has a list of song names and links.

import asyncio
# This helps run "wait for internet" tasks without freezing everything.

import edge_tts
# This is a better, newer talking tool. Sounds more human.
# It needs internet.

import pygame
# This tool is normally for games, but here we only use it
# to play sound files (like the mp3 the computer makes).

import requests
# This tool gets data from the internet, like news.

from google import genai
# This connects to Google's AI, called Gemini.

import time
# This tool lets us "wait" for a few seconds.

import os
# This tool lets us delete files from the computer.


# --- SETTING THINGS UP ---

recognizer = sr.Recognizer()
# This makes a "listener" that turns speech into text.

engine = pyttsx3.init()
# This starts the old talking tool.
# (Note: it is not really used later. It is wasted here.)

newsapi = "pub_12c9a22bbd464839907fd462cf334a01"
# This is your secret key to get news. Keep it private, like a password.


# --- OLD WAY TO TALK (not really used) ---

def speak_old(text):
    engine = pyttsx3.init()   # start the talking tool
    engine.say(str(text))     # tell it what words to say
    engine.runAndWait()       # actually say it out loud
    engine.stop()             # turn off the talking tool
# This function is never called anywhere else in the code.
# It was replaced by the new speak() function below.


VOICE = "en-US-AndrewNeural"
# This is the name of the voice we want to use.


# --- NEW WAY TO MAKE SPEECH (turns text into an audio file) ---

async def generate_speech(text):
    # "async" means: this can wait for the internet
    # without freezing the whole program.

    communicate = edge_tts.Communicate(
        text=text,        # the words to say
        voice=VOICE,       # which voice to use
        rate="-10%",       # talk a little slower
        pitch="-15Hz"       # make the voice a little deeper
    )
    await communicate.save("temp.mp3")
    # This saves the spoken words as a sound file called temp.mp3


def speak(text):
    asyncio.run(generate_speech(text))
    # This runs the function above and waits till it's done.

    pygame.mixer.init()
    # This turns on the sound player.

    pygame.mixer.music.load("temp.mp3")
    # This loads the sound file we just made.

    pygame.mixer.music.play()
    # This plays the sound out loud.

    while pygame.mixer.music.get_busy():
        # Keep asking: "Is it still playing?"
        pygame.time.Clock().tick(10)
        # If yes, wait a tiny bit and check again.
        # This keeps the program waiting until the talking is done.

    pygame.mixer.music.unload()
    # This lets go of the sound file.

    os.remove("temp.mp3")
    # This deletes the sound file. We don't need it anymore.


# --- CONNECTING TO GOOGLE'S AI (GEMINI) ---

client = genai.Client(api_key="AQ.Ab8RN6LMJVxlZBJE_nklHUPNOR0vqWcJgrvTtB53JKaHF2dpbg")
# This connects to Gemini AI using your secret key.
# Keep this key private too.


def aiProcess(command):
    # This function sends a question to Gemini AI and gets an answer.

    prompt = f"""
You are Friday, a helpful AI assistant.
Answer the user's question briefly and accurately.

User: {command}
Assistant:
"""
    # This builds the message we send to the AI.
    # It tells the AI to act like "Friday" and adds the user's question.

    response = client.models.generate_content(
        model="gemini-2.5-flash",   # which AI model to use (fast one)
        contents=prompt              # the message we made above
    )
    # This sends the question to Gemini and waits for the answer.

    return response.text
    # This gives back just the answer text.


# --- DECIDING WHAT TO DO, BASED ON WHAT USER SAID ---

def processCommand(c):
    # "c" is the text of what the user said. Example: "open google"

    if "open google" in c.lower():
        # .lower() makes text small letters, so it matches either way
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("play"):
        # Checks if the sentence starts with the word "play"

        song = c.lower().split(" ")[1]
        # Breaks the sentence into words, and takes the 2nd word as song name.
        # Example: "play shape" -> song = "shape"
        # PROBLEM: if a song has two words, this only grabs one word.

        link = musicLibrary.music[song]
        # Looks up that song name in your musicLibrary.py file to find its link.

        webbrowser.open(link)
        # Opens that link (this plays the song).

    elif "news" in c.lower():
        # NOTE: The spacing (indentation) in the ORIGINAL code has mistakes here.
        # I did not fix the logic, only added easy comments, so you can see
        # exactly what happens, mistakes and all.

        r = requests.get(
            f"https://newsdata.io/api/1/latest?apikey={newsapi}&country=in&language=en"
        )
        # This asks a news website for the newest news from India, in English.

        if r.status_code == 200:
            # 200 means "it worked, no errors"
            data = r.json()
            # Turns the answer into something Python can read.

        articles = data.get("results", [])
        # PROBLEM: this line should be INSIDE the "if" above, but it is not.
        # So if the request fails, this line will cause an error,
        # because "data" won't exist yet.
        # This line gets the list of news stories.

        if articles:
            speak("Here are the latest news headlines.")
            # Says an intro sentence out loud.

            for article in articles[:5]:
                # Goes through the first 5 news stories only.
                print(article["title"])
                # Shows the headline in the console.
                speak(article["title"])
                # Says the headline out loud.

        else:
            print("Calling Gemini...")
            output = aiProcess(c)
            # If there are no news stories, this part runs instead.
            # It asks Gemini AI to answer the question.
            print("Gemini replied:", output)
            speak(output)
            # Says the AI's answer out loud.


# --- MAIN PART: THIS RUNS WHEN YOU START THE PROGRAM ---

if __name__ == "__main__":
    # This means: "only run this part if you run this file directly."

    speak("Initializing friday....")
    # Says out loud that it is starting.

    while True:
        # This makes a loop that never stops by itself.
        # It keeps listening forever, until you stop the program yourself.

        r = sr.Recognizer()
        # Makes another "listener" tool (a copy of the one made earlier).

        print("recognizing...")

        try:
            # "try" means: try this code. If something breaks,
            # don't crash - just go to "except" below instead.

            with sr.Microphone() as source:
                # Turns on the microphone.
                print("Listening...")
                audio = r.listen(source, timeout=1, phrase_time_limit=1)
                # Listens for a short time (1 second) to catch the wake word.

            word = r.recognize_google(audio)
            # Sends that sound to Google, and gets back the text.

            if word.lower() == "friday":
                # Checks if the word said was "friday".

                speak("Yes sir, how can I help you?")
                # Talks back to say it's ready to help.

                time.sleep(0.5)
                # Waits half a second before listening again.

                with sr.Microphone() as source:
                    # Turns on the mic again to hear the real command.
                    print("friday Active...")
                    audio = r.listen(source)
                    # This time it waits as long as needed (no short timer).

                    command = r.recognize_google(audio)
                    # Turns that speech into text.

                    print("You said:", command)

                    processCommand(command)
                    # Sends the command to our function above,
                    # which decides what to do with it.

        except Exception as e:
            # If anything went wrong, this catches the error
            # so the program does not crash.
            print("Error; {0}".format(e))
            # Shows what went wrong, then the loop starts again.