---
name: movie_guess
description: "Guidelines and instructions for conducting a movie guessing game, including fetching a movie frame, managing user attempts, providing hints, and revealing the answer."
---

# Movie Guessing Game Skill

This skill guides the agent on how to run an interactive movie guessing game with the user.

## Operational Guidelines

### 1. Language Selection
* Before initiating the game, the agent must ask the user for their preferred movie language.

### 2. Movie Selection
* Choose a well-known, recognizable movie in the user's preferred language.
* For languages utilizing non-Latin scripts (e.g. Tamil, Telugu, Hindi), always select the movie but pass its standard English transliteration or release title (e.g. "Roja", "Nayakan", or "Baahubali") to the search tool to ensure it succeeds.

### 3. Retrieve Movie Frame
* Call the custom tool `fetch_movie_frame(movie_name)` with the chosen movie's name to retrieve a scene still.

### 4. User Notification
* Notify the user that the image is ready for viewing, and print ONLY the exact local path of the retrieved scene still.
* Do NOT print the source URL, website name, or any metadata returned by the tool that could contain or leak the movie name to the user.

### 5. Guess Validation
* Accept and validate the user's movie guess.
* Support a maximum of 3 attempts for the user to guess the correct movie.

### 6. Hints and Reveal
* Provide helpful hints (e.g., release year, director, cast, or genre) if the user asks.
* Reveal the correct movie name if the user fails to guess it after all 3 attempts.
