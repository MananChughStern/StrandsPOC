"""
Agent 1: we provide a goal and a tool and the model figures out when to use which
tool on its own to solve the problem.
"""

from strands import Agent, tool
from strands_tools import calculator


@tool
def pm_metric_calculator(daily_active_users: int, monthly_active_users: int) -> dict:
    if monthly_active_users == 0:
        return {"error": "MAU cannot be zero"}

    dau_mau = daily_active_users / monthly_active_users

    return {
        "dau": daily_active_users,
        "mau": monthly_active_users,
        "dau_mau_ratio": round(dau_mau, 3),
        "stickiness_percentage": round(dau_mau * 100, 1),
        "interpretation": (
            "Excellent (>60%)" if dau_mau > 0.6
            else "Good (40-60%)" if dau_mau > 0.4
            else "Needs improvement (<40%)"
        )
    }


def main():
    agent = Agent(tools=[calculator, pm_metric_calculator])

    test_queries = [
        "What's 234 multiplied by 567?",
        "Calculate DAU/MAU for a product with 50,000 daily users and 200,000 monthly users",
        "Compare stickiness: Product A has 60k DAU and 150k MAU, Product B has 40k DAU and 80k MAU"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"QUERY {i}: {query}")
        response = agent(query)
        print(response)

    print("\n")


if __name__ == "__main__":
    main()