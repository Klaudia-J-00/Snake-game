import pygame
import random

from astar import MazeSolver

pygame.init()

# Ustawienia sceny i siatki
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 30, 30  # 30x30 grid
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labirynt A*")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) # sciany
PINK = (255, 105, 180) # snake
BLUE = (0, 0, 255)  # start
GREEN = (0, 255, 0)  # meta

maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
# 0 oznacza sciane, 1 oznacza sciezke, na poczatek wypelniane jest samymi zerami (scianami)

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
# kierunki w ktorych sciany moga byc przesuwane (prawo, lewo, dol, gora)

def is_in_bounds(x, y):
    """
    Sprawdza, czy dana komorka jest w granicach labiryntu
    """
    return 0 <= x < COLS and 0 <= y < ROWS

def dfs(x, y):
    """
    Rekurenycjna funkcja do generowania labiryntu, zaczyna od punktu (0, 0) i przesuwa sie w losowe strony
    tworzac sciezke w labiryncie. Zamienia 0 na 1, co ze sciany zamieniaja sie w sciezke. Poniewaz moze sie
    przesuwac tylko w mozliwych kierunkach definiowanych przez DIRECTIONS, wiec nie moze przeskoczyc sciany.
    Przesuwa sie o 2 komorki, poniewaz w przeciwnym razie nie byloby sciany miedzy sciezkami. Dla kazdego kierunku
    (dx, dy) obliczane sa wspolrzedne nx, ny i sprawdzane czy sa w granicach labiryntu i czy nie sa juz sciezka.
    """
    maze[y][x] = 1  # Oznacza aktualna komorke jako sciezke
    random.shuffle(DIRECTIONS)  # Losowo przemieszaj kierunki

    for dx, dy in DIRECTIONS:
        nx, ny = x + dx * 2, y + dy * 2  # Przesuniecie o 2, aby nie przeskoczyc sciany
        if is_in_bounds(nx, ny) and maze[ny][nx] == 0:
            # Jesli komorka jest w granicach i jest sciana
            maze[y + dy][x + dx] = 1  # Zamien sciane na sciezke
            dfs(nx, ny) # Rekurencyjnie wywolaj funkcje dla nowej komorki

def generate_maze():
    """ Generates a maze using DFS """
    # Zaczyna dfs od punktu (0, 0)
    dfs(0, 0)

    # By upewnic sie, ze zawsze na koncu jest sciezka do mety, ustawiamy ostatnie dwie komorki jako sciezke
    maze[ROWS - 1][COLS - 1] = 1
    maze[ROWS - 2][COLS - 1] = 1

# Generowanie labiryntu
generate_maze()

# Punkt startu i mety (lewy gorny rog i prawy dolny rog)
start = (0, 0)
end = (COLS - 1, ROWS - 1)

# korzystamy z klasy MazeSolver z pliku astar.py
solver = MazeSolver(maze)
rotated_path  = solver.a_star(start, end)
# Obracamy sciezke, poniewaz w naszym przypadku (x, y) to (row, col), a nie (x, y)
path = [(y, x) for x, y in rotated_path]

# def print_maze(maze):
#     for row in maze:
#         print(row)
#
# print_maze(maze)

# Indeks sciezki i odwiedzonych komorek (do rysowania)
path_index = 0
visited_cells = []

# Petla gry
running = True
while running:
    screen.fill(WHITE)  # Fill the screen with white

    # Rysowanie labiryntu
    for row in range(ROWS):
        for col in range(COLS):
            # Rysuje sciane jako czarna, a sciezke jako biala
            color = WHITE if maze[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Rysuje poczatkowy punkt jako zielony i koncowy punkt jako niebieski
    pygame.draw.rect(screen, GREEN, (start[0] * CELL_SIZE, start[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, BLUE, (end[0] * CELL_SIZE, end[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Rysuje sciezke w kolorze rozowym
    if path_index < len(path):
        # Jesli nie doszlismy do konca sciezki, rysujemy kolejny krok
        current_x, current_y = path[path_index]
        # aktualne x i y to wspolrzedne sciezki
        visited_cells.append((current_x, current_y))  # Przechowujemy odwiedzone komorki do rysowania ogona
        path_index += 1  # Przesuwamy sie do nastepnego punktu odnalezionej przez algorytm sciezki
        pygame.time.delay(50)  # Delay zeby mozna bylo zobaczyc jak sciezka sie rysuje

    # Rysuje odwiedzone komorki jako rozowe
    for vx, vy in visited_cells:
        pygame.draw.rect(screen, PINK, (vx * CELL_SIZE, vy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Obsluga zdarzen (zamkniecie okna)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # flip sluzy do odswiezania ekranu
    pygame.display.flip()

# Koniec programu
pygame.quit()
