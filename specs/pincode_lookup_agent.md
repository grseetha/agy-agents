# Spec: Multi-Country Postal Information Assistant

## Objective
Implement an interactive agent that assists users in looking up postal code information for India and the United States.

## Tech Stack
* Python 3.10+
* `google-antigravity`
* Standard libraries: `urllib.request`, `urllib.parse`, `json`, `os`

## Specifications
* **Configuration**:
  * Loads API endpoints from `config.json` (keys: `INDIA_POSTAL_API_URL`, `US_POSTAL_API_URL`).
* **Tools**:
  1. `get_india_postal_details(pincode: str) -> dict`: Validates pincode (6-digit numeric) and calls the Indian postal API.
  2. `get_us_postal_details(zipcode: str) -> dict`: Validates ZIP code (5-digit numeric) and calls the US postal API.
* **Skill Integration**:
  * Incorporates the `pincode_lookup` skill in `skills/pincode_lookup`.
  * Guidelines require country selection first (e.g., India or US), proper tool routing based on validation, and clean formatting (markdown table for India, bulleted list or table for US).

## Commands
* Run the interactive loop:
  ```bash
  python pincode_agent.py
  ```

## Boundaries
* **Always**:
  * Request the country name first before asking for or validating any postal codes.
  * Validate that the code matches the formatting requirements (6 digits for India, 5 digits for US) before invoking the respective API tool.
* **Ask first**:
  * Changing API providers or adding support for new countries.
* **Never**:
  * Invoke the postal tools with unvalidated or empty input values.

## Success Criteria
* The interactive loop successfully starts by greeting the user and requesting a country.
* Entering `India` followed by `560001` queries the correct tool and prints a clean markdown table.
* Entering `United States` followed by `90210` queries the correct tool and prints a bulleted list or table.
* Typing `exit` or `quit` gracefully terminates the interactive session.
