import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file




print("Result for current file:")
print(" " + run_python_file("calculator", "main.py"))

print("Result for current file:")
print(" " + run_python_file("calculator", "main.py", ["3 + 5"]))

print("Result for current file:")
print(" " + run_python_file("calculator", "tests.py"))

print("Result for current file:")
print(" " + run_python_file("calculator", "../main.py"))

print("Result for current file:")
print(" " + run_python_file("calculator", "nonexistent.py"))

