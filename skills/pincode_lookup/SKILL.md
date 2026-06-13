---
name: pincode_lookup
description: "Guidelines and instructions for lookup of postal codes (pincodes and ZIP codes) for India and the United States."
---

# Pincode and ZIP Code Lookup Skill

This skill guides the agent on how to retrieve and format postal code information for **India** and the **United States**.

## Operational Guidelines

### 1. Country Selection First
* The agent **must** ask the user for the country first (supporting "India" and "United States" / "US" / "USA").
* Do not attempt to query any postal code without knowing the target country first.

### 2. Validation & Tool Routing
Depending on the country chosen by the user, validate the code and call the correct tool:

* **India**:
  * Validation: Must be a 6-digit numeric string (e.g., `560001`).
  * Tool to use: `get_india_postal_details(pincode)`
  
* **United States**:
  * Validation: Must be a 5-digit numeric string (e.g., `90210`).
  * Tool to use: `get_us_postal_details(zipcode)`

### 3. Formatting Guidelines

* **India Output**:
  * List the matching post office names, branch types, district, state, and delivery status.
  * Use a clean markdown table.
  
* **United States Output**:
  * List the matching place name, state, state abbreviation, and coordinates (latitude/longitude).
  * Format it clearly in a bulleted list or table.
