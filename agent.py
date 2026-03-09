import os
import json
import re
from dotenv import load_dotenv, find_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.cursor import Cursor
from langchain.agents import create_agent


from agent_tools.tools import get_player_profile , search_for_attributes_in_players , sort_players_list

from prompts.llm_system_prompt import SYSTEM_PROMPT

from mongo_data.intial_data import data1 , data2



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
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['Sports']
collection1 = db['squash']

# =============================================================================
# Data which is added inside the mongo db
# =============================================================================
# We wrap the inserts in a check to prevent duplicate documents on multiple script runs
if collection1.count_documents({}) == 0:
    collection1.insert_many(data1)

    collection1.insert_many(data2)


# =============================================================================
# Creating the ai agent
# =============================================================================

if __name__ == "__main__":
    agent = create_agent('groq:llama-3.3-70b-versatile' , tools=[get_player_profile , search_for_attributes_in_players , sort_players_list] ,
                         system_prompt=SYSTEM_PROMPT)
    

    while(True):
      print(80*'*')
      user_question = input('Please enter your question \n')
  
      # Run a test inference
      res = agent.invoke({"messages": [{"role": "user", "content": user_question}]})
      print(res['messages'][-1].content)
      
      

