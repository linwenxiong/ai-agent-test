from langchain_core.tools import tool
from app.ollama.common import chat_prompt_template, llm  # 直接运行文件时
from pydantic import BaseModel, Field

# 使用pydantic 做类型校验，定义工具函数的输入参数

# 第一步：开发工具函数
class AddInputArgs(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")
@tool(
        description="add two numbers",
        args_schema=AddInputArgs
)
def add(a, b):
    """add two numbers."""
    return a + b

# add_tools = Tool.from_function(func=add, name="add", description="Add two numbers")
tool_dict = {
    "add": add
}

llm_with_tools = llm.bind_tools([add])

chain = chat_prompt_template | llm_with_tools

 
resp = chain.invoke(
   input={"role": "计算", "domain": "数学计算", "question": "计算100+100等于多少"}
)

for tool_calls in resp.tool_calls:
    print(tool_calls)
    
    args = tool_calls["args"]
    print("===>参数：", args)
    
    func_name = tool_calls["name"]
    print("===>工具方法名：", func_name)

    tool_func = tool_dict[func_name]

    tool_content = tool_func.invoke(args)
    print(tool_content)

    # 使用LangChain调用大模型
    # 第一步：实例化大模型
    # 第二部：初始化提示词模板
    # 第三步：链式调用大模型

    # 绑定自定义工具
    # 第一步：开发工具函数
    # 第二步：将工具函数转为LangChain Tool对象
    # 第三步：将大模型和Tool对象绑定
    # 第四步：调用大模型，尝试让大模型调用工具
    # 第五步：主动调用工具