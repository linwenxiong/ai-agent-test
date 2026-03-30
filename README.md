执行脚本
& e:/ai_agent_demo/ai-agent-test/.venv/Scripts/python.exe -m app.ollama.ChatPromptTemplate


# 绑定自定义工具
- 第一步：开发工具函数
```python
def add(a, b):
    """add two numbers."""
    return a + b
```
- 第二步：将工具函数转为LangChain Tool对象
    - 方法一：
        ```python
        #使用Tool.from_function
        from langchain_core.tools import Tool
        add_tools = Tool.from_function(
            func=add, 
            name="add", 
            description="Add two numbers"
        )
        ```
    - 方法二：使用装饰器@tool
        ```python
        #使用装饰器@tool
        from langchain_core.tools import tool
        @tool
        def add(a, b):
            """add two numbers."""
            return a + b
        ```
    - 使用pydantic 做类型校验，定义工具函数的输入参数, 这样可以更好的控制入参类型
        ```python
        from pydantic import BaseModel, Field
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
        ```
- 第三步：将大模型和Tool对象绑定
```python
llm_with_tools = llm.bind_tools([add])
```

- 第四步：调用大模型，尝试让大模型调用工具
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "你i是一名资深的开发工程师，叫小林"),
    ("human", "{user_input}"),
])
chain = prompt | llm_with_tools
response = chain.invoke({"user_input", "计算1+10"})
```
 - 此时response会返回我们需要的参数
```python
{'name': 'add', 'args': {'a': 100, 'b': 100}, 'id': '42ecb318-264b-4416-a67d-3361e13377d5', 'type': 'tool_call'}
```
- 只需要取tool_calls就可以了
 ```python
for tool_calls in resp.tool_calls:
    print(tool_calls)
    
    args = tool_calls["args"]
    print("===>参数：", args)
    
    func_name = tool_calls["name"]
    print("===>工具方法名：", func_name)

    tool_func = tool_dict[func_name]

    tool_content = tool_func.invoke(args)
    print(tool_content)
 ```