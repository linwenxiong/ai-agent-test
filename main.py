# ===== FewShotPromptTemplate (少样本提示模板)
# 适用场景:
# 1. 用于少样本学习(Few-Shot Learning)，在提示中包含示例(Examples)，帮助模型理解任务。
# 2. 适用于复杂任务(如翻译、分类、推理)，需要通过示例引导模型行为。
# 特点:
# 示例嵌入     :通过examples参数提供示例输入和输出。
# 动态示例选择 :支持ExampleSelector动态选择最相关的示例。
# 模板格式     :通常包含前缀(Prefix)、示例(Examples)和后缀(Suffix)。

from langchain_ollama import ChatOllama
from langchain_core.prompts import  FewShotPromptTemplate, PromptTemplate

if __name__ == "__main__":
    llm = ChatOllama(
        model="deepseek-r1:8b",
        temperature=0,
    )
example_template = "输入：{input}\n输出:{output}"
# examples = [
#     {"input": "将'Hello'翻译成中文", "output": "你好"},
#     {"input": "将'Goodbye'翻译成中文", "output": "再见"},
# ]
examples = [
    {"input": "将'你好'翻译成英文", "output": "Hello"},
    {"input": "将'再见'翻译成英文", "output": "Goodbye"},
]
few_shot_prompt_template = FewShotPromptTemplate(
    examples        = examples, #样例
    example_prompt  = PromptTemplate.from_template(example_template),
    prefix          = "请将以下中文翻译成英文：", #前缀
    suffix          = "输入：{text}\n输出:",     #后缀
    input_variables = ["text"]
)
print(few_shot_prompt_template)
print("=============提示词开始=============")
chain = few_shot_prompt_template | llm # 数据先经过 few_shot_prompt_template（少量示例提示模板）处理, 然后将处理结果传递给LLM，形成一个链式调用
resp = chain.stream(input={"text": "迭代器"})
for chunk in resp:
    print(chunk.content, end="")

# ======================================  拆分提示词模板
## ChatMessagePromptTemplate 结合 ChatPromptTemplate 使用，同时对提示词模板和消息体进行抽象和复用；
# from langchain_ollama import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate, ChatMessagePromptTemplate

# if __name__ == "__main__":
#     llm = ChatOllama(
#         model="deepseek-r1:8b",
#         temperature=0,
#         )
# # 系统模板
# ststem_message_template = ChatMessagePromptTemplate.from_template(
#     template = "你是一位{role}专家，擅长回答{domain}领域的问题。",
#     role="system"
# )
# # 用户模板
# human_message_template = ChatMessagePromptTemplate.from_template(
#     template = "用户问题:{question}",
#     role="user"
# )

# # 创建提示词模板
# chat_prompt_template = ChatPromptTemplate.from_messages([
#     ststem_message_template,
#     human_message_template,
# ])
# # 给提示词模板变量赋值
# propmt = chat_prompt_template.format_messages(
#     role="编程", 
#     domain="Web开发", 
#     question="你擅长什么？"
# )
# print("=============提示词开始=============")
# print(propmt)
#     # resp = llm.invoke(messages)
#     # print(resp)
# resp = llm.stream(propmt)
# for chunk in resp:
#     print(chunk.content, end="")





# ====================================== 未拆分提示词
# from langchain_ollama import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate

# if __name__ == "__main__":
#     llm = ChatOllama(
#         model="deepseek-r1:8b",
#         temperature=0,
#         )

#     messages = [
#     ("system", "You are a helpful assistant that translates English to French. Translate the user sentence."),
#     ("human", "I love programming."),
# ]
# # 创建提示词模板
# chat_prompt_template = ChatPromptTemplate.from_messages([
#     ("system", "你是一位{role}专家，擅长回答{domain}领域的问题。"),
#     ("user", "用户问题:{question}"),
# ])
# # 给提示词模板变量赋值
# propmt = chat_prompt_template.format_messages(
#     role="编程", 
#     domain="Web开发", 
#     question="如何使用Python进行Web开发？"
# )
# print("=============提示词开始=============")
# print(propmt)
# resp = llm.stream(propmt)
# for chunk in resp:
#     print(chunk.content, end="")
