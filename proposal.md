# Project Proposal

## 1. Project Identification
- Project Title: cpt-discord-help-bot
- Course: CPT 273
- Term: Fall 2026
- Student Name(s): Jeff Begin, Alan Crawford
- Primary Contact: Project 1 – Group 1 Channel
- Proposed Start Date: November 1, 2026
- Proposed End Date: December 6, 2026

---

### Revision History

- **November 16, 2026:** Updated the proposed project architecture to target Ollama for local AI processing, based on instructor feedback.

---

## 2. Project Selection & Motivation
We as a team chose this idea because of the relevance and availability of large language models. We both have interest in working more with them for our careers and believe this project would aid us in gaining experience in both LLMs and integrating them into user environments. Our team has experience with utilizing Python to manipulate data and publish via Discord web-hooks, so we know where to start. We also have experience with setting up LLMs to fulfill a specified purpose for its user, with one of us having taken Introduction to AI Applications as a class.
This project also aligns with our interest in software development and automation. It will give us hands-on experience working with APIs, integrating AI into applications, and developing a tool that other students can use. We believe these skills will be valuable in future coursework and careers in information technology.

---

## 3. Problem Statement
Students sometimes need additional help understanding course material, especially when working on assignments outside of class. They may have questions about programming concepts, syntax, or functions when an instructor or another student is not available to help.
Our project would address this need by providing a Discord chatbot that students can use to ask basic questions and receive explanations. The goal is to help students better understand the material and work through problems on their own rather than having the chatbot complete their assignments. This could also provide a foundation for future projects and improvements.

---

## 4. Proposed Solution Overview
Our proposed project is to develop a Python-based Discord bot that allows students to ask questions about course material through a designated Discord channel. The bot will receive messages, send questions to an LLM through the Ollama API, and return responses to the channel. The LLM will be configured to provide educational guidance, such as explaining programming concepts, syntax, and functions, without providing complete assignment solutions. Our initial goal is to create a fully functional bot that communicates with Ollama. The program will include basic error handling for failed requests and connection issues. The bot will be designed to connect to a locally hosted Ollama server within the CPT network once the school's AI server becomes available. The initial project will not include generating complete assignments or advanced features such as managing multiple conversations across different channels. If time permits, we would like to explore support for additional LLM APIs.

---

## 5. Technical Stack & Tools

- **Operating System(s):** Linux, using the environment provided within the CPT network.
- **Programming Language(s):** Python.
- **Frameworks / Libraries:** discord.py for receiving and responding to Discord messages, requests or the Ollama Python library for communicating with the locally hosted LLM, python-dotenv for managing environment variables, and Python's built-in logging module for troubleshooting.
- **Databases / Storage:** Local log files for errors and program activity. A database is not planned for the initial project.
- **Infrastructure (VMs, containers, etc.):** A Linux virtual machine or container hosted within the cpt.internal network. The bot will connect to the designated Discord server and communicate with Ollama running on the school's local AI server once it becomes available.
- **Tools (Git, CI, monitoring, APIs, etc.):** Git and GitHub for version control, VS Code for development, Discord for testing, Ollama for generating AI responses, and Python logging for monitoring and troubleshooting.

We will organize the Python program into manageable components and provide documentation explaining how to install, configure, troubleshoot, and update the bot. Configuration settings, including the Ollama server address and Discord bot credentials, will be stored separately from the source code to make the project easier to maintain and more secure.


---

## 6. Prerequisite Knowledge & Skills
  I (Alan Crawford) have worked with setting up system prompts with LLMs before to ensure output stays appropriate to the project's purpose. I am taking Intro to AI Applications and have experience through Process Automation and Capstone of creating code to handle sending and receiving data. I will need to sharpen my skills on prompting to ensure our LLM of choice responds within our guidelines. Other than that, I feel comfortable taking on the coding work that will come with building the Python program for this project.

  I (Jeff Begin) have experience using Python, APIs, JSON data, automation, and Discord webhooks through previous coursework in Process Automation. I also have experience working with Linux, virtual machines, logging, error handling, and scheduling tasks using CRON. These skills will help me develop and troubleshoot the Python program for this project. I would like to learn more about LLM APIs, Discord bots, and how to securely integrate them.


---

## 7. Project Scope & Deliverables
**Minimum Viable Product (MVP):**
A fully functioning Python Discord bot that can receive questions from students, send them to an LLM through the Ollama API, and return responses to a designated Discord channel. The bot will provide educational explanations rather than complete assignment solutions and include basic error handling.

**Required Deliverables:**
The completed Python program, LLM system prompt, GitHub repository containing the source code, installation and configuration documentation, testing results, weekly team meeting minutes, and a final presentation demonstrating the working bot.

**Optional Stretch Goals:**
If time permits, we would like to improve conversation handling, explore additional features that could make the bot more useful to students, and expand support for different locally hosted models through Ollama.

---

## 8. Milestones & Timeline
Phase 1 (Nov 8–14): Research Ollama and available locally hosted LLM models, and plan the Discord bot.

Phase 2 (Nov 15–21): Develop the Python Discord bot and connect it to the Ollama API.

Phase 3 (Nov 22–24): Configure and refine the LLM system prompt to provide appropriate educational responses.

Phase 4 (Nov 25–29): Test the bot, troubleshoot issues, and improve error handling.

Phase 5 (Nov 30–Dec 3): Complete documentation, prepare the presentation, and perform final testing.

Phase 6 (Dec 4–6): Review the completed project, demonstrate the working bot, and submit all required materials.

---

## 9. Risks, Constraints & Dependencies
The largest technical risks for this project are the availability of the school's local AI server, connection failures with Ollama, and possible issues with Discord bot permissions. We will need to include error handling and logging to identify and troubleshoot these problems. The performance of the locally hosted LLM may also depend on the available server hardware.

Another challenge is the limited time available to complete the project before December 6, 2026. To manage this, we will focus on developing a working Discord bot that communicates with Ollama before attempting additional features.

The project will also depend on receiving Discord bot credentials, having access to the CPT network, and being able to connect to a locally hosted Ollama server. Since the school's AI server is not currently available, we will plan for alternative testing methods, such as a temporary local Ollama installation or simulated API responses. We will test these connections as early as possible and work with our instructor if access or permission issues arise.

---

## 10. Security, Ethics & Safety Considerations
  The main security concerns for this project involve protecting Discord bot credentials, student information, and connections to the locally hosted Ollama server. We will store Discord bot credentials and configuration settings in environment variables rather than directly in the Python code. The bot will only be given the Discord permissions needed to function.

Since the bot will operate within the CPT network and communicate with a locally hosted Ollama server, we will follow the network access requirements provided by our instructor. We will inform students that their questions are processed by the school's local AI server and remind them not to share personal or sensitive information.

We will use logging to monitor errors and troubleshoot problems while avoiding the unnecessary collection of student information. The bot will also be configured to provide educational explanations rather than complete assignment solutions. Since LLMs can sometimes provide incorrect information, students will be encouraged to verify answers and use the bot as a learning tool rather than a replacement for their instructor.

---

## 11. Team Structure (If Applicable)
  Alan Crawford and Jeff Begin will work together to develop, test, and document the Discord bot. We will divide responsibilities based on our experience and the needs of the project, with both team members contributing to development and troubleshooting.

  We will communicate through Discord and meet at least once a week to discuss progress, assign tasks, and address any problems. We will document our meetings and submit meeting minutes as required by the instructor.

  If disagreements arise, we will discuss possible solutions and work toward an agreement. If necessary, we will ask our instructor for guidance. We will divide the workload as evenly as possible and use GitHub to track our progress and contributions.

---

## 12. Documentation & Knowledge Transfer Plan
  We will document our Python code and the LLM system prompts used by the Discord bot. Our GitHub repository will include a README.md file explaining the project's purpose, requirements, installation, configuration, and basic usage.

We will also provide instructions for deploying and maintaining the bot within the CPT network, including how to configure environment variables, troubleshoot common errors, and configure the connection to the locally hosted Ollama server. We will document these procedures in the UVDesk knowledgebase so future students and administrators can access them.

The program will be organized to make it easier for future students to understand, maintain, and expand. Our documentation will explain how the main components work together and how additional locally hosted models through Ollama or other features could be added in the future.

---

## 13. Faculty/cpt.internal Resources Requested
- VM Access
- Internet Access
- Access to the CPT internal network for development and deployment.
- Discord bot token credentials provided by the instructor.
- A dedicated Discord channel for testing and communicating with the bot.
- Access to the school's local AI server running Ollama once it becomes available.
- Permission to install required Python libraries and run the bot on the assigned VM or container.
- UVDesk knowledgebase access, if additional permissions are required.
- No additional hardware is expected to be required beyond the school's existing AI server and assigned development environment.

---

## 14. Acknowledgement of Expectations
By submitting this proposal, I acknowledge that:
- This is a self-directed technical project
- I am responsible for research and troubleshooting
- Evaluation will consider process, documentation, and professionalism

**Signature (Name & Date):**

Student 1:   Alan Crawford III           Date: 11/6/2026

Student 2:  Jeff Begin                   Date: 11/7/2026

Instructor: ____________________________ Date: _______________
