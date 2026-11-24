# CPT Discord Help Bot – Development Log

## November 17, 2026

### Work Completed

- Set up the project in Visual Studio Code on Windows.
- Installed Git and Python.
- Created and activated a Python virtual environment.
- Installed the required Python libraries: `discord.py`, `ollama`, and `python-dotenv`.
- Created `requirements.txt` to track dependencies.
- Created `.gitignore` to exclude virtual environments, credentials, cache files, and logs.
- Created `.env` for Discord and Ollama configuration.
- Created `bot.py` with logging, Discord client configuration, and the `on_ready()` event.
- Created `ollama_client.py` with Ollama configuration and a function to send questions and receive responses.
- Added basic error handling for Ollama API and connection failures.

### Problems Encountered

**PowerShell Execution Policy**

PowerShell initially prevented activation of the Python virtual environment because script execution was disabled.

**Solution:** Used a process-scoped execution policy bypass to activate the virtual environment.

**Ollama Connection**

The school's local AI server is not yet available, so the Ollama connection cannot be tested against the intended server.

**Solution:** Created configurable Ollama connection settings so the server address can be updated later.

### Testing Status

- Python libraries installed successfully.
- Discord connection has not been tested.
- Ollama API requests have not been tested.
- Error handling has been written but still needs testing.
- One VS Code warning remains to be investigated.

### Next Steps

1. Resolve the remaining VS Code warning.
2. Test the Ollama response function.
3. Test connection error handling.
4. Connect the Discord message handler to Ollama.
5. Add Alan's AI system prompts and educational restrictions.
6. Test the complete bot when Discord credentials and the Ollama server become available.

### Outstanding Dependencies

- Discord bot token from the instructor.
- Access to the school's locally hosted Ollama server.
- Confirmation of the AI model that will be used.

## November 23, 2026 – Discord Bot Development and Testing

### Work Completed
- Added Discord message handling using the `!ask` command.
- Added validation for empty questions.
- Implemented a configurable test mode.
- Connected the Discord bot to the Ollama response function.
- Added asynchronous processing and error handling.
- Added Discord token validation.
- Created `test_bot.py` for automated testing.

### Testing Results
Successfully completed six automated tests covering Discord commands, message handling, simulated AI integration, and error handling.

### Current Limitations
- Live Discord testing requires the bot token.
- Real Ollama API testing requires access to an AI server or Ollama Cloud.

### Next Steps
- Continue improving automated tests.
- Test live Discord communication when the token is available.
- Test the Ollama API when access is available.
- Prepare the bot for deployment on the school's Linux server.

## November 23, 2026 – Long AI Response Handling

### Work Completed
- Created `split_message()` to divide AI responses into messages of 2,000 characters or fewer.
- Updated Discord message handling to send long AI responses in multiple messages.
- Added error handling for empty AI responses.
- Expanded automated testing from six to nine tests.

### Testing Results
- All nine automated tests passed.
- Verified that a 4,500-character response splits into three messages (2,000, 2,000, and 500 characters).
- Verified that Discord sends all three messages in simulated testing.
- Confirmed that empty AI responses produce a helpful message.

### Next Steps
- Improve message splitting to avoid breaking words or sentences.
- Test with the live Discord bot and Ollama API when access is available.
- Continue preparing for deployment to the school's Linux server.

## November 23, 2026 – Improved AI Message Splitting

### Work Completed
- Improved the `split_message()` function to prioritize natural line breaks and word boundaries.
- Retained character-based splitting when no natural break is available.
- Preserved the original response text without losing characters.
- Added validation for invalid maximum message lengths.
- Maintained Discord's 2,000-character message limit.

### Testing Results
- Expanded automated testing from nine to twelve tests.
- Verified splitting at natural line breaks.
- Verified splitting at word boundaries.
- Verified handling of empty messages, short messages, character limits, and invalid maximum lengths.
- All twelve automated tests passed successfully.

### Next Steps
- Improve the handling of Markdown formatting and code blocks in long AI responses.
- Test the bot with live Discord and Ollama connections when access becomes available.
- Continue preparing the application for deployment to the school's Linux server.

### Markdown-Aware AI Response Handling

**Development Completed:**
- Implemented the `split_markdown_message()` function.
- Added automatic closing and reopening of Markdown code blocks across multiple Discord messages.
- Preserved programming language identifiers for syntax highlighting.
- Added support for unfinished Markdown code blocks.
- Improved handling of responses containing both explanations and code examples.
- Preserved complete lines of code whenever possible.
- Maintained Discord's 2,000-character message limit.
- Integrated Markdown-aware message splitting into the Discord `on_message()` function.

**Testing Completed:**
- Verified regular text handling.
- Tested short and long Markdown code blocks.
- Tested Python, Bash, SQL, and JavaScript language identifiers.
- Verified unfinished code block handling.
- Tested mixed text and code responses.
- Verified complete code line preservation without losing or duplicating code in the tested examples.
- Successfully tested Markdown integration using simulated Discord messages.
- Completed regression testing with all 20 automated tests passing.

**Current Status:**
- Markdown-aware response handling is implemented and locally tested.
- No errors or warnings reported by VS Code.
- Live Discord and AI API integration testing remains pending.

**Next Steps:**
- Coordinate AI API integration with Alan.
- Contact the instructor regarding Discord access and webhook requirements.
- Perform live end-to-end testing using Groq.
- Transition to the school's local Ollama server when available.