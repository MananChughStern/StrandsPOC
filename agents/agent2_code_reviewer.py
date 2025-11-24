"""
Agent 2: Code Reviewer Agent with memory, self-improvement, iterative refinement
"""

from strands import Agent, tool
from typing import List, Dict
import json


@tool
def save_review_learnings(insight: str, code_pattern: str, recommendation: str) -> str:
    """Save learnings from code reviews to improve future reviews.

    Args:
        insight: What agent learned from this review
        code_pattern: Code pattern this applies to
        recommendation: Improved recommendation for future

    Returns:
        Confirmation message
    """
    learnings = {
        "insight": insight,
        "pattern": code_pattern,
        "recommendation": recommendation
    }

    with open("../review_learnings.json", "a") as f:
        f.write(json.dumps(learnings) + "\n")

    return f"Learning saved: {insight[:50]}..."


@tool
def get_past_learnings() -> List[Dict]:
    """Get previous CR learnings for current review"""
    try:
        with open("../review_learnings.json", "r") as f:
            learnings = [json.loads(line) for line in f]
            return learnings[-5:]  # Last 5 learnings
    except FileNotFoundError:
        return []

reviewer = Agent(
    tools=[save_review_learnings, get_past_learnings],
    system_prompt="""You are an autonomous code reviewer that improves over time.

    For each code review:
    1. Check past learnings to see if you've reviewed similar patterns
    2. Provide detailed, actionable feedback
    3. Rate the code quality (1-10)
    4. After each review, reflect: What did you learn? How can you improve?
    5. Save your learnings for future reviews
    
    Your reviews should get better over time by building on past insights."""
)


def test_autonomous_learning():
    code1 = """
    def calculate_total(items):
        total = 0
        for item in items:
            total = total + item['price']
        return total
    """

    print("REVIEW 1: First review (no prior learnings)")
    response1 = reviewer(f"Review this Python code:\n{code1}")
    print(response1)

    code2 = """
    def sum_values(data):
        result = 0
        for entry in data:
            result += entry['value']
        return result
    """

    print("REVIEW 2: Similar review but should get prior learning")
    response2 = reviewer(f"Review this Python code:\n{code2}")
    print(response2)

    code3 = """
    def process_data(items):
        return [item['price'] * 1.1 for item in items if item['active']]
    """

    print("REVIEW 3: More advanced review")
    response3 = reviewer(f"Review this Python code:\n{code3}")
    print(response3)

    print("AGENT SELF-REFLECTION")
    reflection = reviewer("Reflect on your code reviews. How has your reviewing improved? What patterns have you learned to recognize?")
    print(reflection)

if __name__ == "__main__":
    test_autonomous_learning()
