
# CPT Discord Help Bot
# Ollama API Integration
# Jeff Begin & Alan Crawford

# Libraries
import os
import logging
import httpx

from ollama import Client, ResponseError
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "")


# Create the Ollama API client
ollama_client = Client(
    host=OLLAMA_HOST,
    timeout=30.0
)

# Send a question to Ollama and return the AI response
def get_ollama_response(question):
    # Check that a model has been configured
    if not OLLAMA_MODEL:
        logger.warning("No Ollama model has been configured")
        return "The AI model has not been configured yet."

 
    # Send the question to Ollama
    try:
        response = ollama_client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        # Extract the AI response
        answer = response.message.content

        return answer

    except ResponseError as error:
        logger.error("Ollama API error: %s", error)
        return "The AI server returned an error. Please try again later."

    except httpx.RequestError as error:
        logger.error("Ollama connection error: %s", error)
        return "Unable to connect to the AI server. Please try again later."

    except Exception:
        logger.exception("Unexpected error communicating with Ollama")
        return "An unexpected error occurred. Please try again later."

