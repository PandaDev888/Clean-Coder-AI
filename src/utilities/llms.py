from langchain_openai.chat_models import ChatOpenAI as ChatOpenRouter
from os import getenv
import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama

load_dotenv()

def llm_open_router(model):
    return ChatOpenRouter(
    openai_api_key=getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    model_name=model,
    default_headers={
        "HTTP-Referer": "https://github.com/Grigorij-Dudnik/Clean-Coder-AI",
        "X-Title": "Clean Coder",
    },
    timeout=60,
)


def init_llms(tools=None, run_name="Clean Coder", temp=0):
    llms = []
    if os.getenv("ANTHROPIC_API_KEY"):
        llms.append(ChatAnthropic(model='claude-3-5-sonnet-20241022', temperature=temp, timeout=60, max_tokens=2048))
    if os.getenv("OPENROUTER_API_KEY"):
        llms.append(llm_open_router("anthropic/claude-3.5-sonnet"))
    if os.getenv("OPENAI_API_KEY"):
        llms.append(ChatOpenAI(model="gpt-4o", temperature=temp, timeout=60))
    if os.getenv("OLLAMA_MODEL"):
        llms.append(ChatOllama(model=os.getenv("OLLAMA_MODEL")))
    for i, llm in enumerate(llms):
        if tools:
            llm = llm.bind_tools(tools)
        llms[i] = llm.with_config({"run_name": run_name})
    return llms


def init_llms_mini(tools=None, run_name="Clean Coder", temp=0):
    llms = []
    if os.getenv("ANTHROPIC_API_KEY"):
        llms.append(ChatAnthropic(model='claude-3-5-haiku-20241022', temperature=temp, timeout=60))
    if os.getenv("OPENROUTER_API_KEY"):
        llms.append(llm_open_router("anthropic/claude-3.5-haiku"))
    if os.getenv("OPENAI_API_KEY"):
        llms.append(ChatOpenAI(model="gpt-4o-mini", temperature=temp, timeout=60))
    if os.getenv("OLLAMA_MODEL"):
        llms.append(ChatOllama(model=os.getenv("OLLAMA_MODEL")))
    for i, llm in enumerate(llms):
        if tools:
            llm = llm.bind_tools(tools)
        llms[i] = llm.with_config({"run_name": run_name})
    return llms
