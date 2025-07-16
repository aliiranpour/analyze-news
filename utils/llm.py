import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

def get_llm() -> ChatOpenAI:
    """
    مقداردهی مدل زبانی بر اساس تنظیمات .env و بازگرداندن شی ChatOpenAI
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY is not set in environment.")
        raise ValueError("Missing OpenAI API key.")

    model = ChatOpenAI(
        model_name=os.getenv("OPENAI_MODEL_NAME", "deepseek-chat"),
        openai_api_base=os.getenv("OPENAI_API_BASE", "https://api.avalapis.ir/v1"),
        openai_api_key=api_key,
        temperature=float(os.getenv("OPENAI_TEMPERATURE", 0.0)),
    )
    return model
