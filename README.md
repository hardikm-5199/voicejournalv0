# Voice Journal AI

Note: This is a failed attempt :( 

keeping it here anyway

An AI-powered voice journaling assistant built with AgentStack that helps you process and reflect on your daily thoughts and experiences.

## Features

- Voice-based journaling
- Automatic transcription using OpenAI Whisper
- Emotional analysis and theme detection
- Personalized reflection questions
- Persistent storage of journal entries

## Setup

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Run the voice journal:
```bash
python src/main.py
```

2. The AI crew will:
   - Transcribe your voice recording
   - Analyze your journal entry for emotions and themes
   - Generate thoughtful reflection questions
   - Save your entries for future reference

## Project Structure

- `src/crew.py`: Main AgentStack crew implementation with agents
- `src/main.py`: CLI interface and entry point
- `data/`: Directory for storing journal entries

## Requirements

- Python 3.8+
- OpenAI API key
- Microphone for voice recording

## Note

This is a basic implementation. Make sure you have a working microphone and proper audio input setup for the best experience.
