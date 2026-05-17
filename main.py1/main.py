 
from google.auth.transport import requests
from docutils.nodes import address
from langchain_core.tools import tool 
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver 
from langchain_core.messages import HumanMessage 
from dotenv import load_dotenv 
from typing import List 
from langchain_groq import ChatGroq 

import os



load_dotenv()
 
system_prompt = """
<ROLE>
You are a helpful assistant for ecommerce company "SURAJ CARE",
your job is to answer user queries based on the available tools.
your goal is to help the user to get the best answer.
</ROLE>

<Chain-of-Thought>
Always think step by step and use the available tools to get the best answer.
first check which tools are needed to answer the user query
then use the tools to get the best answer
then answer the user query
</Chain-of-Thought>

<COMPANY_INFO>
Our company address is in New York, usa
Our company email is suraj@gmail.com
</COMPANY_INFO>

<CONSTRAINTS>
Respond only in english.
if question is asked in hindi then translate it in english and then answer 
</CONSTRAINTS>

<TOOLS_INFO>
    user_info tool provides user information
    products tool provides list of products
    order_history tool provides order history of user
    internet_searrch_tool provides information from the internet
</TOOLS_INFO>



<OUTPUT_FORMAT>
    Respond in the following format:
    - user_info
    - products
    - order_history
    - date
</OUTPUT_FORMAT>
"""

 
@tool()
def user_info(user_name: str) -> int:
    """ this tool provides user information """
    return 101

@tool()
def products() -> List[str]:
    """ this tool provides list of products """
    return ["laptop", "mobile", "tablet", "headphones", "smartwatch"]

@tool()
def order_history(user_name: str) -> List[str]:
    """ this tool provides order history of user """
    return ["laptop", "mobile"]

@tool
def internet_searrch_tool(query:str) ->str:
    """ this tool provides information from the internet """
    import requests
    url = "https://google.serper.dev/search"

    payload = {
    "q": "apple inc"
    }
    headers = {
  'X-API-KEY': 'a8f3febe81109ca0296a1e46153b56e5096b3b01',
  'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    return response.text

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0.7
)
 
 
memory = InMemorySaver()
agent = create_agent(
    model=llm,
    tools=[user_info, products, order_history,internet_searrch_tool],
    system_prompt=system_prompt,
    checkpointer=memory,
    
)


 
 
config = {"configurable": {"thread_id": "session_001"}}

response = agent.invoke( 
    {"messages": [{"role": "user", "content": "Which team is won yesterday match in IpL 2026? "}]}, 
    config=config 
)
print(response["messages"][-1].content) 
 
 
