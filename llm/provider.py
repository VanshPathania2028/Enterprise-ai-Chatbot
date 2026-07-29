from ollama import Client

from config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL
)

from utils.logger import logger


# Create Ollama client
client = Client(
    host=OLLAMA_BASE_URL
)


def generate_response(prompt: str) -> str:
    """
    Send a prompt to Ollama and return the generated response.
    """

    try:
        logger.info("=" * 60)
        logger.info("Starting Ollama Request")
        logger.info(f"Model: {OLLAMA_MODEL}")
        logger.info(f"Prompt: {prompt}")

        response = client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response["message"]["content"]

        logger.info("Ollama response received successfully.")
        logger.info(f"Response Length: {len(answer)} characters")
        logger.info("=" * 60)

        return answer

    except Exception as e:
        logger.exception("Error while communicating with Ollama")
        raise