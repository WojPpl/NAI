#Michał Zaremba
#problem: https://www.codingame.com/ide/puzzle/shadows-of-the-knight-episode-1
import sys
import math

# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in input().split()]
n = int(input())  # maximum number of turns before game over.
x0, y0 = [int(i) for i in input().split()]

min_w = 0
min_h = 0
max_w = w - 1
max_h = h - 1

# game loop
while True:
    bomb_dir = input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
    if bomb_dir == "U":
        max_h = y0 - 1
    if bomb_dir == "UR":
        max_h = y0 - 1
        min_w = x0 + 1
    if bomb_dir == "R":
        min_w = x0 + 1
    if bomb_dir == "DR":
        min_h = y0 + 1
        min_w = x0 + 1
    if bomb_dir == "D":
        min_h = y0 + 1
    if bomb_dir == "DL":
        min_h = y0 + 1
        max_w = x0 - 1
    if bomb_dir == "L":
        max_w = x0 - 1
    if bomb_dir == "UL":
        max_h = y0 - 1
        max_w = x0 - 1
    x0 = min_w + math.ceil((max_w - min_w)/2)
    y0 = min_h + math.ceil((max_h - min_h)/2)
    
    print(x0, y0) 
