# Snake-game
This game is a simple maze simulation in which a snake navigates along a path generated using the A* algorithm. The goal of the game is for the snake to collect as many "apples" (yellow points) as possible while moving from the starting point to the endpoint in the maze.

The maze is generated using the DFS (Depth-First Search) algorithm, and then the shortest path is calculated using the A* algorithm.

## Setup a virtual environment
```bash
python3 -m venv venv
.\venv\Scripts\activate
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run the maze
```bash
python maze.py
```

## Run the snake game
```bash
python snake.py
```

## Features
1. **Maze generation** - The maze is generated using the DFS algorithm.
2. **A-STAR algorithm** - The A* algorithm is used to find the shortest path from the starting point to the endpoint.
3. **Snake Movement** - The snake moves along the path found by the A* algorithm.
4. **Point collection** - The snake collects points (apples) along the path, which increase its length and score when collected. 
5. **Game Over** - The game ends when the snake reaches the endpoint of the maze and screen displays the final score.

## Maze generation 
Maze is being generated using recursive algorithm dfs. 
The 1s represent the path and 0s represent the walls. 

## A* algorithm
A* algorithm is used to find the shortest path for the snake to travel 
to reach the end of the maze. It looks for the path (1's) in the maze. 
It uses the Manhattan distance as the heuristic function. It calculates 
g_score, f_score for each node in the maze. g_score is the 
distance from the start node to the current node, f_score is the sum of
g_score and h_score. 

## UI 
The game is implemented using pygame library. The maze walls are 
represented by black color, the path is represented by white color and
the snake is represented by pink and purple color. The apples are displayed 
as yellow dots. 

### astar.py 
This file contains the implementation of the A* algorithm. 

### maze.py 
This file contains the implementation of the maze generation algorithm. 
It also has a simple UI to display the maze and the path found by the A* algorithm.
The path is displayed in pink color.
![maze](/img/maze.png)

### snake.py
This file contains the implementation of the snake game. 
The snake automatically moves through the maze, following the path found by the A* algorithm.
The snake collects points (apples) along the path, which increase its length and score when collected.
The player's score is displayed in the top-right corner. When the snake reaches the endpoint, the game ends, 
and a final score screen is displayed. 

#### Settings 
The settings for the game can be changed in the settings.py file.
You can adjust them to change game settings: 
- **WIDTH** - Width of the screen
- **HEIGHT** - Height of the screen
- **ROWS** - Number of rows in the maze
- **COLS** - Number of columns in the maze
- **CELL_SIZE** - Size of each cell in the maze
- **Colors** - Colors used in the game

## Screenshots
Snake game: 
![snake](/img/snake.png)


Final score screen:
![score](/img/score.png)

