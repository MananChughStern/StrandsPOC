"""
First Strands Agent - Hello World
Tests basic Strands functionality
"""

from strands import Agent

def main():
    # Create agent with default settings (uses AWS Bedrock + Claude 4)
    agent = Agent()

    # Ask a question
    response = agent("What makes a good AI agent framework?")

    print("="*60)
    print("AGENT RESPONSE:")
    print("="*60)
    print(response)
    print("="*60)


if __name__ == "__main__":
    main()