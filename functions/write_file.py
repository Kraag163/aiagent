import os

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