"""
🤖 AI Virtual Assistant
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Features:
  ✅ Voice Input (speech recognition)
  ✅ Voice Output (text-to-speech)
  ✅ Text Chat Interface
  ✅ AI-powered answers (Claude API)
  ✅ Open websites & apps

Requirements:
  pip install anthropic SpeechRecognition pyttsx3 pyaudio

Usage:
  python virtual_assistant.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import sys
import webbrowser
import subprocess
import platform
import datetime
import threading

# ── Try importing optional libraries ──────────────────────────────────────────
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("⚠️  'anthropic' not installed. Run: pip install anthropic")

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️  'SpeechRecognition' not installed. Run: pip install SpeechRecognition pyaudio")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  'pyttsx3' not installed. Run: pip install pyttsx3")


# ── Configuration ──────────────────────────────────────────────────────────────
ASSISTANT_NAME = "Aria"
API_KEY = "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"

SYSTEM_PROMPT = f"""You are {ASSISTANT_NAME}, a helpful, friendly, and concise desktop voice assistant.
Keep your answers short and clear (2-4 sentences max unless asked for detail).
When the user asks to open a website or app, reply with:
  OPEN_URL:<url>  — to open a website
  OPEN_APP:<app>  — to open an application
You can combine a brief spoken reply with one of these commands on a new line.
Today's date is {datetime.date.today().strftime('%A, %B %d, %Y')}."""

WEBSITES = {
    "youtube":   "https://youtube.com",
    "google":    "https://google.com",
    "gmail":     "https://mail.google.com",
    "github":    "https://github.com",
    "wikipedia": "https://wikipedia.org",
    "reddit":    "https://reddit.com",
    "twitter":   "https://twitter.com",
    "x":         "https://twitter.com",
    "maps":      "https://maps.google.com",
    "news":      "https://news.google.com",
    "amazon":    "https://amazon.com",
}


# ── Text-to-Speech ─────────────────────────────────────────────────────────────
class Speaker:
    def __init__(self):
        self.engine = None
        if TTS_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 175)
                voices = self.engine.getProperty("voices")
                # Prefer a female voice if available
                for v in voices:
                    if "female" in v.name.lower() or "zira" in v.name.lower() or "samantha" in v.name.lower():
                        self.engine.setProperty("voice", v.id)
                        break
            except Exception as e:
                print(f"⚠️  TTS init error: {e}")
                self.engine = None

    def speak(self, text: str):
        print(f"\n🤖 {ASSISTANT_NAME}: {text}")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass  # Silent fallback to text-only


# ── Speech Recognition ─────────────────────────────────────────────────────────
class Listener:
    def __init__(self):
        self.recognizer = None
        self.mic = None
        if SPEECH_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
                self.mic = sr.Microphone()
                # Calibrate once at startup
                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
            except Exception as e:
                print(f"⚠️  Microphone init error: {e}")
                self.recognizer = None

    def listen(self) -> str | None:
        if not self.recognizer or not self.mic:
            return None
        print("🎤 Listening... (speak now)")
        try:
            with self.mic as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("⌛ No speech detected.")
            return None
        except sr.UnknownValueError:
            print("🔇 Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"⚠️  Speech recognition error: {e}")
            return None


# ── AI Brain ───────────────────────────────────────────────────────────────────
class Brain:
    def __init__(self):
        self.client = None
        self.history = []
        if ANTHROPIC_AVAILABLE and API_KEY:
            self.client = anthropic.Anthropic(api_key=API_KEY)
        elif ANTHROPIC_AVAILABLE and not API_KEY:
            print("⚠️  No ANTHROPIC_API_KEY found. Set it as an environment variable or in the script.")

    def ask(self, user_input: str) -> str:
        # Local quick-replies (no API needed)
        low = user_input.lower().strip()
        if any(w in low for w in ["hello", "hi", "hey"]):
            return f"Hey there! I'm {ASSISTANT_NAME}. How can I help you today?"
        if "time" in low and "date" not in low:
            return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
        if "date" in low or "today" in low:
            return f"Today is {datetime.date.today().strftime('%A, %B %d, %Y')}."
        if any(w in low for w in ["bye", "goodbye", "exit", "quit", "stop"]):
            return "QUIT"

        # Check for direct website open command
        for site, url in WEBSITES.items():
            if f"open {site}" in low or f"go to {site}" in low:
                return f"Opening {site} for you!\nOPEN_URL:{url}"

        # Fall back to AI
        if not self.client:
            return "I don't have an AI brain connected right now. Please set your ANTHROPIC_API_KEY."

        self.history.append({"role": "user", "content": user_input})
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=512,
                system=SYSTEM_PROMPT,
                messages=self.history,
            )
            reply = response.content[0].text
            self.history.append({"role": "assistant", "content": reply})
            # Keep history manageable
            if len(self.history) > 20:
                self.history = self.history[-20:]
            return reply
        except anthropic.AuthenticationError:
            return "Authentication failed. Please check your ANTHROPIC_API_KEY."
        except Exception as e:
            return f"Oops, I ran into an error: {e}"


# ── Action Handler ─────────────────────────────────────────────────────────────
def handle_actions(response: str, speaker: Speaker) -> str:
    """
    Parse assistant response for special commands like OPEN_URL or OPEN_APP,
    execute them, and return the clean spoken text.
    """
    lines = response.strip().split("\n")
    spoken_lines = []

    for line in lines:
        if line.startswith("OPEN_URL:"):
            url = line.replace("OPEN_URL:", "").strip()
            try:
                webbrowser.open(url)
                print(f"🌐 Opened: {url}")
            except Exception as e:
                print(f"⚠️  Could not open URL: {e}")

        elif line.startswith("OPEN_APP:"):
            app = line.replace("OPEN_APP:", "").strip()
            _open_app(app)

        elif line == "QUIT":
            speaker.speak("Goodbye! Have a great day!")
            sys.exit(0)

        else:
            spoken_lines.append(line)

    return " ".join(spoken_lines).strip()


def _open_app(app_name: str):
    """Attempt to open a desktop application cross-platform."""
    os_name = platform.system()
    app_lower = app_name.lower()
    print(f"🖥️  Trying to open app: {app_name}")

    try:
        if os_name == "Windows":
            os.startfile(app_name)
        elif os_name == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", app_name])
        else:  # Linux
            subprocess.Popen([app_lower])
    except Exception as e:
        print(f"⚠️  Could not open '{app_name}': {e}")


# ── Main Loop ──────────────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print(f"  🤖  {ASSISTANT_NAME} — AI Virtual Assistant")
    print("=" * 55)
    print("  Commands:")
    print("    • Type your message and press Enter")
    print("    • Type 'voice' to speak instead of typing")
    print("    • Type 'quit' or 'exit' to stop")
    print("=" * 55)

    speaker = Speaker()
    listener = Listener()
    brain = Brain()

    speaker.speak(f"Hello! I'm {ASSISTANT_NAME}, your AI assistant. How can I help you?")

    while True:
        try:
            print()
            mode = input("👤 You (type or 'voice'): ").strip()

            if not mode:
                continue

            if mode.lower() == "voice":
                user_input = listener.listen()
                if not user_input:
                    print("💬 (Could not capture voice. Try typing instead.)")
                    continue
            else:
                user_input = mode

            if not user_input:
                continue

            # Get AI response
            raw_response = brain.ask(user_input)

            # Handle any commands embedded in the response
            clean_response = handle_actions(raw_response, speaker)

            # Speak & display (if there's text to say)
            if clean_response:
                speaker.speak(clean_response)

        except KeyboardInterrupt:
            speaker.speak("Goodbye!")
            print("\n👋 See you later!")
            break
        except EOFError:
            break


if __name__ == "__main__":
    main()
