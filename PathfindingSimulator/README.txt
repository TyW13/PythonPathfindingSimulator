Pathfinding Simulator

Created using Python and Pyside6 library

A small application where the user can place start, end and obstacle nodes on a square-based grid. The shortest path available (avoiding the obstacles) will be calculated and displayed, starting at the start node and going all the way to the end node (if the path is traversable). The user also has the option to enable/disable the displaying of the pathfinding process that the algorithm takes by toggling the "Show Progress" box. The progress shown is which nodes have been added to the open and closed sets during the pathfinding process. A nice explaination is available in a video created by Youtuber Sebastian Lague called " A* Pathfinding (E01: algorithm explanation) "

Currently only one algorithm is available, A*/AStar, but more are soon to come!

I created this project as a way for me to practice, remind myself and display what I had previously learnt about pathfinding algorithms and also as a way to more familierise myself with the Python programming language and libraries that can be associated with it.


Notes:
Press "Start" to start the algorithm only have a Start node has been placed and an End node has been placed
The path generated will avoid obstacles placed down however it will move through diagonal spaces if there is not an obstacle node on the other side
If the "Show progress" box is ticked, nodes around the path will be coloured either red or green.
- Green nodes symbolise nodes that were to be checked (to find the shortest path to the end) but were never moved to (open set)
- Red nodes symbolise nodes that were to be checked, that eventually have been moved to in the process of finding the shortest path to the end (closed set
Press "Reset Path" to clear only the nodes that make up the path and the nodes within the open/closed sets (green/red)
Press "Clear All" to clear everything in the grid, returning it to its default, empty state