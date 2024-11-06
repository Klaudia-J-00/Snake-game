import math
import heapq
import pygame
import random

pygame.init()

# Screen and grid settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 50, 50  # 50x50 grid
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labirynt")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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

    :param x:
    :param y:
    :return:
    """
    maze[y][x] = 1  # Oznacza aktualna komorke jako sciezke
    random.shuffle(DIRECTIONS)  # Losowo przemieszaj kierunki

    for dx, dy in DIRECTIONS:
        nx, ny = x + dx * 2, y + dy * 2  # Przesuniecie o 2, aby nie przeskoczyc sciany
        if is_in_bounds(nx, ny) and maze[ny][nx] == 0:
            # Jesli komorka jest w granicach i jest sciana
            maze[y + dy][x + dx] = 1  # Zamien sciane na sciezke
            dfs(nx, ny) # Rekurencyjnie wywolaj funkcje dla nowej komorki

dfs(0, 0) # Rozpoczyna rekurencyjny algorytm generowania labiryntu od punktu (0, 0)

dots = [] # Punkty w labiryncie
max_dots = (ROWS * COLS) // 20  # Maksymalna liczba punktow w labiryncie - 5% komorek
last_dot_time = pygame.time.get_ticks()  # Ostatni czas dodania punktu
dot_interval = 500
dot_progression = 0 # Postep w dodawaniu punktow

# Punkt startu i mety (lewy gorny rog i prawy dolny rog) - w celu wizualizacji kolorem niebieskim i zielonym
start = (0, 0)
end = (COLS - 1, ROWS - 1)

def generate_dot(progress, min_distance=5, max_attempts=100):
    """
    Generuje punkt w labiryncie w zaleznosci od postepu
    """
    # Sprawdza, czy punkt nie jest zbyt blisko startu lub mety
    x_start, x_end = 0, min(COLS - 1, start[0] + progress)
    y_start, y_end = 0, min(ROWS - 1, start[1] + progress)

    attempts = 0
    while attempts < max_attempts:
        x_local, y_local = random.randint(x_start, x_end), random.randint(y_start, y_end)
        if maze[y_local][x_local] == 1 and (x_local, y_local) not in dots:
            # Ensure the point is far enough from existing points
            too_close = False
            for (x, y, _) in dots:
                distance = math.sqrt((x_local - x) ** 2 + (y_local - y) ** 2)
                if distance < min_distance:
                    too_close = True
                    break
            if not too_close:
                random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                dots.append((x_local, y_local, random_color))
                return  # Successfully generated a dot, exit the function
        attempts += 1

# Petla gry
running = True
while running:
    screen.fill(WHITE) # Wypelnia ekran bialym kolorem

    # Rysuje labirynt
    for row in range(ROWS):
        for col in range(COLS):
            # Rysuje sciane lub sciezke w zaleznosci od wartosci w tablicy labiryntu
            color = WHITE if maze[row][col] == 1 else BLACK
            # Rysuje prostokat w miejscu komorki
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Rysuje punkty
        for x, y, color in dots:
            pygame.draw.circle(screen, color, (x * CELL_SIZE + CELL_SIZE // 2,
                                               y * CELL_SIZE + CELL_SIZE // 2), 5)

    # Ryuje punkt startu i mety
    pygame.draw.rect(screen, BLUE, (start[0] * CELL_SIZE, start[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, GREEN, (end[0] * CELL_SIZE, end[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    current_time = pygame.time.get_ticks() # Aktualny czas
    if current_time - last_dot_time > dot_interval and len(dots) < max_dots:
        # Jesli nie osiagnieto maksymalnej liczby punktow w labiryncie i uplynal odpowiedni czas
        # od dodania ostatniego punktu, dodaj nowy punkt
        generate_dot(dot_progression)
        # Zaktualizuj czas ostatniego dodania punktu
        last_dot_time = current_time
        # Zaktualizuj postep dodawania punktow
        dot_progression += 1

    # Sprawdza zdarzenia (zamkniecie okna)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
