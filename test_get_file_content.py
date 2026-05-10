from functions.get_file_content import get_file_content  
from config import MAX_CHARS

result = get_file_content("calculator", "lorem.txt")
#print(f"The file is {len(result)} characters long and contains added message- {result[MAX_CHARS:]}")

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat")) #(this should return an error string)
print(get_file_content("calculator", "pkg/does_not_exist.py")) #(this should return an error string)