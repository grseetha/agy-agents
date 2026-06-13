# Spec: Movie Guessing Agent

## Objective
Create an interactive CLI-based agent using the Google Antigravity SDK that hosts a movie guessing game. 
* The agent asks the user for a movie language first.
* Once the language is selected, the agent selects a movie, fetches a real scene frame or image of that movie from online portals (Film-Grab with Wikipedia as fallback), and saves it to a local folder.
* The user gets three attempts to guess the movie name based on the scene frame.
* The agent provides feedback on each guess and manages the game lifecycle.

## Tech Stack
* Python 3.10+
* `google-antigravity`
* `requests` (for web scraping and API calls)
* Standard libraries: `os`, `asyncio`, `random`, `re`, `urllib.parse`

## Specifications
* **Input**: A string representing a birthdate or country query is not applicable here. Instead, the user inputs the target movie language first, and then makes guesses at the movie name.
* **Persona**: The agent acts as a Movie Guessing Game Master.
* **Custom Tool**:
  * `fetch_movie_frame(movie_name: str) -> dict`: Searches Film-Grab.com for high-quality movie still frames, randomly selects one, downloads it to `generated_images/`, and returns the local path. If not found on Film-Grab, it queries the Wikipedia PageImages API to retrieve the movie's main poster/image as a fallback.
* **Skill Integration**:
  * The agent relies on the `movie_guess` skill located in `skills/movie_guess`.
  * The skill defines rules for selecting movies in various languages, handling hint requests, tracking remaining guesses, and verifying guess correctness.

## Commands
* Run the game:
  ```bash
  python movie_guess_agent.py
  ```

## Project Structure
```
skills/
  movie_guess/
    SKILL.md               -> Guideline for the movie guess game (rules, hint handling)
specs/
  movie_guess_agent.md     -> This technical specification
movie_guess_agent.py       -> The game entry point and interaction loop
generated_images/          -> Directory where downloaded movie stills are saved
```

## Code Style
* Follow PEP 8 guidelines.
* Asynchronous execution for AGY agent chat calls.
* Clean error handling for network/download failures in `fetch_movie_frame`.
* Clear prompts to the user with standard CLI output formatting.

Example snippet:
```python
async def start_game():
    config = LocalAgentConfig(
        tools=[fetch_movie_frame],
        skills_paths=[movie_guess_skill_dir],
        system_instructions="You are a Movie Guessing Game Master..."
    )
    # Interactive game loop
```

## Testing Strategy
* **Manual Testing**:
  * Run `python movie_guess_agent.py`.
  * Select a language (e.g., English).
  * Confirm that an image is downloaded in `generated_images/` and the path is printed.
  * Guess the movie correctly (should win).
  * Guess incorrectly three times (should lose and reveal the movie).
* **Automated Testing**:
  * Assert that `fetch_movie_frame` returns a success dict and downloads a valid file for known movies.

## Boundaries
* **Always**:
  * Ask for the movie language before initiating the game.
  * Limit the guess count strictly to three attempts.
  * Clean up or organize generated files under `generated_images/`.
* **Ask first**:
  * Adding hints or multiplayer capabilities.
* **Never**:
  * Disclose the movie title directly in the prompts until the game ends.
  * Allow the game to continue after the 3rd failed guess.

## Success Criteria
1. Agent prompts the user: "Welcome to the Movie Guessing Game! What language of movies would you like to play with?"
2. Agent successfully calls `fetch_movie_frame` to download a still image.
3. The image path is printed (and automatically opened via system tool on macOS), and the user is prompted to guess.
4. If the user guesses correctly within 3 attempts, they win.
5. If the user fails 3 times, they are informed of the correct answer and the game ends.
