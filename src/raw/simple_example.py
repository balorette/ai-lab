import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from IPython.display import Markdown, display
load_dotenv(override=True)



openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')
grok_api_key = os.getenv('GROK_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set - please head to the troubleshooting guide in the setup folder")

from openai import OpenAI

openai = OpenAI()

messages = [{"role": "user", "content": "What is 2+2?"}]

response = openai.chat.completions.create(
    model="gpt-4.1-nano",
    messages=messages
)

print(response.choices[0].message.content)

question = "Please propose a hard, challenging question to assess someone's IQ. Respond only with the question."
messages = [{"role": "user", "content": question}]

response = openai.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages
)

question = response.choices[0].message.content

print(question)

# First create the messages:

messages = [{"role": "user", "content": "What is a business area worth exploring for an Agentic AI opportunity? Propose only one business area."}]

# Then make the first call:

response = openai.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages
)

# Then read the business idea:

business_area = response.choices[0].message.content
print(business_area)

# And repeat!
next_question = f"Please highlight a pain point in the following business area that might be ripe for an Agentic Solution: {business_area}."
messages = [{"role": "user", "content": next_question}]

response = openai.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages
)

pain_point = response.choices[0].message.content
print(pain_point)

last_question = f"Please propose an agentic AI solution to the following pain point: {pain_point} in the following business area {business_area}."
messages = [{"role": "user", "content": last_question}]
response = openai.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages
)
solution = response.choices[0].message.content

display(Markdown(solution))


# Next EXP
request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaluate their intelligence. "
request += "Answer only with the question, no explanation."
messages = [{"role": "user", "content": request}]

openai = OpenAI()
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)
question = response.choices[0].message.content
print(question)

competitors = []
answers = []
messages = [{"role": "user", "content": question}]

# The API we know well

model_name = "gpt-4o-mini"

response = openai.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

model_name = "claude-3-7-sonnet-latest"

claude = Anthropic()
response = claude.messages.create(model=model_name, messages=messages, max_tokens=1000)
answer = response.content[0].text

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model_name = "gemini-2.0-flash"

response = gemini.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

grok = OpenAI(api_key=grok_api_key, base_url="https://api.x.ai/v1")
model_name = "grok-3"


response = grok.chat.completions.create(model=model_name, messages=messages, stream=False)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

groq = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
model_name = "llama-3.3-70b-versatile"

response = groq.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)


for competitor, answer in zip(competitors, answers):
    print(f"Competitor: {competitor}\n\n{answer}")

    together = ""
for index, answer in enumerate(answers):
    together += f"# Response from competitor {index+1}\n\n"
    together += answer + "\n\n"


judge = f"""You are judging a competition between {len(competitors)} competitors.
Each model has been given this question:

{question}

Your job is to evaluate each response for clarity and strength of argument, and rank them in order of best to worst.
Respond with JSON, and only JSON, with the following format:
{{"results": ["best competitor number", "second best competitor number", "third best competitor number", ...]}}

Here are the responses from each competitor:

{together}

Now respond with the JSON with the ranked order of the competitors, nothing else. Do not include markdown formatting or code blocks."""

judge_messages = [{"role": "user", "content": judge}]

# Judgement time!

openai = OpenAI()
response = openai.chat.completions.create(
    model="o3-mini",
    messages=judge_messages,
)
results = response.choices[0].message.content
print(results)

results_dict = json.loads(results)
ranks = results_dict["results"]
for index, result in enumerate(ranks):
    competitor = competitors[int(result)-1]
    print(f"Rank {index+1}: {competitor}")