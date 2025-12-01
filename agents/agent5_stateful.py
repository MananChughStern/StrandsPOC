"""
Agent 5: Persists memory using FileSessionManager to show agents updating state using tool calls.
"""

from strands import Agent, tool
from strands.agent.state import AgentState
from strands.session import FileSessionManager
import json
from pathlib import Path
from datetime import datetime

def demo_tool_based_state():
    print("DEMO 1: STATE MUTATION USING TOOLS")

    @tool(context=True)
    def update_task_count(task_count: int, tool_context) -> str:
        """Updates number of completed tasks for user

        Args:
            task_count: New total no. of completed tasks
            tool_context: Strands context with agent state

        Returns:
            Confirmation message with old and new values
        """
        state = tool_context.agent.state
        old_count = state.get("tasks_completed") or 0

        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "update_task_count",
            "old_value": old_count,
            "new_value": task_count
        }

        audit_log = state.get("audit_log") or []
        audit_log.append(audit_entry)

        state.set("tasks_completed", task_count)
        state.set("audit_log", audit_log)
        state.set("last_updated", datetime.now().isoformat())

        return f"Updated task count: {old_count} → {task_count}"

    @tool(context=True)
    def add_task(task_name: str, category: str, tool_context) -> str:
        """Adding completed task to user task list

        Args:
            task_name: Name/description of completed task
            category: Category (docs, bugs, review, meeting, other)
            tool_context: Strands context with agent state

        Returns:
            Confirmation with task details
        """
        state = tool_context.agent.state

        tasks = state.get("task_list") or []
        task_entry = {
            "name": task_name,
            "category": category,
            "completed_at": datetime.now().isoformat()
        }
        tasks.append(task_entry)

        audit_log = state.get("audit_log") or []
        audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": "add_task",
            "task_name": task_name,
            "category": category
        })

        state.set("task_list", tasks)
        state.set("tasks_completed", len(tasks))
        state.set("audit_log", audit_log)
        state.set("last_updated", datetime.now().isoformat())

        return f"Added task: '{task_name}' [{category}]. Total tasks: {len(tasks)}"

    @tool(context=True)
    def get_productivity_summary(tool_context) -> str:
        """get summary of user productivity metrics

        Args:
            tool_context: Strands context with agent state

        Returns:
            Formatted productivity summary
        """
        state = tool_context.agent.state

        tasks = state.get("task_list") or []
        total = len(tasks)

        categories = {}
        for task in tasks:
            cat = task.get("category", "other")
            categories[cat] = categories.get(cat, 0) + 1

        summary = f"Total tasks completed: {total}\n"
        if categories:
            summary += "By category:\n"
            for cat, count in sorted(categories.items()):
                summary += f"  - {cat}: {count}\n"

        return summary

    initial_state = AgentState({
        "user_name": "demo_user",
        "tasks_completed": 0,
        "task_list": [],
        "audit_log": [],
        "last_updated": None
    })

    agent = Agent(
        state=initial_state,
        tools=[update_task_count, add_task, get_productivity_summary],
        system_prompt="""You are a productivity tracking assistant.

        IMPORTANT: You must use the provided tools to track tasks:
        - Use 'add_task' when user mentions completing a task
        - Use 'get_productivity_summary' when user asks about their progress
        - Use 'update_task_count' only for bulk count corrections
        
        Categories for tasks: docs, bugs, review, meeting, other
        
        Always confirm what you've logged after using a tool."""
    )

    print("\nInitial state:")
    print(json.dumps(agent.state.get(), indent=2))

    print("\n[User reports completed work]")
    response = agent("I finished writing the API docs, fixed the login bug, and did 2 code reviews today.")
    print(f"Agent: {response}")

    print("\nState after tool-based updates:")
    print(json.dumps(agent.state.get(), indent=2))

    print("\n[User asks for summary]")
    response2 = agent("How am I doing today? Give me a summary.")
    print(f"Agent: {response2}")

    print("\n[Audit log shows all state changes]")
    print(f"Audit entries: {len(agent.state.get('audit_log') or [])}")
    print()

def demo_session_persistence():
    print("DEMO 2: SESSION PERSISTENCE")

    session_dir = Path("./sessions")
    session_dir.mkdir(exist_ok=True)

    session_id = f"user_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    session_manager = FileSessionManager(
        session_id=session_id,
        storage_dir=str(session_dir)
    )

    print(f"\nSession ID: {session_id}")
    print(f"Storage: {session_dir} (local)")

    agent = Agent(
        session_manager=session_manager,
        system_prompt="""You are a helpful assistant who remembers user preferences and context.
    Track what users tell you about their work, preferences, and goals."""
    )

    print("\n[Session - Turn 1]")
    r1 = agent("I'm working on the Q4 product launch. My focus areas are AI features and performance.")
    print(f"Agent: {r1}")

    print("\n[Session - Turn 2]")
    r2 = agent("What am I working on?")
    print(f"Agent: {r2}")

    print("\n--- Simulating application restart ---")

    restored_session_manager = FileSessionManager(
        session_id=session_id,
        storage_dir=str(session_dir)
    )

    restored_agent = Agent(
        session_manager=restored_session_manager,
        system_prompt="""You are a helpful assistant who remembers user preferences and context.
    Track what users tell you about their work, preferences, and goals."""
    )

    print("\n[Session restored - Turn 3]")
    r3 = restored_agent("Do you remember what I'm working on and my focus areas?")
    print(f"Agent: {r3}")

    session_files = list(session_dir.glob('**/*.json'))
    print(f"\nSession persisted: {len(session_files)} files")
    print("For non-local deployments, S3SessionManager or AgentCore Memory would handle this automatically\n")

def demo_multi_agent():
    print("DEMO 3: MULTI-AGENT ORCHESTRATION")

    @tool(context=True)
    def log_task(task: str, priority: str, tool_context) -> str:
        """Logs a task with priority level

        Args:
            task: Task description
            priority: Priority (high, medium, low)
            tool_context: Agent context

        Returns:
            Confirmation message
        """
        state = tool_context.agent.state
        tasks = state.get("tasks") or []
        tasks.append({"task": task, "priority": priority, "status": "pending"})
        state.set("tasks", tasks)
        return f"Logged: {task} (priority: {priority})"

    task_tracker = Agent(
        state=AgentState({"tasks": [], "agent_name": "TaskTracker"}),
        tools=[log_task],
        system_prompt="""You are a task tracking specialist.
        Use log_task to record tasks users mention.
        Assign priority based on urgency keywords (urgent/asap = high, normal = medium, whenever = low)."""
    )

    @tool(context=True)
    def record_completion(item: str, tool_context) -> str:
        """Records completed item

        Args:
            item: What was completed
            tool_context: Agent context

        Returns:
            Confirmation
        """
        state = tool_context.agent.state
        completed = state.get("completed") or []
        completed.append({"item": item, "completed_at": datetime.now().isoformat()})
        state.set("completed", completed)
        return f"Recorded completion: {item}"

    progress_reporter = Agent(
        state=AgentState({"completed": [], "agent_name": "ProgressReporter"}),
        tools=[record_completion],
        system_prompt="""You are a progress tracking specialist.
        Use record_completion to log completed work items.
        Extract specific deliverables from user messages."""
    )

    @tool
    def delegate_to_task_tracker(message: str) -> str:
        """delegates task-related requests to TaskTracker agent

        Args:
            message: The task-related message to process

        Returns:
            TaskTracker's response
        """
        response = task_tracker(message)
        return f"[TaskTracker]: {response}"

    @tool
    def delegate_to_progress_reporter(message: str) -> str:
        """Delegates progress related requests to ProgressReporter

        Args:
            message: progress-related message to process

        Returns:
            ProgressReporter's response
        """
        response = progress_reporter(message)
        return f"[ProgressReporter]: {response}"

    coordinator = Agent(
        tools=[delegate_to_task_tracker, delegate_to_progress_reporter],
        system_prompt="""You are a productivity coordinator managing specialist agents.

        For task/todo items, delegate_to_task_tracker
        For completed work/progress updates, delegate_to_progress_reporter
        
        You can call multiple specialists for complex requests.
        Synthesize their responses into a coherent summary for the user."""
    )

    print("\n[Multi-agent request: mixed tasks and completions]")
    response = coordinator("""
    Today I need to:
    - Review the PR for auth service (urgent)
    - Update documentation (whenever I have time)
    
    I already completed:
    - Fix the database connection bug
    - Deploy v2.1 to staging
    """)
    print(f"Coordinator: {response}")

    print("\n[Specialist states after delegation]")
    print(f"TaskTracker state: {json.dumps(task_tracker.state.get(), indent=2)}")
    print(f"ProgressReporter state: {json.dumps(progress_reporter.state.get(), indent=2)}")

if __name__ == "__main__":
    demo_tool_based_state()

    demo_session_persistence()

    demo_multi_agent()
