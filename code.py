#Michał Zaremba
#problem: https://www.codingame.com/ide/puzzle/power-of-thor-episode-1

import sys
import math
import string

light_x, light_y, initial_tx, initial_ty = [int(i) for i in input().split()]
dir_x = light_x - initial_tx
dir_y = light_y - initial_ty

# game loop
while True:
    remaining_turns = int(input()) 
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    move = ""
    if dir_y > 0:
        move = move + "S"
        dir_y -= 1
    elif dir_y < 0:
        move = move + "N"
        dir_y += 1

    if dir_x > 0:
        move = move + "E"
        dir_x -= 1
    elif dir_x < 0:
        move = move + "W"
        dir_x += 1
    # A single line providing the move to be made: N NE E SE S SW W or NW
    print(move)
