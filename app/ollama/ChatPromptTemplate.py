# ======================================  拆分提示词模板
## ChatMessagePromptTemplate 结合 ChatPromptTemplate 使用，同时对提示词模板和消息体进行抽象和复用；
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, ChatMessagePromptTemplate
if __name__ == "__main__":
    llm = ChatOllama(
        model="qwen3.5:0.8b",
        temperature=0,
        )
# # 系统模板
ststem_message_template = ChatMessagePromptTemplate.from_template(
    template = "你是一位{role}专家，擅长回答{domain}领域的问题。",
    role="system"
)
# 用户模板
human_message_template = ChatMessagePromptTemplate.from_template(
    template = "用户问题:{question}",
    role="user"
)

# 创建提示词模板
chat_prompt_template = ChatPromptTemplate.from_messages([
    ststem_message_template,
    human_message_template,
])
# 给提示词模板变量赋值
propmt = chat_prompt_template.format_messages(
    role="编程", 
    domain="Web开发", 
    question="你擅长什么？"
)
print("=============提示词开始=============")
print(propmt)
    # resp = llm.invoke(messages)
    # print(resp)
resp = llm.stream(propmt)
for chunk in resp:
    print(chunk.content, end="")

