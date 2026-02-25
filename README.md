# 🤖 Aria — AI Virtual Assistant

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Anthropic](https://img.shields.io/badge/Powered%20by-Claude%20AI-orange?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

> A smart, voice-enabled AI desktop assistant powered by Anthropic's Claude API. Talk to it, type to it, and let it open websites and apps for you — all from your terminal.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🎤 Voice Input | Speak your commands using your microphone |
| 🔊 Voice Output | Aria speaks back to you using text-to-speech |
| 🧠 AI-Powered | Answers any question using Claude (Anthropic) |
| 🌐 Open Websites | Say "open YouTube" or "go to GitHub" |
| 🖥️ Open Apps | Launch desktop applications by name |
| 🕐 Time & Date | Instantly tells you the current time and date |
| 💬 Text Chat | Fully works via keyboard — no mic required |

---

## 🖥️ Demo

```
═══════════════════════════════════════════════════════
  🤖  Aria — AI Virtual Assistant
═══════════════════════════════════════════════════════

🤖 Aria: Hello! I'm Aria, your AI assistant. How can I help you?

👤 You: what's the weather like in Tokyo?
🤖 Aria: Tokyo is currently experiencing mild temperatures around 18°C...

👤 You: open youtube
🌐 Opened: https://youtube.com
🤖 Aria: Opening YouTube for you!

👤 You: voice
🎤 Listening... (speak now)
👤 You said: what time is it
🤖 Aria: The current time is 03:45 PM.
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- An [Anthropic API key](https://console.anthropic.com/settings/keys)
- A microphone (optional, for voice input)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ai-virtual-assistant.git
cd ai-virtual-assistant
```

**2. Install dependencies**
```bash
pip install anthropic SpeechRecognition pyttsx3 pyaudio
```

> ⚠️ On Windows, if `pyaudio` fails, install it with:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

**3. Add your API key**

Open `virtual_assistant.py` and replace the API key line:
```python
API_KEY = "your_anthropic_api_key_here"
```

**4. Run it**
```bash
python virtual_assistant.py
```

---

## 🎮 How to Use

| Command | Action |
|---------|--------|
| Type any message | Chat with Aria via text |
| Type `voice` | Switch to voice input mode |
| Say `open youtube` | Opens YouTube in browser |
| Say `open github` | Opens GitHub in browser |
| Say `what time is it` | Tells current time |
| Say `what's today's date` | Tells today's date |
| Type `quit` or `exit` | Close the assistant |

### Supported Quick-Open Websites
`youtube` · `google` · `gmail` · `github` · `wikipedia` · `reddit` · `twitter` · `maps` · `news` · `amazon`

---

## 🛠️ Tech Stack

- **[Python](https://python.org)** — Core language
- **[Anthropic Claude API](https://anthropic.com)** — AI brain
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)** — Voice input (Google Speech API)
- **[pyttsx3](https://pypi.org/project/pyttsx3/)** — Text-to-speech (offline)
- **[PyAudio](https://pypi.org/project/PyAudio/)** — Microphone access

---

## 📁 Project Structure

```
ai-virtual-assistant/
│
├── virtual_assistant.py   # Main application
└── README.md              # Project documentation
```

---

## 🔮 Future Improvements

- [ ] GUI interface with Tkinter or PyQt
- [ ] Spotify / music playback control
- [ ] Smart home integration
- [ ] Custom wake word (e.g., "Hey Aria")
- [ ] Conversation memory between sessions
- [ ] Weather API integration

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@your_username](https://github.com/your_username)
- LinkedIn: [your_linkedin](https://linkedin.com/in/your_linkedin)

---

## 📄 License

This project is licensed under the MIT License — feel free to use and modify it!

---

⭐ **If you found this project useful, please give it a star!** ⭐
