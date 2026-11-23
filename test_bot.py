# CPT Discord Help Bot
# Local testing for Discord message handling

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from bot import client, split_message


async def test_ask_command():
    # Create a simulated Discord message
    message = MagicMock()
    message.author = MagicMock()
    message.content = "!ask What is a Python function?"
    message.channel.send = AsyncMock()

        # Simulate the bot's identity
    with patch.object(
        type(client), "user", new_callable=lambda: MagicMock()
    ):
        # Process the simulated message
        await client.on_message(message)

            # Verify that the bot responded correctly
    message.channel.send.assert_awaited_once_with(
        "Your question was received! Running in test mode."
    )

    print("PASS: !ask command received the expected test response")

async def test_empty_question():
    # Create a simulated Discord message without a question
    message = MagicMock()
    message.author = MagicMock()
    message.content = "!ask"
    message.channel.send = AsyncMock()

    # Simulate the bot's identity
    with patch.object(
        type(client), "user", new_callable=lambda: MagicMock()
    ):
        await client.on_message(message)

    # Verify that the bot requests a question
    message.channel.send.assert_awaited_once_with(
        "Please include a question after !ask."
    )

    print("PASS: Empty question handled correctly")

async def test_regular_message():
    # Create a regular Discord message
    message = MagicMock()
    message.author = MagicMock()
    message.content = "Hello everyone!"
    message.channel.send = AsyncMock()

    # Simulate the bot's identity
    with patch.object(
        type(client), "user", new_callable=lambda: MagicMock()
    ):
        await client.on_message(message)

    # Verify that the bot did not respond
    message.channel.send.assert_not_awaited()

    print("PASS: Regular messages are ignored correctly")

async def test_bot_own_message():
    # Create a simulated message
    message = MagicMock()
    message.content = "!ask What is Python?"
    message.channel.send = AsyncMock()

    # Simulate the bot's identity
    bot_user = MagicMock()
    message.author = bot_user

    with patch.object(type(client), "user", new=bot_user):
        await client.on_message(message)

    # Verify the bot ignored its own message
    message.channel.send.assert_not_awaited()

    print("PASS: Bot ignores its own messages")

async def test_ai_integration():
    # Create a simulated student question
    message = MagicMock()
    message.author = MagicMock()
    message.content = "!ask What is Python?"
    message.channel.send = AsyncMock()

    # Simulate an AI response without contacting Ollama
    with (
        patch.object(type(client), "user", new=MagicMock()),
        patch("bot.TEST_MODE", False),
        patch(
            "bot.get_ollama_response",
            return_value="Python is a programming language."
        )
    ):
        await client.on_message(message)

    # Verify that Discord received the AI response
    message.channel.send.assert_awaited_once_with(
        "Python is a programming language."
    )

    print("PASS: Discord and AI integration works correctly")

async def test_ai_error():
    # Create a simulated student question
    message = MagicMock()
    message.author = MagicMock()
    message.content = "!ask What is Python?"
    message.channel.send = AsyncMock()

    # Simulate an unexpected AI error
    with (
        patch.object(type(client), "user", new=MagicMock()),
        patch("bot.TEST_MODE", False),
        patch(
            "bot.get_ollama_response",
            side_effect=RuntimeError("Simulated AI failure")
        )
    ):
        await client.on_message(message)

    # Verify that the student receives an error message
    message.channel.send.assert_awaited_once_with(
        "Sorry, an unexpected error occurred. Please try again later."
    )

    print("PASS: AI errors are handled correctly")

def test_split_message():
    # Create a simulated AI response with 4,500 characters
    long_response = "A" * 4500

    # Split the response into Discord-sized messages
    chunks = split_message(long_response)

    # Verify that three messages were created
    assert len(chunks) == 3

    # Verify the size of each message
    assert len(chunks[0]) == 2000
    assert len(chunks[1]) == 2000
    assert len(chunks[2]) == 500

    # Verify no text was lost
    assert "".join(chunks) == long_response

    print("PASS: Long AI responses are split correctly")

async def test_long_ai_response():
    # Create a simulated student question
    message = MagicMock()
    message.author = MagicMock()
    message.content = "!ask Explain Python programming"
    message.channel.send = AsyncMock()

    # Simulate a long AI response
    long_response = "A" * 4500

    with (
        patch.object(type(client), "user", new=MagicMock()),
        patch("bot.TEST_MODE", False),
        patch("bot.get_ollama_response", return_value=long_response)
    ):
        await client.on_message(message)

    # Verify that Discord receives three separate messages
    assert message.channel.send.await_count == 3

    # Verify each message contains the correct text
    message.channel.send.assert_any_await("A" * 2000)
    message.channel.send.assert_any_await("A" * 500)

    print("PASS: Long AI responses are sent in multiple messages")

async def test_empty_ai_response():
    # Create a simulated student question
    message = MagicMock()
    message.author = MagicMock()
    message.content = "!ask What is Python?"
    message.channel.send = AsyncMock()

    # Simulate an empty AI response
    with (
        patch.object(type(client), "user", new=MagicMock()),
        patch("bot.TEST_MODE", False),
        patch("bot.get_ollama_response", return_value="")
    ):
        await client.on_message(message)

    # Verify the bot sends a helpful message
    message.channel.send.assert_awaited_once_with(
        "The AI did not return a response. Please try again."
    )

    print("PASS: Empty AI responses are handled correctly")

# Run all automated tests
if __name__ == "__main__":
    asyncio.run(test_ask_command())
    asyncio.run(test_empty_question())
    asyncio.run(test_regular_message())
    asyncio.run(test_bot_own_message())
    asyncio.run(test_ai_integration())
    asyncio.run(test_ai_error())
    test_split_message()
    asyncio.run(test_long_ai_response())
    asyncio.run(test_empty_ai_response())