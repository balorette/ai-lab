import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI, AsyncAzureOpenAI, DefaultHttpxClient
from agents import Agent, Runner, trace, function_tool, OpenAIChatCompletionsModel, input_guardrail, GuardrailFunctionOutput
from typing import Dict
import os
from pydantic import BaseModel

load_dotenv(override=True)

ai_api_key = os.getenv('MMC_AI_APIKEY')

instructions1 = "You are a sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails."

instructions2 = "You are a humorous, engaging sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response."

instructions3 = "You are a busy sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write concise, to the point cold emails."

AI_BASE_URL = "https://stg1.mmc-dallas-int-non-prod-ingress.mgti.mmc.com/coreapi/openai/v1/"

authHeaders = {
    'X-Api-Key': ai_api_key,}
# hc = DefaultHttpxClient(headers=authHeaders)
# aic = AzureOpenAI(azure_endpoint=AI_BASE_URL, api_key=ai_api_key, http_client=hc)

api_version = "2024-10-21"

def create_model(model: str ="mmc-tech-gpt-4o-mini-128k-2024-07-18", api_version: str = "2024-10-21" ) -> AsyncAzureOpenAI:
    client = AsyncAzureOpenAI(api_key=ai_api_key, azure_endpoint=AI_BASE_URL, azure_deployment=model, api_version=api_version)
    return client

aic1 = create_model()
aic2 = create_model(model="mmc-tech-gpt-4o-128k-2024-05-13")
aic3 = create_model(model="mmc-tech-gpt-4-turbo-128k-2024-04-09")

ai_model = OpenAIChatCompletionsModel(model="mmc-tech-gpt-4o-mini-128k-2024-07-18", openai_client=aic1)
ai_2_model = OpenAIChatCompletionsModel(model="mmc-tech-gpt-4o-128k-2024-05-13", openai_client=aic2)
ai_3_model = OpenAIChatCompletionsModel(model="mmc-tech-gpt-4-turbo-128k-2024-04-09", openai_client=aic3)

sales_agent1 = Agent(name="4o Mini Sales Agent", instructions=instructions1, model=ai_model)
sales_agent2 =  Agent(name="4o Sales Agent", instructions=instructions2, model=ai_2_model)
sales_agent3  = Agent(name="4 Turbo Sales Agent",instructions=instructions3,model=ai_3_model)

async def doit():
    result = await Runner.run(sales_agent1, "Send out a cold sales email addressed to Dear CEO from Alice")
    print(result.final_output)  

asyncio.run(doit())

"""

description = "Write a cold sales email"

tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description=description)
tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description=description)
tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description=description)

@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    " Send out an email with the given subject and HTML body to all sales prospects "
    from_email = "bryan.a.lorette@gmail.com"  # Change to your verified sender
    to_email = "bryan.a.lorette@gmail.com" # Change to your recipient
    print(subject)
    print(html_body)
    return {"status": "success"}

subject_instructions = "You can write a subject for a cold sales email. \
You are given a message and you need to write a subject for an email that is likely to get a response."

html_instructions = "You can convert a text email body to an HTML email body. \
You are given a text email body which might have some markdown \
and you need to convert it to an HTML email body with simple, clear, compelling layout and design."

subject_writer = Agent(name="Email subject writer", instructions=subject_instructions, model=ai_model)
subject_tool = subject_writer.as_tool(tool_name="subject_writer", tool_description="Write a subject for a cold sales email")

html_converter = Agent(name="HTML email body converter", instructions=html_instructions, model=ai_model)
html_tool = html_converter.as_tool(tool_name="html_converter",tool_description="Convert a text email body to an HTML email body")

email_tools = [subject_tool, html_tool, send_html_email]

instructions ="You are an email formatter and sender. You receive the body of an email to be sent. \
You first use the subject_writer tool to write a subject for the email, then use the html_converter tool to convert the body to HTML. \
Finally, you use the send_html_email tool to send the email with the subject and HTML body."


emailer_agent = Agent(
    name="Email Manager",
    instructions=instructions,
    tools=email_tools,
    model=ai_model,
    handoff_description="Convert an email to HTML and send it")

tools = [tool1, tool2, tool3]
handoffs = [emailer_agent]

sales_manager_instructions = "You are a sales manager working for ComplAI. You use the tools given to you to generate cold sales emails. \
You never generate sales emails yourself; you always use the tools. \
You try all 3 sales agent tools at least once before choosing the best one. \
You can use the tools multiple times if you're not satisfied with the results from the first try. \
You select the single best email using your own judgement of which email will be most effective. \
After picking the email, you handoff to the Email Manager agent to format and send the email."


sales_manager = Agent(
    name="Sales Manager",
    instructions=sales_manager_instructions,
    tools=tools,
    handoffs=handoffs,
    model=ai_model)

message = "Send out a cold sales email addressed to Dear CEO from Alice"

async def run_sales_agent():
    "Run the sales agent to generate a cold sales email."   
    result = await Runner.run(sales_manager, message)
    return result

asyncio.run(run_sales_agent())

"""