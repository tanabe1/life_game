#!/usr/bin/python3

import numpy
import curses
from curses import wrapper

row2str = lambda row: "".join(["0" if c != 0 else " " for c in row])
cell_value = lambda world, height, width, y, x : world[y % height, x % width]

def print_world(stdscr, world):
    height, width = world.shape
    for y in range(height):
        row = world[y]
        stdscr.addstr(y, 0, row2str(row))
    stdscr.refresh()

def set_next_cell_value(world, next_world, height, width, y, x):
    current_value = cell_value(world, height, width, y, x)
    next_value = current_value
    num_live = 0
    num_live += cell_value(world, height, width, y - 1 , x - 1)
    num_live += cell_value(world, height, width, y - 1 , x    )
    num_live += cell_value(world, height, width, y - 1 , x + 1)
    num_live += cell_value(world, height, width, y     , x - 1)
    num_live += cell_value(world, height, width, y     , x + 1)
    num_live += cell_value(world, height, width, y + 1 , x - 1)
    num_live += cell_value(world, height, width, y + 1 , x    )
    num_live += cell_value(world, height, width, y + 1 , x + 1)
   
    # 条件
    if current_value == 0 and num_live == 3:
        next_value = 1
    elif current_value == 1 and num_live in (2,3):
        next_value = 1
    else: 
        next_value = 0
    next_world[y, x] = next_value
    

def calc_next_world(world, next_world):
    height, weight = world.shape
    for y in range(height):
        for x in range(weight):
            set_next_cell_value(world, next_world, height, weight, y, x)

def life_game(stdscr, height, width):
    #初期世界
    world = numpy.random.randint(2, size=(height, width), dtype=numpy.int32)

    # 次の世代の世界を保持する２次元配列
    next_world = numpy.empty((height, width), dtype=numpy.int32)
    while True:
        print_world(stdscr, world)
        calc_next_world(world, next_world)
        world, next_world = next_world, world



def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    scr_height, str_width = stdscr.getmaxyx()
    life_game(stdscr, scr_height - 1, str_width)

if __name__ == "__main__":
    curses.wrapper(main)
