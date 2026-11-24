# CPT Discord Help Bot
# Local testing for Discord message handling

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from bot import (
    client,
    split_message,
    split_markdown_message,
    get_remaining_cooldown,
    record_user_request,
    user_cooldowns,
    get_request_cooldown,
)


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

def test_split_at_line_break():
    # Create a response containing a line break
    response = "Python is useful.\nPython supports automation."

    # Split using a smaller limit for testing
    chunks = split_message(response, max_length=25)

    # Verify the first message ends at the line break
    assert chunks[0] == "Python is useful.\n"

    # Verify all messages are within the limit
    assert all(len(chunk) <= 25 for chunk in chunks)

    # Verify no text was lost
    assert "".join(chunks) == response

    print("PASS: Messages split at natural line breaks")

def test_split_at_word_boundary():
    # Create a response without line breaks
    response = "Python is a useful programming language."

    # Split using a smaller limit for testing
    chunks = split_message(response, max_length=20)

    # Verify that words are not split
    assert chunks[0] == "Python is a useful "
    assert chunks[1] == "programming "
    assert chunks[2] == "language."

    # Verify all messages are within the limit
    assert all(len(chunk) <= 20 for chunk in chunks)

    # Verify no text was lost
    assert "".join(chunks) == response

    print("PASS: Messages split at word boundaries")

def test_split_message_edge_cases():
    # Test an empty response
    assert split_message("") == []

    # Test a short response
    assert split_message("Hello") == ["Hello"]

    # Test a response exactly at the Discord limit
    response = "A" * 2000
    assert split_message(response) == [response]

    # Test a response one character over the limit
    response = "A" * 2001
    assert split_message(response) == ["A" * 2000, "A"]

    # Test an invalid maximum length
    try:
        split_message("Hello", max_length=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")

    print("PASS: Message splitting edge cases handled correctly")

# Test Markdown splitting with regular text
def test_markdown_plain_text():
    response = "Python is a useful programming language."

    # Compare Markdown splitting with standard splitting
    chunks = split_markdown_message(response, max_length=20)

    expected = split_message(response, max_length=20)

    # Verify that both functions produce the same result
    assert chunks == expected

    # Verify that no text was lost
    assert "".join(chunks) == response

    print("PASS: Markdown splitting preserves regular text")

# Test Markdown splitting with a short Python code block
def test_markdown_short_code_block():
    response = '```python\nprint("Hello, world!")\n```'

    # Process the Markdown response
    chunks = split_markdown_message(response)

    # Verify that only one message was created
    assert len(chunks) == 1

    # Verify that the original formatting was preserved
    assert chunks[0] == response

    # Verify the Discord character limit
    assert len(chunks[0]) <= 2000

    print("PASS: Short Markdown code blocks are preserved")

# Test Markdown splitting with a long Python code block
def test_markdown_long_code_block():
    # Create a long Python code example
    code = 'print("Hello, world!")\n' * 200
    response = "```python\n" + code + "```"

    # Process the long Markdown response
    chunks = split_markdown_message(response)

    # Verify that multiple messages were created
    assert len(chunks) > 1

    # Verify each message stays within Discord's limit
    assert all(len(chunk) <= 2000 for chunk in chunks)

    # Verify each message has opening and closing fences
    for chunk in chunks:
        assert chunk.startswith("```python\n")
        assert chunk.endswith("```")

    print("PASS: Long Markdown code blocks are split correctly")

# Test Markdown splitting with multiple programming languages
def test_markdown_multiple_languages():
    languages = ["python", "bash", "sql", "javascript"]

    for language in languages:
        # Create a long code block
        code = "Example code line\n" * 200
        response = "```" + language + "\n" + code + "```"

        # Process the Markdown response
        chunks = split_markdown_message(response)

        # Verify that multiple messages were created
        assert len(chunks) > 1

        # Verify formatting and character limits
        for chunk in chunks:
            assert chunk.startswith("```" + language + "\n")
            assert chunk.endswith("```")
            assert len(chunk) <= 2000

    print("PASS: Multiple programming languages are preserved")

# Test Markdown splitting with an unfinished code block
def test_markdown_unclosed_code_block():
    # Create a response without a closing code fence
    response = '```python\nprint("Hello, world!")'

    # Process the unfinished Markdown response
    chunks = split_markdown_message(response)

    # Verify that only one message was created
    assert len(chunks) == 1

    # Verify that the missing code fence was added
    assert chunks[0] == response + "\n```"

    # Verify the Discord character limit
    assert len(chunks[0]) <= 2000

    print("PASS: Unfinished Markdown code blocks are closed")

# Test Markdown splitting with mixed text and code
def test_markdown_mixed_content():
    # Create a response containing explanations and code
    introduction = "Here is a Python example:\n\n"
    code = 'print("Hello, world!")\n' * 200
    conclusion = "\n\nThis code demonstrates the print function."

    response = introduction + "```python\n" + code
    response += "```" + conclusion

    # Process the Markdown response
    chunks = split_markdown_message(response)

    # Verify that multiple messages were created
    assert len(chunks) > 1

    # Verify that the introduction and conclusion remain
    assert chunks[0].startswith(introduction)
    assert chunks[-1].endswith(conclusion)

    # Verify message lengths and balanced code fences
    for chunk in chunks:
        assert len(chunk) <= 2000
        assert chunk.count("```") % 2 == 0
        
    print("PASS: Mixed text and code blocks are handled correctly")

# Test Markdown splitting preserves complete code lines
def test_markdown_code_line_preservation():
    # Create a Python code block with multiple lines
    code_line = 'print("Hello, world!")\n'
    code = code_line * 200
    response = "```python\n" + code + "```"

    # Process the Markdown response
    chunks = split_markdown_message(response)

    # Verify that multiple messages were created
    assert len(chunks) > 1

    # Verify that complete lines of code are preserved
    recovered_code = ""

    for chunk in chunks:
        assert len(chunk) <= 2000
        assert chunk.startswith("```python\n")
        assert chunk.endswith("```")

        # Remove the Markdown code fences
        content = chunk[len("```python\n"):-3]

        # Verify each line remains complete
        for line in content.splitlines():
            assert line == code_line.rstrip("\n")

        recovered_code += content

    # Verify that no code was lost or duplicated
    assert recovered_code == code

    print("PASS: Complete lines of code are preserved")

# Test Markdown integration with Discord message handling
async def test_markdown_integration():
    # Create a simulated Discord message
    message = MagicMock()
    message.author = MagicMock()
    message.content = "!ask How does Python print work?"
    message.channel.send = AsyncMock()

    # Create a long Markdown AI response
    code = 'print("Hello, world!")\n' * 200
    response = "```python\n" + code + "```"

    # Simulate the Discord bot and AI response
    with patch.object(
        type(client), "user", new_callable=lambda: MagicMock()
    ), patch(
        "bot.TEST_MODE", False
    ), patch(
        "bot.get_ollama_response", return_value=response
    ):
        await client.on_message(message)

    # Retrieve the messages sent to Discord
    chunks = [
        call.args[0]
        for call in message.channel.send.await_args_list
    ]

    # Verify that multiple messages were sent
    assert len(chunks) > 1

    # Verify Markdown formatting and message lengths
    for chunk in chunks:
        assert len(chunk) <= 2000
        assert chunk.startswith("```python\n")
        assert chunk.endswith("```")

    # Verify that no code was lost or duplicated
    recovered_code = "".join(
        chunk[len("```python\n"):-3]
        for chunk in chunks
    )

    assert recovered_code == code

    print("PASS: Discord Markdown integration works correctly")

# Test Discord typing indicator during AI processing
async def test_typing_indicator():
    # Create a simulated Discord message
    message = MagicMock()
    message.author = MagicMock()
    message.content = "!ask What is Python?"
    message.channel.send = AsyncMock()

    # Create a simulated typing context manager
    typing_context = MagicMock()
    typing_context.__aenter__ = AsyncMock()
    typing_context.__aexit__ = AsyncMock(return_value=False)

    message.channel.typing.return_value = typing_context

    # Simulate the Discord bot and AI response
    with patch.object(
        type(client), "user", new_callable=lambda: MagicMock()
    ), patch(
        "bot.TEST_MODE", False
    ), patch(
        "bot.get_ollama_response",
        return_value="Python is a programming language."
    ):
        await client.on_message(message)

    # Verify that the typing indicator was activated
    message.channel.typing.assert_called_once()

    # Verify that the typing context started and stopped
    typing_context.__aenter__.assert_awaited_once()
    typing_context.__aexit__.assert_awaited_once()

    # Verify that the AI response was sent
    message.channel.send.assert_awaited_once_with(
        "Python is a programming language."
    )

    print("PASS: Discord typing indicator works correctly")

# Test typing indicator cleanup during an AI failure
async def test_typing_indicator_error():
    # Create a simulated Discord message
    message = MagicMock()
    message.author = MagicMock()
    message.content = "!ask What is Python?"
    message.channel.send = AsyncMock()

    # Create a simulated typing context manager
    typing_context = MagicMock()
    typing_context.__aenter__ = AsyncMock()
    typing_context.__aexit__ = AsyncMock(return_value=False)

    message.channel.typing.return_value = typing_context

    # Simulate an unexpected AI failure
    with patch.object(
        type(client), "user", new_callable=lambda: MagicMock()
    ), patch(
        "bot.TEST_MODE", False
    ), patch(
        "bot.get_ollama_response",
        side_effect=RuntimeError("Simulated AI failure")
    ):
        await client.on_message(message)

    # Verify that the typing indicator was activated
    message.channel.typing.assert_called_once()

    # Verify that the typing context started and stopped
    typing_context.__aenter__.assert_awaited_once()
    typing_context.__aexit__.assert_awaited_once()

    # Verify that the student received an error message
    message.channel.send.assert_awaited_once()
    error_message = message.channel.send.await_args.args[0]
    assert "unexpected error" in error_message.lower()

    print("PASS: Typing indicator stops during AI failures")

# Test that a student's first request has no cooldown
def test_cooldown_first_request():
    user_id = 1001

    # Isolate cooldown tracking for this test
    with patch.dict(user_cooldowns, {}, clear=True):

        # Verify that a new student has no cooldown
        remaining = get_remaining_cooldown(user_id)

        assert remaining == 0.0

    print("PASS: First request has no cooldown")

# Test that a recent request activates the cooldown
def test_cooldown_active():
    user_id = 1001

    # Isolate cooldown tracking and configuration
    with patch.dict(user_cooldowns, {}, clear=True), patch(
        "bot.REQUEST_COOLDOWN", 10
    ):
        # Simulate the student's first request
        with patch("bot.time.monotonic", return_value=100.0):
            record_user_request(user_id)

        # Simulate another request three seconds later
        with patch("bot.time.monotonic", return_value=103.0):
            remaining = get_remaining_cooldown(user_id)

        # Verify that seven seconds remain
        assert remaining == 7.0

    print("PASS: Active cooldown is calculated correctly")

# Test that the cooldown expires correctly
def test_cooldown_expired():
    user_id = 1001

    # Isolate cooldown tracking and configuration
    with patch.dict(user_cooldowns, {}, clear=True), patch(
        "bot.REQUEST_COOLDOWN", 10
    ):
        # Simulate the student's first request
        with patch("bot.time.monotonic", return_value=100.0):
            record_user_request(user_id)

        # Verify cooldown expires at exactly ten seconds
        with patch("bot.time.monotonic", return_value=110.0):
            assert get_remaining_cooldown(user_id) == 0.0

        # Verify expired cooldown does not become negative
        with patch("bot.time.monotonic", return_value=115.0):
            assert get_remaining_cooldown(user_id) == 0.0

    print("PASS: Cooldown expires correctly")

# Test that students have independent cooldowns
def test_cooldown_independent_users():
    first_user = 1001
    second_user = 1002

    # Isolate cooldown tracking and configuration
    with patch.dict(user_cooldowns, {}, clear=True), patch(
        "bot.REQUEST_COOLDOWN", 10
    ):
        # Record the first student's request
        with patch("bot.time.monotonic", return_value=100.0):
            record_user_request(first_user)

        # Verify the second student is not affected
        with patch("bot.time.monotonic", return_value=103.0):
            assert get_remaining_cooldown(first_user) == 7.0
            assert get_remaining_cooldown(second_user) == 0.0

            # Record the second student's request
            record_user_request(second_user)

        # Verify both students have independent cooldowns
        with patch("bot.time.monotonic", return_value=105.0):
            assert get_remaining_cooldown(first_user) == 5.0
            assert get_remaining_cooldown(second_user) == 8.0

    print("PASS: Student cooldowns are independent")

# Test that repeated requests are rejected during cooldown
async def test_cooldown_repeated_request():
    # Create a simulated Discord message
    message = MagicMock()
    message.author = MagicMock()
    message.author.id = 1001
    message.content = "!ask What is Python?"
    message.channel.send = AsyncMock()

    # Isolate cooldown tracking and configuration
    with patch.dict(user_cooldowns, {}, clear=True), patch(
        "bot.REQUEST_COOLDOWN", 10
    ), patch(
        "bot.TEST_MODE", True
    ), patch.object(
        type(client), "user", new_callable=lambda: MagicMock()
    ):
        # Process the student's first request
        await client.on_message(message)

        # Verify the first request was accepted
        message.channel.send.assert_awaited_once_with(
            "Your question was received! Running in test mode."
        )

        # Reset the simulated message history
        message.channel.send.reset_mock()

        # Process an immediate second request
        await client.on_message(message)

        # Verify the second request was rejected
        message.channel.send.assert_awaited_once()
        response = message.channel.send.await_args.args[0]

        assert "Please wait" in response
        assert "before asking another question" in response

    print("PASS: Repeated requests are rejected during cooldown")

# Test that rejected requests do not reset the cooldown
async def test_cooldown_rejection_no_reset():
    # Create a simulated Discord message
    message = MagicMock()
    message.author = MagicMock()
    message.author.id = 1001
    message.content = "!ask What is Python?"
    message.channel.send = AsyncMock()

    # Isolate cooldown tracking and configuration
    with patch.dict(user_cooldowns, {}, clear=True), patch(
        "bot.REQUEST_COOLDOWN", 10
    ), patch(
        "bot.TEST_MODE", True
    ), patch.object(
        type(client), "user", new_callable=lambda: MagicMock()
    ):
        # Process the student's first request
        with patch("bot.time.monotonic", return_value=100.0):
            await client.on_message(message)

        # Store the original request timestamp
        original_time = user_cooldowns[1001]

        # Reset the simulated message history
        message.channel.send.reset_mock()

        # Submit another request three seconds later
        with patch("bot.time.monotonic", return_value=103.0):
            await client.on_message(message)

        # Verify that the request was rejected
        message.channel.send.assert_awaited_once_with(
            "Please wait 7.0 seconds "
            "before asking another question."
        )

        # Verify that the original timestamp was preserved
        assert user_cooldowns[1001] == original_time

        # Verify that the cooldown expires as originally scheduled
        with patch("bot.time.monotonic", return_value=110.0):
            assert get_remaining_cooldown(1001) == 0.0

    print("PASS: Rejected requests do not reset cooldown")

# Test that empty questions do not trigger a cooldown
async def test_cooldown_empty_question():
    # Create a simulated Discord message
    message = MagicMock()
    message.author = MagicMock()
    message.author.id = 1001
    message.content = "!ask"
    message.channel.send = AsyncMock()

    # Isolate cooldown tracking and configuration
    with patch.dict(user_cooldowns, {}, clear=True), patch(
        "bot.REQUEST_COOLDOWN", 10
    ), patch(
        "bot.TEST_MODE", True
    ), patch.object(
        type(client), "user", new_callable=lambda: MagicMock()
    ):
        # Process the empty question
        await client.on_message(message)

        # Verify that the student received a warning
        message.channel.send.assert_awaited_once_with(
            "Please include a question after !ask."
        )

        # Verify that no cooldown was recorded
        assert 1001 not in user_cooldowns
        assert get_remaining_cooldown(1001) == 0.0

        # Reset the simulated message history
        message.channel.send.reset_mock()

        # Submit a valid question
        message.content = "!ask What is Python?"
        await client.on_message(message)

        # Verify that the valid question was accepted
        message.channel.send.assert_awaited_once_with(
            "Your question was received! Running in test mode."
        )

        # Verify that the valid request triggered a cooldown
        assert 1001 in user_cooldowns

    print("PASS: Empty questions do not trigger cooldown")

# Test that requests are accepted after cooldown expiration
async def test_cooldown_request_after_expiration():
    # Create a simulated Discord message
    message = MagicMock()
    message.author = MagicMock()
    message.author.id = 1001
    message.content = "!ask What is Python?"
    message.channel.send = AsyncMock()

    # Isolate cooldown tracking and configuration
    with patch.dict(user_cooldowns, {}, clear=True), patch(
        "bot.REQUEST_COOLDOWN", 10
    ), patch(
        "bot.TEST_MODE", True
    ), patch.object(
        type(client), "user", new_callable=lambda: MagicMock()
    ):
        # Process the student's first request
        with patch("bot.time.monotonic", return_value=100.0):
            await client.on_message(message)

        # Verify the first request was accepted
        message.channel.send.assert_awaited_once_with(
            "Your question was received! Running in test mode."
        )

        # Reset the simulated message history
        message.channel.send.reset_mock()

        # Submit another request after cooldown expiration
        with patch("bot.time.monotonic", return_value=110.0):
            await client.on_message(message)

            # Verify that a new cooldown was activated
            assert get_remaining_cooldown(1001) == 10.0

        # Verify that the second request was accepted
        message.channel.send.assert_awaited_once_with(
            "Your question was received! Running in test mode."
        )

        # Verify that the request timestamp was updated
        assert user_cooldowns[1001] == 110.0

    print("PASS: Requests are accepted after cooldown expiration")

# Test valid request cooldown configuration values
def test_cooldown_valid_configuration():
    # Define valid configuration values and expected results
    valid_values = {
        "10": 10.0,
        "5.5": 5.5,
        "0": 0.0,
        "30": 30.0,
    }

    # Verify each valid configuration value
    for value, expected in valid_values.items():
        with patch.dict(
            "os.environ", {"REQUEST_COOLDOWN": value}
        ):
            assert get_request_cooldown() == expected

    print("PASS: Valid cooldown configuration values are accepted")

# Test invalid request cooldown configuration values
def test_cooldown_invalid_configuration():
    # Define invalid configuration values
    invalid_values = [
        "-10",
        "-0.5",
        "abc",
        "",
        "inf",
        "-inf",
        "nan",
    ]

    # Verify each invalid configuration value
    for value in invalid_values:
        with patch.dict(
            "os.environ", {"REQUEST_COOLDOWN": value}
        ):
            # Verify the default cooldown is returned
            assert get_request_cooldown() == 10.0

    print("PASS: Invalid cooldown values use the default")

# Test missing request cooldown configuration
def test_cooldown_missing_configuration():
    # Simulate a missing environment variable
    with patch.dict("os.environ", {}, clear=True):

        # Verify the default cooldown is returned
        assert get_request_cooldown() == 10.0

    print("PASS: Missing cooldown configuration uses the default")

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
    test_split_at_line_break()
    test_split_at_word_boundary()
    test_split_message_edge_cases()
    test_markdown_plain_text()
    test_markdown_short_code_block()
    test_markdown_long_code_block()
    test_markdown_multiple_languages()
    test_markdown_unclosed_code_block()
    test_markdown_mixed_content()
    test_markdown_code_line_preservation()
    asyncio.run(test_markdown_integration())
    asyncio.run(test_typing_indicator())
    asyncio.run(test_typing_indicator_error())
    test_cooldown_first_request()
    test_cooldown_active()
    test_cooldown_expired()
    test_cooldown_independent_users()
    asyncio.run(test_cooldown_repeated_request())
    asyncio.run(test_cooldown_rejection_no_reset())
    asyncio.run(test_cooldown_empty_question())
    asyncio.run(test_cooldown_request_after_expiration())
    test_cooldown_valid_configuration()
    test_cooldown_invalid_configuration()
    test_cooldown_missing_configuration()