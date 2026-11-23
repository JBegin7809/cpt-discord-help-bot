# CPT Discord Help Bot
# CPT 273 - Process Automation and Shell Scripting
# Final Project
# Jeffrey Begin & Alan Crawford

# libraries
import os
import logging
import discord
import asyncio
from dotenv import load_dotenv
from ollama_client import get_ollama_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Discord bot configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# Enable temporary responses while the AI API is unavailable
TEST_MODE = os.getenv("TEST_MODE", "true").lower() == "true"


# Configure Discord bot permissions
intents = discord.Intents.default()
intents.message_content = True

# Create the Discord bot client
client = discord.Client(intents=intents)

# Split long AI responses at natural break points
def split_message(text, max_length=2000):
    # Return an empty list if there is no text
    if not text:
        return []

    # Validate the maximum message length
    if max_length <= 0:
        raise ValueError("Maximum length must be positive")

    chunks = []

    while len(text) > max_length:
        # Prefer splitting at a line break
        split_at = text.rfind("\n", 0, max_length)

        # Otherwise, split at a space
        if split_at <= 0:
            split_at = text.rfind(" ", 0, max_length)

        # Fall back to the character limit
        if split_at <= 0:
            split_at = max_length
        else:
            split_at += 1

        # Store the chunk and preserve the remaining text
        chunks.append(text[:split_at])
        text = text[split_at:]

    # Add the remaining text
    if text:
        chunks.append(text)

    return chunks

# Event triggered when the bot connects to Discord
@client.event
async def on_ready():
    logger.info("Discord bot connected successfully")
    logger.info("Logged in as: %s", client.user)


# Event triggered when a message is received in Discord
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Check if the message starts with the !ask command
    if message.content == "!ask" or message.content.startswith("!ask "):
        # Remove the command and extract the question
        question = message.content[5:].strip()

        # Check if the student provided a question
        if not question:
            await message.channel.send(
                "Please include a question after !ask."
            )
            return

        # Log that a question was received
        logger.info("Received a student question")

        # Respond using test mode or the AI
        if TEST_MODE:
            # Temporary response without contacting Ollama
            await message.channel.send(
            "Your question was received! Running in test mode."
        )
        else:
            # Send the question to Ollama without blocking Discord
            try:
                response = await asyncio.to_thread(
                get_ollama_response, question
                )

                # Handle empty AI responses
                if not response or not response.strip():
                    await message.channel.send(
                        "The AI did not return a response. Please try again."
                )
                else:
                    # Split long AI responses into Discord-sized messages
                    for chunk in split_message(response):
                        await message.channel.send(chunk)

            except Exception:
                # Log unexpected errors
                logger.exception("Unexpected error processing AI response")

                # Notify the student
                await message.channel.send(
                    "Sorry, an unexpected error occurred. Please try again later."
                )



# Start the Discord bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN is not configured in the .env file.")
    else:
        client.run(DISCORD_TOKEN)