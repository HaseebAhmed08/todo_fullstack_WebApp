# Feature: AI Chatbot (Phase III)
 
## Objective
Enable users to manage their tasks using natural language via an AI chatbot.

## User Stories
- As a user, I can type "Add a task to buy groceries" and the chatbot creates it.
- As a user, I can ask "What are my pending tasks?" and the chatbot lists them.
- As a user, I can say "Mark the grocery task as done" and the chatbot updates it.

## Technical Approach
- **Frontend**: A floating chat widget or a dedicated sidebar.
- **Backend**: Integration with an LLM (e.g., Gemini 2.0 Flash) using MCP (Model Context Protocol) or custom tools.
- **Tools**:
  - `list_tasks`: Retrieves user tasks (filtered by user_id).
  - `create_task`: Adds a new task.
  - `update_task`: Modifies status or details.
  - `delete_task`: Removes a task.

## UI/UX
- Real-time streaming response.
- Task "chips" or cards within the chat for quick interaction.
- Toggle for voice input (optional).
