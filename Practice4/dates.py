from datetime import date, timedelta, datetime

# 1 
today = date.today()
result = today - timedelta(days=5)

print("Today is", today)
print("5 days ago was", result)
print()

# 2
today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)
print()

# 3 
now = datetime.now()
no_micro = now.replace(microsecond=0)

print("With microseconds:", now)
print("Without microseconds:", no_micro)
print()

# 4
# 2026-02-23 10:15:30
d1_str = input("Enter the first date : ")
d2_str = input("Enter the second date : ")

d1 = datetime.strptime(d1_str, "%Y-%m-%d %H:%M:%S")
d2 = datetime.strptime(d2_str, "%Y-%m-%d %H:%M:%S")

ans = abs((d2 - d1).total_seconds()) 
print(f"Difference =: {ans}")
