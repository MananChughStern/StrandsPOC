
This is a light-weight POC for Strands Agents. The python files include implementations of the agents. Their corresponding markdown files contain execution output.

Agents Implemented:

1. Custom Tools Agent (`agent1_tools.py`): Basic tool creation with a MAU/DAU calculator. Shows how Python functions with type hints become agent tools. Validates Strands' simple tool definition pattern.
2. Code Reviewer with Learning (`agent2_code_reviewer.py`): Autonomously learns from past code reviews by saving insights locally. Shows pattern recognition based on tool use.
3. Multi-Agent Swarm Coordinator (`agent_swarm_coordinator.py`): Coordinator agent delegates complex queries to specialist agents (analyst, strategist, critic) without explicit orchestration code. Shows multi-agent orchestration.


## Setup
### Install Dependencies
```
pip install strands-agents
pip install anthropic
pip install boto3
```

### Verify AWS Access
```
python test_aws_setup.py
```
Expected output:

```commandline
AWS credentials configured correctly

Region: us-west-2
```
