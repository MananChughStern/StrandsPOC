

### Verify AWS Access
```
(.venv) mananchugh@Manans-Laptop StrandsPOC % python test_aws_setup.py
```
##### Output:

```commandline
AWS credentials configured correctly

Region: us-west-2
```

### Agent To Test Basic Strands Functionality
```
(.venv) mananchugh@Manans-Laptop StrandsPOC % python agent_01_hello.py
```
##### Output:

```commandline
A good AI agent framework should have several key characteristics:

## Core Architecture
- **Modular design** that separates reasoning, planning, memory, and tool execution
- **Clear abstractions** for different agent types (reactive, deliberative, hybrid)
- **Extensible plugin system** for adding new capabilities

## Essential Components
- **Robust memory management** (short-term working memory, long-term episodic/semantic memory)
- **Planning and reasoning capabilities** that can handle multi-step tasks
- **Tool integration system** for external APIs, databases, and services
- **State management** to track context across interactions

## Developer Experience
- **Simple, intuitive APIs** that don't require deep AI expertise to use
- **Good documentation and examples** for common use cases
- **Debugging and observability tools** to understand agent behavior
- **Testing frameworks** for validating agent performance

## Reliability & Safety
- **Error handling and recovery** mechanisms
- **Rate limiting and resource management**
- **Security measures** for tool access and data handling
- **Guardrails** to prevent harmful or off-task behavior

## Performance & Scalability
- **Efficient prompt management** and token optimization
- **Caching strategies** for repeated operations
- **Concurrent execution** capabilities
- **Model flexibility** (support for different LLMs/providers)

## Observability
- **Logging and monitoring** of agent decisions and actions
- **Metrics and analytics** for performance tracking
- **Human-in-the-loop** capabilities for oversight

The best frameworks balance power and flexibility with ease of use, making sophisticated AI agents accessible to developers while maintaining safety and reliability.============================================================
```

### Strands Agent with Custom Tools

```
python agent_02_tools.py
```
Output:
```commandline
============================================================
QUERY 1: What's 234 multiplied by 567?
============================================================
I'll calculate 234 multiplied by 567 for you.
Tool #1: calculator
234 multiplied by 567 equals **132,678**.234 multiplied by 567 equals **132,678**.


============================================================
QUERY 2: Calculate DAU/MAU for a product with 50,000 daily users and 200,000 monthly users
============================================================
I'll calculate the DAU/MAU ratio and stickiness score for your product with 50,000 daily active users and 200,000 monthly active users.
Tool #2: pm_metric_calculator
Here are your product engagement metrics:

**Key Metrics:**
- **DAU/MAU Ratio:** 0.25 (25%)
- **Stickiness Score:** 25.0%

**Interpretation:** The metrics indicate that engagement "Needs improvement (<40%)"

This means that on average, 25% of your monthly active users are engaging with your product daily. While this shows there's a solid user base, there's significant room for improvement in user engagement and retention. Products with strong engagement typically see DAU/MAU ratios of 40% or higher.

Consider focusing on strategies to increase daily usage patterns and user retention to improve these metrics.Here are your product engagement metrics:

**Key Metrics:**
- **DAU/MAU Ratio:** 0.25 (25%)
- **Stickiness Score:** 25.0%

**Interpretation:** The metrics indicate that engagement "Needs improvement (<40%)"

This means that on average, 25% of your monthly active users are engaging with your product daily. While this shows there's a solid user base, there's significant room for improvement in user engagement and retention. Products with strong engagement typically see DAU/MAU ratios of 40% or higher.

Consider focusing on strategies to increase daily usage patterns and user retention to improve these metrics.


============================================================
QUERY 3: Compare stickiness: Product A has 60k DAU and 150k MAU, Product B has 40k DAU and 80k MAU
============================================================
I'll calculate the stickiness metrics for both products to compare their engagement levels.
Tool #3: pm_metric_calculator

Tool #4: pm_metric_calculator
Here's the stickiness comparison between your two products:

## Product A (60k DAU, 150k MAU)
- **DAU/MAU Ratio:** 0.40 (40%)
- **Stickiness Score:** 40.0%
- **Interpretation:** Needs improvement (<40%)

## Product B (40k DAU, 80k MAU)
- **DAU/MAU Ratio:** 0.50 (50%)
- **Stickiness Score:** 50.0%
- **Interpretation:** Good (40-60%)

## Key Insights:

**Product B has significantly better stickiness** despite having fewer absolute users:
- Product B engages 50% of its monthly users daily vs. Product A's 40%
- Product B has crossed the 40% threshold into "Good" engagement territory
- Product A sits right at the 40% boundary but is still categorized as needing improvement

**Strategic Implications:**
- **Product B** demonstrates superior user engagement and retention
- **Product A** has a larger user base but lower engagement quality
- Product A could benefit from studying Product B's engagement strategies
- Consider whether Product A should focus on growing its existing user base engagement before pursuing new user acquisition

Product B shows that smaller, more engaged user bases can be more valuable than larger, less sticky ones.Here's the stickiness comparison between your two products:

## Product A (60k DAU, 150k MAU)
- **DAU/MAU Ratio:** 0.40 (40%)
- **Stickiness Score:** 40.0%
- **Interpretation:** Needs improvement (<40%)

## Product B (40k DAU, 80k MAU)
- **DAU/MAU Ratio:** 0.50 (50%)
- **Stickiness Score:** 50.0%
- **Interpretation:** Good (40-60%)

## Key Insights:

**Product B has significantly better stickiness** despite having fewer absolute users:
- Product B engages 50% of its monthly users daily vs. Product A's 40%
- Product B has crossed the 40% threshold into "Good" engagement territory
- Product A sits right at the 40% boundary but is still categorized as needing improvement

**Strategic Implications:**
- **Product B** demonstrates superior user engagement and retention
- **Product A** has a larger user base but lower engagement quality
- Product A could benefit from studying Product B's engagement strategies
- Consider whether Product A should focus on growing its existing user base engagement before pursuing new user acquisition

Product B shows that smaller, more engaged user bases can be more valuable than larger, less sticky ones.


============================================================
```
