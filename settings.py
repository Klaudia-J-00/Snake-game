import pygame

# Ustawienia sceny i siatki
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 30, 30  # 30x30 grid
CELL_SIZE = WIDTH // COLS

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) # sciany
PINK = (255, 105, 180) # snake
PURPLE = (128, 0, 128)  # do zwiekszania ciala snake'a
BLUE = (0, 0, 255)  # start
GREEN = (0, 255, 0)  # meta
YELLOW = (255, 255, 0)  # "jablka" do zebrania przez snake'a
