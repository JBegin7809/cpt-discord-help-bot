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

# Split AI responses while preserving Markdown formatting
def split_markdown_message(text, max_length=2000):
    # Return an empty list if there is no text
    if not text:
        return []

    # Validate the maximum message length
    if max_length <= 0:
        raise ValueError("Maximum length must be positive")

    # Check whether the response contains Markdown code fences
    if "```" not in text:
        return split_message(text, max_length)

    # Initialize Markdown message tracking
    chunks = []
    current_chunk = ""
    inside_code_block = False
    code_language = ""

    # Close an unfinished Markdown code block
    def close_code_block(chunk):
        if chunk.endswith("\n"):
            return chunk + "```"

        return chunk + "\n```"

    # Reopen a Markdown code block with its original language
    def reopen_code_block(language):
        return "```" + language + "\n"

    # Calculate the remaining space in the current message
    def available_space(chunk, in_code_block):
        remaining = max_length - len(chunk)

        # Reserve space for closing Markdown code fences
        if in_code_block:
            remaining -= 4

        return remaining

    # Finalize the current message and prepare the next one
    def finalize_chunk():
        nonlocal current_chunk

        # Ignore empty messages
        if not current_chunk:
            return

        if inside_code_block:
            # Close the current code block
            chunks.append(close_code_block(current_chunk))

            # Reopen the code block in the next message
            current_chunk = reopen_code_block(code_language)
        else:
            # Save the current message and reset it
            chunks.append(current_chunk)
            current_chunk = ""

    # Separate the response into lines while preserving line breaks
    lines = text.splitlines(keepends=True)

    # Process each line of the response
    for line in lines:
        stripped_line = line.strip()

        # Detect Markdown code fences
        if stripped_line.startswith("```"):
            if not inside_code_block:
                # Store the programming language
                code_language = stripped_line[3:].strip()

                # Ensure the opening fence leaves room for content
                if len(line) + 4 >= max_length:
                    raise ValueError("Code fence exceeds message limit")

                # Start a new message if there is insufficient space
                if len(current_chunk) + len(line) + 4 >= max_length:
                    finalize_chunk()

                # Add the opening code fence
                current_chunk += line
                inside_code_block = True

            else:
                # Add the closing code fence
                if len(current_chunk) + len(line) > max_length:
                    finalize_chunk()

                current_chunk += line
                inside_code_block = False
                code_language = ""

            continue

                # Process regular text and code block content
        while line:
            remaining = available_space(
                current_chunk, inside_code_block
            )

            # Start a new message when no space remains
            if remaining <= 0:
                finalize_chunk()

                remaining = available_space(
                    current_chunk, inside_code_block
                )

                # Prevent an infinite loop
                if remaining <= 0:
                    raise ValueError("Insufficient message space")

            # Add the entire line if it fits
            if len(line) <= remaining:
                current_chunk += line
                break

            # Preserve complete lines when possible
            if inside_code_block:
                opening_fence = reopen_code_block(code_language)

                # Check whether the line fits in a new code block
                if (
                    current_chunk != opening_fence
                    and len(line) <= available_space(opening_fence, True)
                ):
                    finalize_chunk()
                    continue

            elif current_chunk:
                finalize_chunk()
                continue

            # Split lines that exceed the available space
            current_chunk += line[:remaining]
            line = line[remaining:]

            # Finalize the message and prepare the next one
            finalize_chunk()

    # Save the final message
    if current_chunk:
        if inside_code_block:
            chunks.append(close_code_block(current_chunk))
        else:
            chunks.append(current_chunk)

    # Return all completed Discord messages
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
                # Display typing indicator while the AI processes the question
                async with message.channel.typing():
                    response = await asyncio.to_thread(
                        get_ollama_response, question
                    )

                # Handle empty AI responses
                if not response or not response.strip():
                    await message.channel.send(
                        "The AI did not return a response. Please try again."
                )
                else:
                    # Split AI responses while preserving Markdown formatting
                    for chunk in split_markdown_message(response):
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