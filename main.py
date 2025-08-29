import os
from dotenv import load_dotenv
import sys
from functions.config import system_prompt
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python_file
from functions.call_function import call_function



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)



def main():

    prompt_words = ""
    verbose = False
    


    for i in sys.argv[1:]:
        if i.startswith("--"):
            if i == "--verbose":
                verbose = True
            
        else:
            prompt_words += i + " "

    user_prompt = prompt_words
    function_call_result = None
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

    print("Hello from practiceaiagent!")
    if len(sys.argv) < 2:
        print("no promt provided, please try again")
        exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )

            if response.candidates:
                for cand in response.candidates:
                    if cand.content:
                        messages.append(cand.content)

            if response.function_calls and len(response.function_calls) > 0:
                fc = response.function_calls[0]
                print(f" - Calling function: {fc.name}")
  
                function_call_result = call_function(response.function_calls[0], verbose=verbose)
                messages.append(types.Content(role="user", parts=function_call_result.parts))
                continue

            if response.text:
                print(response.text)
                break

            if response.text:
                print("Final response:")
                print(response.text)
                break
        except Exception as e:
            print(f"Error: {e}")
            break


if __name__ == "__main__":
    main()

