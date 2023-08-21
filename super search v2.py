import os
from langchain.chat_models import ChatOpenAI 
from langchain.schema import ( AIMessage, HumanMessage, SystemMessage )
import requests
import openai
from bs4 import BeautifulSoup
from IPython.display import Image, display
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS


# Set your API keys
API_KEY = "谷歌KEY"  
SEARCH_ENGINE_ID = "谷歌引擎ID"
os.environ["OPENAI_API_KEY"] = "OpenAI 秘钥"
# Define the GPT-3 model
MODEL = "gpt-3.5-turbo" 

# Create a chat model
chat = ChatOpenAI(model_name=MODEL)


# 定义谷歌搜索函数  
def searchGoogle(query):
    page = 1
    start = (page - 1) * 10 + 1
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}" 
    data = requests.get(url).json()
    return data["items"][:1]



# 定义获取页面内容函数  
# 定义获取页面内容函数  
def getWebPageContent(url):
    try:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        
        web_page_text = {}
        title_tag = soup.find("title")
        title_text = title_tag.get_text()
        web_page_text["title"] = title_text
        
        p_tags = soup.find_all("p")
        p_text = ""
        for p_tag in p_tags:
            p_text += p_tag.get_text()
        web_page_text["content"] = p_text
        
        return web_page_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# 主循环
def main():
    messages = []
    system_message = SystemMessage(content="")
    
    while True:
        query = input("You: "+ "\n")
        if query == "quit":
            break

        human_message = HumanMessage(content=query)
        messages.append(system_message)
        messages.append(human_message)
        embeddings = OpenAIEmbeddings()
        results = searchGoogle(query)
        texts=[]
        for result in results:
            page = getWebPageContent(result['link'])
            # 检查 page 是否为 None
            if page is not None:
                text_splitter = CharacterTextSplitter(        
                    separator = "\n",
                    chunk_size = 200,
                    chunk_overlap  = 50,
                    length_function = len,
                )
                search = page['title'] + "\n" + page['content']
                
                chunk_size = 100
                search = [search[i:i+chunk_size] for i in range(0, len(search), chunk_size)]

                
                texts.extend(search)
                
    
                if "pagemap" in result:
                    pagemap = result["pagemap"]
                    if "cse_image" in pagemap:
                      cse_image = pagemap["cse_image"]
                      if "src" in cse_image[0]:
                        image_url = cse_image[0]["src"]
                        print(image_url)
                        image = Image(url=image_url)
                        display(image)
                        

                print(result['title']) 
                print(result['link'])
                print(result['snippet'])

        docsearch = FAISS.from_texts(texts, embeddings)
        docs = docsearch.similarity_search(query)       
        docs0=str(docs)       
                

        # 删除旧的 SystemMessage
        messages = [message for message in messages if not isinstance(message, SystemMessage)]
        
        # 添加新的 SystemMessage
        system_message.content = """你是一个搜索专家，可以根据system中搜索到的信息给用户提供帮助"""+docs0
        messages.append(system_message)
        
        """
        print(messages)
        print(len(docs))         
        print(len(texts))        
        print("search:")
        print(search)
        print("text:")
        print(texts)
        print("docs:")
        print(docs)
        print("context:")
        print(context)
        """
        
        response = chat(messages)
        print("超级搜索AI: " + response.content+ "\n")

        ai_message = AIMessage(content=response.content)
        messages.append(ai_message)            
main()

