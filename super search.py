import json
import openai
import requests
import wikipedia
import os

# 设置你的OpenAI API密钥，请替换成你自己的密钥
openai.api_key = "你自己的秘钥key"

# 定义一个函数，使用Wikipedia API搜索问题的答案
# 参数：question - 一个字符串，表示要搜索的问题
# 返回值：answer - 一个字符串，表示维基百科上的答案摘要
def search_wikipedia(question):
    try:
        answer = wikipedia.summary(question, sentences=3)
        return answer
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find an answer to your question on Wikipedia."

# 定义一个函数，使用GPT API生成一些可能的问题
# 参数：topic - 一个字符串，表示要生成问题的主题
# 返回值：questions - 一个列表，包含生成的问题或搜索词

def generate_questions(messages):
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages = messages,
        temperature=0)
    return response['choices'][0]['message']['content']

# 定义一个主函数，使用GPT API和其他API来查询解释量子力学
def main():
    # 让用户输入想要查询的问题
    topic = input("Please enter your question: ")
    d={"role":"user","content":topic}
    messages = [{"role": "system","content":"Please break down the user's question into multiple related segmented English Entries suitable for searching in Wikipedia and output them in English Json format. {\"questions\": []}"}]
    messages.append(d)
    
        # 打印出用户输入的问题，并调用search_wikipedia函数来获取维基百科上的答案，并打印出来
    print(f"Question: {topic}")
    answer_wiki = search_wikipedia(topic)
    print(f"Answer from Wikipedia: {answer_wiki}")
    # 打印出一句话，表示还有更多的问题和答案关于这个主题
    print("\nHere are some more questions and answers about this topic:")
        # 调用generate_questions函数来获取一些可能的问题，并遍历这些问题，在每个问题前打印出"Question:"，
        # 并调用search_wikipedia函数来获取对应的答案，在每个答案前打印出"Answer:"。最后在每个问题和答案之间打印出一个空行。
    questions = generate_questions(messages)
    data = json.loads(questions) # 解析Json格式的字符串
    questions = data["questions"]
    print(f"{questions}")
    for q in questions:
        print(f"Question: {q}")
        answer = search_wikipedia(q)
        print(f"Answer: {answer}\n")


# 调用主函数
main()
