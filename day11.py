import sys

paths = {}
for line in open("day11_input.txt"):
    source, targets = line.strip().split(": ")
    paths[source] = targets.split(" ")

def count_paths(start, end):
    dic1 = {}

    def search(node):
        if node == end:
            return 1
        if node not in paths:
            return 0
        
        if node in dic1:
            return dic1[node]
        
        total = 0
        for neighbor in paths[node]:
            total += search(neighbor)
        
        dic1[node] = total        
        return total

    return search(start)

paths_dac_first = (
    count_paths('svr','dac') * count_paths('dac','fft') * count_paths('fft','out')
)

paths_fft_first = (
    count_paths('svr','fft') * count_paths('fft','dac') * count_paths('dac','out')
)

total = paths_dac_first + paths_fft_first

print(total)