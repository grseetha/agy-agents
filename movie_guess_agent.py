import asyncio
import os
import re
import random
import shlex
import requests
import urllib.parse
import uuid
from google.antigravity import Agent, LocalAgentConfig

# --- Custom Tool ---

def fetch_movie_frame(movie_name: str) -> dict:
    """Searches Film-Grab.com (or Wikipedia as fallback) for a movie image, downloads it, and returns the path.

    Args:
        movie_name: The name of the movie to search for (e.g. "Inception", "The Dark Knight").
    """
    # Create the directory for generated images if it doesn't exist
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "generated_images")
    os.makedirs(output_dir, exist_ok=True)
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    # 1. Try Film-Grab first
    print(f"\n[Tool] Searching Film-Grab.com for '{movie_name}'...")
    search_url = f"https://film-grab.com/?s={urllib.parse.quote(movie_name)}"
    try:
        r = requests.get(search_url, headers=headers, timeout=10)
        if r.status_code == 200:
            # Find all post links: href="https://film-grab.com/YYYY/MM/DD/movie-name/"
            links = re.findall(r'href="(https://film-grab\.com/\d{4}/\d{2}/\d{2}/[^"]+)"', r.text)
            unique_links = list(set(links))
            if unique_links:
                post_url = unique_links[0]
                print(f"[Tool] Found Film-Grab post: {post_url}. Fetching scene still frames...")
                post_r = requests.get(post_url, headers=headers, timeout=10)
                if post_r.status_code == 200:
                    post_html = post_r.text
                    # Extract images under /wp-content/uploads/photo-gallery/
                    matches = re.findall(r'["\']([^"\']*/wp-content/uploads/photo-gallery/[^"\']+)["\']', post_html)
                    
                    valid_urls = []
                    for m in matches:
                        url_no_query = m.split('?')[0]
                        if url_no_query.lower().endswith(('.jpg', '.jpeg', '.png')):
                            if '/thumb/' not in url_no_query:
                                if url_no_query.startswith('/'):
                                    url_no_query = "https://film-grab.com" + url_no_query
                                elif not url_no_query.startswith('http'):
                                    url_no_query = "https://film-grab.com/" + url_no_query
                                valid_urls.append(url_no_query)
                    
                    unique_urls = list(set(valid_urls))
                    if unique_urls:
                        chosen_url = random.choice(unique_urls)
                        print(f"[Tool] Selected random still frame: {chosen_url}")
                        
                        img_r = requests.get(chosen_url, headers=headers, timeout=15)
                        if img_r.status_code == 200:
                            ext = os.path.splitext(chosen_url.split('?')[0])[1] or '.jpg'
                            filename = f"frame_{uuid.uuid4().hex}{ext}"
                            local_path = os.path.join(output_dir, filename)
                            
                            with open(local_path, "wb") as f:
                                f.write(img_r.content)
                            
                            # Automatically trigger opening the downloaded image on macOS
                            print(f"[Tool] Automatically opening downloaded image: {local_path}")
                            os.system(f"open {shlex.quote(local_path)}")
                            
                            return {
                                "status": "success",
                                "source": "film-grab",
                                "url": chosen_url,
                                "local_path": local_path
                            }
    except Exception as e:
        print(f"[Tool] Film-Grab retrieval failed or timed out: {e}")

    # 2. Fallback to Wikipedia PageImages API
    print(f"[Tool] Film-Grab failed. Falling back to Wikipedia PageImages API for '{movie_name}'...")
    wiki_api = "https://en.wikipedia.org/w/api.php"
    
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": movie_name,
        "format": "json"
    }
    
    try:
        r = requests.get(wiki_api, params=search_params, headers=headers, timeout=10)
        if r.status_code == 200:
            search_data = r.json()
            search_results = search_data.get("query", {}).get("search", [])
            if search_results:
                best_title = search_results[0].get("title")
                for res in search_results[:3]:
                    title_lower = res.get("title", "").lower()
                    if "(film)" in title_lower or "(20" in title_lower or "(19" in title_lower:
                        best_title = res.get("title")
                        break
                
                print(f"[Tool] Searching Wikipedia page '{best_title}' image...")
                # Query PageImages API first
                pi_params = {
                    "action": "query",
                    "prop": "pageimages",
                    "piprop": "original",
                    "titles": best_title,
                    "redirects": "1",
                    "format": "json"
                }
                pi_r = requests.get(wiki_api, params=pi_params, headers=headers, timeout=10)
                wiki_img_url = None
                if pi_r.status_code == 200:
                    pi_data = pi_r.json()
                    pages = pi_data.get("query", {}).get("pages", {})
                    for page_id, page_data in pages.items():
                        original = page_data.get("original", {})
                        if original.get("source"):
                            wiki_img_url = original.get("source")
                            break
                
                # If PageImages API returned nothing, query page image list
                if not wiki_img_url:
                    print(f"[Tool] PageImages API returned no source. Querying page image file list for '{best_title}'...")
                    img_params = {
                        "action": "query",
                        "prop": "images",
                        "titles": best_title,
                        "imlimit": "50",
                        "redirects": "1",
                        "format": "json"
                    }
                    img_r = requests.get(wiki_api, params=img_params, headers=headers, timeout=10)
                    if img_r.status_code == 200:
                        img_data = img_r.json()
                        pages = img_data.get("query", {}).get("pages", {})
                        all_files = []
                        for page_id, page_data in pages.items():
                            for img in page_data.get("images", []):
                                all_files.append(img.get("title"))
                        
                        poster_file = None
                        for f in all_files:
                            lf = f.lower()
                            if "poster" in lf or "cover" in lf or "still" in lf or "frame" in lf:
                                poster_file = f
                                break
                        if not poster_file and all_files:
                            for f in all_files:
                                lf = f.lower()
                                if lf.endswith(('.jpg', '.jpeg', '.png')):
                                    poster_file = f
                                    break
                        
                        if poster_file:
                            info_params = {
                                "action": "query",
                                "prop": "imageinfo",
                                "iiprop": "url",
                                "titles": poster_file,
                                "format": "json"
                            }
                            info_r = requests.get(wiki_api, params=info_params, headers=headers, timeout=10)
                            if info_r.status_code == 200:
                                info_pages = info_r.json().get("query", {}).get("pages", {})
                                for page_id, page_data in info_pages.items():
                                    imageinfo = page_data.get("imageinfo", [])
                                    if imageinfo:
                                        wiki_img_url = imageinfo[0].get("url")
                                        break
                
                if wiki_img_url:
                    print(f"[Tool] Found Wikipedia image URL: {wiki_img_url}")
                    img_r = requests.get(wiki_img_url, headers=headers, timeout=15)
                    if img_r.status_code == 200:
                        ext = os.path.splitext(wiki_img_url.split('?')[0])[1] or '.jpg'
                        filename = f"frame_{uuid.uuid4().hex}{ext}"
                        local_path = os.path.join(output_dir, filename)
                        
                        with open(local_path, "wb") as f:
                            f.write(img_r.content)
                            
                        # Automatically trigger opening the downloaded image on macOS
                        print(f"[Tool] Automatically opening downloaded image: {local_path}")
                        os.system(f"open {shlex.quote(local_path)}")
                        
                        return {
                            "status": "success",
                            "source": "wikipedia",
                            "url": wiki_img_url,
                            "local_path": local_path
                        }
    except Exception as e:
        print(f"[Tool] Wikipedia API retrieval failed: {e}")
        
    return {
        "status": "failed",
        "error": f"Could not retrieve image for movie '{movie_name}' from Film-Grab or Wikipedia."
    }

def cleanup_generated_images():
    """Deletes all files in the generated_images directory to prevent leak and save disk space."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "generated_images")
    if os.path.exists(output_dir):
        for f in os.listdir(output_dir):
            file_path = os.path.join(output_dir, f)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"[Warning] Failed to delete {file_path}: {e}")

# --- Main Game Execution ---

async def main():
    cleanup_generated_images()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    movie_guess_skill_dir = os.path.join(base_dir, "skills", "movie_guess")
    
    config = LocalAgentConfig(
        tools=[fetch_movie_frame],
        skills_paths=[movie_guess_skill_dir],
        system_instructions=(
            "You are the Movie Guessing Game Master, a fun and engaging host of a movie guessing game. "
            "You have access to the 'movie_guess' skill and the 'fetch_movie_frame' tool.\n\n"
            "CRITICAL RULES:\n"
            "1. GREET the user and ask for their preferred movie language first.\n"
            "2. Once they select a language, choose a highly recognizable, well-known movie in that language. If the selected language uses a non-Latin script (like Tamil or Telugu), always choose the movie but pass its standard English transliteration or release title (e.g. 'Roja', 'Nayakan', or 'Baahubali' instead of local scripts) to the fetch_movie_frame tool to ensure lookup succeeds. "
            "DO NOT tell the user which movie you chose!\n"
            "3. IMMEDIATELY call the 'fetch_movie_frame' tool with the chosen movie name. "
            "Wait for the tool to return the result.\n"
            "4. When the tool returns success, notify the user that the scene frame has been downloaded "
            "and opened on their machine. Print ONLY the exact local path to the image. DO NOT print the "
            "source URL, website names (e.g. Film-Grab, Wikipedia), or any tool output metadata that could leak "
            "the movie name.\n"
            "5. Prompt the user to guess the movie name. You must keep the chosen movie name strictly secret. "
            "Do not reveal the movie name or print any clue about it until the game is completed.\n"
            "6. Track the attempts. The user has a maximum of 3 attempts. If they guess incorrectly, "
            "inform them of the remaining attempts (e.g., 'Incorrect! You have 2 attempts remaining.') "
            "and ask for another guess.\n"
            "7. If they ask for a hint, provide a helpful but non-obvious hint (e.g., release year, director, genre, "
            "or main cast) without revealing the title. Hints do not count as attempts.\n"
            "8. If they guess correctly (case-insensitively, allowing minor typos or lack of subtitles/suffixes), "
            "congratulate them on winning and end the game.\n"
            "9. If they fail 3 times, reveal the correct movie name, say 'Game Over', and invite them to play again."
        )
    )

    print("==================================================")
    print("Welcome to the Movie Guessing Game!")
    print("Type 'exit' or 'quit' to end the session.")
    print("==================================================")

    async with Agent(config) as agent:
        # Let the agent greet the user and start the game
        init_response = await agent.chat(
            "Start the movie guessing game by greeting the user, introducing yourself as the Movie Guessing Game Master, and asking what language of movies they would like to play with (explicitly suggesting options including English, Tamil, Telugu, and Hindi)."
        )
        print("\nAgent: ", end="")
        async for chunk in init_response:
            print(chunk, end="", flush=True)
        print()

        while True:
            try:
                user_query = input("\nYou: ").strip()
                if not user_query:
                    continue
                if user_query.lower() in ("exit", "quit"):
                    print("Agent: Goodbye!")
                    break
                
                print("Agent: thinking...")
                response = await agent.chat(user_query)
                print("\nAgent: ", end="")
                async for chunk in response:
                    print(chunk, end="", flush=True)
                print()
            except KeyboardInterrupt:
                print("\nAgent: Goodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
