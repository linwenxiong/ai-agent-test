
print("This is a tool for adding two numbers.")
from langchain_core.tools import Tool
from app.ollama.common import chat_prompt_template, llm  # 直接运行文件时

def add(a, b):
    """Add two numbers."""
    return a + b

add_tools = Tool.from_function(func=add, name="add", description="Add two numbers")
llm_with_tools = llm.bind_tools([add_tools])
chain = chat_prompt_template | llm_with_tools
