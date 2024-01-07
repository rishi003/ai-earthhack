from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

openai_llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
