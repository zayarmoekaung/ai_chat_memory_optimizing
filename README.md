# AI Chat Memory Optimizing

## Overview

This project is designed to test the concepts for optimizing prompts for an AI chatbot client. The main goal is to minimize token size while preventing or reducing memory loss. The chatbot operates in a persistent world where characters have long-term memories and identities that evolve over time.

## Features

- **Dynamic Character Management**: Characters can be created and updated with reflections and facts.
- **Prompt Optimization**: Utilizes various prompts to guide the AI's responses while minimizing token usage.
- **Memory Maintenance**: Regularly updates character reflections and extracts important facts to ensure memory retention.
- **Web Interface**: Provides a simple web interface to visualize events and character states.

## Project Structure

```
source/
├── app.py                # Main application file
├── world.db              # SQLite database for storing character data
├── agents/               # Contains agent-related logic
│   └── kobold.py         # Interface for interacting with the Kobold API
├── controllers/          # Contains route handlers for the web interface
│   ├── events.py
│   └── home.py
├── database/             # Database connection and initialization
│   └── db.py
├── helpers/              # Utility functions
│   ├── json_helper.py    # JSON extraction helper
│   └── memory_helper.py   # Memory management functions
├── prompts/              # Prompt templates for the AI
│   ├── __init__.py       # Loads prompt templates
│   ├── decide_action.txt # Prompt for deciding actions
│   ├── extract_facts.txt # Prompt for extracting facts
│   ├── system.txt        # System prompt for character context
│   └── update_reflection.txt # Prompt for updating character reflections
└── templates/            # HTML templates for the web interface
    └── index.html
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai_chat_memory_optimizing
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python source/app.py
   ```

4. Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage

- Characters are initialized with basic personalities and can evolve through interactions.
- The chatbot generates responses based on the current state of the world, including character reflections and recent events.
- The web interface displays the timeline of events and character information.

## Prompt Management

The project includes a module for managing prompts used by the AI chatbot. The prompts are loaded dynamically from text files, allowing for easy updates and modifications. 

### Prompt Loader

The `load_prompt` function is defined in `source/prompts/__init__.py`:

```python
# filepath: ai_chat_memory_optimizing/source/prompts/__init__.py
def load_prompt(name): 
    return open(f"prompts/{name}").read()

SYSTEM_PROMPT = load_prompt("system.txt")
DECIDE_PROMPT = load_prompt("decide_action.txt")
FACT_PROMPT = load_prompt("extract_facts.txt")
REFLECT_PROMPT = load_prompt("update_reflection.txt")
```

#### Prompts Loaded

- **SYSTEM_PROMPT**: Loaded from `system.txt`, this prompt provides the context for the AI's behavior and personality.
- **DECIDE_PROMPT**: Loaded from `decide_action.txt`, this prompt helps the AI determine its next actions based on the current state.
- **FACT_PROMPT**: Loaded from `extract_facts.txt`, this prompt is used to extract relevant facts from the conversation.
- **REFLECT_PROMPT**: Loaded from `update_reflection.txt`, this prompt allows the AI to update its reflections based on interactions.

This modular approach to prompt management ensures that the chatbot can be easily adapted and improved over time.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License.