import os
from dotenv import load_dotenv
from langchain.agents import create_agent
import asyncio
from pymongo import AsyncMongoClient
from langgraph.checkpoint.memory import InMemorySaver

from agent_tools.tools import get_player_profile , search_for_attributes_in_players , sort_players_list

from agent_tools.tools import execute_mongo_query , execute_mongo_crud

from prompts.llm_system_prompt import SYSTEM_PROMPT ,SYSTEM_PROMPT_2 , SYSTEM_PROMPT_3
from agent_middleware.guardrails import delete_guard

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

client = AsyncMongoClient(MONGO_URI)
db = client['Sports']
collection = db['squash']

checkpointer = InMemorySaver()

agent = create_agent('groq:openai/gpt-oss-120b' , tools=[execute_mongo_crud] ,
                     system_prompt=SYSTEM_PROMPT_3 , checkpointer=checkpointer, middleware=[delete_guard])


if __name__ == "__main__":

    async def main():
        while(True):
          print(80*'*')
          user_question = input('Please enter your question \n')
      
          # Run a test inference
          res = await agent.ainvoke({"messages": [{"role": "user", "content": user_question}]} , 
                                            config={"configurable": {"collection": collection , "thread_id": "1"}})
    
          print(res['messages'][-1].content)
          
    asyncio.run(main())

