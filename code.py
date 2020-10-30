#Michał Zaremba
#problem: https://www.codingame.com/ide/puzzle/the-descent
import sys
import math

#game loop
while True: 
    max_height = 0
    max_height_index = 0   
    for i in range(8):
        mountain_h = int(input())  # represents the height of one mountain.
        if mountain_h > max_height:
            max_height = mountain_h
            max_height_index = i        

    print(max_height_index)
