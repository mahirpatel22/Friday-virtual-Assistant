# Friday Voice Assistant — LINE BY LINE Explanation (Very Easy English)

Every line of your code is explained below, one by one, in very simple words.

---

## PART 1 — Importing tools

```python
import os
```
This line brings in a tool called `os`. It lets Python talk to your computer's operating system — like finding folders, files, and paths.

```python
import threading
```
This brings in a tool that lets the program do two jobs at the same time — like listening to your voice while the window is open.

```python
import pyautogui
```
This brings in a tool that can control your mouse and keyboard automatically — like pressing keys or clicking, by itself.

```python
import pyperclip
```
This brings in a tool that can copy and paste text using the clipboard, just like when you press Ctrl+C and Ctrl+V.

```python
import webbrowser
```
This brings in a tool that can open a web browser and go to a website, automatically.

```python
import eel
```
This brings in "Eel" — a special tool that connects your Python code to a small webpage (HTML file), so Python and the webpage can talk to each other.

```python
import pyttsx3
```
This brings in a tool that makes the computer speak out loud, using offline text-to-speech (no internet needed).

```python
import requests
```
This brings in a tool that can send messages to websites over the internet and get answers back.

```python
import speech_recognition as sr
```
This brings in a tool that turns spoken voice into written text. We are giving it a short nickname, `sr`, so we don't have to type the long name every time.

```python
import subprocess
```
This brings in a tool that can open other programs on your computer, like Notepad or Word.

```python
import re
```
This brings in "regular expressions" — a tool for searching and finding patterns inside text, like "find any sentence that has the word open in it."

```python
import time
```
This brings in a tool that lets the program wait/pause for a few seconds before continuing.

```python
import ctypes
```
This brings in a tool that lets Python talk directly to very low-level Windows system functions.

```python
import shutil
```
This brings in a tool for file tasks, like checking whether a certain program exists on your computer.

```python
import unicodedata
```
This brings in a tool that cleans up strange or fancy text characters and makes them normal/standard.

```python
from urllib.parse import urlparse, parse_qs, unquote, quote_plus
```
This line brings in four small tools for working with website links (URLs):
- `urlparse` — breaks a link into pieces (like the website name).
- `parse_qs` — reads the extra information after a `?` in a link.
- `unquote` — turns encoded web text (like `%20`) back into normal text (like a space).
- `quote_plus` — turns normal text into web-safe text (the opposite of `unquote`).

```python
from google import genai
```
This brings in Google's Gemini AI tool, called `genai`. This is the "brain" that will answer questions and write text for us.

---

## PART 2 — Setting up Eel and the API keys

```python
eel.init("web")
```
This tells the program: "My website files (HTML, CSS, JavaScript) are stored inside a folder called `web`." This sets up Eel to use that folder.

```python
NEWS_API_KEY = os.environ.get("NEWS_API_KEY",)
```
This creates a variable called `NEWS_API_KEY`. It looks at your computer's saved "environment variables" (a safe hidden storage place) and grabs the value named `NEWS_API_KEY`, which is your secret password to use the news website's service.

```python
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY",)
```
Same idea as above, but this grabs your secret key for using Google's Gemini AI.

```python
if not GEMINI_API_KEY:
```
This checks: "Is the Gemini key missing or empty?" If yes, go into this block.

```python
    print("WARNING: GEMINI_API_KEY is not configured.")
```
If the key is missing, print a warning message in the console so you know the AI won't work.

```python
    client = None
```
Since there's no key, set `client` (which will represent our connection to Gemini) to `None`, meaning "nothing/empty."

```python
else:
```
If the key WAS found (not missing), do this part instead.

```python
    try:
```
Start a "try" block — this means "attempt the following code, and if something goes wrong, don't crash, just handle it calmly."

```python
        client = genai.Client(api_key=GEMINI_API_KEY)
```
Try to create a connection to Gemini AI, using your secret key, and save that connection into the variable `client`.

```python
    except Exception as e:
```
If anything went wrong while connecting (like a bad key or no internet), catch that error and call it `e`.

```python
        print("Gemini initialization error:", e)
```
Print the error message so you can see what went wrong.

```python
        client = None
```
Since the connection failed, set `client` to `None` (nothing), so the program knows there's no working AI connection.

---

## PART 3 — Making the computer speak (Text-to-Speech)

```python
tts_lock = threading.Lock()
```
This creates a "lock" — think of it like a single microphone that only one person can use at a time. This stops two parts of the program from trying to speak out loud at the exact same moment (which would sound like a mess).

```python
def speak(text):
```
This starts a new function named `speak`. A function is a mini reusable program. This one takes one piece of information called `text` (the words to say).

```python
    """Local offline speech synthesis."""
```
This is just a note/comment (called a docstring) explaining what the function does — it doesn't run any code, it's just documentation.

```python
    if not text:
```
Check: "Is `text` empty or missing?"

```python
        return
```
If `text` is empty, stop the function right here — there's nothing to say, so don't continue.

```python
    try:
```
Start trying the following code, and if it fails, don't crash.

```python
        with tts_lock:
```
"Lock" the speaker system now — this means nothing else can speak until this part finishes and releases the lock.

```python
            engine = pyttsx3.init()
```
Start up ("initialize") the text-to-speech engine and store it in a variable called `engine`.

```python
            engine.setProperty("rate",180)
```
Set the talking speed to 180 (a number representing words per minute — medium-fast speed).

```python
            engine.setProperty("volume", 1.0 )
```
Set the volume to 1.0, which means 100% — the loudest setting.

```python
            engine.say(str(text))
```
Tell the engine: "Get ready to say this text." `str(text)` makes sure it's definitely treated as normal text, even if it wasn't already.

```python
            engine.runAndWait()
```
Actually make the computer speak now, and wait here until it's completely done talking before moving on.

```python
            engine.stop()
```
Shut down the speech engine cleanly after it's finished.

```python
    except Exception as e:
```
If ANY error happened anywhere in the "try" block above (like no speakers connected), catch it here and call it `e`.

```python
        print("TTS Error:", e)
```
Print out what the error was, so you can see it in the console, instead of the whole program crashing.

---

## PART 4 — Updating the screen (UI)

```python
def update_ui(state, user_text="", response=""):
```
This starts a new function called `update_ui`. It needs one required piece of info called `state`, and two optional pieces called `user_text` and `response` (if you don't provide them, they'll just be empty text `""` by default).

```python
    try:
```
Try the following code safely.

```python
        eel.updateUI(state,user_text, response )()
```
This calls a JavaScript function named `updateUI` that exists inside your webpage (HTML file), and sends it three pieces of information: the current `state`, what the user said, and what the response is. This makes the webpage update what it shows on screen.

```python
    except Exception as e:
```
If that call fails for any reason (like the webpage isn't ready yet), catch the error.

```python
        print("UI Error:", e)
```
Print the error message instead of crashing the whole program.

---

## PART 5 — Getting the latest news

```python
def fetch_latest_news():
```
Start a new function called `fetch_latest_news`. It doesn't need any input information.

```python
    if not NEWS_API_KEY:
```
Check: "Do we have a news API key saved?" If not...

```python
        print("NEWS_API_KEY is not configured.")
```
Print a message saying the key is missing.

```python
        return None
```
Stop the function here and give back `None` (nothing), since we can't fetch news without a key.

```python
    url = ("https://newsdata.io/api/1/latest"f"?apikey={NEWS_API_KEY}" "&language=en" )
```
Build the full web address (URL) we need to ask for news. It combines three text pieces: the base website address, then adds `?apikey=` followed by your actual key, then adds `&language=en` to ask for English news only.

```python
    try:
```
Try the following code safely.

```python
        response = requests.get( url, timeout=8 )
```
Send a request to that web address to get data, and give up automatically if it takes longer than 8 seconds. Save the answer into `response`.

```python
        if response.status_code != 200:
```
Check the "status code" the website sent back. `200` means "everything worked fine." This line checks: "Is it NOT 200?" (meaning something went wrong).

```python
            print( "News API Error:",response.status_code)
```
If something went wrong, print the error status code number.

```python
            print(response.text)
```
Also print the full raw error message text from the website, to help figure out what happened.

```python
            return None
```
Stop the function here and return nothing, since we couldn't get valid news data.

```python
        data = response.json()
```
If everything WAS fine, take the website's raw answer and convert it from text into a Python dictionary (an easy-to-use data structure), and save it as `data`.

```python
        results = data.get("results",[])
```
Try to grab the list of news articles from inside `data`, using the key `"results"`. If it's not there, use an empty list `[]` instead (so the program doesn't crash).

```python
        if not results:
```
Check: "Is the `results` list empty?"

```python
            print("News API returned 0 articles.")
```
If it's empty, print a message saying no articles were found.

```python
            return None
```
Stop the function and return nothing.

```python
        headlines = []
```
Create a new empty list called `headlines`, which we will fill with news titles.

```python
        for article in results[:5]:
```
Start a loop that goes through the first 5 articles only (`[:5]` means "take the first 5 items from the list").

```python
            title = article.get("title")
```
For each article, try to grab its `"title"` value (the headline text) and save it as `title`.

```python
            if title:
```
Check: "Does this article actually have a title (not empty)?"

```python
                headlines.append(title)
```
If yes, add that title to our `headlines` list.

```python
        return headlines
```
After the loop finishes, give back the full list of headlines we collected.

```python
    except Exception as e:
```
If anything went wrong anywhere in the whole "try" block (like no internet connection), catch the error here.

```python
        print("Failed to fetch news:", e)
```
Print what the error was.

```python
        return None
```
Return nothing, since fetching the news failed.

---

## PART 6 — Talking to Gemini AI for normal chat

```python
def aiProcess(command):
```
Start a new function called `aiProcess`. It takes one input called `command` — whatever the user said.

```python
    if not command:
```
Check: "Is `command` empty?"

```python
        return None
```
If yes, stop here and return nothing — there's nothing to process.

```python
    if client is None:
```
Check: "Is our Gemini AI connection missing (was it never set up)?"

```python
        print("Gemini client is not available.")
```
If it's missing, print a warning message.

```python
        return None
```
Stop the function and return nothing, since we have no AI to ask.

```python
    prompt = f"""
You are Friday, a helpful personal AI assistant.

Answer the user's request clearly and naturally.

Keep normal conversational answers concise.

User:
{command}

Assistant:
"""
```
This builds a big block of instruction text called `prompt`. The `f"""..."""` means it's a "formatted multi-line string" — the `{command}` part gets automatically replaced with whatever the user actually said. This whole block is like writing a note that tells the AI: "You are Friday, be helpful, answer clearly, keep it short, here's what the user said, now respond."

```python
    try:
```
Try the following code safely.

```python
        response = client.models.generate_content(model="gemini-3.5-flash",contents=prompt)
```
Send that `prompt` (instructions) to the Gemini AI model named `"gemini-3.5-flash"`, and wait for its answer. Save the answer as `response`.

```python
        if response is None:
```
Check: "Did we get absolutely nothing back?"

```python
            return None
```
If nothing came back, stop and return nothing.

```python
        if not response.text:
```
Check: "Does the response have any actual text inside it?"

```python
            return None
```
If there's no text, stop and return nothing.

```python
        return response.text.strip()
```
If we got valid text, remove any extra blank spaces from the start and end of it (`.strip()`), and give that cleaned-up text back as the final answer.

```python
    except Exception as e:
```
If anything went wrong while talking to the AI (like no internet), catch the error.

```python
        print("Gemini Error:", e)
```
Print what the error was.

```python
        return None
```
Return nothing, since the AI request failed.

---

## PART 7 — Asking Gemini to write full documents (emails, letters, reports)

```python
def generate_document(command):
```
Start a new function called `generate_document`. It takes one input, `command` — what the user asked to be written.

```python
    """
    Generates a complete document/email/report/message
    based on the user's voice command.
    """
```
This is just a comment/note explaining what the function does — it doesn't run any code.

```python
    if not command:
```
Check: "Is `command` empty?"

```python
        return None
```
If yes, stop and return nothing.

```python
    if client is None:
```
Check: "Is the Gemini AI connection missing?"

```python
        print("Gemini client is not available.")
```
If missing, print a warning.

```python
        return None
```
Stop and return nothing.

```python
    prompt = f"""
You are Friday, a professional AI writing assistant.

The user wants you to create a complete document.

User request:
{command}
IMPORTANT RULES:
1. Actually generate the requested content.
2. Do not explain what you would write.
3. Do not say that you cannot write it.
4. If the user asks for an email, generate a complete professional email.
5. If the user asks for a letter, generate a complete letter.
6. If the user asks for a report, generate the complete report.
7. If the user asks for an application, generate the complete application.
8. If the user asks for a message, generate the complete message.
9. If the user gives a reason such as submitting a report late, include that reason naturally.
10. Use professional formatting with clear paragraphs.
11. Do not use HTML.
12. Do not use markdown code blocks.
13. Do not add explanations before or after the requested document.
Generate ONLY the final document that should be written into Word or Notepad.
"""
```
This builds another big instruction block for the AI, but this time it's stricter. It tells the AI: "You are a professional writer. Actually write the full document (email/letter/report/etc.), don't just describe it, don't refuse, don't use HTML or markdown symbols, don't add extra explanations — just give the final clean document text."

```python
    try:
```
Try the following code safely.

```python
        response = client.models.generate_content(model="gemini-3.5-flash",contents=prompt)
```
Send this prompt to the Gemini AI model and wait for its written document. Save it as `response`.

```python
        if response is None:
```
Check: "Did we get nothing back at all?"

```python
            return None
```
If so, stop and return nothing.

```python
        if not response.text:
```
Check: "Is there no actual text in the response?"

```python
            return None
```
If so, stop and return nothing.

```python
        return response.text.strip()
```
Otherwise, clean up extra blank space at the edges and return the final document text.

```python
    except Exception as e:
```
If anything failed while asking the AI, catch the error.

```python
        print("Document Generation Error:", e)
```
Print what the error was.

```python
        return None
```
Return nothing since the request failed.

---

## PART 8 — Cleaning up AI text (removing Markdown symbols)

```python
def clean_document_text(text):
```
Start a new function called `clean_document_text`. It takes one input, `text` — the raw AI-generated text.

```python
    if not text:
```
Check: "Is `text` empty?"

```python
        return ""
```
If yes, return an empty piece of text (nothing to clean).

```python
    text = re.sub(  r"```.*?```", "", text,flags=re.DOTALL)
```
This uses `re.sub` (find and replace using a pattern). It looks for anything between triple backticks (```` ``` ````) — which is how AI marks "code blocks" — and DELETES it completely, replacing it with nothing (`""`). `flags=re.DOTALL` means "let the pattern match across multiple lines, not just one line."

```python
    text = re.sub(r"\*\*(.*?)\*\*",r"\1",text, flags=re.DOTALL )
```
This finds any text wrapped in double stars, like `**bold text**`, and replaces it with JUST the text inside (removing the stars but keeping the words). `\1` means "whatever was captured inside the parentheses in the pattern."

```python
    text = re.sub( r"__(.*?)__",r"\1",text, flags=re.DOTALL)
```
Same idea, but for text wrapped in double underscores, like `__bold text__` — remove the underscores, keep the words inside.

```python
    text = re.sub(r"(?<!\*)\*(.*?)\*(?!\*)",r"\1",text,flags=re.DOTALL)
```
This finds text wrapped in SINGLE stars, like `*italic text*`, and removes the stars while keeping the words. The `(?<!\*)` and `(?!\*)` parts make sure it doesn't accidentally match parts of a double-star (`**`) pattern — it only matches truly single stars.

```python
    return text.strip()
```
Finally, remove any leftover blank space from the very start and end of the text, and return the cleaned-up result.

---

## PART 9 — Figuring out exactly what to write

```python
def extract_document_request(command,application):
```
Start a new function called `extract_document_request`. It takes two inputs: `command` (what the user said) and `application` (either "word" or something else, like "notepad").

```python
    text = command.strip()
```
Copy the user's command into a variable called `text`, removing any extra blank space from the edges.

```python
    if application == "word":
```
Check: "Is the target application Word?"

```python
        patterns = [
            r"open\s+microsoft\s+word",
            r"open\s+ms\s+word",
            r"open\s+word",
            r"write\s+in\s+microsoft\s+word",
            r"write\s+in\s+ms\s+word",
            r"write\s+in\s+word",
            r"write\s+this\s+in\s+word",
            r"put\s+this\s+in\s+word",
            r"create\s+in\s+word",
            r"make\s+in\s+word",
            r"save\s+in\s+word"
        ]
```
If it is Word, create a list called `patterns` — this is a list of different phrases people might say when they mean "use Word." `\s+` means "one or more spaces" in a regex pattern (this allows for slightly different spacing).

```python
    else:
```
If the application is NOT Word (so it must be Notepad), do this instead.

```python
        patterns = [
            r"open\s+notepad",
            r"write\s+in\s+notepad",
            r"write\s+this\s+in\s+notepad",
            r"put\s+this\s+in\s+notepad",
            r"create\s+in\s+notepad",
            r"make\s+in\s+notepad",
            r"save\s+in\s+notepad"
        ]
```
Create a similar list of phrases, but for Notepad instead.

```python
    for pattern in patterns:
```
Start a loop that goes through each phrase pattern in our list, one at a time.

```python
        text = re.sub(pattern,"",text,flags=re.IGNORECASE)
```
For each pattern, search inside `text` and delete it if found (replace it with nothing), ignoring uppercase/lowercase differences (`re.IGNORECASE`).

```python
    text = re.sub(r"^\s*(and|then)\s+","",text,flags=re.IGNORECASE)
```
After removing all the command phrases, this cleans up leftover connecting words like "and" or "then" that might be stuck at the very beginning of the remaining text.

```python
    return text.strip()
```
Return the final cleaned text (removing extra blank space at the edges) — this is what actually gets sent to the AI to write.

---

## PART 10 — Typing text into Notepad

```python
def write_to_notepad(text):
```
Start a new function called `write_to_notepad`. It takes one input, `text` — the content to type into Notepad.

```python
    try:
```
Try the following code safely.

```python
        print("Opening Notepad...")
```
Print a message to the console saying we're about to open Notepad.

```python
        subprocess.Popen(["notepad.exe"])
```
Actually launch the Notepad program on the computer.

```python
        time.sleep(2)
```
Wait for 2 seconds, to give Notepad enough time to fully open before we try to type into it.

```python
        plain_text = clean_document_text(text)
```
Run our cleaning function from Part 8 on the text, removing Markdown symbols, and save the clean version as `plain_text`.

```python
        pyperclip.copy(plain_text)
```
Copy that cleaned text onto the clipboard, just like pressing Ctrl+C.

```python
        time.sleep(0.3)
```
Wait a short moment (0.3 seconds) to make sure the clipboard has fully updated.

```python
        pyautogui.hotkey("ctrl", "v")
```
Simulate pressing the Ctrl and V keys together — this pastes the clipboard text into whatever window is currently active (Notepad).

```python
        time.sleep(0.5)
```
Wait half a second after pasting, just to be safe.

```python
        print( "Response successfully written to Notepad." )
```
Print a success message to the console.

```python
        return True
```
Give back `True`, meaning "yes, this worked successfully."

```python
    except Exception as e:
```
If anything went wrong anywhere above (like Notepad not being installed), catch the error.

```python
        print("Notepad Error:", e)
```
Print what the error was.

```python
        return False
```
Give back `False`, meaning "no, this did not work."

---

## PART 11 — Typing text into Microsoft Word

```python
def write_to_word(text):
```
Start a new function called `write_to_word`. It takes one input, `text` — the content to type into Word.

```python
    try:
```
Try the following code safely.

```python
        import win32com.client
```
Try to bring in a special tool called `win32com.client`, which lets Python directly control Windows programs like Word.

```python
    except ImportError:
```
If that tool isn't installed on this computer, catch that specific kind of error (`ImportError`).

```python
        print("pywin32 is not installed.")
```
Print a message saying the required library is missing.

```python
        print("Install it using: pip install pywin32")
```
Print instructions telling the user how to install it.

```python
        return False
```
Stop the function and return `False`, since we can't continue without this tool.

```python
    try:
```
Start a second "try" block for the actual Word automation steps.

```python
        print("Opening Microsoft Word...")
```
Print a message saying we're about to open Word.

```python
        word = win32com.client.Dispatch(
            "Word.Application"
        )
```
This actually opens Microsoft Word in the background, and gives us a variable called `word` that we can use to control it, like a remote control.

```python
        word.Visible = True
```
Make sure the Word window is visible on screen (not hidden in the background).

```python
        document = word.Documents.Add()
```
Create a brand new, blank document inside Word.

```python
        time.sleep(1)
```
Wait 1 second, giving Word time to finish creating the document.

```python
        plain_text = clean_document_text(text)
```
Clean the text using our function from Part 8 (removing Markdown symbols), and save it as `plain_text`.

```python
        selection = word.Selection
```
Grab Word's current "selection" (basically, where the cursor currently is / what's currently active), and save it as `selection`.

```python
        selection.Font.Name = "Calibri"
```
Set the font style to "Calibri" for anything we're about to type.

```python
        selection.Font.Size = 11
```
Set the font size to 11.

```python
        selection.Font.Bold = False
```
Make sure the text won't be bold.

```python
        selection.Font.Italic = False
```
Make sure the text won't be italic.

```python
        selection.Font.Underline = False
```
Make sure the text won't be underlined.

```python
        selection.TypeText(plain_text)
```
This actually types the cleaned text directly into the Word document, like an invisible super-fast typist.

```python
        print("Response successfully written to Microsoft Word.")
```
Print a success message.

```python
        return True
```
Return `True`, meaning "success."

```python
    except Exception as e:
```
If anything went wrong during any of the Word steps (like Word isn't installed), catch the error.

```python
        print("Word Error:", e)
```
Print what the error was.

```python
        return False
```
Return `False`, meaning "this failed."

---

## PART 12 — Finding the real Desktop folder

```python
def get_desktop_path():
```
Start a new function called `get_desktop_path`. It doesn't need any inputs.

```python
    """Return the real Windows Desktop path, including OneDrive/redirection."""
```
A comment explaining what the function does.

```python
    try:
```
Try the following code safely.

```python
        from ctypes import wintypes
```
Bring in a special part of `ctypes` called `wintypes`, which contains Windows-specific data types we'll need.

```python
        shell32 = ctypes.windll.shell32
```
Get access to a Windows system file called `shell32.dll`, which has built-in Windows functions we can call, and save it as `shell32`.

```python
        ole32 = ctypes.windll.ole32
```
Similarly, get access to another Windows system file called `ole32.dll`, and save it as `ole32`.

```python
        shell32.SHGetKnownFolderPath.argtypes = [
            ctypes.c_void_p,
            wintypes.DWORD,
            wintypes.HANDLE,
            ctypes.POINTER(ctypes.c_wchar_p)
        ]
```
This tells Python exactly what TYPES of data the Windows function `SHGetKnownFolderPath` expects to receive, so Python can talk to it correctly (this is a low-level technical setup step).

```python
        shell32.SHGetKnownFolderPath.restype = ctypes.HRESULT
```
This tells Python what TYPE of data that Windows function will give back as its answer.

```python
        # Use the GUID structure instead of relying on a hard-coded folder path.
```
A comment explaining why the next part exists — GUIDs are special unique ID codes Windows uses to identify things (like "the real Desktop folder"), which works more reliably than guessing a fixed path.

```python
        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", ctypes.c_ulong),
                ("Data2", ctypes.c_ushort),
                ("Data3", ctypes.c_ushort),
                ("Data4", ctypes.c_ubyte * 8),
            ]
```
This creates a custom data structure called `GUID`, describing the exact format Windows uses for these special ID codes (made of 4 specific data pieces).

```python
        import uuid
```
Bring in Python's built-in tool for working with unique ID codes (UUIDs).

```python
        u = uuid.UUID("B4BFCC3A-DB2C-424C-B029-7FE99A87C641")
```
Create a UUID object using this exact code — this specific code is Windows' official ID number that always means "the Desktop folder."

```python
        guid = GUID(
            u.fields[0],
            u.fields[1],
            u.fields[2],
            (ctypes.c_ubyte * 8)(*u.bytes[8:])
        )
```
Convert that UUID into our custom `GUID` structure format (from a few lines above), so Windows' function can understand and use it.

```python
        result = ctypes.c_wchar_p()
```
Create an empty placeholder variable called `result`, ready to receive text back from Windows (this is where the Desktop path will be stored once we get it).

```python
        hr = shell32.SHGetKnownFolderPath(
            ctypes.byref(guid),
            0,
            None,
            ctypes.byref(result)
        )
```
Actually call the Windows function, asking it: "Please find me the folder that matches this GUID (Desktop), and put the answer into `result`." The answer code (success or failure) is saved into `hr`.

```python
        if hr == 0 and result.value and os.path.isdir(result.value):
```
Check three things at once: Did the function succeed (`hr == 0` means success)? Did we actually get some text back (`result.value`)? And does that folder path actually exist on the computer (`os.path.isdir`)?

```python
            desktop = result.value
```
If all three checks passed, save the found path into a variable called `desktop`.

```python
            ole32.CoTaskMemFree(result)
```
Free up the memory that Windows used to give us that answer (cleaning up after ourselves, a technical requirement when using these low-level Windows functions).

```python
            return desktop
```
Give back the Desktop folder path we found — success!

```python
        if result:
```
If we get here, it means the checks above failed, but check anyway: "Did `result` at least have SOME value in it?"

```python
            ole32.CoTaskMemFree(result)
```
If so, still clean up that memory properly, even though we're not using the value.

```python
    except Exception as e:
```
If ANY error happened during this whole low-level Windows process, catch it here.

```python
        print("Known Desktop lookup error:", e)
```
Print what the error was.

```python
    # Fallbacks for older/custom Windows configurations.
```
A comment explaining that the following code is a "backup plan" in case the fancy method above didn't work.

```python
    user_home = os.path.expanduser("~")
```
Get the path to the current user's home folder (like `C:\Users\YourName`), using the shortcut symbol `~`.

```python
    candidates = [
        os.path.join(user_home, "Desktop"),
        os.path.join(user_home, "OneDrive", "Desktop"),
        os.path.join(os.environ.get("OneDrive", ""), "Desktop"),
    ]
```
Build a list of 3 "guesses" for where the Desktop folder might be: the normal `Desktop` folder, a `OneDrive\Desktop` folder, or a Desktop folder based on wherever the `OneDrive` environment variable points to.

```python
    for path in candidates:
```
Loop through each of these 3 guesses, one at a time.

```python
        if path and os.path.isdir(path):
```
Check: "Does this guess actually exist as a real folder AND is it not empty?"

```python
            return os.path.abspath(path)
```
If it exists, return the full, absolute version of that path — success (using the backup method)!

```python
    return None
```
If we tried everything and found nothing, give back `None`, meaning "couldn't find the Desktop folder."

---

## PART 13 — Cleaning file/folder names

```python
def clean_windows_name(name):
```
Start a new function called `clean_windows_name`. It takes one input, `name` — the raw folder/file name the user spoke.

```python
    """Clean a spoken Windows file/folder name without removing spaces."""
```
A comment explaining what this function does.

```python
    name = unicodedata.normalize("NFKC", name or "")
```
This "normalizes" the text — it fixes weird/fancy Unicode characters and turns them into their normal standard forms. `name or ""` means: "if `name` is empty/missing, use an empty text instead" (to avoid crashing).

```python
    name = re.sub(r'[<>:"/\\|?*]', '', name)
```
Find any of these forbidden Windows characters — `< > : " / \ | ? *` — anywhere in the name, and delete them completely.

```python
    name = re.sub(r"\s+", " ", name).strip()
```
Find any group of multiple spaces and squash them down into just one single space, then remove extra blank space from the start/end.

```python
    name = name.rstrip(" .")
```
Remove any spaces or dots specifically from the END of the name (Windows doesn't allow file names to end with a space or a dot).

```python
    # Windows reserved names.
```
A comment explaining the next part is about special "forbidden" words.

```python
    if name.upper() in {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }:
```
Check: "Is this name (converted to uppercase) exactly one of these special reserved Windows words that can't be used as file/folder names?"

```python
        name = "_" + name
```
If it IS one of those reserved words, add an underscore in front of it, to make it a valid, safe name (e.g. `CON` becomes `_CON`).

```python
    return name
```
Give back the final cleaned-up name.

---

## PART 14 — Searching the Start Menu for app shortcuts

```python
def find_start_menu_shortcut(app_name):
```
Start a new function called `find_start_menu_shortcut`. It takes one input, `app_name` — the app we're trying to find.

```python
    """Find a Start Menu shortcut for a classic desktop application."""
```
A comment explaining the purpose of this function.

```python
    app_name = re.sub(r"\s+", " ", app_name.lower()).strip()
```
Make the app name lowercase, squash multiple spaces into one, and trim extra blank space from the edges.

```python
    roots = [
        os.path.join(
            os.environ.get("APPDATA", ""),
            "Microsoft", "Windows", "Start Menu", "Programs"
        ),
        os.path.join(
            os.environ.get("PROGRAMDATA", ""),
            "Microsoft", "Windows", "Start Menu", "Programs"
        )
    ]
```
Build a list of 2 folder locations where Start Menu shortcuts are normally stored on Windows — one for the current user only, and one shared by all users on the computer.

```python
    best_match = None
```
Create a variable called `best_match`, starting empty (`None`) — we'll use this to remember a "close enough" match if we don't find a perfect one.

```python
    for root in roots:
```
Loop through each of those 2 folder locations, one at a time.

```python
        if not os.path.isdir(root):
```
Check: "Does this folder actually NOT exist?"

```python
            continue
```
If the folder doesn't exist, skip it and move to the next one in the list.

```python
        for current_root, _, files in os.walk(root):
```
Go through every single folder and sub-folder inside this location (`os.walk` explores everything, including folders inside folders), giving us the current folder path (`current_root`) and the list of files (`files`) inside it. The underscore `_` means "we don't care about this piece of information" (it would normally be the list of sub-folder names).

```python
            for filename in files:
```
Loop through every single file found in the current folder.

```python
                if not filename.lower().endswith(".lnk"):
```
Check: "Does this filename NOT end with `.lnk`?" (`.lnk` files are Windows shortcut files).

```python
                    continue
```
If it's not a `.lnk` shortcut file, skip it and check the next file.

```python
                label = os.path.splitext(filename)[0].lower()
```
Remove the `.lnk` extension from the filename (keeping just the name part), and make it lowercase. Save it as `label`.

```python
                normalized = re.sub(r"[^a-z0-9 ]+", " ", label)
```
Clean up the label by replacing anything that ISN'T a lowercase letter, number, or space, with a space instead (removing weird symbols).

```python
                normalized = re.sub(r"\s+", " ", normalized).strip()
```
Squash multiple spaces down to one, and trim the edges.

```python
                if normalized == app_name:
```
Check: "Does this shortcut's cleaned-up name exactly match the app name we're looking for?"

```python
                    return os.path.join(current_root, filename)
```
If it's an EXACT match, immediately return the full path to this shortcut file — we found it, no need to keep looking!

```python
                if app_name in normalized or normalized in app_name:
```
If it's not an exact match, check: "Is the app name we want somewhere INSIDE this shortcut's name, or vice versa?" (a partial match).

```python
                    best_match = os.path.join(current_root, filename)
```
If there's a partial match, remember this shortcut's path as our "best guess so far," but keep looking in case we find an exact match later.

```python
    return best_match
```
After checking everywhere, if we never found an exact match, return whatever partial match we remembered (or `None` if we found nothing at all).

---

## PART 15 — Launching Microsoft Store apps

```python
def launch_start_app(app_name):
```
Start a new function called `launch_start_app`. It takes one input, `app_name` — the app we want to open.

```python
    """Launch a Microsoft Store/UWP app by its StartApps registration."""
```
A comment explaining the purpose.

```python
    try:
```
Try the following code safely.

```python
        safe_name = app_name.replace("'", "''")
```
Replace any single-quote character in the app name with two single-quotes — this is needed because PowerShell uses single quotes specially, and this prevents errors/bugs from names that contain a quote.

```python
        ps_script = (
            f"Get-StartApps | Where-Object {{ $_.Name -like '*{safe_name}*' }} "
            "| Select-Object -First 1 -ExpandProperty AppID"
        )
```
Build a PowerShell script (a command written for Windows' PowerShell tool) as text. In simple words, this command means: "Get a list of all installed apps. Find the ones whose name contains our search text. Take just the first match, and give me its special AppID code."

```python
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-Command", ps_script
            ],
            capture_output=True,
            text=True,
            timeout=8
        )
```
Actually run that PowerShell command. `-NoProfile` means "don't load extra personal settings" (faster). `-ExecutionPolicy Bypass` means "allow this script to run without extra security prompts." `capture_output=True` means "save whatever this command prints, so we can read it." `text=True` means "give us the output as normal readable text." `timeout=8` means "give up if it takes longer than 8 seconds." Save everything into `result`.

```python
        app_id = result.stdout.strip().splitlines()
```
Take the output text from that command (`result.stdout`), remove extra blank space (`.strip()`), and split it into separate lines (`.splitlines()`) — because there could technically be multiple lines of output.

```python
        if not app_id:
```
Check: "Is this list of lines empty?" (meaning no app was found).

```python
            return False
```
If nothing was found, return `False`.

```python
        app_id = app_id[0].strip()
```
Take just the FIRST line from the list (the actual AppID text), and remove any extra blank space around it.

```python
        subprocess.Popen([
            "explorer.exe",
            f"shell:AppsFolder\\{app_id}"
        ])
```
Launch `explorer.exe` (Windows File Explorer) with a special address, `shell:AppsFolder\...`, followed by the app's ID — this is the correct trick Windows uses to actually open Microsoft Store apps from code.

```python
        time.sleep(1.5)
```
Wait 1.5 seconds to give the app time to start opening.

```python
        return True
```
Return `True`, meaning "success, we launched the app."

```python
    except Exception as e:
```
If anything went wrong anywhere in this process, catch the error.

```python
        print("StartApps launch error:", e)
```
Print what the error was.

```python
        return False
```
Return `False`, meaning "this failed."

---

## PART 16 — The App Aliases dictionary

```python
APP_ALIASES = {
    "powerpoint": ["powerpnt.exe"],
    "microsoft powerpoint": ["powerpnt.exe"],
    "power point": ["powerpnt.exe"],
    "ms powerpoint": ["powerpnt.exe"],
    "word": ["winword.exe"],
    "microsoft word": ["winword.exe"],
    "ms word": ["winword.exe"],
    "excel": ["excel.exe"],
    "microsoft excel": ["excel.exe"],
    "outlook": ["outlook.exe"],
    "microsoft outlook": ["outlook.exe"],

    "notepad": ["notepad.exe"],
    "notepad app": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "calc": ["calc.exe"],
    "paint": ["mspaint.exe"],
    "file explorer": ["explorer.exe"],
    "explorer": ["explorer.exe"],
    "task manager": ["taskmgr.exe"],
    "control panel": ["control.exe"],

    "chrome": ["chrome.exe"],
    "google chrome": ["chrome.exe"],
    "edge": ["msedge.exe"],
    "microsoft edge": ["msedge.exe"],
    "firefox": ["firefox.exe"],
    "vs code": ["code"],
    "visual studio code": ["code"],
    "vscode": ["code"],

    "whatsapp": [],
    "whatsapp app": [],
    "spotify": [],
    "discord": [],
    "telegram": []
}
```
This creates a big dictionary (a lookup table) called `APP_ALIASES`. Each item on the left (like `"word"`) is a spoken name someone might use, and each item on the right (like `["winword.exe"]`) is a LIST of possible real program file names that match it (as a list, in case there could be more than one option in the future). Some apps like `"whatsapp"` have an EMPTY list `[]`, because they don't have a simple `.exe` file — they're Store apps that need to be found using the Start Menu search (Part 14) or the Store-app method (Part 15) instead.

---

## PART 17 — Cleaning up spoken app requests

```python
def normalize_app_query(query):
```
Start a new function called `normalize_app_query`. It takes one input, `query` — the raw spoken app request.

```python
    query = query.lower().strip()
```
Make the whole text lowercase, and remove extra blank space from the start/end.

```python
    query = re.sub(
        r"\b(on|in)\s+(my|the)\s+laptop\b",
        "",
        query
    )
```
Search for phrases like "on my laptop" or "in the laptop" and delete them. `\b` means "word boundary" (makes sure we match whole words, not parts of other words).

```python
    query = re.sub(r"\bapp(lication)?\b", "", query)
```
Search for the word "app" or "application" as a whole word, and delete it. The `(lication)?` part means "the letters 'lication' are optional" — so this matches both "app" and "application."

```python
    query = re.sub(r"\bplease\b", "", query)
```
Search for the word "please" as a whole word, and delete it.

```python
    query = re.sub(r"\s+", " ", query).strip()
```
Squash multiple spaces down to one single space, then trim extra blank space from the edges.

```python
    return query
```
Return the final cleaned-up app name.

---

## PART 18 — Launching an application

```python
def launch_application(app_query):
```
Start a new function called `launch_application`. It takes one input, `app_query` — the raw app request from the user.

```python
    """Launch a Windows application from an alias, PATH, Start Menu, or StartApps."""
```
A comment explaining the purpose.

```python
    app_name = normalize_app_query(app_query)
```
Clean up the raw request using our function from Part 17, and save the clean name as `app_name`.

```python
    if not app_name:
```
Check: "Is the cleaned-up name empty?" (meaning there's nothing useful left to search for).

```python
        return False
```
If empty, return `False` — nothing to launch.

```python
    print("Application requested:", app_name)
```
Print a message showing what app name we're trying to open.

```python
    # Windows Settings is a URI, not a normal EXE.
```
A comment explaining that Windows Settings works differently from normal programs.

```python
    if app_name in {"settings", "windows settings", "system settings"}:
```
Check: "Did the user ask for Settings (in any of these spoken forms)?"

```python
        try:
```
Try the following code safely.

```python
            os.startfile("ms-settings:")
```
Open Windows Settings using its special internal address, `ms-settings:`.

```python
            return True
```
Return `True`, meaning it opened successfully.

```python
        except Exception as e:
```
If that failed for any reason, catch the error.

```python
            print("Settings launch error:", e)
```
Print what went wrong.

```python
    # Exact known aliases first.
```
A comment saying we'll first check our known dictionary of apps.

```python
    candidates = APP_ALIASES.get(app_name)
```
Look up `app_name` in our `APP_ALIASES` dictionary from Part 16. If it's found, save the list of possible `.exe` files as `candidates`. If not found, `candidates` will be `None`.

```python
    if candidates is not None:
```
Check: "Did we actually find this app in our dictionary?"

```python
        for target in candidates:
```
If found, loop through each possible `.exe` file option in the list.

```python
            try:
```
Try to launch this option safely.

```python
                if os.path.isabs(target) and not os.path.exists(target):
```
Check: "Is this a full/absolute file path, AND does that file NOT actually exist?"

```python
                    continue
```
If it's supposed to exist but doesn't, skip this option and try the next one.

```python
                if target == "code":
```
Check: "Is this specific target the text 'code'?" (used for VS Code, which is special).

```python
                    if shutil.which("code"):
```
Check: "Can we find the 'code' command somewhere in the system's PATH (the list of places Windows searches for programs)?"

```python
                        subprocess.Popen(["code"])
```
If yes, launch VS Code using that command.

```python
                        return True
```
Return `True` — success!

```python
                    # Fall through to Start Menu if 'code' is not in PATH.
```
A comment explaining that if 'code' wasn't found in PATH, we'll continue trying other methods below.

```python
                    continue
```
Skip the rest of this loop iteration and try the next candidate (if any), or move on afterward.

```python
                subprocess.Popen([target])
```
For any normal `.exe` name, just try to launch it directly.

```python
                return True
```
Return `True` — success!

```python
            except Exception as e:
```
If launching this specific option failed, catch the error.

```python
                print(f"Alias launch failed for {target}:", e)
```
Print which specific target failed and why.

```python
    # Search Start Menu shortcuts, which supports many installed apps.
```
A comment explaining the next step, in case the dictionary method didn't work.

```python
    shortcut = find_start_menu_shortcut(app_name)
```
Try to find a matching Start Menu shortcut, using our function from Part 14, and save the result as `shortcut`.

```python
    if shortcut:
```
Check: "Did we actually find a shortcut?"

```python
        try:
```
Try the following code safely.

```python
            os.startfile(shortcut)
```
Open that shortcut file, just like double-clicking it.

```python
            return True
```
Return `True` — success!

```python
        except Exception as e:
```
If that failed, catch the error.

```python
            print("Shortcut launch error:", e)
```
Print what went wrong.

```python
    # Search Microsoft Store/packaged apps (excellent for WhatsApp, etc.).
```
A comment explaining the next step.

```python
    if launch_start_app(app_name):
```
Try our Store-app launching function from Part 15. Check: "Did it succeed?"

```python
        return True
```
If yes, return `True` — success!

```python
    # Last attempt: Windows 'start' command can resolve registered executables.
```
A comment explaining this final fallback attempt.

```python
    try:
```
Try the following code safely.

```python
        subprocess.Popen(f'start "" "{app_name}"',shell=True)
```
Use Windows' own built-in `start` command as a last resort, hoping Windows itself can figure out and launch the right program based on the name. `shell=True` means "run this through the command shell" (needed for the `start` command to work this way).

```python
        time.sleep(1)
```
Wait 1 second to give it a chance to launch.

```python
        return True
```
Return `True`, assuming it worked.

```python
    except Exception as e:
```
If even this failed, catch the error.

```python
        print("Generic application launch error:", e)
```
Print what went wrong.

```python
    return False
```
If we tried EVERYTHING and nothing worked, return `False` — we could not open the app.

---

## PART 19 — Creating a folder/file on the Desktop

```python
def create_desktop_item(command):
```
Start a new function called `create_desktop_item`. It takes one input, `command` — the full sentence the user said.

```python
    """Create a folder/file on the user's real Desktop path."""
```
A comment explaining the purpose.

```python
    try:
```
Try the following code safely.

```python
        desktop = get_desktop_path()
```
Find the real Desktop folder path, using our function from Part 12, and save it as `desktop`.

```python
        if not desktop:
```
Check: "Did we fail to find the Desktop folder?"

```python
            print("Desktop folder not found.")
```
Print an error message.

```python
            speak("I could not find your Desktop folder.")
```
Say this error message out loud too.

```python
            return False
```
Stop the function and return `False`.

```python
        print("Desktop:", desktop)
```
Print the Desktop path we found, for debugging purposes.

```python
        command = command.strip()
```
Remove extra blank space from the edges of the command text.

```python
        print("Command:", command)
```
Print the command text, for debugging.

```python
        # Examples
        #   make a folder named generative AI
        #   create folder called project files on desktop
        #   make a file named notes.txt in folder named generative AI
```
These are just comments showing example sentences this code is designed to understand.

```python
        folder_match = re.search(
            r"(?:a\s+)?(?:folder|directory)\s+"
            r"(?:named|called)\s+(.+?)"
            r"(?=\s+(?:and|then)\s+(?:make|create)\s+(?:a\s+)?file\b|$)",
            command,
            re.IGNORECASE
        )
```
This uses `re.search` to look through the command text for a specific pattern: the word "folder" or "directory" (optionally preceded by "a"), followed by "named" or "called," followed by the actual name we want to capture (`(.+?)`). The `(?=...)` part is a "lookahead" — it means "stop capturing the name once you see 'and make a file' or 'then create a file' coming up, or once the text ends (`$`)." This is how the function figures out where the folder name ends. Save whatever was found into `folder_match`.

```python
        if not folder_match:
```
Check: "Did the pattern above NOT find anything?"

```python
            folder_match = re.search(
                r"(?:a\s+)?(?:folder|directory)\s+(.+?)"
                r"(?=\s+(?:and|then)\s+(?:make|create)\s+(?:a\s+)?file\b|\s+on\s+(?:the\s+)?desktop\b|$)",
                command,
                re.IGNORECASE
            )
```
If the first pattern found nothing (maybe the user didn't say "named" or "called"), try a slightly looser pattern instead — this one just looks for "folder" followed directly by the name, stopping at "and make a file," "on the desktop," or the end of the sentence.

```python
        file_match = re.search(
            r"(?:file)\s+(?:named|called)\s+(.+?)"
            r"(?=\s+(?:in|inside|within)\s+(?:the\s+)?folder\b|$)",
            command,
            re.IGNORECASE
        )
```
Similarly, search for the word "file" followed by "named" or "called," then capture the file name, stopping when it sees "in the folder" / "inside the folder" / "within the folder," or the end of the sentence.

```python
        if not file_match:
```
Check: "Did we NOT find a match with that pattern?"

```python
            file_match = re.search(
                r"(?:file)\s+([A-Za-z0-9_. -]+?)"
                r"(?=\s+(?:in|inside|within)\s+(?:the\s+)?folder\b|$)",
                command,
                re.IGNORECASE
            )
```
If not, try a looser pattern: just "file" followed by letters/numbers/dots/spaces/dashes (typical file name characters) as the file name, again stopping at the folder-reference words or the end.

```python
        folder_name = None
```
Create a variable called `folder_name`, starting as empty (`None`).

```python
        if folder_match:
```
Check: "Did we successfully find a folder name match?"

```python
            folder_name = clean_windows_name(folder_match.group(1))
```
If yes, take the captured text (`folder_match.group(1)` — the part inside the parentheses we captured), clean it up using our Part 13 function, and save it as `folder_name`.

```python
            # Remove spoken location words accidentally captured by STT.
```
A comment explaining the next line's purpose.

```python
            folder_name = re.sub(
                r"\s+(?:on|in)\s+(?:the\s+)?desktop\s*$",
                "",
                folder_name,
                flags=re.IGNORECASE
            ).strip()
```
Sometimes speech recognition accidentally includes extra words like "on the desktop" at the end of the captured name. This removes that leftover phrase from the very end, then trims extra blank space.

```python
        folder_path = desktop
```
Start by assuming the target folder path is just the Desktop itself (the default, if no specific folder name was given).

```python
        if folder_name:
```
Check: "Do we actually have a folder name?"

```python
            folder_path = os.path.join(desktop, folder_name)
```
If yes, build the full folder path by joining the Desktop path with the folder name (e.g. `Desktop\Generative AI`).

```python
            os.makedirs(folder_path, exist_ok=True)
```
Actually create that folder on the computer. `exist_ok=True` means "don't throw an error if the folder already exists — just leave it as is."

```python
            print("Folder created/verified:", folder_path)
```
Print a confirmation message.

```python
        if file_match:
```
Check: "Did we find a file name to create too?"

```python
            file_name = clean_windows_name(file_match.group(1))
```
If yes, take the captured file name text, clean it up, and save it as `file_name`.

```python
            file_name = re.sub(
                r"\s+(?:on|in)\s+(?:the\s+)?desktop\s*$",
                "",
                file_name,
                flags=re.IGNORECASE
            ).strip()
```
Remove any accidentally-captured "on the desktop" wording from the end of the file name, same idea as before.

```python
            if not file_name:
```
Check: "Is the file name empty after all this cleaning?"

```python
                raise ValueError("The file name was empty.")
```
If so, deliberately trigger an error (`raise`) saying the file name was empty — this will be caught by the `except` block further down.

```python
            file_path = os.path.join(folder_path, file_name)
```
Build the full path to the new file by joining the folder path with the file name.

```python
            with open(file_path, "a", encoding="utf-8"):
                pass
```
Open the file in "append" mode (`"a"`) using UTF-8 text encoding. Opening a file in append mode automatically CREATES it if it doesn't exist yet. The `pass` means "do nothing else" — we just wanted to create the file, not write anything into it right now. As soon as this block ends, the file is automatically closed properly (that's what the `with` statement does).

```python
            print("File created/verified:", file_path)
```
Print a confirmation message.

```python
        if not folder_name and not file_match:
```
Check: "Did we fail to find BOTH a folder name AND a file request?"

```python
            print("Could not detect folder or file.")
```
If so, print a message saying nothing could be understood.

```python
            speak("I could not understand what you want me to create.")
```
Say that message out loud too.

```python
            return False
```
Stop the function and return `False`.

```python
        spoken_target = "the folder" if folder_name and not file_match else "the file" if file_match and not folder_name else "the folder and file"
```
This is a compact way of choosing a phrase to speak, depending on what was created: if only a folder was made, say "the folder"; if only a file was made, say "the file"; if both were made, say "the folder and file."

```python
        speak(f"Done. I created {spoken_target} on your Desktop.")
```
Speak out a confirmation message using whichever phrase we just chose.

```python
        update_ui(
            "idle",
            command,
            f"Created successfully on Desktop: {folder_path}"
        )
```
Update the on-screen UI to show that the item was created, along with the path.

```python
        return True
```
Return `True` — success!

```python
    except Exception as e:
```
If ANYTHING went wrong anywhere in this whole function, catch the error here.

```python
        print()
        print("==========================================")
        print("CREATE ERROR")
        print(e)
        print("==========================================")
```
Print a clearly visible error block in the console, with separator lines, showing exactly what the error was.

```python
        speak("There was an error while creating it.")
```
Speak an apology/error message out loud.

```python
        return False
```
Return `False` — this failed.

---

## PART 20 — Handling Word voice commands

```python
def handle_word_command(command):
```
Start a new function called `handle_word_command`. It takes one input, `command` — the full user sentence.

```python
    print()
    print("WORD DOCUMENT COMMAND")
    print(command)
```
Print a blank line, a header, and the actual command text, for debugging purposes.

```python
    document_request = extract_document_request(command,"word")
```
Use our function from Part 9 to strip out the "open/write in Word" phrases, leaving just the actual content request, and save it as `document_request`.

```python
    if not document_request:
```
Check: "Is there nothing left after stripping the command words?" (meaning the user just said "open Word" with no writing request).

```python
        try:
```
Try the following code safely.

```python
            subprocess.Popen( ["winword.exe"] )
```
Just open Microsoft Word normally, with no content to write.

```python
            update_ui("idle",command,"Microsoft Word opened.")
```
Update the on-screen UI to say Word was opened.

```python
            speak( "Microsoft Word opened.")
```
Speak that same confirmation out loud.

```python
        except Exception as e:
```
If opening Word failed, catch the error.

```python
            print("Could not open Word:",e)
```
Print what went wrong.

```python
            update_ui("idle",command, "I could not open Microsoft Word.")
```
Update the UI to show an error message.

```python
            speak("I could not open Microsoft Word.")
```
Speak that error message out loud too.

```python
        return
```
Stop the function here (whether it succeeded or failed) — there's nothing else to do since there was no writing request.

```python
    update_ui("speaking",command,"Generating your Word document...")
```
If we DO have a writing request, update the UI to show "Generating your Word document..." with the state set to "speaking."

```python
    speak(  "Generating your Word document.")
```
Speak that message out loud too.

```python
    response = generate_document(
        document_request
    )
```
Ask the AI to actually write the document, using our function from Part 7, passing in the cleaned request. Save the AI's answer as `response`.

```python
    if not response:
```
Check: "Did the AI fail to generate anything?"

```python
        update_ui("idle",command, "I could not generate the document.")
```
If so, update the UI with an error message.

```python
        speak( "I could not generate the document.")
```
Speak that error message.

```python
        return
```
Stop the function here since there's nothing to write.

```python
    update_ui("speaking",command,response)
```
If we DID get a response, update the UI to show the generated document text.

```python
    print()
    print("GENERATED WORD DOCUMENT:")
    print(response)
```
Print the generated document text to the console, for debugging/logging purposes.

```python
    success = write_to_word(response)
```
Actually type this generated text into Word, using our function from Part 11. Save whether it worked (`True`/`False`) as `success`.

```python
    if success:
```
Check: "Did writing to Word succeed?"

```python
        update_ui("idle",command, response)
```
If yes, update the UI showing the final response, with state set back to "idle."

```python
        speak( "The document has been written to Microsoft Word.")
```
Speak a success confirmation.

```python
    else:
```
If writing to Word did NOT succeed, do this instead.

```python
        update_ui("idle",command,"I could not write the document to Microsoft Word." )
```
Update the UI with a failure message.

```python
        speak("I could not write the document to Microsoft Word.")
```
Speak that failure message out loud.

---

## PART 21 — Handling Notepad voice commands

```python
def handle_notepad_command(command):
```
Start a new function called `handle_notepad_command`. It takes one input, `command` — the full user sentence.

```python
    print()
    print("NOTEPAD DOCUMENT COMMAND")
    print(command)
```
Print a blank line, a header, and the command, for debugging.

```python
    document_request = extract_document_request(command,"notepad")
```
Strip out the "open/write in Notepad" phrases (using Part 9's function, but for notepad this time), leaving just the content request.

```python
    if not document_request:
```
Check: "Is there nothing left?" (the user just said "open Notepad").

```python
        try:
```
Try the following code safely.

```python
            subprocess.Popen(  ["notepad.exe"])
```
Just open Notepad normally, with nothing to write.

```python
            update_ui("idle",command, "Notepad opened." )
```
Update the UI saying Notepad was opened.

```python
            speak( "Notepad opened.")
```
Speak that message.

```python
        except Exception as e:
```
If it failed, catch the error.

```python
            print("Could not open Notepad:",e)
```
Print the error.

```python
            update_ui("idle", command,"I could not open Notepad.")
```
Update the UI with a failure message.

```python
            speak( "I could not open Notepad.")
```
Speak the failure message.

```python
        return
```
Stop the function here.

```python
    update_ui("speaking",command,"Generating your Notepad content..." )
```
If there IS a writing request, update the UI to show "Generating your Notepad content..."

```python
    speak( "Generating your Notepad content.")
```
Speak that message.

```python
    response = generate_document( document_request)
```
Ask the AI to write the content, using our Part 7 function.

```python
    if not response:
```
Check: "Did the AI fail?"

```python
        update_ui("idle",command,"I could not generate the content.")
```
If so, update the UI with an error.

```python
        speak(  "I could not generate the content." )
```
Speak that error.

```python
        return
```
Stop the function.

```python
    update_ui("speaking",command, response)
```
If we got a response, update the UI to show it.

```python
    print()
    print("GENERATED NOTEPAD CONTENT:")
    print(response)
```
Print the generated content to the console for debugging.

```python
    success = write_to_notepad(
        response
    )
```
Actually type this text into Notepad, using our Part 10 function, and save whether it worked.

```python
    if success:
```
Check: "Did it work?"

```python
        update_ui("idle",command, response )
```
If yes, update the UI to show the final response.

```python
        speak("The response has been written to Notepad.")
```
Speak a success message.

```python
    else:
```
If it did NOT work, do this instead.

```python
        update_ui( "idle", command, "I could not write the response to Notepad.")
```
Update the UI with a failure message.

```python
        speak( "I could not write the response to Notepad.")
```
Speak that failure message.

---

## PART 22 — Playing YouTube videos

```python
def get_youtube_video_url(query):
```
Start a new function called `get_youtube_video_url`. It takes one input, `query` — the song/video name to search for.

```python
    """Return the first YouTube video URL for a spoken song/video query."""
```
A comment explaining the purpose.

```python
    # Best option: yt-dlp resolves the first result directly to a watch URL.
```
A comment saying the following method is the preferred/best one.

```python
    try:
```
Try the following code safely.

```python
        import yt_dlp
```
Try to bring in a library called `yt_dlp`, which can search YouTube directly.

```python
        options = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extract_flat": True,
            "noplaylist": True,
        }
```
Create a dictionary of settings for `yt_dlp`: don't print extra logs (`quiet`), don't show warnings, don't actually download anything (`skip_download`), just get basic quick info instead of deep details (`extract_flat`), and ignore playlists — only look at single videos (`noplaylist`).

```python
        with yt_dlp.YoutubeDL(options) as ydl:
```
Create a `yt_dlp` search tool using those settings, and call it `ydl` (this also makes sure it's properly closed afterward, thanks to `with`).

```python
            result = ydl.extract_info(
                f"ytsearch1:{query}",
                download=False
            )
```
Ask `ydl` to search YouTube for our `query` text. The `ytsearch1:` prefix means "search YouTube and give me just 1 result." `download=False` means "don't actually download the video, just get information about it." Save the result.

```python
        entries = result.get("entries") or []
```
Try to grab the `"entries"` (the search results list) from `result`. If there's nothing there, use an empty list `[]` instead.

```python
        if entries:
```
Check: "Do we actually have at least one search result?"

```python
            first = entries[0]
```
Grab the first (and only) result from the list.

```python
            video_id = first.get("id")
```
Try to get that video's unique ID code.

```python
            if video_id:
```
Check: "Did we get a valid video ID?"

```python
                return f"https://www.youtube.com/watch?v={video_id}"
```
If yes, build and return a full YouTube watch link using that video ID.

```python
            webpage_url = first.get("webpage_url")
```
If there was no video ID for some reason, try to get the full webpage URL directly instead.

```python
            if webpage_url:
```
Check: "Did we get a webpage URL?"

```python
                return webpage_url
```
If yes, return that URL directly.

```python
    except ImportError:
```
If the `yt_dlp` library isn't installed at all, catch that specific error.

```python
        print("yt-dlp is not installed. Trying YouTube HTML lookup.")
```
Print a message saying we'll try a backup method instead.

```python
    except Exception as e:
```
If any OTHER kind of error happened while using `yt_dlp`, catch it here.

```python
        print("YouTube direct search error:", e)
```
Print what went wrong.

```python
    # Lightweight fallback: YouTube's search HTML normally contains video IDs
    # even when yt-dlp is unavailable.
```
A comment explaining that the next part is our backup plan, in case `yt_dlp` didn't work.

```python
    try:
```
Try the following code safely.

```python
        search_url = (
            "https://www.youtube.com/results?search_query="
            + requests.utils.quote(query)
        )
```
Build a YouTube search webpage URL manually, using our search query, safely encoded for use in a web address (`requests.utils.quote` makes sure special characters like spaces are properly converted).

```python
        response = requests.get(
            search_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/151.0.0.0 Safari/537.36"
                )
            },
            timeout=8
        )
```
Send a request to that search page's web address, pretending to be a normal Chrome web browser (using the `User-Agent` header) so YouTube doesn't block the request as being from a robot/script. Give up after 8 seconds if there's no response.

```python
        if response.ok:
```
Check: "Did the request succeed?" (`.ok` is `True` if the status code was in the "success" range).

```python
            video_ids = re.findall(
                r'"videoId":"([A-Za-z0-9_-]{11})"',
                response.text
            )
```
Search through the raw webpage text for the pattern `"videoId":"..."`, which is how YouTube embeds video IDs in its page data, and collect ALL matches found into a list called `video_ids`. `{11}` means "exactly 11 characters," since YouTube video IDs are always 11 characters long.

```python
            seen = set()
```
Create an empty "set" (a collection with no duplicates) called `seen`, to keep track of video IDs we've already looked at.

```python
            for video_id in video_ids:
```
Loop through each video ID found.

```python
                if video_id in seen:
```
Check: "Have we already seen/processed this exact video ID before?" (YouTube's page often repeats the same ID multiple times).

```python
                    continue
```
If we've already seen it, skip it and check the next one.

```python
                seen.add(video_id)
```
Otherwise, remember that we've now seen this video ID.

```python
                return f"https://www.youtube.com/watch?v={video_id}&autoplay=1"
```
Build and immediately return a YouTube link using this video ID, with `&autoplay=1` added so the video starts playing automatically when opened.

```python
    except Exception as e:
```
If anything went wrong with this backup method too, catch the error.

```python
        print("YouTube HTML lookup error:", e)
```
Print what went wrong.

```python
    return None
```
If BOTH methods failed completely, return `None` — we couldn't find any video.

```python
def play_youtube(command):
```
Start a new function called `play_youtube`. It takes one input, `command` — the full user sentence (like "play shape of you").

```python
    parts = command.split(" ", 1)
```
Split the command into 2 pieces, at the FIRST space only. So `"play shape of you"` becomes `["play", "shape of you"]`.

```python
    if len(parts) < 2:
```
Check: "Do we have fewer than 2 pieces?" (meaning the user only said "play" with nothing after it).

```python
        speak("Please tell me what you want to play.")
```
If so, ask the user to say what to play.

```python
        return False
```
Stop the function and return `False`.

```python
    song = parts[1].strip()
```
Otherwise, take the second piece (everything after "play "), and remove extra blank space — this is our song/video name.

```python
    if not song:
```
Check: "Is the song name empty after cleaning?" (in case the user just said "play    " with only spaces).

```python
        speak("Please tell me what you want to play.")
```
If so, ask them to specify what to play.

```python
        return False
```
Return `False` and stop.

```python
    print("Playing:", song)
```
Print the song name we're about to play, for debugging.

```python
    update_ui(
        "speaking",
        command,
        f"Finding {song} on YouTube..."
    )
```
Update the UI to show "Finding [song] on YouTube..."

```python
    # Open the actual first video instead of only opening search results.
```
A comment explaining why we try to get a direct video first.

```python
    video_url = get_youtube_video_url(song)
```
Try to find the direct video link using our function above.

```python
    if video_url:
```
Check: "Did we successfully get a video link?"

```python
        print("Opening YouTube video:", video_url)
```
Print the link, for debugging.

```python
        webbrowser.open(video_url, new=2)
```
Open that video link in a new browser tab (`new=2` means "open in a new tab if possible").

```python
        time.sleep(5)
```
Wait 5 seconds to give the video time to start loading and playing.

```python
        # The direct watch URL uses autoplay=1. Avoid blindly pressing Space:
        # Space toggles play/pause and would pause a video that already started.
```
A comment explaining why the code deliberately does NOT try to press Space to start the video — since the link already has autoplay, pressing Space could accidentally pause it instead.

```python
        speak(f"Playing {song} on YouTube.")
```
Speak a confirmation message saying the song is now playing.

```python
        update_ui(
            "idle",
            command,
            f"Playing {song} on YouTube."
        )
```
Update the UI with that same confirmation.

```python
        return True
```
Return `True` — success!

```python
    # Fallback when yt-dlp is unavailable or YouTube blocks extraction.
```
A comment explaining the next part is a backup plan, used if we couldn't get a direct video link.

```python
    search_url = (
        "https://www.youtube.com/results?search_query="
        + requests.utils.quote(song)
    )
```
Build a plain YouTube search page URL, encoding the song name safely for use in a web address.

```python
    webbrowser.open(search_url, new=2)
```
Open that search page in a new browser tab.

```python
    time.sleep(4)
```
Wait 4 seconds for the search page to load.

```python
    # Move to the first search result and open it with keyboard navigation.
```
A comment explaining the next part's purpose.

```python
    try:
```
Try the following code safely.

```python
        pyautogui.press("tab", presses=7, interval=0.15)
```
Simulate pressing the Tab key 7 times in a row, with a 0.15 second pause between each press — this moves the browser's focus through the page elements, roughly landing on the first video result (this is a rough trick, since exact tab counts can vary).

```python
        pyautogui.press("enter")
```
Simulate pressing the Enter key, which "clicks" whatever is currently focused/selected — hopefully the first video.

```python
    except Exception as e:
```
If this keyboard trick failed for any reason, catch the error.

```python
        print("YouTube result navigation fallback error:", e)
```
Print what went wrong.

```python
    speak(f"I opened the YouTube result for {song}.")
```
Speak a message saying we opened the search results (not a specific confirmed video, since we're not 100% sure it worked).

```python
    update_ui(
        "idle",
        command,
        f"YouTube search opened for {song}."
    )
```
Update the UI with that same message.

```python
    return True
```
Return `True` — we did something, even if we're not 100% sure it clicked the right video.

---

## PART 23 — Opening any website

```python
def clean_website_command(text):
```
Start a new function called `clean_website_command`. It takes one input, `text` — the raw spoken website request.

```python
    """Convert spoken website commands into a clean search/site name."""
```
A comment explaining the purpose.

```python
    text = text.strip()
```
Remove extra blank space from the edges of the text.

```python
    # Remove common command prefixes.
```
A comment explaining the next step.

```python
    text = re.sub(
        r"^(?:please\s+)?(?:open|go\s+to|visit|browse)\s+",
        "",
        text,
        flags=re.IGNORECASE
    )
```
At the very START of the text (`^`), look for an optional "please," followed by "open," "go to," "visit," or "browse," and delete that whole beginning phrase.

```python
    # Remove natural-language suffixes.
```
A comment explaining the next step.

```python
    text = re.sub(
        r"\s+(?:website|web\s*site|site)\s*$",
        "",
        text,
        flags=re.IGNORECASE
    )
```
At the very END of the text (`$`), look for the word "website," "web site," or "site," and delete it.

```python
    return text.strip()
```
Return the final cleaned text, with any remaining extra blank space trimmed off — this should now be just the site name (like "amazon").

```python
def is_explicit_website_request(text):
```
Start a new function called `is_explicit_website_request`. It takes one input, `text` — the full user sentence.

```python
    """Return True when the user clearly asked for a website."""
```
A comment explaining the purpose.

```python
    lowered = text.lower().strip()
```
Make the text lowercase and trim extra blank space, saving it as `lowered`.

```python
    return bool(
        re.match(
            r"^(?:please\s+)?(?:open|go\s+to|visit|browse)\s+.+?\s+(?:website|web\s*site|site)\s*$",
            lowered
        )
```
Check the FIRST pattern: does the whole sentence match "open/go to/visit/browse [something] website/site" from start to end?

```python
        or
        re.match(
            r"^(?:please\s+)?(?:open|go\s+to|visit|browse)\s+https?://",
            lowered
        )
```
OR does it match "open/go to/visit/browse http://..." at the start?

```python
        or
        re.match(
            r"^(?:please\s+)?(?:open|go\s+to|visit|browse)\s+www\.",
            lowered
        )
    )
```
OR does it match "open/go to/visit/browse www...." at the start? `bool(...)` converts whatever `re.match` gives back (which could be a match object or `None`) into a clean `True` or `False` value.

```python
def looks_like_web_address(value):
```
Start a new function called `looks_like_web_address`. It takes one input, `value` — some text to check.

```python
    value = value.strip().lower()
```
Trim extra blank space and make it lowercase.

```python
    return (
        value.startswith("http://")
        or value.startswith("https://")
        or value.startswith("www.")
        or bool(re.match(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$", value))
    )
```
Return `True` if the text starts with `http://`, `https://`, `www.`, OR if it matches a simple pattern that looks like a domain name (letters/numbers/dashes, followed by a dot, repeated — like `google.com` or `my-site.co.in`). Otherwise return `False`.

```python
def extract_url_from_search_html(html):
```
Start a new function called `extract_url_from_search_html`. It takes one input, `html` — raw webpage text from a search engine.

```python
    """
    Extract the first external result from DuckDuckGo HTML.
    This avoids hard-coding website names.
    """
```
A comment explaining the purpose.

```python
    if not html:
```
Check: "Is `html` empty?"

```python
        return None
```
If so, return nothing — there's nothing to search through.

```python
    # DuckDuckGo redirect format:
    # //duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.com
```
A comment explaining a special format DuckDuckGo uses for its links (an encoded redirect address).

```python
    patterns = [
        r'href=["\'](?:https?:)?//duckduckgo\.com/l/\?uddg=([^&"\']+)',
        r'href=["\'](https?://[^"\']+)["\']'
    ]
```
Create a list of 2 regex patterns to try: the first one specifically matches DuckDuckGo's special redirect links, and the second one matches any normal `href="https://..."` link.

```python
    for pattern in patterns:
```
Loop through each of these 2 patterns.

```python
        for match in re.finditer(pattern, html, flags=re.IGNORECASE):
```
For each pattern, search through the ENTIRE `html` text and find ALL matches (`re.finditer` gives back every match found, one at a time, rather than just the first).

```python
            raw_url = match.group(1)
```
For each match found, grab the captured URL part (inside the parentheses of the pattern).

```python
            if pattern.startswith(r'href=["\'](?:https'):
```
Check: "Is this the FIRST pattern (the DuckDuckGo redirect one)?" — checking by comparing the start of the pattern text itself.

```python
                raw_url = unquote(raw_url)
```
If it's the DuckDuckGo redirect format, the URL inside it is web-encoded (special characters replaced with codes like `%3A`), so decode it back into a normal readable URL.

```python
            else:
```
If it's the second, simpler pattern instead, do this.

```python
                raw_url = raw_url.replace("&amp;", "&")
```
Just clean up one common HTML encoding issue: replace `&amp;` (HTML's way of writing "&") back into a normal `&` symbol.

```python
            try:
```
Try the following code safely.

```python
                parsed = urlparse(raw_url)
```
Break the URL apart into its pieces (like protocol, domain name, path) using `urlparse`, and save it as `parsed`.

```python
                if parsed.scheme in {"http", "https"} and parsed.netloc:
```
Check: "Does this URL use http or https AND does it actually have a domain name (`netloc`)?" — making sure it's a real, valid web link.

```python
                    # Skip search/social infrastructure pages.
```
A comment explaining the next part.

```python
                    blocked_hosts = {
                        "duckduckgo.com",
                        "www.duckduckgo.com",
                        "google.com",
                        "www.google.com",
                        "bing.com",
                        "www.bing.com"
                    }
```
Create a set of website domains we want to IGNORE, since these are search engines themselves, not the actual result we want.

```python
                    if parsed.netloc.lower() not in blocked_hosts:
```
Check: "Is this URL's domain name NOT one of those blocked/ignored ones?"

```python
                        return raw_url
```
If it's a genuine, non-blocked website, return this URL immediately — we found our answer!

```python
            except Exception:
```
If parsing this particular URL caused any error, catch it silently.

```python
                continue
```
Skip this one and keep checking the next match in the loop.

```python
    return None
```
If we went through everything and found no valid external link, return `None`.

```python
def resolve_website_url(site_name):
```
Start a new function called `resolve_website_url`. It takes one input, `site_name` — the raw spoken site name.

```python
    """
    Resolve a spoken website name to an actual URL.

    Examples:
        amazon -> https://amazon.com
        github -> https://github.com
        openai -> https://openai.com

    For unknown domains, it first performs an Internet search and opens
    the first relevant external result. This keeps website handling generic.
    """
```
A comment block explaining exactly what this function does, with examples.

```python
    site_name = clean_website_command(site_name)
```
Clean up the site name using our earlier function, removing "open," "website," etc.

```python
    if not site_name:
```
Check: "Is the cleaned name empty?"

```python
        return None
```
If so, return nothing — there's nothing to resolve.

```python
    #Direct URL
```
A comment marking the start of a section that handles when the user already gave a full URL.

```python
    if site_name.startswith(("http://", "https://")):
```
Wait — actually let's check the real code again for accuracy: the actual line is `if looks_like_web_address(site_name):`
```python
    if looks_like_web_address(site_name):
```
Check: "Does this already look like a proper web address?" (using our function from earlier).

```python
        if site_name.startswith(("http://", "https://")):
```
If it does look like a web address, check further: "Does it already start with http:// or https://?"

```python
            return site_name
```
If yes, it's already a complete, usable link — just return it exactly as is.

```python
        if site_name.startswith("www."):
```
Otherwise, check: "Does it start with www.?"

```python
            return "https://" + site_name
```
If yes, just add `https://` in front of it and return that.

```python
        return "https://" + site_name
```
If it matched neither of those exact cases (meaning it's something like `google.com` without www or http), just add `https://` in front anyway and return it.

```python
    # Try common TLDs first.
```
A comment explaining the next section — trying common domain endings like `.com`.

```python
    normalized = re.sub(
        r"\s+",
        "",
        site_name.lower()
    )
```
Make the site name lowercase and remove ALL spaces completely (not just extra ones — every single space), saving it as `normalized`.

```python
    # Only use direct-domain guesses for a single simple site name.
```
A comment explaining a safety check coming up.

```python
    if re.match(r"^[a-z0-9-]+$", normalized):
```
Check: "Is `normalized` made up ONLY of lowercase letters, numbers, and dashes, with nothing else?" This makes sure we only try the domain-guessing trick for simple single-word names (not full sentences).

```python
        candidates = [
            f"https://www.{normalized}.com",
            f"https://{normalized}.com",
            f"https://www.{normalized}.in",
            f"https://{normalized}.in",
            f"https://www.{normalized}.org",
            f"https://{normalized}.org",
            f"https://www.{normalized}.net",
            f"https://{normalized}.net"
        ]
```
Build a list of 8 different guesses, trying the name with `www.` or without, combined with `.com`, `.in`, `.org`, and `.net` endings — these are the most common website types.

```python
        for candidate in candidates:
```
Loop through each of these 8 guesses, one at a time.

```python
            try:
```
Try to check this specific guess safely.

```python
                response = requests.head(
                    candidate,
                    allow_redirects=True,
                    timeout=4,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    }
                )
```
Send a quick "HEAD" request (which just checks if a page exists, without downloading its full content — faster than a normal request) to this guessed URL. `allow_redirects=True` means "if this address redirects somewhere else, follow it." `timeout=4` means "give up after 4 seconds." Pretend to be a normal browser using the `User-Agent` header.

```python
                if response.status_code < 500:
```
Check: "Is the status code LESS than 500?" (Status codes 500+ usually mean serious server errors; anything below that, even 404 "not found," at least means the server responded normally, so we'll consider it valid enough).

```python
                    final_url = response.url
```
Grab the FINAL URL after any redirects happened (in case the site redirected us somewhere slightly different).

```python
                    if (
                        final_url.startswith("http://")
                        or
                        final_url.startswith("https://")
                    ):
```
Double check: "Does this final URL properly start with http:// or https://?"

```python
                        return final_url
```
If everything checks out, return this working URL — we found it!

```python
            except requests.RequestException:
```
If sending this request failed for any internet-related reason (site doesn't exist, timeout, etc.), catch that specific type of error.

```python
                continue
```
Skip this guess and try the next one in the list.

```python
    # Universal search fallback.
```
A comment explaining that if none of our guesses worked, we'll do an actual internet search instead.

```python
    try:
```
Try the following code safely.

```python
        search_url = "https://html.duckduckgo.com/html/"
```
Set the address for DuckDuckGo's simple HTML-only search page (easier to read through with code than the fancy JavaScript version).

```python
        response = requests.get(
            search_url,
            params={
                "q": f"{site_name} official website"
            },
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=8
        )
```
Send a search request to DuckDuckGo, searching for `"[site name] official website"`. `params` automatically builds the correct search query part of the URL for us. Pretend to be a normal browser, and give up after 8 seconds.

```python
        if response.ok:
```
Check: "Did the search request succeed?"

```python
            found_url = extract_url_from_search_html(
                response.text
            )
```
If it succeeded, search through the raw search results webpage text using our earlier function, trying to find the first real external link.

```python
            if found_url:
```
Check: "Did we actually find a URL?"

```python
                return found_url
```
If yes, return it — success!

```python
    except requests.RequestException as e:
```
If sending the search request itself failed (no internet, etc.), catch that error.

```python
        print("Website resolution request error:", e)
```
Print what went wrong.

```python
    return None
```
If literally nothing worked at all (no domain guesses, no search results), return `None` — total failure.

```python
def open_website_universal(command):
```
Start a new function called `open_website_universal`. It takes one input, `command` — the full user sentence.

```python
    """Open any website requested in natural voice."""
```
A comment explaining the purpose.

```python
    site_name = clean_website_command(command)
```
Clean up the command to extract just the core site name.

```python
    if not site_name:
```
Check: "Is the cleaned name empty?"

```python
        speak("Please tell me which website you want to open.")
```
If so, ask the user to clarify.

```python
        return False
```
Return `False` and stop.

```python
    update_ui(
        "speaking",
        command,
        f"Finding {site_name}..."
    )
```
Update the UI to show "Finding [site name]..."

```python
    print("Website requested:", site_name)
```
Print the site name we're looking for, for debugging.

```python
    resolved_url = resolve_website_url(site_name)
```
Try to figure out the actual working URL, using our big function above.

```python
    if not resolved_url:
```
Check: "Did we fail to find any working URL?"

```python
        # Final fallback: search the requested site in the browser.
```
A comment explaining the next backup plan.

```python
        search_url = (
            "https://www.google.com/search?q="
            + quote_plus(
                f"{site_name} official website"
            )
        )
```
Build a plain Google search link for `"[site name] official website"`, safely encoded for a URL.

```python
        webbrowser.open(search_url,new=2)
```
Open that Google search results page in a new browser tab.

```python
        speak(f"I could not identify the exact website, so I searched for {site_name}." )
```
Speak a message explaining what happened.

```python
        update_ui("idle",command,f"Searched for {site_name}.")
```
Update the UI with that same message.

```python
        return True
```
Return `True` — we still did something useful, even though we couldn't find the exact site.

```python
    print("Resolved website:", resolved_url)
```
If we DID find a working URL, print it for debugging.

```python
    webbrowser.open(resolved_url, new=2)
```
Open that actual resolved website in a new browser tab.

```python
    hostname = urlparse( resolved_url).netloc
```
Break apart the URL and grab just the domain/hostname part (like "amazon.com" from the full link).

```python
    speak(f"Opening {hostname}.")
```
Speak a confirmation message saying which website we're opening.

```python
    update_ui("idle",command,f"Opened {hostname}.")
```
Update the UI with that same confirmation.

```python
    return True
```
Return `True` — success!

---

## PART 24 — The Command Processor (traffic controller)

```python
def processCommand(command):
```
Start a new function called `processCommand`. It takes one input, `command` — whatever the user said.

```python
    if not command:
```
Check: "Is `command` empty?"

```python
        return
```
If so, stop immediately — nothing to process.

```python
    command = command.strip()
```
Remove extra blank space from the edges.

```python
    if not command:
```
Check again: "Is it STILL empty after trimming?" (in case it was only spaces).

```python
        return
```
If so, stop.

```python
    c_clean = command.lower()
```
Create a lowercase version of the command, called `c_clean`, used for easier text-matching checks below (case doesn't matter for checking, but we keep the original `command` for actually sending to functions, in case capitalization matters somewhere).

```python
    print()
    print("PROCESSING COMMAND:")
    print(command)
```
Print a blank line, a header, and the actual command, for debugging.

```python
    # WINDOWS APPLICATION
    app_open_match = re.match(
        r"^(?:open|launch|start|run)\s+(.+?)\s*$",
        command,
        re.IGNORECASE
    )
```
Check if the command starts with "open," "launch," "start," or "run," followed by some text (captured as the app name) all the way to the end. Save the match result.

```python
    if app_open_match:
```
Check: "Did that pattern match?"

```python
        app_query = app_open_match.group(1).strip()
```
If yes, grab the captured app name text and trim extra blank space.

```python
        normalized_query = normalize_app_query(app_query)
```
Clean it up further using our Part 17 function.

```python
        # Don't interpret these as app names when the user clearly wants a URL.
```
A comment explaining the next check's purpose.

```python
        looks_like_url = (
            normalized_query.startswith("http://")
            or normalized_query.startswith("https://")
            or normalized_query.startswith("www.")
            or ".com" in normalized_query
            or ".in" in normalized_query
            or ".org" in normalized_query
        )
```
Check several conditions to guess whether this actually looks like a website address rather than an app name (starts with http/www, or contains `.com`/`.in`/`.org` anywhere). Save `True` or `False`.

```python
        document_action_words = {
            "write", "create", "make", "document", "email",
            "report", "letter", "application", "save", "put this"
        }
```
Create a set of words that would suggest the user actually wants to WRITE a document, not open an app.

```python
        is_document_command = any(
            word in normalized_query
            for word in document_action_words
        )
```
Check: "Does ANY of those document-related words appear inside our cleaned query?" `any(...)` returns `True` if at least one match is found.

```python
        explicit_app_request = (
            "app" in app_query.lower()
            or normalized_query in APP_ALIASES
            or normalized_query in {
                "settings", "windows settings", "system settings"
            }
        )
```
Check: "Did the user specifically say the word 'app,' OR is this name already a known app in our dictionary, OR is it a Settings request?" This tells us the user CLEARLY wants an application, not something else.

```python
        if (
            not looks_like_url
            and normalized_query not in {"this", "this app"}
            and not is_document_command
            and not is_explicit_website_request(command)
        ):
```
Check ALL of these conditions together: it does NOT look like a URL, AND it's not just the vague words "this"/"this app," AND it's not a document-writing command, AND it's not an explicit website request. Only if ALL of these are true do we treat it as an app-launching command.

```python
            print("Application command detected:", app_query)
```
Print a debug message confirming we detected an app command.

```python
            update_ui("speaking",command,f"Opening {app_query}...")
```
Update the UI to show "Opening [app]..."

```python
            success = launch_application(app_query)
```
Actually try to launch the app, using our Part 18 function, and save whether it worked.

```python
            if success:
```
Check: "Did launching succeed?"

```python
                update_ui(   "idle",   command, f"{app_query} opened successfully.")
```
If yes, update the UI with a success message.

```python
                speak(f"{app_query} opened.")
```
Speak a confirmation.

```python
                return
```
Stop the whole `processCommand` function here — we're done, don't check any other command types.

```python
            # If the user explicitly said "app" or the app is a known alias,
            # report the failure instead of interpreting it as a website.
```
A comment explaining the next check.

```python
            if explicit_app_request:
```
If launching FAILED, check: "Did the user clearly ask for an app (not something ambiguous)?"

```python
                update_ui("idle", command, f"I could not find {app_query} on your laptop." )
```
If it was a clear app request that failed, update the UI with a "not found" message.

```python
                speak(f"I could not find {app_query} on your laptop.")
```
Speak that failure message.

```python
                return
```
Stop the function here. (Note: if it WASN'T an explicit app request and launching failed, the code doesn't return here — it will continue down and get checked against the other command types below, like websites.)

```python
    # CREATE FOLDER / FILE
    if (
        (
            "create" in c_clean
            or
            "make" in c_clean)
        and
        (
            "folder" in c_clean
            or
            "directory" in c_clean
            or
            "file" in c_clean
        )
    ):
```
Check: "Does the command contain 'create' OR 'make,' AND ALSO contain 'folder' OR 'directory' OR 'file'?" This roughly detects a folder/file creation request.

```python
        print("Create folder/file command detected.")
```
Print a debug message.

```python
        success = create_desktop_item(command)
```
Try to create the folder/file, using our Part 19 function, and save whether it worked.

```python
        if success:
```
Check: "Did it succeed?"

```python
            update_ui("idle",command, "The folder or file was created successfully.")
```
If yes, update the UI with a success message.

```python
        else:
```
If it did NOT succeed, do this instead.

```python
            update_ui("idle",command, "I could not create the folder or file.")
```
Update the UI with a failure message.

```python
        return
```
Stop the function here — we handled this command, no need to check further.

```python
    # MICROSOFT WORD
    if (
        "word" in c_clean
        and
        (
            "open" in c_clean
            or
            "write" in c_clean
            or
            "create" in c_clean
            or
            "make" in c_clean
            or
            "document" in c_clean
            or
            "email" in c_clean
            or
            "report" in c_clean
            or
            "letter" in c_clean
            or
            "application" in c_clean
        )
    ):
```
Check: "Does the command contain the word 'word,' AND ALSO contain at least one action word like 'open,' 'write,' 'create,' etc.?" This detects Word-related commands.

```python
        handle_word_command(command)
```
If it matched, run our Word handler function from Part 20.

```python
        return
```
Stop the function here.

```python
    # NOTEPAD
    if (
        "notepad" in c_clean
        and
        (
            "open" in c_clean
            or
            "write" in c_clean
            or
            "create" in c_clean
            or
            "make" in c_clean
            or
            "document" in c_clean
            or
            "email" in c_clean
            or
            "report" in c_clean
            or
            "letter" in c_clean
            or
            "application" in c_clean
        )
    ):
```
Same idea as Word, but checking for "notepad" instead.

```python
        handle_notepad_command(command)
```
Run our Notepad handler from Part 21.

```python
        return
```
Stop the function.

```python
    # NEWS
    if "news" in c_clean:
```
Check: "Does the command contain the word 'news'?"

```python
        update_ui("speaking",command,"Fetching real-time news headlines...")
```
If so, update the UI to show we're fetching news.

```python
        speak("Fetching latest news headlines.")
```
Speak that same message.

```python
        headlines = fetch_latest_news()
```
Actually fetch the news headlines, using our Part 5 function.

```python
        if headlines:
```
Check: "Did we actually get some headlines back?"

```python
            for idx, headline in enumerate( headlines, 1):
```
If yes, loop through each headline, and also get a counting number for each one, starting from 1 (`enumerate(headlines, 1)` gives us both the position number and the headline text together).

```python
                update_ui("speaking",f"Headline {idx}", headline)
```
Update the UI to show "Headline [number]" and its text.

```python
                print(f"Headline {idx}:",headline)
```
Print the headline to the console too.

```python
                speak(headline)
```
Speak this headline out loud.

```python
            update_ui("idle",command,"Finished reading news.")
```
After the loop finishes (all headlines read), update the UI saying we're done.

```python
        else:
```
If we did NOT get any headlines, do this instead.

```python
            update_ui("idle",command,"sorry, I couldn't fetch live news right now.")
```
Update the UI with an apology message.

```python
            speak("Sorry, I was unable to fetch the news at this moment.")
```
Speak that apology out loud.

```python
        return
```
Stop the function here.

```python
    # PLAY YOUTUBE
    if c_clean.startswith("play "):
```
Check: "Does the command start with the word 'play' followed by a space?"

```python
        play_youtube(command)
```
If so, run our YouTube player function from Part 22.

```python
        return
```
Stop the function.

```python
    # UNIVERSAL WEBSITE
    if is_explicit_website_request(command):
```
Check: "Does this clearly look like a request to open a website?" (using our Part 23 function).

```python
        open_website_universal(command)
```
If so, run our website opener function.

```python
        return
```
Stop the function.

```python
    # Direct URL commands without the word "website".
    if re.match(
        r"^(?:open|go\s+to|visit|browse)\s+(?:https?://|www\.)",
        c_clean,
        re.IGNORECASE
    ):
```
Check: "Does the command start with 'open/go to/visit/browse' followed directly by 'http://', 'https://', or 'www.'?" (even without the word "website" being said).

```python
        open_website_universal(command)
```
If so, still treat it as a website request.

```python
        return
```
Stop the function.

```python
    # Generic "open <domain>" support.
    if c_clean.startswith("open "):
```
Check: "Does the command start with 'open '?" (a more general check, in case none of the earlier patterns matched).

```python
        site_candidate = command.split(" ",   1)[1].strip()
```
Split the command at the first space, take the second piece (everything after "open "), and trim it — this is our possible site name.

```python
        if looks_like_web_address(site_candidate):
```
Check: "Does this piece actually look like a web address?" (using our Part 23 function).

```python
            open_website_universal( command )
```
If it does, treat it as a website request.

```python
            return
```
Stop the function.

```python
    # NORMAL GEMINI AI
    print("No special command detected.")
```
If NONE of the checks above matched anything, print a message saying no special command was found.

```python
    print("Sending command to Gemini...")
```
Print a message saying we're sending this to the AI instead.

```python
    update_ui("speaking",command, "Thinking...")
```
Update the UI to show "Thinking..." while we wait for the AI.

```python
    output = aiProcess( command )
```
Send the command to our general AI chat function from Part 6, and save the AI's answer.

```python
    if output:
```
Check: "Did we get a valid answer back?"

```python
        update_ui("speaking",command, output )
```
If yes, update the UI to show the AI's answer.

```python
        print()
        print("FRIDAY:")
        print(output)
```
Print the answer to the console with a header, for debugging.

```python
        speak( output)
```
Speak the AI's answer out loud.

```python
        update_ui( "idle",command, output )
```
Update the UI again, this time with state set back to "idle," still showing the answer.

```python
    else:
```
If we did NOT get a valid answer, do this instead.

```python
        update_ui("idle", command,"Sorry, I could not generate a response." )
```
Update the UI with an apology message.

```python
        speak( "Sorry, I could not generate a response.")
```
Speak that apology out loud.

---

## PART 25 — The Assistant Loop (always listening)

```python
def assistant_loop():
```
Start a new function called `assistant_loop`. It doesn't need any inputs — this is the main listening engine.

```python
    recognizer = sr.Recognizer()
```
Create a new speech-recognition tool, and save it as `recognizer`.

```python
    recognizer.energy_threshold = 150
```
Set how loud a sound needs to be before it's counted as "someone speaking." 150 is a starting sensitivity level.

```python
    recognizer.dynamic_energy_threshold = True
```
Turn on automatic adjustment — the sensitivity level will change on its own depending on how noisy the room is.

```python
    recognizer.pause_threshold = 2.0
```
Set how many seconds of silence mean "the person has finished talking" — here, 2 full seconds.

```python
    recognizer.phrase_threshold = 0.3
```
Set the minimum length of sound (0.3 seconds) needed before it's even considered the start of speech (filters out tiny random noises).

```python
    recognizer.non_speaking_duration = 1.0
```
Set how many seconds of silence to keep around the edges of a recorded phrase (helps capture full sentences cleanly).

```python
    time.sleep(2)
```
Wait 2 seconds before continuing, giving the program time to fully start up.

```python
    update_ui("idle","","Initializing Friday..." )
```
Update the UI to show "Initializing Friday..."

```python
    speak("Initializing Friday.")
```
Speak that same message out loud.

```python
    try:
```
Try the following code safely.

```python
        with sr.Microphone() as source:
```
Open a connection to the computer's microphone, and call it `source` (this also makes sure it's properly closed afterward).

```python
            print("Calibrating ambient noise background...")
```
Print a message saying we're about to measure the background noise level.

```python
            recognizer.adjust_for_ambient_noise(source, duration=1.5)
```
Listen to the microphone for 1.5 seconds of "silence" (background noise only) to automatically figure out the right sensitivity level for THIS specific room.

```python
            print("Energy threshold:", recognizer.energy_threshold)
```
Print out whatever sensitivity level was calculated, for debugging.

```python
    except Exception as e:
```
If setting up the microphone failed for any reason (like no mic connected), catch the error.

```python
        print("Microphone initialization error:",e)
```
Print what went wrong.

```python
        update_ui("idle","","Microphone initialization failed." )
```
Update the UI with a failure message.

```python
        speak( "Microphone initialization failed.")
```
Speak that failure message.

```python
        return
```
Stop the ENTIRE function here — without a working microphone, there's no point continuing.

```python
    print()
    print("FRIDAY IS READY")
    print("Say: Friday")
```
Print a few lines announcing that everything is ready and the wake word to use.

```python
    update_ui("idle","","Listening for 'Friday'..." )
```
Update the UI to show we're now listening for the wake word.

```python
    while True:
```
Start an infinite loop — this means "keep repeating the following code forever" (until something stops it, like an error or Ctrl+C).

```python
        try:
```
Try the following code safely (so one bad moment doesn't crash the whole loop).

```python
            with sr.Microphone() as source:
```
Open the microphone again for this round of listening.

```python
                update_ui("idle","", "Listening for 'Friday'...")
```
Update the UI to confirm we're actively listening.

```python
                print( "Listening for wake word...")
```
Print a message for debugging.

```python
                audio = recognizer.listen(source,timeout=None, phrase_time_limit=8 )
```
Actually listen and record audio from the microphone. `timeout=None` means "wait forever until someone starts talking" (no time limit to START). `phrase_time_limit=8` means "once they start talking, only record up to 8 seconds max." Save the recorded audio.

```python
            word = recognizer.recognize_google(audio,language="en-IN").lower().strip()
```
Send that recorded audio to Google's speech recognition service, asking it to convert the sound into text, specifically expecting Indian English (`en-IN`). Then make it lowercase and trim extra blank space. Save the result as `word`.

```python
            print(    "Heard:", word )
```
Print whatever was heard, for debugging.

```python
            if "friday" not in word:
```
Check: "Does the word 'friday' NOT appear anywhere in what was heard?"

```python
                continue
```
If the wake word wasn't said, skip the rest of this loop and go straight back to listening again (ignore whatever was said).

```python
            print("WAKE WORD DETECTED!")
```
If "friday" WAS heard, print a confirmation message.

```python
            update_ui("speaking","Friday","Yes sir, how can I help you?" )
```
Update the UI to show Friday is responding.

```python
            speak("Yes sir, how can I help you?")
```
Speak that greeting out loud.

```python
            update_ui("listening","","Listening for your command...")
```
Update the UI to show we're now waiting for the actual command.

```python
            with sr.Microphone() as source:
```
Open the microphone again, for listening to the actual command this time.

```python
                print("Listening for command...")
```
Print a debug message.

```python
                command_audio = recognizer.listen(source, timeout=10,phrase_time_limit=60)
```
Listen and record audio. `timeout=10` means "wait up to 10 seconds for the person to START talking, then give up if they say nothing." `phrase_time_limit=60` means "once they start, allow up to 60 seconds total for the whole command." Save the recording.

```python
            command = recognizer.recognize_google(command_audio,language="en-IN")
```
Convert that recorded command audio into text, using Indian English, and save it as `command` (this time we keep the original capitalization, unlike the wake word check).

```python
            print("Recognized command:",command)
```
Print what was understood, for debugging.

```python
            processCommand(command)
```
Send this command to our big traffic-controller function from Part 24, which will figure out what to actually do with it.

```python
        except sr.UnknownValueError:
```
If the speech recognition couldn't understand any words in the audio (like mumbling or just noise), catch this specific error type.

```python
            print("Speech Recognition could not understand audio.")
```
Print a message explaining this.

```python
        except sr.WaitTimeoutError:
```
If nobody spoke at all within the allowed waiting time, catch this specific error type.

```python
            print("Listening timed out waiting for phrase.")
```
Print a message explaining this.

```python
        except sr.RequestError as e:
```
If there was a problem actually REACHING Google's speech recognition servers (like no internet), catch this specific error type.

```python
            print("Google Speech Recognition error:", e)
```
Print what the error was.

```python
            time.sleep(2)
```
Wait 2 seconds before trying again, in case it was a temporary internet hiccup.

```python
        except KeyboardInterrupt:
```
If the person running the program manually presses Ctrl+C to stop it, catch this specific event.

```python
            print("Friday stopped.")
```
Print a message saying the program is stopping.

```python
            break
```
Exit the `while True:` loop completely — this stops the endless listening cycle for good.

```python
        except Exception as e:
```
If ANY other unexpected kind of error happens that we didn't specifically plan for, catch it here as a general safety net.

```python
            print( "Audio Error:", e )
```
Print what the unexpected error was.

```python
            time.sleep(1)
```
Wait 1 second before the loop tries again, so a single glitch doesn't spam errors non-stop.

---

## PART 26 — Starting the whole program

```python
if __name__ == "__main__":
```
This is a standard Python safety check. It means: "Only run the following code if this file is being run directly (not imported as a helper file into some other program)."

```python
    print(
        "Starting Friday..."
    )
```
Print a startup message to the console.

```python
    assistant_thread = threading.Thread(target=assistant_loop,daemon=True)
```
Create a new background "thread" (a second independent task running alongside the main program). `target=assistant_loop` means "when this thread starts, run the `assistant_loop` function." `daemon=True` means "if the main program closes, automatically stop this background thread too — don't let it keep running forever by itself."

```python
    assistant_thread.start()
```
Actually START that background thread now — this begins the microphone-listening loop running quietly in the background.

```python
    eel.start("index.html", size=(1920, 1200))
```
Start the Eel window, opening the file `index.html` (your webpage/UI), with the window sized at 1920 pixels wide by 1200 pixels tall. This becomes the "main" visible part of the program — while it runs, the microphone is listening in the background at the same time, thanks to the separate thread we just started.

---

# The End

That's every single line of your Friday assistant, explained one at a time, in easy English.

**Quick recap of the big picture:**
Friday starts two things at once — a window you can see, and a background "ear" that listens through your microphone.
It waits quietly until it hears the word "Friday," then listens to your actual request, checks it against a list of known patterns (open app, write document, play music, open website, get news), and does whatever matches — always speaking back to you and updating the screen along the way. If nothing matches, it just asks Google's Gemini AI to answer normally, like a chatbot.
