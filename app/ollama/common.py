
from langchain_core.prompts import ChatPromptTemplate, ChatMessagePromptTemplate
from langchain_ollama import ChatOllama
llm = ChatOllama(
    model="deepseek-r1:8b",
    temperature=0,
        )
# 系统模板
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