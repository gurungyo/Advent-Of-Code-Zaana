import sys

paths = {}
for line in open("day11_input.txt"):
    source, targets = line.strip().split(": ")
    paths[source] = targets.split(" ")

dic1 = {}
def count_paths(node):
    if node == 'out':
        return 1
    
    if node not in paths:
        return 0
    
    if node in dic1:
        return dic1[node]
    
    total = 0
    for neighbor in paths[node]:
        total += count_paths(neighbor)
    
    dic1[node] = total
    return total

print(count_paths("you"))