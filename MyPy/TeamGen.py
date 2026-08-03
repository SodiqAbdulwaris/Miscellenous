import random

NoOfPplPT = int(input("How many people per team: "))
noofppl = 0
nooft = 0
nams = []

while True: 
    name = input("What are the names of the team members?(press q to quit) ")
    if name.lower() == "q":
        break
    nams.append(name)
    
names = list(set(nams))


team = []
random.shuffle(names)
while len(names) > 0:
    nooft += 1
    newteam = []
    for i in range(NoOfPplPT):
        newteam.append(names.pop(0))
        noofppl += 1
    team.append(newteam)

for index, newteam in enumerate(team):
    print(f"Team {index + 1} : {', '.join(newteam)}")

print(f"\nSuccessfully shared {noofppl} people into {nooft} teams ")

