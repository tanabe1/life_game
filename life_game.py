#!/usr/bin/python3

import numpy
import curses
from curses import wrapper

row2str = lambda row: "".join(["0" if c != 0 else " " for c in row])

def print_world(stdscr, world):
    height, width = world.shape
    for y in range(height):
        row = world[y]
        stdscr.addstr(y, 0, row2str(row))

    stdscr.refresh()


def life_game(stdscr, height, width):
    world = numpy.random.randint(2, size=(height, width), dtype=numpy.int32)
    while True:
        print_world(stdscr, world)


def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    scr_height, str_width = stdscr.getmaxyx()
    life_game(stdscr, scr_height - 1, str_width)

if __name__ == "__main__":
    curses.wrapper(main)
