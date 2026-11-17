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