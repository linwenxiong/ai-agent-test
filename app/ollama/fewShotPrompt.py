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

# 当文件被直接运行时：__name__ = "__main__"
# 当文件被导入作为模块时：__name__ = 文件名（不含.py）
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