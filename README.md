# CPT Discord Help Bot

## Project Overview

CPT Discord Help Bot is a CPT 273 Process Automation project for the Fall 2026 semester, developed by Jeff Begin and Alan Crawford.

The goal is to create a Python-based Discord bot that uses Ollama to communicate with a locally hosted Large Language Model (LLM) to help students understand programming concepts and course material. The bot will be designed to connect to the school's local AI server when it becomes available.

Students will be able to ask questions through a designated Discord channel and receive educational explanations. The bot is intended to support learning rather than complete assignments for students.

## Project Status

**Current Status:** Proposal submitted; awaiting final instructor approval.

**Planned Completion Date:** December 6, 2026

Development will begin after the project proposal has been approved.

## Project Team

- Jeff Begin
- Alan Crawford

**Course:** CPT 273 – Process Automation  
**Semester:** Fall 2026

## Project Features

- Receive student questions through a designated Discord channel.
- Send questions to a locally hosted LLM through the Ollama API.
- Return educational responses to Discord.
- Explain programming concepts, syntax, and functions.
- Include error handling for Ollama connection failures and server errors.
- Maintain logs for troubleshooting.
- Protect Discord bot credentials and configuration settings using environment variables.
- Test mode for development without contacting the Ollama server.
- Automatic splitting of long Discord responses.
- Preserve Markdown formatting when splitting responses.
- Display a typing indicator while the AI processes questions.
- Configurable per-user request cooldown to prevent spam.
- Concurrent AI request protection to prevent server overload.
- Prevent overlapping AI requests from individual students.
- Automatically release active request slots after AI processing.
- Automated testing to verify bot functionality and error handling.

### Optional Features

If time permits, we would like to add support for different locally hosted models through Ollama and improve conversation handling.

## Technical Stack

- **Operating System:** Linux
- **Programming Language:** Python
- **Discord Integration:** discord.py
- **LLM Integration:** Ollama API with a locally hosted LLM
- **Environment Variables:** python-dotenv
- **Logging:** Python logging module
- **Version Control:** Git and GitHub
- **Development Environment:** VS Code
- **Deployment:** Linux VM or container within the cpt.internal network, connecting to the school's local AI server running Ollama when available

## Configuration

The bot uses a `.env` file to manage credentials and
configuration settings. An `.env.example` file is provided
as a configuration template.

### Request Cooldown

The bot limits how frequently individual students can
submit questions.

`REQUEST_COOLDOWN=10`

- The default cooldown is 10 seconds.
- Each student has an independent cooldown.
- Rejected requests do not reset the cooldown.
- Invalid or missing values default to 10 seconds.
- Setting the value to 0 disables the cooldown.

### Concurrent Request Protection

The bot limits the number of simultaneous AI requests
to prevent overloading the Ollama server.

`MAX_CONCURRENT_REQUESTS=1`

- The default limit is one simultaneous AI request.
- Students cannot submit overlapping AI requests.
- Requests exceeding the configured limit are rejected.
- Rejected requests do not trigger a new cooldown.
- Active request slots are automatically released after
  successful, failed, or empty AI responses.
- Invalid or missing configuration values default to 1.
- Concurrent request protection is bypassed in test mode.

## Project Documentation

The completed project will include installation, configuration, troubleshooting, and maintenance instructions. This will include instructions for connecting the Discord bot to the locally hosted Ollama server.

Documentation will also be added to the UVDesk knowledgebase to help future students and administrators maintain and expand the bot.

## Project Proposal

The completed project proposal is available in this repository:

[View Project Proposal](proposal.md)

## Project Timeline

| Phase | Dates | Description |
|---|---|---|
| 1 | Nov 8–14 | Research Ollama and available locally hosted LLM models, and plan the bot |
| 2 | Nov 15–21 | Develop the Discord bot and connect it to the Ollama API |
| 3 | Nov 22–24 | Configure and refine the LLM system prompt |
| 4 | Nov 25–29 | Test functionality and improve error handling |
| 5 | Nov 30–Dec 3 | Complete documentation and prepare presentation |
| 6 | Dec 4–6 | Final review, demonstration, and submission |

## Future Development

The project will be designed so future students can maintain the bot, update its configuration, and potentially integrate additional locally hosted LLM models through Ollama.

## Important Notice

This bot is intended to provide educational assistance. Students should verify AI-generated information and should not submit personal or sensitive information through the bot.

The project must receive instructor approval before implementation begins.

---

## Original Instructor Template Instructions

The following instructions were provided with the original
CPT Project Proposal Template and are retained for reference.

---

# Technical Project Proposal Template

This repository contains the required materials for submitting a project proposal
for upper-level Computer Technology courses and Capstone projects.

## Purpose
This proposal is used to:
- Evaluate project fit and scope
- Assess technical readiness
- Approve or redirect project direction before implementation begins

## Instructions
1. **Fork this repository** - please name it what you intend on naming your final project as **this will be your project repository**.  You can make this private if you'd like, but you'll need to invite at least myself to it.
3. Complete the `proposal.md` file.
4. Commit all changes with clear commit messages
5. Submit the repository URL via Brightspace if part of an assignment, or send it to me via email or discord message if you are undertaking this for extra credit.
6. **Do not get started on this project until your proposal has been approved!**

> Proposals are evaluated on clarity, feasibility, technical understanding, and planning.  While ambition is certainly a factor you need to demonstrate you have the understanding and capacity to complete the project!

## Notes
- This proposal is considered a *living document* until approval
- Once approved, scope changes require instructor review as while this readme SHOULD be updated your proposal will live with your final repository in perpetuity!
