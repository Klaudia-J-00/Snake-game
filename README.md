# Snake-game
Snake game implemented using A* algorithm

## Setup a virtual environment
```bash
python3 -m venv venv
.\venv\Scripts\activate
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run the game
```bash
python snake.py
```

## Maze generation 
Maze is being generated using recursive algorithm dfs. 
The 1s represent the path and 0s represent the walls. 

## A* algorithm
A* algorithm is used to find the shortest path for the snake to travel 
to reach the end of the maze. 

## UI 
The game is implemented using pygame library. The maze walls are 
represented by black color, the path is represented by white color and
the snake is represented by pink color.

