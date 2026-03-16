import os
 
os.makedirs("myproject/docs", exist_ok=True)
os.makedirs("myproject/src", exist_ok=True)
 
print(os.listdir("myproject"))
 
for f in os.listdir("."):
    print(f)
 