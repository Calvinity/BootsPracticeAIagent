import os
import sys
from google.genai import types







schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),


        },
    ),
)



def write_file(working_directory, file_path, content):
    
    
    abs_base = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))



    if not (abs_target == abs_base or abs_target.startswith(abs_base + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_target):
        try:
            os.makedirs(os.path.dirname(abs_target), exist_ok=True)
            with open(abs_target, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Error: {e}"
    
    try:
        with open(abs_target, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

        

    except Exception as e:
        return f"Error: {e}"