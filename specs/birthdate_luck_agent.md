# Spec: Birthdate Luck Agent

## Objective
Implement a fun, intuitive agent that accepts a user's birthdate (in `YYYY-MM-DD` format) and generates personalized luck attributes.

## Tech Stack
* Python 3.10+
* `google-antigravity`
* `pydantic`

## Specifications
* **Input**: A string representing a birthdate (formatted as `YYYY-MM-DD`).
* **Persona**: The agent acts as a fun and intuitive guide.
* **Skill Integration**:
  * The agent relies on the `birthdate_luck` skill located in `skills/birthdate_luck`.
  * The skill provides rules for zodiac sign traits, numerology values, and seasonal associations to guide the analysis.
* **Structured Output Schema**:
  * Must conform to the `PetResponse` schema:
    * `petname` (str): A creative, symbolic pet name matching the astrological/zodiac element or personality traits.
    * `color` (str): A lucky or representative color.
    * `quote` (str): An inspiring, custom quote combining zodiac and numerology traits.

## Commands
* Run the agent interface:
  ```bash
  python birthdate_agent.py
  ```

## Boundaries
* **Always**: 
  * Validate that input is not empty before invoking the agent.
  * Retrieve the structured output utilizing `response.structured_output()`.
* **Ask first**:
  * Changing the properties or fields of `PetResponse`.
* **Never**:
  * Allow empty input queries to trigger the model chat.

## Success Criteria
* Asking the agent for a birth date returns a valid structured dictionary matching the `PetResponse` fields.
* The script outputs formatted Pet Name, Lucky Color, and Quote properties correctly in the terminal.
