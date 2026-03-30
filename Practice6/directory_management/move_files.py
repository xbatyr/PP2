import shutil
import os
 
os.makedirs("folder1", exist_ok=True)
os.makedirs("folder2", exist_ok=True)
 
with open("folder1/notes.txt", "w") as f:
    f.write("some notes\n")
 
shutil.move("folder1/notes.txt", "folder2/notes.txt")
print(os.listdir("folder2"))