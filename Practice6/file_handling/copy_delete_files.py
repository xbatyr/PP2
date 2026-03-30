import shutil
import os

shutil.copy("sample.txt", "sample_backup.txt")
print("file copied")

os.remove("sample_backup.txt")
print("backup deleted")

os.remove("sample.txt")
print("original deleted")
