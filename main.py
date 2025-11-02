
import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *




load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():

    
    messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]

    if len(sys.argv) < 2: 
        print("Error") 
        sys.exit(1) 

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )
    print(response.text)
    
    if "--verbose" in sys.argv[1:]:
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
