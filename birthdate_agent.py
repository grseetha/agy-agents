import asyncio
import os
import pydantic
from google.antigravity import Agent, LocalAgentConfig

# Define the structured schema using Pydantic
class PetResponse(pydantic.BaseModel):
    petname: str = pydantic.Field(description="A creative pet name suited for someone born on this date, reflecting zodiac, numerology, or birth traits.")
    color: str = pydantic.Field(description="A lucky or representative color associated with this birth date.")
    quote: str = pydantic.Field(description="An inspiring, insightful, or fun quote tailored for a person born on this date.")

async def generate_pet_details(birth_date: str) -> dict:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    birthdate_skill_dir = os.path.join(base_dir, "skills", "birthdate_luck")

    # Set up configuration with the response schema and the specific birthdate skill
    config = LocalAgentConfig(
        response_schema=PetResponse,
        skills_paths=[birthdate_skill_dir],
        system_instructions=(
            "You are a fun and intuitive agent. You have access to the 'birthdate_luck' skill. "
            "Refer to its guidelines and instructions to analyze the birth date and generate "
            "the luck attributes."
        )
    )

    async with Agent(config) as agent:
        prompt = f"Please generate a pet name, lucky color, and custom quote for the birth date: {birth_date}"
        response = await agent.chat(prompt)
        
        # Retrieve the structured output matching the schema
        output = await response.structured_output()
        return output

async def main():
    print("Agent: Hello! I can generate a custom pet name, lucky color, and quote based on your birth date.")
    
    # Prompt the user for their birth date
    birth_date = input("Agent: Please enter your birth date (YYYY-MM-DD): ").strip()
    if not birth_date:
        print("Agent: Birth date cannot be empty. Exiting.")
        return

    print(f"\nAgent: Querying for birth date: {birth_date}...")
    try:
        result = await generate_pet_details(birth_date)
        print("\n--- Agent Result ---")
        if result:
            print(f"Pet Name: {result.get('petname')}")
            print(f"Lucky Color: {result.get('color')}")
            print(f"Quote: \"{result.get('quote')}\"")
        else:
            print("Agent: Failed to get structured output.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
