# Project Spec: Google Antigravity SDK Agent Examples

## Objective
This project contains a collection of example agents built using the Google Antigravity (AGY) SDK. The goals are:
1. Demonstrate how to build single-purpose local agents with custom system instructions.
2. Demonstrate how to integrate custom tools (using Python functions) with an agent.
3. Demonstrate how to integrate custom skills (specified in a `SKILL.md` markdown guideline format) with an agent.
4. Demonstrate how to enforce structured outputs using Pydantic schemas.

The project currently contains two agent examples:
1. **Birthdate Luck Agent**: Analyzes a birthdate, applies numerology/astrology rules via its skill, and returns structured recommendations (pet name, lucky color, and quote).
2. **Multi-Country Postal Information Assistant**: Interactively queries a user for a country (India or US), validates the input, uses the corresponding postal API tool, and formats the output via markdown.

## Tech Stack
* **Python**: 3.10+
* **Dependencies**:
  * `google-antigravity` (AGY SDK)
  * `pydantic` (for structured outputs)
  * `urllib` (standard library, for API requests)
  * `json` (standard library)

## Commands
* **Run Birthdate Agent**:
  ```bash
  python birthdate_agent.py
  ```
* **Run Pincode Agent**:
  ```bash
  python pincode_agent.py
  ```

## Project Structure
```
.gitignore
.env                       -> Environment secrets (GEMINI_API_KEY)
config.json                -> Configuration parameters for APIs
birthdate_agent.py         -> Execution entry point for Birthdate Luck Agent
pincode_agent.py           -> Execution entry point for Postal Code Agent
skills/                    -> Folder containing guidelines/rules for agents
  birthdate_luck/
    SKILL.md               -> Guideline for birthdate analysis and output
  pincode_lookup/
    SKILL.md               -> Guideline for country validation and formatting
specs/                     -> Specifications folder (Spec-Driven Development)
  SPEC.md                  -> General workspace specification
  birthdate_luck_agent.md  -> Tech spec for the birthdate luck agent
  pincode_lookup_agent.md  -> Tech spec for the pincode lookup agent
```

## Code Style
* Follow standard PEP 8 naming conventions.
* Type annotations should be used for all function definitions.
* Docstrings must follow the Google style guide.
* Standard Python asynchronous pattern (`async`/`await`) for AGY SDK interactions.

Example snippet:
```python
async def main():
    config = LocalAgentConfig(
        tools=[get_india_postal_details],
        skills_paths=[pincode_skill_dir],
        system_instructions="You are a helpful postal assistant..."
    )
    async with Agent(config) as agent:
        response = await agent.chat("Start the conversation")
        ...
```

## Testing Strategy
* *Note: Currently, there is no automated test framework set up.*
* **Verification**:
  * Visual check by running the scripts manually.
  * Validation of input formats (errors returned on empty inputs or invalid pincodes).
  * Check that output meets the guidelines defined in the skills (Pydantic schema structure for birthdate, markdown tables/bullets for pincode).

## Boundaries
* **Always**: 
  * Keep `.env` and sensitive `config.json` configurations local (in `.gitignore`).
  * Run agents inside `async with Agent(config)` context managers to ensure cleanup.
  * Keep agent instructions aligned with the skill definitions.
* **Ask first**:
  * Modifying the API endpoints used in `config.json`.
  * Adding new external packages.
* **Never**:
  * Check in API keys or credentials to Git.
  * Edit files inside `.venv`.

## Success Criteria
* Both agents run successfully and interact via the terminal.
* Birthdate agent returns structured JSON output parsing to `PetResponse`.
* Pincode agent resolves zipcodes/pincodes to respective details via external APIs.
