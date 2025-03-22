from agentstack import Agent, AgentStack
import openai
import json
import datetime
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class VoiceJournalAgent(Agent):
    def __init__(self):
        super().__init__(name="Voice Journal Agent")
        self.journal_file = Path("data/journal_entries.json")
        self.journal_file.parent.mkdir(exist_ok=True)
        if not self.journal_file.exists():
            self.journal_file.write_text(json.dumps({"entries": []}))

    async def transcribe_audio(self, audio_file):
        """Transcribe audio using OpenAI Whisper"""
        try:
            with open(audio_file, "rb") as file:
                transcript = await client.audio.transcriptions.create(
                    model="whisper-1",
                    file=file
                )
            return transcript.text
        except Exception as e:
            return f"Error transcribing audio: {str(e)}"

    async def analyze_entry(self, entry_text):
        """Analyze journal entry for emotions and insights"""
        prompt = f"""
        Analyze the following journal entry and provide:
        1. Main emotions detected
        2. Key themes or topics
        3. Potential insights or questions for reflection
        
        Entry: {entry_text}
        """
        
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    async def save_entry(self, entry_text, analysis):
        """Save journal entry and analysis to file"""
        entries = json.loads(self.journal_file.read_text())
        new_entry = {
            "date": datetime.datetime.now().isoformat(),
            "entry": entry_text,
            "analysis": analysis
        }
        entries["entries"].append(new_entry)
        self.journal_file.write_text(json.dumps(entries, indent=2))

    async def generate_reflection_questions(self, analysis):
        """Generate reflection questions based on the analysis"""
        prompt = f"""
        Based on this analysis of the journal entry, generate 3 thoughtful
        questions for deeper reflection:
        
        Analysis: {analysis}
        """
        
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    async def process_journal_entry(self, audio_file):
        """Main method to process a journal entry"""
        # Transcribe audio
        entry_text = await self.transcribe_audio(audio_file)
        
        # Analyze entry
        analysis = await self.analyze_entry(entry_text)
        
        # Save entry and analysis
        await self.save_entry(entry_text, analysis)
        
        # Generate reflection questions
        questions = await self.generate_reflection_questions(analysis)
        
        return {
            "entry": entry_text,
            "analysis": analysis,
            "reflection_questions": questions
        }

# Initialize AgentStack
stack = AgentStack()
journal_agent = VoiceJournalAgent()
stack.add_agent(journal_agent)
