number_of_balls = int(input())

billiard = {}

for _ in range(number_of_balls):
    name = input()
    respect_list = list(map(int, input().split()))
    billiard[name] = round(sum(respect_list) / len(respect_list), 2)

for name, respect in billiard.items():
    print(name, respect)

billiard = sorted(billiard.items(), key=lambda r: r[1], reverse=True)

positive = 0
negative = 0

for name, respect in billiard:
    print(name)
    if respect >= 0:
        positive += 1
    else:
        negative += 1

overall_respect = []

for name, respect in billiard:
    if respect >= 0:
        overall_respect.append(respect * (positive - negative))
    else:
        overall_respect.append(respect * (negative - positive))
    
print(round(sum(overall_respect) / len(overall_respect), 2))