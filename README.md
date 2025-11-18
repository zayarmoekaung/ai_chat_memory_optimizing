# AI Chat Memory Optimizing

## Overview

AI Chat Memory Optimizing is a project that explores optimizing prompts for AI chatbot clients, focusing on minimizing token size while preventing memory loss. This toolkit enables dynamic character management and prompt optimization to sustain long-term chatbot interactions without significant loss of context.

## Features

- **Dynamic Character Management:** Create and update characters with evolving reflections and facts.
- **Prompt Optimization:** Use modular prompts to guide AI responses while minimizing token usage.
- **Memory Maintenance:** Regular character reflection updates and fact extraction for robust contextual memory.
- **Web Interface:** A simple interface to visualize events and character states.

## Project Structure

```
source/
├── app.py                  # Main application file
├── world.db                # SQLite database for storing character data
├── agents/
│   └── kobold.py           # Interface for Kobold API
├── controllers/
│   ├── events.py
│   └── home.py
├── database/
│   └── db.py
├── helpers/
│   ├── json_helper.py      # JSON extraction helper
│   └── memory_helper.py    # Memory management functions
├── prompts/
│   ├── __init__.py         # Loads prompt templates
│   ├── decide_action.txt   # Prompt for deciding actions
│   ├── extract_facts.txt   # Prompt for extracting facts
│   ├── system.txt          # System prompt for context
│   └── update_reflection.txt # Reflection prompt
└── templates/
    └── index.html
```

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd ai_chat_memory_optimizing
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    python source/app.py
    ```
4. Open your browser to `http://127.0.0.1:5000`.

## Usage

- Characters are initialized with personalities and evolve with interactions.
- Responses are generated based on the world's state, including reflections and events.
- The web interface displays events and character information.

## Prompt Management

Prompts for the AI are loaded dynamically from text files in the `source/prompts/` directory. This structure allows for easy modification and addition of new prompt templates.

Example prompt loader (`prompts/__init__.py`):
```python
def load_prompt(name): 
    return open(f"prompts/{name}").read()

SYSTEM_PROMPT = load_prompt("system.txt")
DECIDE_PROMPT = load_prompt("decide_action.txt")
FACT_PROMPT = load_prompt("extract_facts.txt")
REFLECT_PROMPT = load_prompt("update_reflection.txt")
```

### Loaded Prompts

- **system.txt:** Main context for AI behavior
- **decide_action.txt:** Determines next actions from state
- **extract_facts.txt:** Extracts facts from conversations
- **update_reflection.txt:** Updates character reflections

## Contributing

Contributions, issues, and feature requests are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
