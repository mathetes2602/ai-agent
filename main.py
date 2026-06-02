import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_functions import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("api key not found")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
)
if response.usage_metadata == None:
    raise RuntimeError("failed api request")

function_results = []
if response.function_calls != None:
    for function_call in response.function_calls:
        function_call_result = call_function(function_call)
        if len(function_call_result.parts) == 0:
            raise Exception("Empty '.parts' list")
        
        if function_call_result.parts[0].function_response == None:
            raise Exception("Function response is None")
        
        if function_call_result.parts[0].function_response.response == None:
            raise Exception("Response object is None")
        
        function_results.append(function_call_result.parts[0])
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    print(response.text)
