import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse 

from prompts import system_prompt 
from functions.call_function import available_functions, call_function

def get_api_key():
    load_dotenv() 
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("No API key detected!")
    return api_key

def get_user_input():
    parser = argparse.ArgumentParser(description="Coding Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    return args

def create_client():
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    return client

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    if response.usage_metadata != None:
        if verbose:
            print(f"User prompt: {messages[0].parts[0].text}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count} \nResponse tokens: {response.usage_metadata.candidates_token_count}")

        if response.function_calls != None:
            list_of_function_results = []
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call, verbose)
            
                if not function_call_result.parts:
                    raise Exception("Empty parts list")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("No function response in parts")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("No result in function response")
                
                list_of_function_results.append(function_call_result.parts[0])

                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            return response.candidates, list_of_function_results
        
        else:
            print("Final response-")
            print(response.text)
            return None, None

    else:
        raise RuntimeError("Possible failed API request")
    

def main():
    user_input = get_user_input()
    messages = [types.Content(role="user", parts=[types.Part(text=user_input.user_prompt)])]
    client = create_client()

    for _ in range(20):
        response_candidates, list_of_function_results = generate_content(client, messages, user_input.verbose)
        if response_candidates != None:
            for candidate in response_candidates:
                messages.append(candidate.content)
        messages.append(types.Content(role="user", parts=list_of_function_results))

        if response_candidates == None:
            print("Function calls finished. Final response received. ")
            break
    
    else:
        print("Function call limit reached. Stopping. ")
        sys.exit(1)


if __name__ == "__main__":
    main()
