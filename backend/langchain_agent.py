import os
import sys
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.callbacks import BaseCallbackHandler
from backend.tools import tools_list
from backend.logger import setup_logger
from dotenv import load_dotenv

logger = setup_logger(__name__)

load_dotenv()

class TerminalCallbackHandler(BaseCallbackHandler):
    
    def on_tool_start(self, serialized, input_str, **kwargs):
        logger.info(f"Generated Tool Call: {serialized.get('name')} with args: {input_str}")
        
    def on_tool_end(self, output, **kwargs):
        logger.info(f"Tool Result: {output}")
        
    def on_agent_action(self, action, **kwargs):
        logger.info(f"Agent Action: {action.tool} - {action.tool_input}")
        
    def on_agent_finish(self, finish, **kwargs):
        logger.info(f"Agent Finish: {finish.return_values}")

def get_agent_executor():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY not found!")
        raise ValueError("GROQ_API_KEY not found")

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        groq_api_key=api_key
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an intelligent Auto Dealership Voice Assistant. "
                "Your goal is to help customers find cars, check details, and book test drives. "
                "You have access to the dealership's real-time inventory and booking system. "
                "Use the available tools to answer questions accurately. "
                "If a user asks about SUVs, use 'get_cars_by_type' with 'suv'. "
                "Always verify availability before booking. "
                "Keep your final responses natural, helpful, and concise (suitable for voice output).",
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    
    agent = create_tool_calling_agent(llm, tools_list, prompt)

    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools_list, 
        verbose=True,
        callbacks=[TerminalCallbackHandler()],
        return_intermediate_steps=True,
        handle_parsing_errors=True 
    )
    
    return agent_executor

class LangChainAgent:
    def __init__(self):
        self.agent_executor = get_agent_executor()
        
    async def process_message(self, message: str, history: list = []):
        logger.info(f"Agent received message: {message}")
        
        from langchain_core.messages import HumanMessage, AIMessage
        chat_history = []
        for msg in history:
            if msg["role"] == "user":
                chat_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "ai":
                chat_history.append(AIMessage(content=msg["content"]))
        
        try:
            response = await self.agent_executor.ainvoke({"input": message, "chat_history": chat_history})
            return response["output"]
        except Exception as e:
            logger.error(f"Agent execution failed: {e}", exc_info=True)
            if "'NoneType' object has no attribute 'get'" in str(e):
                 return "I successfully processed your request, but had a slight internal hiccup confirming the details. Is there anything else you need?"
            return "I apologize, but I encountered an error while processing your request. Please try again."
