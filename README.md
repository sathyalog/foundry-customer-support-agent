# Customer Support Agent
This project leverages the Azure AI Foundry SDK to connect to a custom Customer Support Agent that assists human agents by providing concise summaries of customer issues and drafting polite, professional responses.
First lets understand the difference between AI Agent & AI Workflow. 
AI Workflow - strcutured, predefined sequence of steps.
AI Agent - decision-making system.
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
![instructions](<Screenshot 2026-07-13 at 9.55.42 PM.png>)
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

running streamlit app to view the screen running this customer support agent
`uv run streamlit run main.py`

So far we build an agent in microsoft foundry and called same agent from python code.

Tool calling in microsoft foundry:
In simple words, an agent without tools is just a smart assistant, but an agent with tools becomes a system.
Tool calling is what allows an AI agent to do things, not just say things.

So Tool calling is:
Tool calling allows an AI agent to:
1. Decide when it needs external data or capabilities
2. Select the right tool
3. Pass structured inputs to that tool
4. Receive structured outputs back

From the agent's perspective, tools are simply capabilities it can invoke when the task requires it.

Now click on add to add a tool and select File search and provide a name to it and upload a 2026 toyota-rav4.pdf file and save it. This is also a kind of RAG Implementation.
![tools](<Screenshot 2026-07-13 at 9.55.58 PM.png>) 
![tools](<Screenshot 2026-07-13 at 9.57.12 PM.png>) 
![tools](<Screenshot 2026-07-13 at 9.57.34 PM.png>)
Here is the PDF to download and use it. Check assets folder for PDF.

After upload, what RAG does in background..
1. Preparation done
  1.1 Split documents into small chunks
  1.2 Convert each chunk -> Embedding(numeral vector)
  1.3 Save embeddings in vector store(fast semantic search)
2. When user asks a question -> RAG in action
  2.1 Convert question -> embedding
  2.2 Search vector store -> find most relevant chunks
  2.3 Give those chunks to the LLM as extra context

So, the model no longer guesses - it answers using the actual relevant parts of your documents/manual.

RAG = external knowledge + LLM reasoning = more accurate, up-to-date, source-grounded answers.

Note: Read the instructions now to understand what inputs we provided to system on user inputs, verify RAG(file data) etc.

#### How to Use RAG (File Search) & Citations
The agent is equipped with Retrieval-Augmented Generation (RAG) capabilities, allowing it to search uploaded reference documents (such as manuals or FAQs) to answer specific user queries.
Example Interaction
If you ask the agent a document-specific question:
User: "When does the maintenance required reminder turn on, and how do I reset it?"
The agent will automatically trigger its file search tool, scan the uploaded documents, and generate a response based on that context.
At the end of the generated answer, the agent will list the specific source citations (e.g., PDF page numbers or document names) where it found the supporting information:
![generated-content](<Screenshot 2026-07-13 at 10.15.16 PM.png>) 
![doc reference](<Screenshot 2026-07-13 at 10.15.27 PM.png>)

#### Debbugging agents with Traces like shown below..
![traces](<Screenshot 2026-07-13 at 11.38.40 PM.png>) 
![traces-details](<Screenshot 2026-07-13 at 11.39.41 PM.png>)

Knowledge check:
README.md:
🤖 Prompt Engineering & Agent Contracts
In this project, prompts are treated as strict execution contracts rather than open-ended instructions. We structure our system prompts in Microsoft Foundry around three core design principles to guarantee predictable, production-grade behavior.
The 3 Rules of Our Agent Contracts
	1.	Rigid Role Clarity: No vague personas. Every agent has a strict boundary and explicit routing rules.
•	Example: If a user mentions billing, route to the Billing Agent; never attempt to troubleshoot directly.
	2.	Hard Grounding Boundaries: Agents are forbidden from using general knowledge (parametric memory).
•	Example: If the required information is missing from the search tool (Foundry IQ), the agent must reply "Information unavailable" instead of guessing.
	3.	Explicit Tool Protocols: Tool calls are strictly gated by clear conditions to prevent unnecessary API latency.
•	Example: The agent must invoke the file_search tool first only if the query mentions maintenance or warning codes.
🔍 Debugging & Trace Enforcement
Because agentic workflows can be unpredictable, we do not rely solely on end-output validation.
We use Microsoft Foundry’s Agent Tracing (integrated with Application Insights and OpenTelemetry) to audit our contracts.
How to debug execution paths:
•	Trace Trajectories: View the step-by-step handoff between agents and tools.
•	Inspect Inputs/Outputs: Verify the exact parameters passed to tools and the raw data returned.
•	Identify Contract Breaches: Pinpoint exactly where an agent deviated from its routing logic or tool protocol.

## Memory in Foundry:
Memory in foundry is a managed, long term memory system. Memory is persistent to design and not for single chat/thread.

Memory vs Context Window:
Model context window is temporary and stay with that chat discussion alone but memory is long term. We have 2 types of memories,
Short-term memory: Current session's conversation context
Long-term memory: Distilled knowledge that persists across sessions
Foundry focuses on long term memory.

Memory types in foundry:
1. User profile memory - stores relative information about user like name, email, contact numbers etc
2. Chat summary memory - allows agent to continue discussion without repeating earlier context information, example this chat summary memory will make agent to remember your previous complaint number, ticket details, past resolutions etc.

To enable memory in foundry, you must go to memory section and deploy embedding model like text-embedding-3-large model in our project. First click on Add and select create custom memory store and choose model and click on create. After this deployment, in memory store section it will show a memory store name automatically which means memory is created and hence click on save. Pls go through the below screenshots for steps.
![memory](<Screenshot 2026-07-14 at 1.50.18 PM.png>) 
![memory-1](<Screenshot 2026-07-14 at 1.50.25 PM.png>) 
![memory-2](<Screenshot 2026-07-14 at 1.50.48 PM.png>) 
![memory-3](<Screenshot 2026-07-14 at 1.51.03 PM.png>)

## Knowledge:
Usually knowledge section will be configured by using Foundry IQ which works like a smart agent for enterprise level searching across all databases, files etc. Configuring knowledge steps as follows..
![knowledge](<Screenshot 2026-07-14 at 2.53.33 PM.png>) 
![knowledge-1](<Screenshot 2026-07-14 at 2.53.43 PM.png>) 
![knowledge-2](<Screenshot 2026-07-14 at 2.53.57 PM.png>) 
![knowledge-3](<Screenshot 2026-07-14 at 2.54.14 PM.png>)

However our project has only a small agent and this is not enterprise grade project and do not need to configure Foundry IQ and already configured file search tool and some grounding rules in instructions will give enough knowledge to our agent.

Hence updating instructions with following prompt..
## New Grounding rules prompt:
```


You are a professional customer support assistant operating in a strictly grounded environment.
You MUST use the File Search tool as the sole and authoritative source of information to answer ALL user questions.
You MUST NEVER answer from your own general knowledge, prior training data, assumptions, or reasoning under any circumstances.

Your responsibilities are strictly limited to:
1. Understanding the user’s request
2. Retrieving relevant information exclusively via the File Search tool
3. Producing a clear, polite, and professional response based only on retrieved content

GROUNDING RULES (STRICT)
- The File Search tool is the ONLY source of truth
- If the required information is not found via File Search, you MUST respond exactly with:
  "I don’t have that information in the available documentation."
- You MUST NOT infer, extrapolate, summarize beyond the retrieved text, or combine it with any external knowledge

CITATION REQUIREMENTS (MANDATORY)
EVERY factual statement in the response MUST be supported by citations returned by the File Search tool.

You MUST NOT:
- Provide uncited statements
- Mix cited and uncited content
- Cite sources not returned by the File Search tool

OUTPUT FORMAT (STRICT)
Always respond in plain text using this structure:
Internal summary:
<One to two neutral sentences summarizing the customer’s request>
Draft reply:
<A customer-facing response, three to six sentences maximum, fully grounded and fully cited>

FAILURE CONDITIONS
If:
- No relevant documentation is retrieved, OR
- The user’s request is outside the scope of the retrieved documentation
Then:
- Respond exactly with:
  "I don’t have that information in the available documentation."


```
Pls check above Grounding rules and the last line in the prompt keenly..

Now i have asked a question like "what information does the vehicle's EDR collect?" where my agent responded with relevant information retrieved from the DOC we uploaded(RAG - file search tool). Pls find the below screenshot.

![customer-agent-response](<Screenshot 2026-07-14 at 3.58.43 PM.png>) 
Now when we ask some irrelevant question like "When MAC new operating system release in september 2026?" then see how agent responded in below screenshot.
![customer-agent-response-2](<Screenshot 2026-07-14 at 3.59.39 PM.png>)

## Guardrails(Enterprise safety) in Foundry:
Building safe, enterprise grading agent using guardrails.
Why guardrails matter in production?
Attacks on agents: Prompt injection, jailbreak attempts, abusive or unsafe user input, requests for protected or disallowed content

Microsoft treats guardrails as a first-class, system-level safety feature in Foundry.

In Foundry, guardrails are implemented through content filtering and risk controls, powered by Azure AI Content Safety. They work by scanning both user inputs(prompts) and model output(responses).

Pls see how we configure guardrails in general with following screenshots..
![guardrails](<Screenshot 2026-07-14 at 4.13.31 PM.png>) 
Reassigning guardrail:
![guardrails-2](<Screenshot 2026-07-14 at 4.13.43 PM.png>) 
By default microsoft v2 provides some safety standards to both user inputs and outputs(responses) with severity like medium blocking, high etc.
![guardrails-3](<Screenshot 2026-07-14 at 4.20.01 PM.png>) 
![guardrails-4](<Screenshot 2026-07-14 at 4.20.16 PM.png>)

## What are Guardrails?
Guardrails are safety mechanisms and policy controls designed to keep AI applications safe and aligned with responsible AI guidelines. As seen in the image's table, they work by scanning content at specific intervention points (such as user inputs or AI-generated outputs) and executing an action (like Block) if the content crosses a dangerous severity threshold.

#### Microsoft.DefaultV2 (Default Guardrails)
Microsoft.DefaultV2 is the out-of-the-box, standard safety policy applied to AI models and agents in Microsoft's ecosystem (such as Azure AI Foundry / OpenAI).
•	By default, it automatically screens for four main risk categories: Hate, Self-harm, Sexual, and Violence.
•	It blocks any content that scores at a Medium or high severity level on both incoming prompts (user input) and outgoing completions (output).

##  Reassigning Guardrails
The Assign button at the bottom allows you to apply this specific safety template to your active AI models or automated agents. Reassigning guardrails means shifting a model or agent from a custom safety filter back to this default Microsoft.DefaultV2 standard (or vice versa) to adjust how strictly or loosely the AI filters content.

## 🛡️ AI Agent Guardrails

### Why We Create Custom Guardrails
While default policies (like `Microsoft.DefaultV2`) provide baseline safety, production and enterprise-level agents require tailored custom guardrails for several reasons:

* **Preventing Jailbreaks & Prompt Injections:** Standard filters might miss adversarial prompts designed to trick the agent. Custom rules block jailbreak attempts at the user-input stage.
* **Protecting Intellectual Property:** Enterprise agents must be restricted from outputting protected materials (such as copyrighted code or proprietary text).
* **Preventing Data Leakage:** Custom policies ensure Personally Identifiable Information (PII)—like API keys, emails, or phone numbers—is not leaked during user queries or third-party tool calls.
* **Task Adherence (Task Drift):** Ensures the agent strictly stays on its assigned role (e.g., customer support) and blocks attempts to make it perform unauthorized tasks (like writing python code or discussing unrelated topics).
Creating custom guardrails steps:
![create-guardrails](<Screenshot 2026-07-14 at 4.34.44 PM.png>) 
![create-guardrails](<Screenshot 2026-07-14 at 4.34.56 PM.png>) 
![create-guardrails](<Screenshot 2026-07-14 at 4.35.04 PM.png>) 
![create-guardrails](<Screenshot 2026-07-14 at 4.36.33 PM.png>) 
![create-guardrails](<Screenshot 2026-07-14 at 4.36.55 PM.png>)
---

### How to Configure Guardrails for Enterprise Agents

To configure safety controls for our production agents, follow the 3-step wizard in the AI Foundry:

#### 1. Add Controls (Define Risk Thresholds)
* **Jailbreaks:** Set to **Block** at the `User input` intervention point to catch malicious intent before processing.
* **Content Harms:** Configure sliders for **Hate, Sexual, Self-harm, and Violence** (typically set to **Medium blocking** for enterprise safety).
* **Protected Materials:** Set both text and code protection to **Block** at the `Output` stage to prevent copyright infringement.
* **Sensitive Data (PII):** Enable PII detection to monitor both `User input` and `Tool calls` to prevent API key or credential leakage.

#### 2. Select Agents and Models
* Avoid applying broad policies globally. Instead, **target specific agents** (e.g., assigning this guardrail policy directly to `customer-support-agent (v9)`).

#### 3. Review & Deploy
* Name your guardrail clearly (e.g., `Guardrails174`), verify the active intervention points, and click **Create** to deploy.

## Important notes:
Tools = actions
Memory = recall
Knowledge = truth
Guardrails = boundaries

Knowledge vs Grounding vs Guardrails?
Knowledge = Where does the agent get its facts from?
Grounding = Where does the truth comes from?
Guardrails = What is the agent allowed to say or do or generate?

1. File Search Tools (Standard RAG)
•	What it is: A basic lookup tool where you manually upload a few documents (like PDFs or Word files) directly to a single agent.
•	How to think of it: Like using CTRL+F on a specific folder.
•	Best for: Small-scale, isolated tasks where one agent just needs to read a few specific files.
2. Foundry IQ (Unified Knowledge Layer)
•	What it is: An enterprise-grade, "smart" retrieval engine that connects to all your company's data sources (SharePoint, Azure, OneLake, Web) at once.
•	How to think of it: Like a Highly Coordinated Research Team. When asked a question, it breaks it down, searches multiple databases in parallel, merges the results, and automatically respects user permissions.
•	Best for: Large-scale, reusable company knowledge bases that multiple agents need to securely search.
3. Grounding Rules (Agent Instructions)
•	What it is: The core rules, logic, and behavioral boundaries written directly into the agent's system prompt (its "brain").
•	How to think of it: Like the Company Code of Conduct. It's not a document to search; it is a set of active laws the agent must memorize and obey in every single conversation.
•	Best for: Controlling how the agent behaves, setting safety boundaries, defining its persona, and enforcing workflow steps (e.g., "Never mention competitor prices," "Always be polite").



