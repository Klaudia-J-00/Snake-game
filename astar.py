import heapq

class MazeSolver:
    """
    Klasa sluzaca do rozwiazywania labiryntu za pomoca algorytmu A*
    """
    def __init__(self, maze):
        """
        Inicjalizuje obiekt klasy MazeSolver
        maze - dwuwymiarowa tablica reprezentujaca labirynt, gdzie 1 oznacza sciezke, a 0 sciane
        rows - liczba wierszy w labiryncie
        cols - liczba kolumn w labiryncie
        """
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def is_valid(self, x, y):
        """
        Sprawdza, czy dana komorka jest w granicach labiryntu i czy jest sciezka

        Jezeli x jest wieksze od 0 i mniejsze od liczby wierszy oraz y jest wieksze od 0 i mniejsze od liczby kolumn
        oraz komorka o wspolrzednych x, y jest sciezka (1), zwraca True, w przeciwnym razie False
        """
        return 0 <= x < self.rows and 0 <= y < self.cols and self.maze[x][y] == 1

    def heuristic(self, a, b):
        """
        Oblicza heurystyke dla dwoch punktow a i b

        Heurystyka to odleglosc Manhattan miedzy punktami a i b zgodnie z wzorem:
        |x1 - x2| + |y1 - y2|
        """
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star(self, start, end):
        """
        Rozwiazuje labirynt za pomoca algorytmu A*

        start - punkt startowy
        end - punkt koncowy
        """
        # Kolejka priorytetowa do przechowywania komorek do odwiedzenia
        open_set = []
        heapq.heappush(open_set, (0, start))

        # G_score to koszt dotarcia do danego punktu
        # F_score to suma g_score i heurystyki
        # Came_from to slownik przechowujacy poprzednie komorki
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}
        came_from = {}

        # Dopoki kolejka nie jest pusta
        while open_set:
            # Pobierz komorke z najmniejszym f_score (bo tras moze byc wiecej, ale szukamy najkrotszej)
            current = heapq.heappop(open_set)[1]

            # Jezeli dotarlismy do konca, zrekonstruuj sciezke
            if current == end:
                return self.reconstruct_path(came_from, current)

            # Pobierz wspolrzedne aktualnej komorki
            x, y = current
            # Sprawdz sasiadow aktualnej komorki (w lewo, prawo, gora, dol)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # Wspolrzedne sasiada
                neighbor = (x + dx, y + dy)

                # Jezeli sasiad jest w granicach labiryntu
                if self.is_valid(*neighbor):
                    # Oblicz nowy g_score
                    tentative_g_score = g_score[current] + 1

                    # Jezeli nowy g_score jest mniejszy niz poprzedni, zaktualizuj wartosci
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        # Zaktualizuj wartosci g_score, f_score i dodaj do kolejki
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # Jezeli nie znaleziono sciezki, zwroc None
        return None

    def reconstruct_path(self, came_from, current):
        """
        Rekonstruuje sciezke na podstawie slownika came_from

        came_from - slownik przechowujacy poprzednie komorki
        current - aktualna komorka
        """
        path = []
        # Rekonstruuj sciezke od konca do poczatku
        while current in came_from:
            # Dodaj komorke do sciezki
            path.append(current)
            # Przejdz do poprzedniej komorki
            current = came_from[current]
        path.append(current)  # Dodaj aktualna komorke
        path.reverse()        # Odwroc sciezke (od poczatku do konca)
        return path

# Przykladowe uzycie:

# maze = [[1, 0, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 1, 1, 0, 1, 0], [1, 0, 0, 0, 1, 0, 0, 0, 1, 0], [1, 1, 1, 1, 1, 0, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#
# num_rows = 0
# for rows in maze:
#     num_rows += 1
#
# solver = MazeSolver(maze)
# start = (0, 0)
# end = (9, 9)
# path = solver.a_star(start, end)
# print("Path found:" if path else "No path found", path)
