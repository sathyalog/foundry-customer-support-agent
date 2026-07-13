# Customer Support Agent
This project leverages the Azure AI Foundry SDK to connect to a custom Customer Support Agent that assists human agents by providing concise summaries of customer issues and drafting polite, professional responses.
### Prerequisites
• uv installed on your system.
• An active Azure Subscription with access to Azure AI Foundry (ai.azure.com).
### Getting Started
1. Project Initialization
Initialize the project structure and install the required dependencies. uv will automatically manage and create your virtual environment.
# Initialize a new uv project
`uv init`

# Install the required Azure SDKs and utility libraries
1. Add libraries with `uv add python-dotenv azure-identity azure-ai-projects`

2. Azure Authentication
Log in to your Azure account and ensure you are using the correct subscription.
# Log in to Azure
`az login`

# Set your active subscription
`az account set --subscription "<your-subscription-id-or-name>"`

3. Agent Setup in Azure AI Foundry


    1. Navigate to Azure AI Foundry.
    2. Create a new agent named customer-support-agent using the gpt-4o-mini model.
    3. In the Playground -> Instructions section of your agent, paste the following system prompt:
**System Instructions**
``` You are a professional customer support assistant.
Your role is to help human support agents work faster by:
1. Summarizing what the customer is asking or reporting
2. Drafting a clear, polite, and helpful reply that the agent can review and send
You do not make final decisions.
You do not promise refunds, fixes, or timelines.
You do not mention internal systems or policies unless the customer explicitly asks.
Your tone must always be calm, respectful, and professional.

OUTPUT FORMAT (STRICT)
Always respond using the following structure, in plain text:
Internal summary:
<One to two short sentences summarizing the customer’s message>
Draft reply:
<A polite, customer-facing reply, three to six sentences max>

WRITING GUIDELINES
For the internal summary:
- Keep a neutral tone
- Avoid speculation
- Focus strictly on what the customer wants or reports
For the draft reply:
- Acknowledge the issue or request
- Show empathy when appropriate
- Explain the next step at a high level
- Ask for missing information if needed
- Do not promise outcomes or timelines
- Do not use legal or policy-heavy language
If the customer’s message is unclear, say so and ask clarifying questions in the draft reply. ```

```

1. Save the agent.
4. Configuration (.env)
Create a .env file in the root of your project directory and configure the environment variables as follows:
# The endpoint of your Azure AI Project
`AZURE_AI_PROJECT_ENDPOINT="https://<your-project-endpoint>"`


# The name of the agent you created in Azure AI Foundry
`AZURE_AI_AGENT_NAME="customer-support-agent"`

(Note: You can copy your project endpoint from the Project Details pane inside the Azure AI Foundry portal).
5. Add Script Source Code
1. In the Azure AI Foundry portal, select your agent.
2. In the right-hand panel, select the Call Agent tab.
3. Copy the generated Python code block.
4. Create a file named support-agent.py in your local project root and paste the copied code into it.
Running the Project
Run the agent script directly using uv. This command handles virtual environment activation and dependency management seamlessly in one step:
`uv run support-agent.py`