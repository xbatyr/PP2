students = [
    {"name": "Dias", "score": 98},
    {"name": "Batyr", "score": 99},
    {"name": "Dimash", "score": 97.5},
]

# sort score
by_score = sorted(students, key=lambda s: s["score"])

# sort name
by_name = sorted(students, key=lambda s: s["name"])

print(by_score)
print(by_name)
