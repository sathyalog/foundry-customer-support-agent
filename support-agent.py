# Before running the sample:
#    pip install azure-ai-projects>=2.1.0

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv
import os
load_dotenv(override=True)
endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

my_agent = os.getenv("AZURE_AI_AGENT_NAME")

openai_client = project_client.get_openai_client()
customer_query = "Hi, I was charged twice for my last order. Can you help me with that?"
# Reference the agent to get a response
response = openai_client.responses.create(
    input=[{"role": "user", "content": customer_query}],
    extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
)

print(f"Response output: {response.output_text}")