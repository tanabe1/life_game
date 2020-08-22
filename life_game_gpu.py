#!/usr/bin/python3

import numpy
import curses
from curses import wrapper
import time

import pycuda.gpuarray as gpuarray
import pycuda.driver as cuda
import pycuda.autoinit

from pycuda.compiler import SourceModule

BLOCKSIZE = 32
GPU_NITER = 1
GPU_NITER = 100

row2str = lambda row: "".join(["0" if c != 0 else " " for c in row])
cell_value = lambda world, height, width, y, x : world[y % height, x % width]

def print_world(stdscr, world, generation, elapsed):
    height, width = world.shape
    for y in range(height):
        row = world[y]
        stdscr.addstr(y, 0, row2str(row))
    stdscr.addstr(height, 0, "generation %06d, Elapsed %.6f[sec]" %(generation, elapsed/generation))
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
    if current_value == 0 and num_live == 3:
        next_value = 1
    elif current_value == 1 and num_live in (2,3):
        next_value = 1
    else:
        next_value = 0
    next_world[y, x] = next_value


def calc_next_world(world, next_world):
    height, width = world.shape
    for y in range(height):
        for x in range(width):
            set_next_cell_value(world, next_world, height, width, y, x)


def life_game(stdscr, height, width):
    h_world = numpy.random.randint(2, size=(height, width), dtype=numpy.int32)
    h_next_world = numpy.empty((height, width), dtype=numpy.int32)

    d_world = gpuarray.to_gpu(h_world)
    d_next_world = gpuarray.to_gpu(h_next_world)

    elapsed = 0.0
    generation = 0
    while True:
        generation += 1

        start_time = time.time()
        print_world(stdscr, h_world, generation, elapsed)
        calc_next_world(d_world, d_next_world)

        duration = time.time() - start_time
        elapsed += duration

        h_next_world = d_next_world.get()
        d_world, d_next_world = d_next_world, d_world
   
mod = SourceModule("""
__global__ void life_of_game(const int* __restrict__ d_world, int* __restrict__ d_next_world, int* world, int* next_world) {

}
        """)

def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)
    scr_height, scr_width = stdscr.getmaxyx()
   
    add_matrix_gpu = mod.get_function("life_of_game")
    block = (BLOCKSIZE, BLOCKSIZE, 1)
    grid = ((scr_height + block[0] - 1) // block[0], 
                (scr_width + block[0]) // block[0])
    print("Grid = ({0}, {1}), Block = ({2}, {3})"
                .format(grid[0], grid[1], block[0], block[1]))

    start = cuda.Event()
    end = cuda.Event()
    life_game(stdscr, scr_height - 1, scr_width)
    end.record()
    end.syncronize()

if __name__ == "__main__":
    curses.wrapper(main)
