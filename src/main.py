#!/usr/bin/env python
import sys
from crew import VoicejournalCrew
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run(audio_file):
    """
    Run the agent.
    """
    crew = VoicejournalCrew()
    instance = crew.crew()
    instance.kickoff(inputs={"audio_file": audio_file})


def train():
    """
    Train the crew for a given number of iterations.
    """
    pass


def replay():
    """
    Replay the crew execution from a specific task.
    """
    pass


def test():
    """
    Test the crew execution and returns the results.
    """
    pass


def main():
    """
    Main function.
    """
    if len(sys.argv) < 2:
        print("Please provide an audio file path")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    run(audio_file)


if __name__ == '__main__':
    main()