import sys


def coco():
  for line in sys.stdin:
      line = line.split()
      # x = line.split("\t")
      return line

# print(coco())

def parse_try():
  n = int(sys.stdin.readline())
  
  board = []
  while n > 0:
    board += [list(map(int, sys.stdin.readline().split()))]
    n -= 1
    
  return board

print(parse_try())