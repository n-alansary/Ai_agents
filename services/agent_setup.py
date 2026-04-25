import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from utils.db import db, collection

from utils.tools import get_player_profile , search_for_attributes_in_players , sort_players_list
from utils.tools import execute_mongo_query , execute_mongo_crud

from utils.prompts import SYSTEM_PROMPT ,SYSTEM_PROMPT_2 , SYSTEM_PROMPT_3
from utils.guardrails import delete_guard

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
# Creating the ai agent
# =============================================================================

checkpointer = InMemorySaver()

agent = create_agent('groq:openai/gpt-oss-120b' , tools=[execute_mongo_crud] ,
                     system_prompt=SYSTEM_PROMPT_3 , checkpointer=checkpointer, middleware=[delete_guard])




