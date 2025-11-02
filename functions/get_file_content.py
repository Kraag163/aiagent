import os
from config import *

def get_file_content(working_directory, file_path):

    try:
    
        abs_work = os.path.abspath(working_directory)
        #print(abs_work)

        if not os.path.isdir(abs_work):
            return(f"Error: \"{working_directory}\" is not a directory")
        
        target = os.path.abspath(os.path.join(abs_work, file_path))
        #print(target)

        if not os.path.commonpath([abs_work, target]) == abs_work:
            return(f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory")
        if not os.path.isfile(target):
            return(f"Error: File not found or is not a regular file: \"{file_path}\"")
    
        with open(target, "r") as f:
            
            file_content_string = f.read(MAX_CHARS)
            
            if f.read(1) != "":
                file_content_string += f"[...File \"{file_path}\" truncated at {MAX_CHARS} characters]"

            return str(file_content_string)
    
    except Exception as error:
        return(f"Error: {error}")