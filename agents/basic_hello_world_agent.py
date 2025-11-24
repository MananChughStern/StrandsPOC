"""
Simplest 2-line agent that just asks a question and gets a response successfully with default bedrock model
"""

from strands import Agent

def main():
    agent = Agent()
    response = agent("What makes a good AI agent framework?")

    print("AGENT RESPONSE:")
    print(response)

if __name__ == "__main__":
    main()