import os
import sys
from google.genai import types


def call_function(function_call_part, verbose=False):

    if "--verbose" in sys.argv[1:]:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f" - Calling function: {function_call_part.name}")

