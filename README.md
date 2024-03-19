# Maze solver

## Requirements
```python
import PIL
```
## How to use
1. Create a txt file and type your maze with the rules below:
   - wall char must be '#'
   - paths must be '(spacebar)'
   - objective must be 'B'
   - start must be 'A'
   - example:
    ```
    #####B#
    ##### #
    ####  #
    #### ##
         ##
    A######

    ```
    
2. open your cmd on the scr folder path and type:
```
python Solver.py [MazeFile].txt 
```

## Results
the code will process the shortest path from the start to the objective and print it. In addition it will also generate a png image, on the same path as the code, with the maze and the path drawn
### Still on production
#### next objectives:
- add a graphic interface
- add a maze generator
- add a 3d maze solver and a graphic interface to it
