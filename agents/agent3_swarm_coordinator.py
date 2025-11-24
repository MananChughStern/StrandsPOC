"""
Agent 3: Multi-Agent Coordinator showing Agents-as-Tools pattern, hierarchical delegation
"""

from strands import Agent, tool
from strands_tools import calculator

@tool
def analyst_agent(query: str) -> str:
    """Expert data analyst for quant analysis and calculaions for use-cases of:
    - Numerical calculations and metrics
    - Statistical analysis
    - Data interpretation
    - Financial modeling

    Args:
        query: The data analysis question or task

    Returns:
        Detailed analysis with calculations
    """
    analyst = Agent(
        name="Data Analyst",
        tools=[calculator],
        system_prompt="""You are a data analyst expert.
        
    When analyzing data:
    1. Focus on quantitative metrics
    2. Calculate key ratios and trends
    3. Show your calculations clearly
    4. Provide numerical insights
    
    Be precise and data-driven."""
    )

    response = analyst(query)
    return str(response)

@tool
def strategist_agent(query: str) -> str:
    """Business strategist for market analysis and strategic planning for use-cases of:
    - Competitive positioning
    - Market dynamics analysis
    - Strategic recommendations
    - Risk assessment

    Args:
        query: The strategic question or business problem

    Returns:
        Strategic analysis and recommendations
    """
    strategist = Agent(
        name="Business Strategist",
        system_prompt="""You are a business strategy expert.
        
    When analyzing business problems:
    1. Consider competitive positioning
    2. Identify market dynamics
    3. Assess strategic risks
    4. Recommend actionable strategies
    
    Be strategic and business-focused."""
    )

    response = strategist(query)
    return str(response)

@tool
def critic_agent(query: str) -> str:
    """Devil's advocate who identifies flaws, risks, and blind spots for use-cases belwo:
    - Challenging assumptions
    - Finding potential flaws
    - Risk identification
    - Quality assurance

    Args:
        query: The analysis, plan, or decision to critique

    Returns:
        Critical analysis highlighting risks and weaknesses
    """
    critic = Agent(
        name="Critical Thinker",
        system_prompt="""You are a critical thinker and devil's advocate.
        
    Your role:
    1. Challenge assumptions
    2. Identify potential flaws
    3. Question conclusions
    4. Highlight blind spots
    
    Be constructively critical."""
    )

    response = critic(query)
    return str(response)


def create_coordinator():
    """Create coordinator agent with specialist tools"""
    coordinator = Agent(
        name="Swarm Coordinator",
        tools=[analyst_agent, strategist_agent, critic_agent],
        system_prompt="""You coordinate a team of specialists to solve complex problems.

    Your team:
    - analyst_agent: For quantitative analysis and calculations
    - strategist_agent: For business strategy and positioning
    - critic_agent: For finding flaws and assessing risks
    
    Process:
    1. Break down complex problems
    2. Route subtasks to appropriate specialists
    3. Have critic challenge key findings
    4. Synthesize responses into final recommendation
    
    Always explain which specialist you're consulting and why."""
    )

    return coordinator


def test_swarm_coordination():
    """Test multi-agent coordination patterns."""
    coordinator = create_coordinator()

    print("TEST 1: Quant Problem (should use analyst)")
    response1 = coordinator("""
    A SaaS company has:
    - 100,000 users
    - $2M annual revenue  
    - 20% monthly churn
    
    Calculate the Customer Lifetime Value (CLV) if average revenue per user is $20/month.
    """)
    print(response1)

    print("TEST 2: Strategic Problem (should use strategist)")
    response2 = coordinator("""
    A fintech startup is deciding between:
    A) Growing user base aggressively (burn cash)
    B) Focusing on profitability (slower growth)
    
    What should they prioritize and why?
    """)
    print(response2)

    print("TEST 3: Complex Problem (multiple specialists)")
    response3 = coordinator("""
    An AI agent framework company is analyzing market entry:
    
    Data:
    - Market size: $5B annually
    - Competitors: 4 major players
    - Our dev cost: $2M/year
    - Potential users Year 1: 10,000
    - Average revenue per user: $50/month
    
    Tasks:
    1. Calculate projected Year 1 revenue (use analyst)
    2. Analyze strategic positioning vs competitors (use strategist)
    3. Identify critical risks and flaws (use critic)
    4. Synthesize into go/no-go recommendation
    """)
    print(response3)
    print("WARM COORDINATION COMPLETE")

if __name__ == "__main__":
    test_swarm_coordination()