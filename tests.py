from functions.run_python_file import run_python_file

#result = get_file_content("calculator", "lorem.txt")
#print(result)

#print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
#print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
#print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

print(run_python_file("calculator", "main.py")) #(should print the calculator's usage instructions)
print(run_python_file("calculator", "main.py", ["3 + 5"])) #(should run the calculator... which gives a kinda nasty rendered result)
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py")) #(this should return an error)
print(run_python_file("calculator", "nonexistent.py")) #(this should return an error)
print(run_python_file("calculator", "lorem.txt")) #(this should return an error)