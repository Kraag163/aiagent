import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    
    try:
    
        abs_work = os.path.abspath(working_directory)

        if not os.path.isdir(abs_work):
            return(f"Error: \"{working_directory}\" is not a directory")
        
        target = os.path.abspath(os.path.join(abs_work, directory))
        
        if not os.path.commonpath([abs_work, target]) == abs_work:
            return(f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory")
        if not os.path.isdir(target):
            return(f"Error: \"{directory}\" is not a directory")
    
        lines = []

        for name in os.listdir(target):
            child = os.path.join(target, name)
            is_dir = os.path.isdir(child)
            size = os.path.getsize(child)
            line = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
            lines.append(line)
            
        return ("\n".join(lines))
            

    except Exception as error:
        return(f"Error: {error}")


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)   

# available_functions = types.Tool(
#     function_declarations=[
#         schema_get_files_info,
#     ]
# )