 
from docutils.nodes import address
from langchain_core.tools import tool 
from langchain_groq import ChatGroq      # ✓ Fix 1: correct class name 
from langgraph.prebuilt import create_react_agent  # ✓ Fix 3: correct import 
from langgraph.checkpoint.memory import InMemorySaver 
from langchain_core.messages import HumanMessage 
from dotenv import load_dotenv 
from typing import List 
 
 
 
 
 
llm = ChatGroq( 
    model="llama-3.3-70b-versatile",  # ✓ Fix 2: valid Groq model 
    temperature=0.7 
)
 
 
 
@tool # ✓ Fix 4: no () on 

def user_info(user_name: str) -> str: 
    """Get user profile info by username. Known users: hrithik, rohan, neha, pratik, suraj""" 
    users = { 
        "hrithik": "name: Hrithik Hadawale, age: 24, number: 1234567890, address: Pune", 
        "rohan":   "name: Rohan Hadawale, age: 22, number: 1234567890, address: Pune", 
        "neha":    "name: Neha Mahale, age: 20, number: 1234567890, address: Pune", 
        "pratik":  "name: Pratik Hadawale, age: 26, number: 1234567890, address: Pune", 
        "suraj":   "name: Suraj, age: 28, number: 1234567890, address: Pune", 
    }
    return users.get(user_name.lower(), "User not found. Valid: hrithik, rohan, neha, pratik, suraj") 

@tool 
def products() -> List[str]: 
    """Get the full list of available products in the store.""" 
    return ["laptop", "mobile", "tablet", "headphones", "smartwatch"] 
 
@tool 
def order_history(user_name: str) -> List[str]: 
    """Get the order history for a specific user by username.""" 
    orders = { 
        "hrithik": ["laptop", "mobile"], 
        "rohan":   ["tablet", "headphones"], 
        "neha":    ["smartwatch", "laptop"], 
        "pratik":  ["mobile", "tablet"], 
        "suraj":   ["headphones", "smartwatch"]
    return orders.get(user_name.lower(), []),  # returns [] if not found 
 
 
checkpointer = InMemorySaver()  # ✓ Fix 7: memory storage 
 
agent = create_react_agent(  # ✓ Fix 3: correct function 
    model=llm, 
    tools=[user_info, products, order_history], 
    checkpointer=checkpointer  # ✓ Fix 7: pass checkpointer 
)
 
 
 
 
config = {"configurable": {"thread_id": "session_001"}}  # ✓ Fix 8 
 
 
response = agent.invoke( 
    {"messages": [HumanMessage(content="What is the order history of hrithik?")]}, 
    config=config 
)
print(response["messages"][-1].content) 
 
 
response2 = agent.invoke( 
    {"messages": [HumanMessage(content="What products are available?")]}, 
    config=config 
)
print(response2["messages"][-1].content) 