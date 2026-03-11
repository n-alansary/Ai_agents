import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from pymongo.mongo_client import MongoClient
from langgraph.checkpoint.memory import InMemorySaver

from agent_tools.tools import get_player_profile , search_for_attributes_in_players , sort_players_list

from prompts.llm_system_prompt import SYSTEM_PROMPT


# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment")

# MongoDB connection URI
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise RuntimeError("MONGO_URI not found in environment")

# =============================================================================
# Connecting to a database
# =============================================================================
# Create a new client and connect to the server






# =============================================================================
# Creating the ai agent
# =============================================================================

if __name__ == "__main__":
    client = MongoClient(MONGO_URI)
    db = client['Sports']
    collection = db['squash']

    checkpointer = InMemorySaver()

    agent = create_agent('groq:openai/gpt-oss-120b' , tools=[get_player_profile , search_for_attributes_in_players , sort_players_list] ,
                         system_prompt=SYSTEM_PROMPT , checkpointer=checkpointer)

    while(True):
      print(80*'*')
      user_question = input('Please enter your question \n')
  
      # Run a test inference
      res = agent.invoke({"messages": [{"role": "user", "content": user_question}]} , 
                                        config={"configurable": {"collection": collection , "thread_id": "1"}})

      print(res['messages'][-1].content)
      
      

