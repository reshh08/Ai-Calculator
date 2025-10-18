from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
import gradio as gr

load_dotenv()

@tool(description= "calculate math expression like '2 * 2' or '10 * 5'")
def calculator(expression :str)-> str:
  try: return str(eval(expression))
  except: return 'invalid expression'

def calculate(message: str, history: list) -> str:
  llm =ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
  system_message ="""you are a helpfull assistant
                  use the calculator tool when you need to perform calculations"""
  prompt= ChatPromptTemplate.from_messages(
       [("system",system_message),
        ("human","{input}"),
        ("placeholder","{agent_scratchpad}")])
  agent = create_tool_calling_agent(llm,[calculator],prompt)
  executor = AgentExecutor(agent=agent,tools=[calculator],verbose=True)
  result = executor.invoke({"input":message})
  return result["output"]

# step 6
PAGE_TITLE = "Caramel AI from HERE AND NOW AI !"
LOGO_URL = "https://raw.githubusercontent.com/hereandnowai/images/refs/heads/main/logos/logo-of-here-and-now-ai.png"
ASSISTANT_AVATAR_URL = "https://raw.githubusercontent.com/hereandnowai/images/refs/heads/main/logos/caramel-face.jpeg"

description_md = f"""<img src='{LOGO_URL}' width='500' style='display: block; margin: auto;'>
                     <br>Your friendly AI teacher for learning the basics of Artificial Intelligence!"""

gr.ChatInterface(
    fn = calculate,
    title = PAGE_TITLE,
    description = description_md,
    chatbot = gr.Chatbot(
        type='messages',
        avatar_images=[None,ASSISTANT_AVATAR_URL]),
    type ='messages'
).launch()
