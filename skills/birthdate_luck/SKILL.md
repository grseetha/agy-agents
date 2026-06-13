---
name: birthdate_luck
description: "Guidelines and instructions for generating custom luck details (pet name, lucky color, and custom quote) based on a user's birth date."
---

# Birthdate Luck Generation Skill

This skill guides the agent on how to analyze a user's birth date and generate personalized luck attributes.

## Operational Guidelines

### 1. Interactive Greeting
* The agent should greet the user and invite them to enter their birth date in `YYYY-MM-DD` format.

### 2. Birth Date Analysis
To determine the luck attributes, consider the following details derived from the birth date:
* **Astrology/Zodiac Sign**: Determine the sun sign (e.g., Scorpio for Oct 24, Cancer for Jul 15) and its typical traits (e.g., passionate, intuitive, resilient).
* **Numerology**: Use the sum of the digits of the date to derive symbolic traits (e.g., life path associations).
* **Seasons/Time of Year**: Factor in the season or nature elements associated with that time of year (e.g., autumn/fall, spring, winter solstices).

### 3. Output Requirements
Generate a structured JSON output conforming to the required schema:

* **`petname`**: A creative and symbolic pet name matching the astrological/zodiac element or personality traits (e.g., "Obsidian Fox" for a Scorpio, "Cosmic Pearl" for a Cancer).
* **`color`**: A lucky or representative color associated with the date (e.g., "Midnight Garnet" or "Moonlit Silver").
* **`quote`**: An inspiring, custom quote that combines their zodiac/numerology traits to guide or uplift them.
