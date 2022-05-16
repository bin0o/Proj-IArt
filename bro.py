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

def parse_list_comp():
  n = int(sys.stdin.readline())
  return [list(map(int, sys.stdin.readline().split())) for i in range(n)]

def all_test():
  board=[[1,2,3,4],[1,2,3,4]]
  return all(len(board)==4)

"""
board=Board.parse_instance_from_stdin()
print("Initial:\n",board,sep="")

print(board.adjacent_vertical_numbers(3, 3))
print(board.adjacent_horizontal_numbers(3, 3))

print(board.adjacent_vertical_numbers(1, 1))
print(board.adjacent_horizontal_numbers(1, 1))
"""

print(all_test())