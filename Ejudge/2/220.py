n = int(input())cd
db = {}
for _ in range(n):
    line = input().strip()
    if line.startswith("set"):
        _, key, value = line.split(" ", 2)
        db[key] = value
    else:
        _, key = line.split(" ", 1)
        if key in db:
            print(db[key])
        else:
            print(f"KE: no key {key} found in the document")
