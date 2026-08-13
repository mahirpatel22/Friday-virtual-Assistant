import os
import threading
import pyautogui
import pyperclip
import webbrowser
import eel
import pyttsx3
import requests
import speech_recognition as sr
import subprocess
import re
import time
import ctypes
import shutil
import unicodedata
from urllib.parse import urlparse, parse_qs, unquote, quote_plus

from google import genai

# Optional but recommended for reliable first-result YouTube playback:
#     pip install yt-dlp
# Word document automation additionally requires:
#     pip install pywin32


# ==================================================================
# 1. EEL & API SETUP
# ==================================================================

eel.init("web")


NEWS_API_KEY = os.environ.get(
    "NEWS_API_KEY",

)

GEMINI_API_KEY = os.environ.get(
    "GEMINI_API_KEY",

)


if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY is not configured.")
    client = None
else:
    try:
        client = genai.Client(
            api_key=GEMINI_API_KEY
        )
    except Exception as e:
        print("Gemini initialization error:", e)
        client = None


# ==================================================================
# 2. TTS FUNCTION
# ==================================================================

tts_lock = threading.Lock()


def speak(text):
    """Local offline speech synthesis."""

    if not text:
        return

    try:
        with tts_lock:
            engine = pyttsx3.init()

            engine.setProperty(
                "rate",
                180
            )

            engine.setProperty(
                "volume",
                1.0
            )

            engine.say(str(text))
            engine.runAndWait()
            engine.stop()

    except Exception as e:
        print("TTS Error:", e)


# ==================================================================
# 3. SAFE UI UPDATE
# ==================================================================

def update_ui(
    state,
    user_text="",
    response=""
):
    try:
        eel.updateUI(
            state,
            user_text,
            response
        )()
    except Exception as e:
        print("UI Error:", e)


# ==================================================================
# 4. REAL-TIME NEWS
# ==================================================================

def fetch_latest_news():

    if not NEWS_API_KEY:
        print("NEWS_API_KEY is not configured.")
        return None

    url = (
        "https://newsdata.io/api/1/latest"
        f"?apikey={NEWS_API_KEY}"
        "&language=en"
    )

    try:
        response = requests.get(
            url,
            timeout=8
        )

        if response.status_code != 200:
            print(
                "News API Error:",
                response.status_code
            )
            print(response.text)
            return None

        data = response.json()

        results = data.get(
            "results",
            []
        )

        if not results:
            print("News API returned 0 articles.")
            return None

        headlines = []

        for article in results[:3]:
            title = article.get("title")

            if title:
                headlines.append(title)

        return headlines

    except Exception as e:
        print("Failed to fetch news:", e)
        return None


# ==================================================================
# 5. GEMINI GENERAL AI
# ==================================================================

def aiProcess(command):

    if not command:
        return None

    if client is None:
        print("Gemini client is not available.")
        return None

    prompt = f"""
You are Friday, a helpful personal AI assistant.

Answer the user's request clearly and naturally.

Keep normal conversational answers concise.

User:
{command}

Assistant:
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        if response is None:
            return None

        if not response.text:
            return None

        return response.text.strip()

    except Exception as e:
        print("Gemini Error:", e)
        return None


# ==================================================================
# 6. GEMINI DOCUMENT GENERATOR
# ==================================================================

def generate_document(command):
    """
    Generates a complete document/email/report/message
    based on the user's voice command.
    """

    if not command:
        return None

    if client is None:
        print("Gemini client is not available.")
        return None

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

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        if response is None:
            return None

        if not response.text:
            return None

        return response.text.strip()

    except Exception as e:
        print("Document Generation Error:", e)
        return None


# ==================================================================
# 7. CLEAN DOCUMENT TEXT
# ==================================================================

def clean_document_text(text):

    if not text:
        return ""

    text = re.sub(
        r"```.*?```",
        "",
        text,
        flags=re.DOTALL
    )

    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        text,
        flags=re.DOTALL
    )

    text = re.sub(
        r"__(.*?)__",
        r"\1",
        text,
        flags=re.DOTALL
    )

    text = re.sub(
        r"(?<!\*)\*(.*?)\*(?!\*)",
        r"\1",
        text,
        flags=re.DOTALL
    )

    return text.strip()


# ==================================================================
# 8. EXTRACT DOCUMENT REQUEST
# ==================================================================

def extract_document_request(
    command,
    application
):

    text = command.strip()

    if application == "word":

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

    else:

        patterns = [
            r"open\s+notepad",
            r"write\s+in\s+notepad",
            r"write\s+this\s+in\s+notepad",
            r"put\s+this\s+in\s+notepad",
            r"create\s+in\s+notepad",
            r"make\s+in\s+notepad",
            r"save\s+in\s+notepad"
        ]

    for pattern in patterns:
        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE
        )

    text = re.sub(
        r"^\s*(and|then)\s+",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


# ==================================================================
# 9. WRITE RESPONSE TO NOTEPAD
# ==================================================================

def write_to_notepad(text):

    try:
        print("Opening Notepad...")

        subprocess.Popen(
            ["notepad.exe"]
        )

        time.sleep(2)

        plain_text = clean_document_text(text)

        pyperclip.copy(plain_text)

        time.sleep(0.3)

        pyautogui.hotkey(
            "ctrl",
            "v"
        )

        time.sleep(0.5)

        print(
            "Response successfully written to Notepad."
        )

        return True

    except Exception as e:
        print("Notepad Error:", e)
        return False


# ==================================================================
# 10. WRITE RESPONSE TO MICROSOFT WORD
# ==================================================================

def write_to_word(text):

    try:
        import win32com.client
    except ImportError:
        print("pywin32 is not installed.")
        print("Install it using: pip install pywin32")
        return False

    try:
        print("Opening Microsoft Word...")

        word = win32com.client.Dispatch(
            "Word.Application"
        )

        word.Visible = True

        document = word.Documents.Add()

        time.sleep(1)

        plain_text = clean_document_text(text)

        selection = word.Selection

        selection.Font.Name = "Calibri"
        selection.Font.Size = 11
        selection.Font.Bold = False
        selection.Font.Italic = False
        selection.Font.Underline = False

        selection.TypeText(
            plain_text
        )

        print(
            "Response successfully written to Microsoft Word."
        )

        return True

    except Exception as e:
        print("Word Error:", e)
        return False


# ==================================================================
# 11. WINDOWS PATH / APPLICATION HELPERS
# ==================================================================

def get_desktop_path():
    """Return the real Windows Desktop path, including OneDrive/redirection."""

    # Windows Known Folder API: FOLDERID_Desktop
    try:
        from ctypes import wintypes

        shell32 = ctypes.windll.shell32
        ole32 = ctypes.windll.ole32

        shell32.SHGetKnownFolderPath.argtypes = [
            ctypes.c_void_p,
            wintypes.DWORD,
            wintypes.HANDLE,
            ctypes.POINTER(ctypes.c_wchar_p)
        ]
        shell32.SHGetKnownFolderPath.restype = ctypes.HRESULT

        # Use the GUID structure instead of relying on a hard-coded folder path.
        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", ctypes.c_ulong),
                ("Data2", ctypes.c_ushort),
                ("Data3", ctypes.c_ushort),
                ("Data4", ctypes.c_ubyte * 8),
            ]

        import uuid
        u = uuid.UUID("B4BFCC3A-DB2C-424C-B029-7FE99A87C641")
        guid = GUID(
            u.fields[0],
            u.fields[1],
            u.fields[2],
            (ctypes.c_ubyte * 8)(*u.bytes[8:])
        )

        result = ctypes.c_wchar_p()
        hr = shell32.SHGetKnownFolderPath(
            ctypes.byref(guid),
            0,
            None,
            ctypes.byref(result)
        )

        if hr == 0 and result.value and os.path.isdir(result.value):
            desktop = result.value
            ole32.CoTaskMemFree(result)
            return desktop

        if result:
            ole32.CoTaskMemFree(result)

    except Exception as e:
        print("Known Desktop lookup error:", e)

    # Fallbacks for older/custom Windows configurations.
    user_home = os.path.expanduser("~")

    candidates = [
        os.path.join(user_home, "Desktop"),
        os.path.join(user_home, "OneDrive", "Desktop"),
        os.path.join(os.environ.get("OneDrive", ""), "Desktop"),
    ]

    for path in candidates:
        if path and os.path.isdir(path):
            return os.path.abspath(path)

    return None


def clean_windows_name(name):
    """Clean a spoken Windows file/folder name without removing spaces."""

    name = unicodedata.normalize("NFKC", name or "")
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r"\s+", " ", name).strip()
    name = name.rstrip(" .")

    # Windows reserved names.
    if name.upper() in {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }:
        name = "_" + name

    return name


def find_start_menu_shortcut(app_name):
    """Find a Start Menu shortcut for a classic desktop application."""

    app_name = re.sub(r"\s+", " ", app_name.lower()).strip()

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

    best_match = None

    for root in roots:
        if not os.path.isdir(root):
            continue

        for current_root, _, files in os.walk(root):
            for filename in files:
                if not filename.lower().endswith(".lnk"):
                    continue

                label = os.path.splitext(filename)[0].lower()
                normalized = re.sub(r"[^a-z0-9 ]+", " ", label)
                normalized = re.sub(r"\s+", " ", normalized).strip()

                if normalized == app_name:
                    return os.path.join(current_root, filename)

                if app_name in normalized or normalized in app_name:
                    best_match = os.path.join(current_root, filename)

    return best_match


def launch_start_app(app_name):
    """Launch a Microsoft Store/UWP app by its StartApps registration."""

    try:
        safe_name = app_name.replace("'", "''")
        ps_script = (
            f"Get-StartApps | Where-Object {{ $_.Name -like '*{safe_name}*' }} "
            "| Select-Object -First 1 -ExpandProperty AppID"
        )

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

        app_id = result.stdout.strip().splitlines()

        if not app_id:
            return False

        app_id = app_id[0].strip()

        subprocess.Popen([
            "explorer.exe",
            f"shell:AppsFolder\\{app_id}"
        ])

        time.sleep(1.5)
        return True

    except Exception as e:
        print("StartApps launch error:", e)
        return False


APP_ALIASES = {
    # Microsoft Office
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

    # Windows built-ins
    "notepad": ["notepad.exe"],
    "notepad app": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "calc": ["calc.exe"],
    "paint": ["mspaint.exe"],
    "file explorer": ["explorer.exe"],
    "explorer": ["explorer.exe"],
    "task manager": ["taskmgr.exe"],
    "control panel": ["control.exe"],

    # Browsers / development
    "chrome": ["chrome.exe"],
    "google chrome": ["chrome.exe"],
    "edge": ["msedge.exe"],
    "microsoft edge": ["msedge.exe"],
    "firefox": ["firefox.exe"],
    "vs code": ["code"],
    "visual studio code": ["code"],
    "vscode": ["code"],

    # Common Store apps (resolved through StartApps when needed)
    "whatsapp": [],
    "whatsapp app": [],
    "spotify": [],
    "discord": [],
    "telegram": []
}


def normalize_app_query(query):
    query = query.lower().strip()

    query = re.sub(
        r"\b(on|in)\s+(my|the)\s+laptop\b",
        "",
        query
    )
    query = re.sub(r"\bapp(lication)?\b", "", query)
    query = re.sub(r"\bplease\b", "", query)
    query = re.sub(r"\s+", " ", query).strip()

    return query


def launch_application(app_query):
    """Launch a Windows application from an alias, PATH, Start Menu, or StartApps."""

    app_name = normalize_app_query(app_query)

    if not app_name:
        return False

    print("Application requested:", app_name)

    # Windows Settings is a URI, not a normal EXE.
    if app_name in {"settings", "windows settings", "system settings"}:
        try:
            os.startfile("ms-settings:")
            return True
        except Exception as e:
            print("Settings launch error:", e)

    # Exact known aliases first.
    candidates = APP_ALIASES.get(app_name)

    if candidates is not None:
        for target in candidates:
            try:
                if os.path.isabs(target) and not os.path.exists(target):
                    continue

                if target == "code":
                    if shutil.which("code"):
                        subprocess.Popen(["code"])
                        return True
                    # Fall through to Start Menu if 'code' is not in PATH.
                    continue

                subprocess.Popen([target])
                return True
            except Exception as e:
                print(f"Alias launch failed for {target}:", e)

    # Search Start Menu shortcuts, which supports many installed apps.
    shortcut = find_start_menu_shortcut(app_name)

    if shortcut:
        try:
            os.startfile(shortcut)
            return True
        except Exception as e:
            print("Shortcut launch error:", e)

    # Search Microsoft Store/packaged apps (excellent for WhatsApp, etc.).
    if launch_start_app(app_name):
        return True

    # Last attempt: Windows 'start' command can resolve registered executables.
    try:
        subprocess.Popen(
            f'start "" "{app_name}"',
            shell=True
        )
        time.sleep(1)
        return True
    except Exception as e:
        print("Generic application launch error:", e)

    return False


# ==================================================================
# 12. CREATE DESKTOP FOLDER / FILE
# ==================================================================

def create_desktop_item(command):
    """Create a folder/file on the user's real Desktop path."""

    try:
        desktop = get_desktop_path()

        if not desktop:
            print("Desktop folder not found.")
            speak("I could not find your Desktop folder.")
            return False

        print("Desktop:", desktop)
        command = command.strip()
        print("Command:", command)

        # Examples supported:
        #   make a folder named generative AI
        #   create folder called project files on desktop
        #   make a file named notes.txt in folder named generative AI
        folder_match = re.search(
            r"(?:a\s+)?(?:folder|directory)\s+"
            r"(?:named|called)\s+(.+?)"
            r"(?=\s+(?:and|then)\s+(?:make|create)\s+(?:a\s+)?file\b|$)",
            command,
            re.IGNORECASE
        )

        # Also support "create folder generative AI".
        if not folder_match:
            folder_match = re.search(
                r"(?:a\s+)?(?:folder|directory)\s+(.+?)"
                r"(?=\s+(?:and|then)\s+(?:make|create)\s+(?:a\s+)?file\b|\s+on\s+(?:the\s+)?desktop\b|$)",
                command,
                re.IGNORECASE
            )

        file_match = re.search(
            r"(?:file)\s+(?:named|called)\s+(.+?)"
            r"(?=\s+(?:in|inside|within)\s+(?:the\s+)?folder\b|$)",
            command,
            re.IGNORECASE
        )

        # Optional: create a file without 'named'.
        if not file_match:
            file_match = re.search(
                r"(?:file)\s+([A-Za-z0-9_. -]+?)"
                r"(?=\s+(?:in|inside|within)\s+(?:the\s+)?folder\b|$)",
                command,
                re.IGNORECASE
            )

        folder_name = None
        if folder_match:
            folder_name = clean_windows_name(folder_match.group(1))

            # Remove spoken location words accidentally captured by STT.
            folder_name = re.sub(
                r"\s+(?:on|in)\s+(?:the\s+)?desktop\s*$",
                "",
                folder_name,
                flags=re.IGNORECASE
            ).strip()

        folder_path = desktop

        if folder_name:
            folder_path = os.path.join(desktop, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            print("Folder created/verified:", folder_path)

        if file_match:
            file_name = clean_windows_name(file_match.group(1))
            file_name = re.sub(
                r"\s+(?:on|in)\s+(?:the\s+)?desktop\s*$",
                "",
                file_name,
                flags=re.IGNORECASE
            ).strip()

            if not file_name:
                raise ValueError("The file name was empty.")

            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "a", encoding="utf-8"):
                pass

            print("File created/verified:", file_path)

        if not folder_name and not file_match:
            print("Could not detect folder or file.")
            speak("I could not understand what you want me to create.")
            return False

        spoken_target = "the folder" if folder_name and not file_match else "the file" if file_match and not folder_name else "the folder and file"
        speak(f"Done. I created {spoken_target} on your Desktop.")

        update_ui(
            "idle",
            command,
            f"Created successfully on Desktop: {folder_path}"
        )

        return True

    except Exception as e:
        print()
        print("==========================================")
        print("CREATE ERROR")
        print(e)
        print("==========================================")

        speak("There was an error while creating it.")
        return False


# ==================================================================
# 12. OPEN VS CODE
# ==================================================================

def open_vscode():

    try:

        print()
        print("==========================================")
        print("OPENING VISUAL STUDIO CODE")
        print("==========================================")

        subprocess.Popen(
            ["code"],
            shell=True
        )

        time.sleep(2)

        print(
            "Visual Studio Code opened successfully."
        )

        speak(
            "Visual Studio Code opened."
        )

        return True

    except Exception as e:

        print(
            "VS Code command error:",
            e
        )

    possible_paths = [

        os.path.expandvars(
            r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
        ),

        os.path.expandvars(
            r"%PROGRAMFILES%\Microsoft VS Code\Code.exe"
        ),

        os.path.expandvars(
            r"%PROGRAMFILES(X86)%\Microsoft VS Code\Code.exe"
        )
    ]

    for path in possible_paths:

        if os.path.exists(path):

            try:

                subprocess.Popen(
                    [path]
                )

                time.sleep(2)

                print(
                    "VS Code opened from:",
                    path
                )

                speak(
                    "Visual Studio Code opened."
                )

                return True

            except Exception as path_error:

                print(
                    "Could not open:",
                    path_error
                )

    print(
        "Visual Studio Code could not be found."
    )

    speak(
        "I could not open Visual Studio Code."
    )

    return False


# ==================================================================
# 13. WORD COMMAND
# ==================================================================

def handle_word_command(command):

    print()
    print("==========================================")
    print("WORD DOCUMENT COMMAND")
    print(command)
    print("==========================================")

    document_request = extract_document_request(
        command,
        "word"
    )

    if not document_request:

        try:

            subprocess.Popen(
                ["winword.exe"]
            )

            update_ui(
                "idle",
                command,
                "Microsoft Word opened."
            )

            speak(
                "Microsoft Word opened."
            )

        except Exception as e:

            print(
                "Could not open Word:",
                e
            )

            update_ui(
                "idle",
                command,
                "I could not open Microsoft Word."
            )

            speak(
                "I could not open Microsoft Word."
            )

        return

    update_ui(
        "speaking",
        command,
        "Generating your Word document..."
    )

    speak(
        "Generating your Word document."
    )

    response = generate_document(
        document_request
    )

    if not response:

        update_ui(
            "idle",
            command,
            "I could not generate the document."
        )

        speak(
            "I could not generate the document."
        )

        return

    update_ui(
        "speaking",
        command,
        response
    )

    print()
    print("GENERATED WORD DOCUMENT:")
    print(response)

    success = write_to_word(
        response
    )

    if success:

        update_ui(
            "idle",
            command,
            response
        )

        speak(
            "The document has been written to Microsoft Word."
        )

    else:

        update_ui(
            "idle",
            command,
            "I could not write the document to Microsoft Word."
        )

        speak(
            "I could not write the document to Microsoft Word."
        )


# ==================================================================
# 14. NOTEPAD COMMAND
# ==================================================================

def handle_notepad_command(command):

    print()
    print("==========================================")
    print("NOTEPAD DOCUMENT COMMAND")
    print(command)
    print("==========================================")

    document_request = extract_document_request(
        command,
        "notepad"
    )

    if not document_request:

        try:

            subprocess.Popen(
                ["notepad.exe"]
            )

            update_ui(
                "idle",
                command,
                "Notepad opened."
            )

            speak(
                "Notepad opened."
            )

        except Exception as e:

            print(
                "Could not open Notepad:",
                e
            )

            update_ui(
                "idle",
                command,
                "I could not open Notepad."
            )

            speak(
                "I could not open Notepad."
            )

        return

    update_ui(
        "speaking",
        command,
        "Generating your Notepad content..."
    )

    speak(
        "Generating your Notepad content."
    )

    response = generate_document(
        document_request
    )

    if not response:

        update_ui(
            "idle",
            command,
            "I could not generate the content."
        )

        speak(
            "I could not generate the content."
        )

        return

    update_ui(
        "speaking",
        command,
        response
    )

    print()
    print("GENERATED NOTEPAD CONTENT:")
    print(response)

    success = write_to_notepad(
        response
    )

    if success:

        update_ui(
            "idle",
            command,
            response
        )

        speak(
            "The response has been written to Notepad."
        )

    else:

        update_ui(
            "idle",
            command,
            "I could not write the response to Notepad."
        )

        speak(
            "I could not write the response to Notepad."
        )


# ==================================================================
# 15. PLAY YOUTUBE
# ==================================================================

def get_youtube_video_url(query):
    """Return the first YouTube video URL for a spoken song/video query."""

    # Best option: yt-dlp resolves the first result directly to a watch URL.
    try:
        import yt_dlp

        options = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extract_flat": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            result = ydl.extract_info(
                f"ytsearch1:{query}",
                download=False
            )

        entries = result.get("entries") or []

        if entries:
            first = entries[0]
            video_id = first.get("id")

            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"

            webpage_url = first.get("webpage_url")
            if webpage_url:
                return webpage_url

    except ImportError:
        print("yt-dlp is not installed. Trying YouTube HTML lookup.")
    except Exception as e:
        print("YouTube direct search error:", e)

    # Lightweight fallback: YouTube's search HTML normally contains video IDs
    # even when yt-dlp is unavailable.
    try:
        search_url = (
            "https://www.youtube.com/results?search_query="
            + requests.utils.quote(query)
        )

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

        if response.ok:
            video_ids = re.findall(
                r'"videoId":"([A-Za-z0-9_-]{11})"',
                response.text
            )

            seen = set()
            for video_id in video_ids:
                if video_id in seen:
                    continue
                seen.add(video_id)
                return f"https://www.youtube.com/watch?v={video_id}&autoplay=1"

    except Exception as e:
        print("YouTube HTML lookup error:", e)

    return None


def play_youtube(command):
    parts = command.split(" ", 1)

    if len(parts) < 2:
        speak("Please tell me what you want to play.")
        return False

    song = parts[1].strip()

    if not song:
        speak("Please tell me what you want to play.")
        return False

    print("Playing:", song)

    update_ui(
        "speaking",
        command,
        f"Finding {song} on YouTube..."
    )

    # Open the actual first video instead of only opening search results.
    video_url = get_youtube_video_url(song)

    if video_url:
        print("Opening YouTube video:", video_url)
        webbrowser.open(video_url, new=2)

        time.sleep(5)

        # The direct watch URL uses autoplay=1. Avoid blindly pressing Space:
        # Space toggles play/pause and would pause a video that already started.
        speak(f"Playing {song} on YouTube.")
        update_ui(
            "idle",
            command,
            f"Playing {song} on YouTube."
        )
        return True

    # Fallback when yt-dlp is unavailable or YouTube blocks extraction.
    search_url = (
        "https://www.youtube.com/results?search_query="
        + requests.utils.quote(song)
    )

    webbrowser.open(search_url, new=2)
    time.sleep(4)

    # Move to the first search result and open it with keyboard navigation.
    try:
        pyautogui.press("tab", presses=7, interval=0.15)
        pyautogui.press("enter")
    except Exception as e:
        print("YouTube result navigation fallback error:", e)

    speak(f"I opened the YouTube result for {song}.")
    update_ui(
        "idle",
        command,
        f"YouTube search opened for {song}."
    )

    return True


# ==================================================================
# 16. UNIVERSAL WEBSITE OPENING
# ==================================================================

def clean_website_command(text):
    """Convert spoken website commands into a clean search/site name."""
    text = text.strip()

    # Remove common command prefixes.
    text = re.sub(
        r"^(?:please\s+)?(?:open|go\s+to|visit|browse)\s+",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove natural-language suffixes.
    text = re.sub(
        r"\s+(?:website|web\s*site|site)\s*$",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip(" .,!?")


def is_explicit_website_request(text):
    """Return True when the user clearly asked for a website."""
    lowered = text.lower().strip()

    return bool(
        re.match(
            r"^(?:please\s+)?(?:open|go\s+to|visit|browse)\s+.+?\s+(?:website|web\s*site|site)\s*$",
            lowered
        )
        or
        re.match(
            r"^(?:please\s+)?(?:open|go\s+to|visit|browse)\s+https?://",
            lowered
        )
        or
        re.match(
            r"^(?:please\s+)?(?:open|go\s+to|visit|browse)\s+www\.",
            lowered
        )
    )


def looks_like_web_address(value):
    value = value.strip().lower()

    return (
        value.startswith("http://")
        or value.startswith("https://")
        or value.startswith("www.")
        or bool(re.match(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$", value))
    )


def extract_url_from_search_html(html):
    """
    Extract the first external result from DuckDuckGo HTML.
    This avoids hard-coding website names.
    """
    if not html:
        return None

    # DuckDuckGo redirect format:
    # //duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.com
    patterns = [
        r'href=["\'](?:https?:)?//duckduckgo\.com/l/\?uddg=([^&"\']+)',
        r'href=["\'](https?://[^"\']+)["\']'
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, html, flags=re.IGNORECASE):
            raw_url = match.group(1)

            if pattern.startswith(r'href=["\'](?:https'):
                raw_url = unquote(raw_url)
            else:
                raw_url = raw_url.replace("&amp;", "&")

            try:
                parsed = urlparse(raw_url)

                if parsed.scheme in {"http", "https"} and parsed.netloc:
                    # Skip search/social infrastructure pages.
                    blocked_hosts = {
                        "duckduckgo.com",
                        "www.duckduckgo.com",
                        "google.com",
                        "www.google.com",
                        "bing.com",
                        "www.bing.com"
                    }

                    if parsed.netloc.lower() not in blocked_hosts:
                        return raw_url

            except Exception:
                continue

    return None


def resolve_website_url(site_name):
    """
    Resolve a spoken website name to an actual URL.

    Examples:
        amazon -> https://amazon.com
        github -> https://github.com
        openai -> https://openai.com

    For unknown domains, it first performs an Internet search and opens
    the first relevant external result. This keeps website handling generic.
    """

    site_name = clean_website_command(site_name)

    if not site_name:
        return None

    # --------------------------------------------------------------
    # 1. Direct URL
    # --------------------------------------------------------------

    if looks_like_web_address(site_name):

        if site_name.startswith(("http://", "https://")):
            return site_name

        if site_name.startswith("www."):
            return "https://" + site_name

        return "https://" + site_name

    # --------------------------------------------------------------
    # 2. Try common TLDs first.
    # --------------------------------------------------------------

    normalized = re.sub(
        r"\s+",
        "",
        site_name.lower()
    )

    # Only use direct-domain guesses for a single simple site name.
    if re.match(r"^[a-z0-9-]+$", normalized):

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

        for candidate in candidates:

            try:
                response = requests.head(
                    candidate,
                    allow_redirects=True,
                    timeout=4,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    }
                )

                if response.status_code < 500:
                    final_url = response.url

                    if (
                        final_url.startswith("http://")
                        or
                        final_url.startswith("https://")
                    ):
                        return final_url

            except requests.RequestException:
                continue

    # --------------------------------------------------------------
    # 3. Universal search fallback.
    # --------------------------------------------------------------

    try:
        search_url = "https://html.duckduckgo.com/html/"
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

        if response.ok:
            found_url = extract_url_from_search_html(
                response.text
            )

            if found_url:
                return found_url

    except requests.RequestException as e:
        print("Website resolution request error:", e)

    return None


def open_website_universal(command):
    """Open any website requested in natural voice."""
    site_name = clean_website_command(command)

    if not site_name:
        speak("Please tell me which website you want to open.")
        return False

    update_ui(
        "speaking",
        command,
        f"Finding {site_name}..."
    )

    print("Website requested:", site_name)

    resolved_url = resolve_website_url(site_name)

    if not resolved_url:
        # Final fallback: search the requested site in the browser.
        search_url = (
            "https://www.google.com/search?q="
            + quote_plus(
                f"{site_name} official website"
            )
        )

        webbrowser.open(
            search_url,
            new=2
        )

        speak(
            f"I could not identify the exact website, so I searched for {site_name}."
        )

        update_ui(
            "idle",
            command,
            f"Searched for {site_name}."
        )

        return True

    print("Resolved website:", resolved_url)

    webbrowser.open(
        resolved_url,
        new=2
    )

    hostname = urlparse(
        resolved_url
    ).netloc

    speak(
        f"Opening {hostname}."
    )

    update_ui(
        "idle",
        command,
        f"Opened {hostname}."
    )

    return True


# ==================================================================
# 17. COMMAND PROCESSOR
# ==================================================================

def processCommand(command):

    if not command:
        return

    command = command.strip()

    if not command:
        return

    c_clean = command.lower()

    print()
    print("==========================================")
    print("PROCESSING COMMAND:")
    print(command)
    print("==========================================")


    # ==============================================================
    # WINDOWS APPLICATIONS
    # ==============================================================
    # Handles commands such as:
    #   open PowerPoint
    #   open PowerPoint app
    #   open WhatsApp
    #   open WhatsApp app on my laptop
    #   open settings
    #   open calculator
    #   launch Chrome
    #
    # This MUST run before the generic "open website" handler.
    app_open_match = re.match(
        r"^(?:open|launch|start|run)\s+(.+?)\s*$",
        command,
        re.IGNORECASE
    )

    if app_open_match:

        app_query = app_open_match.group(1).strip()
        normalized_query = normalize_app_query(app_query)

        # Don't interpret these as app names when the user clearly wants a URL.
        looks_like_url = (
            normalized_query.startswith("http://")
            or normalized_query.startswith("https://")
            or normalized_query.startswith("www.")
            or ".com" in normalized_query
            or ".in" in normalized_query
            or ".org" in normalized_query
        )

        document_action_words = {
            "write", "create", "make", "document", "email",
            "report", "letter", "application", "save", "put this"
        }

        is_document_command = any(
            word in normalized_query
            for word in document_action_words
        )

        explicit_app_request = (
            "app" in app_query.lower()
            or normalized_query in APP_ALIASES
            or normalized_query in {
                "settings", "windows settings", "system settings"
            }
        )

        if (
            not looks_like_url
            and normalized_query not in {"this", "this app"}
            and not is_document_command
            and not is_explicit_website_request(command)
        ):

            print("Application command detected:", app_query)

            update_ui(
                "speaking",
                command,
                f"Opening {app_query}..."
            )

            success = launch_application(app_query)

            if success:
                update_ui(
                    "idle",
                    command,
                    f"{app_query} opened successfully."
                )
                speak(f"{app_query} opened.")
                return

            # If the user explicitly said "app" or the app is a known alias,
            # report the failure instead of interpreting it as a website.
            if explicit_app_request:
                update_ui(
                    "idle",
                    command,
                    f"I could not find {app_query} on your laptop."
                )
                speak(f"I could not find {app_query} on your laptop.")
                return

    # ==============================================================
    # VS CODE
    # ==============================================================

    if (
        "vs code" in c_clean
        or
        "visual studio code" in c_clean
    ):

        print(
            "VS Code command detected."
        )

        success = open_vscode()

        if success:

            update_ui(
                "idle",
                command,
                "Visual Studio Code opened."
            )

        else:

            update_ui(
                "idle",
                command,
                "I could not open Visual Studio Code."
            )

        return


    # ==============================================================
    # CREATE FOLDER / FILE
    # ==============================================================

    if (
        (
            "create" in c_clean
            or
            "make" in c_clean
        )
        and
        (
            "folder" in c_clean
            or
            "directory" in c_clean
            or
            "file" in c_clean
        )
    ):

        print(
            "Create folder/file command detected."
        )

        success = create_desktop_item(
            command
        )

        if success:

            update_ui(
                "idle",
                command,
                "The folder or file was created successfully."
            )

        else:

            update_ui(
                "idle",
                command,
                "I could not create the folder or file."
            )

        return


    # ==============================================================
    # MICROSOFT WORD
    # ==============================================================

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

        handle_word_command(
            command
        )

        return


    # ==============================================================
    # NOTEPAD
    # ==============================================================

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

        handle_notepad_command(
            command
        )

        return


    # ==============================================================
    # NEWS
    # ==============================================================

    if "news" in c_clean:

        update_ui(
            "speaking",
            command,
            "Fetching real-time news headlines..."
        )

        speak(
            "Fetching latest news headlines."
        )

        headlines = fetch_latest_news()

        if headlines:

            for idx, headline in enumerate(
                headlines,
                1
            ):

                update_ui(
                    "speaking",
                    f"Headline {idx}",
                    headline
                )

                print(
                    f"Headline {idx}:",
                    headline
                )

                speak(
                    headline
                )

            update_ui(
                "idle",
                command,
                "Finished reading news."
            )

        else:

            update_ui(
                "idle",
                command,
                "Sorry, I couldn't fetch live news right now."
            )

            speak(
                "Sorry, I was unable to fetch the news at this moment."
            )

        return


    # ==============================================================
    # PLAY YOUTUBE
    # ==============================================================

    if c_clean.startswith("play "):

        play_youtube(
            command
        )

        return


    # ==============================================================
    # UNIVERSAL WEBSITE
    # ==============================================================

    if is_explicit_website_request(command):

        open_website_universal(
            command
        )

        return


    # Direct URL commands without the word "website".
    if re.match(
        r"^(?:open|go\s+to|visit|browse)\s+(?:https?://|www\.)",
        c_clean,
        re.IGNORECASE
    ):

        open_website_universal(
            command
        )

        return


    # Generic "open <domain>" support.
    if c_clean.startswith("open "):

        site_candidate = command.split(
            " ",
            1
        )[1].strip()

        if looks_like_web_address(site_candidate):

            open_website_universal(
                command
            )

            return


    # ==============================================================
    # NORMAL GEMINI AI
    # ==============================================================

    print(
        "No special command detected."
    )

    print(
        "Sending command to Gemini..."
    )

    update_ui(
        "speaking",
        command,
        "Thinking..."
    )

    output = aiProcess(
        command
    )

    if output:

        update_ui(
            "speaking",
            command,
            output
        )

        print()
        print("==========================================")
        print("FRIDAY:")
        print(output)
        print("==========================================")

        speak(
            output
        )

        update_ui(
            "idle",
            command,
            output
        )

    else:

        update_ui(
            "idle",
            command,
            "Sorry, I could not generate a response."
        )

        speak(
            "Sorry, I could not generate a response."
        )


# ==================================================================
# 18. ASSISTANT LOOP
# ==================================================================

def assistant_loop():

    recognizer = sr.Recognizer()

    recognizer.energy_threshold = 150
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 2.0
    recognizer.phrase_threshold = 0.3
    recognizer.non_speaking_duration = 1.0

    time.sleep(2)

    update_ui(
        "idle",
        "",
        "Initializing Friday..."
    )

    speak(
        "Initializing Friday."
    )

    try:

        with sr.Microphone() as source:

            print(
                "Calibrating ambient noise background..."
            )

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1.5
            )

            print(
                "Energy threshold:",
                recognizer.energy_threshold
            )

    except Exception as e:

        print(
            "Microphone initialization error:",
            e
        )

        update_ui(
            "idle",
            "",
            "Microphone initialization failed."
        )

        speak(
            "Microphone initialization failed."
        )

        return

    print()
    print("==========================================")
    print("FRIDAY IS READY")
    print("Say: Friday")
    print("==========================================")

    update_ui(
        "idle",
        "",
        "Listening for 'Friday'..."
    )

    while True:

        try:

            with sr.Microphone() as source:

                update_ui(
                    "idle",
                    "",
                    "Listening for 'Friday'..."
                )

                print(
                    "Listening for wake word..."
                )

                audio = recognizer.listen(
                    source,
                    timeout=None,
                    phrase_time_limit=8
                )

            word = recognizer.recognize_google(
                audio,
                language="en-IN"
            ).lower().strip()

            print(
                "Heard:",
                word
            )

            if "friday" not in word:
                continue

            print(
                "WAKE WORD DETECTED!"
            )

            update_ui(
                "speaking",
                "Friday",
                "Yes sir, how can I help you?"
            )

            speak(
                "Yes sir, how can I help you?"
            )

            update_ui(
                "listening",
                "",
                "Listening for your command..."
            )

            with sr.Microphone() as source:

                print(
                    "Listening for command..."
                )

                command_audio = recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=60
                )

            command = recognizer.recognize_google(
                command_audio,
                language="en-IN"
            )

            print(
                "Recognized command:",
                command
            )

            processCommand(
                command
            )

        except sr.UnknownValueError:

            print(
                "Speech Recognition could not understand audio."
            )

        except sr.WaitTimeoutError:

            print(
                "Listening timed out waiting for phrase."
            )

        except sr.RequestError as e:

            print(
                "Google Speech Recognition error:",
                e
            )

            time.sleep(2)

        except KeyboardInterrupt:

            print(
                "Friday stopped."
            )

            break

        except Exception as e:

            print(
                "Audio Error:",
                e
            )

            time.sleep(1)


# ==================================================================
# 19. LAUNCH GUI
# ==================================================================

if __name__ == "__main__":

    print(
        "Starting Friday..."
    )

    assistant_thread = threading.Thread(
        target=assistant_loop,
        daemon=True
    )

    assistant_thread.start()

    eel.start(
        "index.html",
        size=(600, 700)
    )