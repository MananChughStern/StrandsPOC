"""
Agent 6: Tool Orchestrator showing automatic tool selection and usage of multiple tools sequentially in a single request
"""

from strands import Agent, tool
from strands_tools import calculator

@tool
def company_valuation(revenue: float, growth_rate: float, industry: str) -> dict:
    """Estimate company valuation using revenue multiples

    Used for valuing companies based on their revenue and growth.

    Args:
        revenue: Annual revenue in millions of dollars
        growth_rate: Year-over-year growth percentage (Eg. it would be 80 for 80%)
        industry: Industry sector like saas, ecommerce or fintech

    Returns:
        Valuation estimate with methodology explained
    """
    multiples = {
        "saas": {"base": 10, "high_growth_bonus": 5},
        "ecommerce": {"base": 3, "high_growth_bonus": 2},
        "fintech": {"base": 8, "high_growth_bonus": 4}
    }

    mult = multiples.get(industry.lower(), multiples["saas"])
    base_multiple = mult["base"]

    if growth_rate > 50:
        base_multiple += mult["high_growth_bonus"]
    elif growth_rate > 25:
        base_multiple += mult["high_growth_bonus"] * 0.5

    valuation = revenue * base_multiple

    return {
        "revenue_millions": revenue,
        "growth_rate_percent": growth_rate,
        "industry": industry,
        "revenue_multiple": round(base_multiple, 1),
        "estimated_valuation_millions": round(valuation, 1),
        "valuation_range": f"${valuation*0.8:.1f}M - ${valuation*1.2:.1f}M",
        "methodology": f"Used {base_multiple}x revenue multiple for {industry} with {growth_rate}% growth"
    }


@tool
def market_sizing(tam: float, target_share: float, years: int) -> dict:
    """Calculate addressable market and revenue projections.

    Used for market analysis and revenue forecasting.

    Args:
        tam: Total addressable market (in millions)
        target_share: target market share percentage (Eg. it would be 5 for 5%)
        years: no. of years to project

    Returns:
        Market size analysis with projections
    """
    target_revenue = tam * (target_share / 100)

    # assuming linear growth to target
    projections = []
    for year in range(1, years + 1):
        year_revenue = target_revenue * (year / years)
        projections.append({
            "year": year,
            "revenue_millions": round(year_revenue, 2),
            "market_share_percent": round((year / years) * target_share, 2)
        })

    return {
        "total_addressable_market_millions": tam,
        "target_market_share_percent": target_share,
        "target_revenue_millions": round(target_revenue, 2),
        "years_to_target": years,
        "year_by_year_projections": projections
    }


def test_tool_selection():
    """To check that it selects appropriate tools based on query type."""

    agent = Agent(
        tools=[calculator, company_valuation, market_sizing],
        system_prompt="""You are a business analyst assistant with multiple tools.

        Available tools:
        - calculator: For basic math
        - company_valuation: For estimating company valuations based on revenue multples
        - market_sizing: For market analysis and revenue projections
        
        Choose the most appropriate tool for each question. Explain your reasoning clearly."""
    )

    test_queries = [
        {
            "query": "What's 15% of $2.4 million?",
            "expected_tool": "calculator",
            "note": "Basic arithmetic"
        },

        {
            "query": "Estimate the valuation of a SaaS company with $50M annual revenue growing at 80% year-over-year",
            "expected_tool": "company_valuation",
            "note": "Company valuation"
        },
        {
            "query": "If a company is valued at $400M with $40M revenue, what's the revenue multiple?",
            "expected_tool": "calculator",
            "note": "Calculate existing multiple"
        },

        {
            "query": "If the AI agent market is $5B and we want to capture 3% over 4 years, what's our revenue projection?",
            "expected_tool": "market_sizing",
            "note": "Market analysis"
        },
        {
            "query": "A fintech startup has $20M revenue growing 60% annually in a $10B market. Estimate their valuation and if they captured 2% market share, what would that revenue be?",
            "expected_tool": "multiple",
            "note": "Compound analysis"
        }
    ]

    print("MULTI-TOOL AGENT: DYNAMIC TOOL SELECTION TEST")

    for i, test in enumerate(test_queries, 1):
        print(f"TEST {i}: {test['note']}")
        print(f"Expected tool: {test['expected_tool']}")
        print(f"\nQuery: {test['query']}")

        response = agent(test['query'])
        print(f"\nAgent Response:\n{response}")

    print("TOOL SELECTION TEST COMPLETE")

def test_tool_composition():
    """Test agent's ability to compose multiple tools for complex queries."""

    agent = Agent(
        tools=[calculator, company_valuation, market_sizing],
        system_prompt="""You are a business analyst assistant,

        For complex questions requiring multiple calculations:
        1. Break down the problem
        2. Use appropriate tools in sequence
        3. Show your work step-by-step
        4. Synthesize results into a clear conclusion"""
    )

    print("TOOL COMPOSITION TEST")

    complex_query = """
    Analyze this scenario:
    
    Company: AI Infrastructure Startup
    - Current revenue: $30M annully
    - Growth rate: 100% YoY
    - Industry: Saas
    - Market: $8B TAM
    
    Questions:
    1. What is their estimated valuation?
    2. If they maintain this growth and capture 4% market share in 5 years, what wold their revenue be?
    3. What would their valuation be at that point (assuming growth slows to 30%)?
    """

    print(f"\nComplex Scenario:\n{complex_query}")

    response = agent(complex_query)
    print(f"\nAgent Analysis:\n{response}")


if __name__ == "__main__":

    test_tool_selection()

    test_tool_composition()
