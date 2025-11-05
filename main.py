import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""



    if len(sys.argv) < 2: 
        print("Error") 
        sys.exit(1) 

    messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]

    available_functions = types.Tool(
        function_declarations=[
            schema_write_file, 
            schema_get_file_content, 
            schema_get_files_info, 
            schema_run_python_file,
        ]
    )

    for iteration in range(0, 20):

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
        except Exception as e:
            print(f"API error: {e}")
            sys.exit(1)

        
        for cand in response.candidates:
            messages.append(cand.content)

        verbose = "--verbose" in sys.argv[1:]

        calls = response.function_calls or []
        if calls:
            for f in calls:
                print(f" - Calling function: {f.name}")
                tool_content = call_function(f, verbose=verbose)

                if not tool_content.parts or not getattr(tool_content.parts[0], "function_response", None):
                    raise RuntimeError("Tool response missing function_response")

                result_obj = tool_content.parts[0].function_response.response

                message_to_append = types.Content(role="user",
                    parts=[
                        types.Part(
                            function_response=types.FunctionResponse(
                                name=f.name,
                                response=result_obj
                ))])
                messages.append(message_to_append)

                if verbose:
                    print(f"-> {result_obj}")
                
            continue

        if response.text:
            print("Final response:")
            print(response.text)
            break
        
            
        if "--verbose" in sys.argv[1:]:
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    else:
        # loop exhausted
        print("No final response after max iterations.")   



if __name__ == "__main__":
    main()
