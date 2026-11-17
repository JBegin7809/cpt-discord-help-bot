# CPT Discord Help Bot
# CPT 273 - Process Automation and Shell Scripting
# Final Project
# Jeffrey Begin & Alan Crawford

# libraries
import os
import logging
import discord
from dotenv import load_dotenv

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


# Configure Discord bot permissions
intents = discord.Intents.default()
intents.message_content = True

# Create the Discord bot client
client = discord.Client(intents=intents)


# Event triggered when the bot connects to Discord
@client.event
async def on_ready():
    logger.info("Discord bot connected successfully")
    logger.info("Logged in as: %s", client.user)

