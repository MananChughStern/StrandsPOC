"""
Agent 4: Streaming agent with context using streaming responses, async streaming, context management
"""

from strands import Agent
from strands.models import BedrockModel

def create_streaming_agent():
    """agent with streaming enabled via model config"""
    streaming_model = BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        temperature=0.7,
        streaming=True
    )
    agent = Agent(
        model=streaming_model,
        system_prompt="""You are a helpful assistant with conversational memory.

        When responding:
        - Reference previous context naturally
        - Build on earlier answers
        - Understand pronouns like "it" or "that" from context
        - Maintain coherent conversation flow"""
    )
    return agent

def demo_streaming_with_default_handler():
    """Streaming with default PrintingCallbackHandler"""

    agent = create_streaming_agent()
    print("\nDEMO 1: DEFAULT STREAMING\n")

    # conversation with context
    queries = [
        "Explain agentic AI in 3 sentences.",
        "What are the main challenges with it?",
        "How do those compare to traditional ML?",
        "Give me a real-world example."
    ]

    for i, query in enumerate(queries, 1):
        print(f"\nQ{i}: {query}\n")
        # it automatically streams with default handler
        result = agent(query)
        # result is auto-displayed by streaming

async def demo_async_streaming():
    """Async streaming for prod use"""

    from strands.handlers import null_callback_handler

    print("\nDEMO 2: ASYNC STREAMING\n")
    # no default handler for manual control
    model = BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        streaming=True
    )
    agent = Agent(
        model=model,
        callback_handler=null_callback_handler  # no auto-printing
    )
    query = "Explain why streaming is important for production UX"
    print(f"Query: {query}\n")
    print("Response: ", end="", flush=True)

    # stream_async for async iteration
    async for event in agent.stream_async(query):
        if "data" in event:
            # streams chunks of text as they arrive
            print(event["data"], end="", flush=True)
        elif "current_tool_use" in event:
            tool = event.get("current_tool_use", {})
            if tool.get("name"):
                print(f"\n[Tool: {tool['name']}]", flush=True)

    print("\n\n")
    print("Full control for production streaming endpoints")

def demo_custom_callback():
    """custom callback handler for streaming"""

    print("\nDEMO 3: CUSTOM CALLBACKS")

    # logging instead of printing
    logged_chunks = []
    def custom_callback(**kwargs):
        """custom callback that for capturing streaming data"""
        if "data" in kwargs:
            chunk = kwargs["data"]
            logged_chunks.append(chunk)
            print(chunk, end="", flush=True)
        elif "current_tool_use" in kwargs:
            tool = kwargs["current_tool_use"]
            if tool.get("name"):
                print(f"\n[Tool: {tool['name']}]\n", flush=True)

    model = BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        streaming=True
    )
    agent = Agent(
        model=model,
        callback_handler=custom_callback
    )
    print("CUSTOM CALLBACK HANDLER")
    query = "Explain the technical benefits of streaming API responses instead of blocking"
    print(f"Query: {query}\n")
    print("Response: ", end="", flush=True)

    result = agent(query)

    print(f"\n\nCaptured {len(logged_chunks)} chunks for monitoring/analytics\n")
    print("Chunks enable cost tracking and production monitoring")

def demo_context_management():
    """context preservation across conversation."""

    agent = create_streaming_agent()

    print("\nDEMO 4: CONTEXT MANAGEMENT TEST")
    # query1 establishes context
    print("\n[Query 1] Establishing context about quantum computing")
    response1 = agent("What is quantum computing?")
    # responses are printed automatically with streaming

    print("\n[Query 2] Using 'it' - tests context")
    response2 = agent("What are the main challenges with it?")

    print("\n[Query 3] Using 'those' - tests deeper context")
    response3 = agent("How do those compare to classical computing challenges?")
    print("Context preserved across 3-turn conversation")

if __name__ == "__main__":
    demo_streaming_with_default_handler()

    import asyncio
    asyncio.run(demo_async_streaming())

    demo_custom_callback()

    demo_context_management()