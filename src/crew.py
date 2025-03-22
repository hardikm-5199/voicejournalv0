from crewai import Agent, Crew, Process, Task
from crewai.tools import tool
from typing import List
import openai
import json
from pathlib import Path
import datetime
from dotenv import load_dotenv
from textwrap import dedent
import os

# Load environment variables
load_dotenv()

class VoicejournalCrew:
    """Voice Journal Crew - An AI-powered journaling assistant that processes voice entries"""

    def __init__(self):
        # Create agents
        self.transcriber = Agent(
            role='Audio Transcription Expert',
            goal='Accurately transcribe voice recordings to text',
            backstory='Expert in converting audio to text with high accuracy',
            tools=[self.transcribe_audio],
            verbose=True,
            allow_delegation=False
        )

        self.analyzer = Agent(
            role='Emotional Analysis Expert',
            goal='Analyze journal entries for emotions, themes, and insights',
            backstory='Skilled psychologist specializing in emotional analysis and personal growth',
            tools=[self.analyze_entry],
            verbose=True,
            allow_delegation=False
        )

        self.reflection_guide = Agent(
            role='Personal Development Coach',
            goal='Generate meaningful questions for deeper self-reflection',
            backstory='Expert in personal development and introspective questioning',
            tools=[self.generate_reflection_questions],
            verbose=True,
            allow_delegation=False
        )

    def crew(self) -> Crew:
        """Creates the Voice Journal crew"""
        tasks = [
            Task(
                description=dedent(f"""
                    Transcribe the voice journal entry to text.
                    You will receive an audio file path.
                    Use the transcribe_audio tool to convert it to text.
                """),
                agent=self.transcriber,
                expected_output="Transcribed text of the journal entry"
            ),
            Task(
                description=dedent(f"""
                    Analyze the journal entry for emotions and themes.
                    Use the analyze_entry tool with the transcribed text from the previous task.
                """),
                agent=self.analyzer,
                expected_output="Analysis of emotions, themes, and insights"
            ),
            Task(
                description=dedent(f"""
                    Generate thoughtful reflection questions.
                    Use the generate_reflection_questions tool with the analysis from the previous task.
                """),
                agent=self.reflection_guide,
                expected_output="List of reflection questions"
            )
        ]

        return Crew(
            agents=[self.transcriber, self.analyzer, self.reflection_guide],
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )

    # Tool functions
    @staticmethod
    @tool("Transcribe audio")
    def transcribe_audio(audio_file: str) -> str:
        """Transcribe audio using OpenAI Whisper"""
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        try:
            with open(audio_file, "rb") as file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=file
                )
            return transcript.text
        except Exception as e:
            return f"Error transcribing audio: {str(e)}"

    @staticmethod
    @tool("Analyze journal entry")
    def analyze_entry(entry_text: str) -> str:
        """Analyze journal entry for emotions and insights"""
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = f"""
        Analyze the following journal entry and provide:
        1. Main emotions detected
        2. Key themes or topics
        3. Potential insights or areas for growth
        
        Entry: {entry_text}
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    @staticmethod
    @tool("Generate reflection questions")
    def generate_reflection_questions(analysis: str) -> List[str]:
        """Generate reflection questions based on the analysis"""
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = f"""
        Based on this analysis of the journal entry, generate 3 thoughtful
        questions for deeper reflection:
        
        Analysis: {analysis}
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.split("\n")