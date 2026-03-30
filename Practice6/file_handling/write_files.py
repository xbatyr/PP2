with open("sample.txt", "w") as f:
    f.write("my name is Batyrlan\n")
    f.write("i am kbtu student mcm 1 year\n")
    f.write("i love c++\n")

with open("sample.txt", "a") as f:
    f.write("c++ top\n")
    f.write("kbtu one love\n")

with open("sample.txt", "r") as f:
    print(f.read())
