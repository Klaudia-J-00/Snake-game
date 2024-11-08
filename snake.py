import time
import pygame
import random

from astar import MazeSolver
from settings import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gra w snake'a")
font = pygame.font.Font(None, 36)  # Rozmiar czcionki 36

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

# Wybieramy co 6 punkt z sciezki, aby umiejscowic na nim "jablka"
potential_points = path[4::6] # zaczynamy od piatego, zebysmy nie umieszczali "jablka" na starcie bo snake nie zdazy go zebrac
points = []

# Indeks sciezki i odwiedzonych komorek (do rysowania)
path_index = 0
visited_cells = []
# Długosc snake'a (poczatkowo 1, bedzie sie zwiekszac po zebraniu "jablka")
snake_length = 1
# Ostatni punkt czasowy
last_point_time = time.time()
point_interval = 0.2  # Co ile sekund pojawia sie nowe "jablko"
# Początkowy licznik punktów
score = 0

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

    if potential_points and time.time() - last_point_time > point_interval:
        points.append(potential_points.pop(0))  # Dodaj nowy punkt do "jablka"
        last_point_time = time.time()  # Zresetuj licznik czasu

    # Rysuje "jablka" jako zolte kropki
    for px, py in points:
        pygame.draw.circle(screen, YELLOW, (px * CELL_SIZE + CELL_SIZE // 2, py * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 3)

    if path_index < len(path):
        # Jesli nie doszlismy do konca sciezki, rysujemy kolejny krok
        current_x, current_y = path[path_index]
        visited_cells.append((current_x, current_y))

        if (current_x, current_y) in points:
            # Jezeli snake dotarl do "jablka", to je zbiera i zwieksza dlugosc
            points.remove((current_x, current_y))
            snake_length += 1  # Zwieksz dlugosc snake'a
            score += 1  # Zwieksz licznik punktow

        if len(visited_cells) > snake_length:
            # Jezeli snake jest dluzszy niz dlugosc, to usuwa ostatni element
            visited_cells.pop(0)

        path_index += 1
        pygame.time.delay(170)  # Delay zeby mozna bylo zobaczyc jak snake sie porusza
    else: # Jezeli doszlismy do konca sciezki, to konczymy gre
        screen.fill(WHITE)  # Wyczyszczenie ekranu

        # Wymiary prostokąta i pozycjonowanie na środku
        rect_width, rect_height = 300, 150
        rect_x = (WIDTH - rect_width) // 2
        rect_y = (HEIGHT - rect_height) // 2

        # Rysowanie białego prostokąta
        pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height))

        # Tworzenie tekstu z końcowym wynikiem
        end_text = font.render(f"Twój wynik: {score}", True, (0, 0, 0))  # Czarny tekst
        text_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Ustawienie tekstu na środku prostokąta

        # Rysowanie tekstu na ekranie
        screen.blit(end_text, text_rect)

    # Rysuje odwiedzone komorki w naprzemiennych kolorach (po to by lepiej zwizualizowac zebrane przez snake'a punkty)
    for i, (vx, vy) in enumerate(visited_cells):
        color = PINK if i % 2 == 0 else PURPLE  # Na przemian różowy i czarny
        pygame.draw.rect(screen, color, (vx * CELL_SIZE, vy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    score_text = font.render(f"Wynik: {score}", True, (136, 78, 203))  # Tekst z wynikiem
    screen.blit(score_text, (470, 10))  # Wyswietl na ekranie w prawym górnym rogu

    # Obsluga zdarzen (zamkniecie okna)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # flip sluzy do odswiezania ekranu
    pygame.display.flip()

# Koniec programu
pygame.quit()
