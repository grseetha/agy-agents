import asyncio
import urllib.request
import urllib.parse
import json
import os
from google.antigravity import Agent, LocalAgentConfig

# --- Load Config ---
def load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {}

CONFIG = load_config()

# --- Define the Tools ---

def get_india_postal_details(pincode: str) -> dict:
    """Fetches details (post office, district, state) for a given Indian pincode.

    Args:
        pincode: A 6-digit Indian postal code (e.g. "560001").
    """
    pincode = pincode.strip()
    if not pincode.isdigit() or len(pincode) != 6:
        return {"error": "Indian pincode must be exactly 6 digits."}
    
    base_url = CONFIG.get("INDIA_POSTAL_API_URL", "https://api.postalpincode.in/pincode")
    url = f"{base_url.rstrip('/')}/{pincode}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return {"error": f"Failed to fetch Indian postal details: {str(e)}"}

def get_us_postal_details(zipcode: str) -> dict:
    """Fetches details (place name, state, state abbreviation, coordinates) for a given United States ZIP code.

    Args:
        zipcode: A 5-digit United States ZIP code (e.g. "90210").
    """
    zipcode = zipcode.strip()
    if not zipcode.isdigit() or len(zipcode) != 5:
        return {"error": "US ZIP code must be exactly 5 digits."}
    
    base_url = CONFIG.get("US_POSTAL_API_URL", "https://api.zippopotam.us/us")
    url = f"{base_url.rstrip('/')}/{zipcode}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return {"error": f"Failed to fetch US ZIP details: {str(e)}"}

# --- Main Interaction Loop ---

async def main():
    # Define absolute path to the specific pincode_lookup skill folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pincode_skill_dir = os.path.join(base_dir, "skills", "pincode_lookup")
    
    # Configure the agent with tools and the specific skill path
    config = LocalAgentConfig(
        tools=[get_india_postal_details, get_us_postal_details],
        skills_paths=[pincode_skill_dir],
        system_instructions=(
            "You are a helpful Multi-Country Postal Information Assistant. "
            "You have access to the 'pincode_lookup' skill. Refer to its guidelines "
            "and instructions to determine how to request information from the user, "
            "validate input, and format the output."
        )
    )

    print("Agent: Hello! I am your Multi-Country Postal Information Assistant.")
    print("       I can help you lookup postal codes in India and the United States.")
    print("       Type 'exit' or 'quit' to end the session.")
    
    async with Agent(config) as agent:
        # Let the agent start the conversation to ask for the country first
        init_response = await agent.chat("Start the conversation by greeting the user and asking which country they want to search for.")
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
                
                print("Agent: Checking...")
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
