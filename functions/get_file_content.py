import os
import sys
from .config import MAX_CHARS
from google.genai import types


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="prints the files text as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)





def get_file_content(working_directory, file_path):

    abs_base = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))


    if not (abs_target == abs_base or abs_target.startswith(abs_base + os.sep)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_target, "r") as f:
            files_content_string = f.read(MAX_CHARS)
            if os.path.getsize(abs_target) > MAX_CHARS:
                files_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return files_content_string
    except Exception as e:
        return f"Error: {e}"