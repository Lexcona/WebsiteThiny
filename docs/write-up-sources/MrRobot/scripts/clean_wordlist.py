import os

lister = []

with open("Dump/172.16.224.131/fsocity.dic", "r") as f:
    data = f.read().splitlines()

for i in data:
    if not i in lister:
        print(f"FOUND: {i}")
        lister.append(i)
    else:
        print(f"EXISTS: {i}")

with open("wordlist.txt", "w+") as f:
    f.write("\n".join(lister))