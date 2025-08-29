import os
import sys
from .config import MAX_CHARS
from google.genai import types
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .write_file import write_file
from .run_python import run_python_file










def call_function(function_call_part, verbose=False):
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    
    

    if function_call_part.name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    use_function = function_map[function_call_part.name]
    kwargs = {"working_directory": "./calculator", **function_call_part.args}

    
    if verbose:
        print(f"Calling function: {function_call_part.name}({kwargs})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_result = use_function(**kwargs)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

