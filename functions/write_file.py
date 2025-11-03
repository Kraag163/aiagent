import os
from google.genai import types

def write_file(working_directory, file_path, content):

    try:
    
        abs_work = os.path.abspath(working_directory)
        
        if not os.path.isdir(abs_work):
            return(f"Error: \"{working_directory}\" is not a directory")
        
        target = os.path.abspath(os.path.join(abs_work, file_path))
        
        if not os.path.commonpath([abs_work, target]) == abs_work:
            return(f"Error: Cannot write \"{file_path}\" as it is outside the permitted working directory")
        
        if not os.path.exists(target):
            
            ht = os.path.split(target)
            
            if not os.path.exists(ht[0]):
                os.makedirs(os.path.dirname(target))
            
            f = open(target, "x")
            f.close()
    
        with open(target, "w") as f:
            f.write(content)
            return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
            
    
    except Exception as error:
        return(f"Error: {error}")

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write inside files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)   

# available_functions = types.Tool(
#     function_declarations=[
#         schema_write_file,
#     ]
# )