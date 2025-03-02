# # Quick test
# with open("./faq-chatbot/data/txt/trash.txt", "r", encoding="utf-8") as f:
#     print(f.read()[:200])  # First 200 characters
# with open("data/txt/Lumen_NbLM_1.txt", "r", encoding="utf-8") as f: # assuming you're running the script from faq-chatbot directory
#     print(f.read()[:200])  # First 200 characters

# C:\Users\ping\Files_win10\python\py310\faq-chatbot\data\txt\Lumen_NbLM_1.txt
# C:\Users\ping\Files_win10\python\py310\faq-chatbot\trash.py
# import os
# print(f"Current working directory: {os.getcwd()}")

import os

filepath = os.path.join(os.path.dirname(__file__), "data", "txt", "Lumen_NbLM_1.txt")  # Constructs the absolute path
print(f'filepath: {filepath}')
with open(filepath, "r", encoding="utf-8") as f:
    print(f.read()[:200]) 
    # ... your code here ...


