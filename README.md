# Wikiracer

The Wikiracer project is a Python-based tool that aims to find a path from a starting Wikipedia page to a target Wikipedia page. It utilizes the HTML parser module to parse webpages and implements multiple strategies, including Breadth-First Search (BFS), Depth-First Search (DFS), and Dijkstra's algorithm, to find the shortest path between the given pages.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/dzhu3/wikiracer.git
   ```

2. Navigate to the project directory:

   ```shell
   cd wikiracer
   ```

## Usage

To use the Wikiracer tool, follow these steps:

1. Open the `wikiracer.py` file in your preferred text editor.

2. Modify the `start_page` and `target_page` variables at the beginning of the file to specify the Wikipedia pages you want to start and end with, respectively. For example:

   ```python
   start_page = "https://en.wikipedia.org/wiki/Python_(programming_language)"
   target_page = "https://en.wikipedia.org/wiki/Artificial_intelligence"
   ```

3. Specify the algorithm you want to use by uncommenting the corresponding line of code. By default, the BFS strategy is selected:

   ```python
   # algorithm = bfs_strategy
   # algorithm = dfs_strategy
   # algorithm = dijkstra_strategy
   ```

4. Save the changes and run the `wikiracer.py` file:

   ```shell
   python wikiracer.py
   ```

5. The program will start searching for the shortest path between the provided Wikipedia pages using the chosen algorithm. The progress will be displayed in the console, and once a path is found, it will be printed.

## Algorithms

The Wikiracer project implements the following algorithms to find a path between the start and target pages:

### Breadth-First Search (BFS)

BFS is an algorithm that explores all the neighbor nodes at the present depth before moving on to the nodes at the next depth level. In the context of Wikiracer, BFS will search Wikipedia pages by examining the links on each page in a breadth-first manner until it finds the target page.

### Depth-First Search (DFS)

DFS is an algorithm that explores as far as possible along each branch before backtracking. It traverses down a path until it reaches a dead-end and then backtracks to the previous unexplored path. In the context of Wikiracer, DFS will search Wikipedia pages by exploring the links on each page in a depth-first manner until it finds the target page.

### Dijkstra's Algorithm

Dijkstra's algorithm is an algorithm for finding the shortest path between nodes in a graph. It maintains a priority queue of nodes and explores the nodes in the order of their priority. In the context of Wikiracer, Dijkstra's algorithm will search Wikipedia pages by assigning weights to the links based on their distance from the start page and finding the shortest path to the target page.

## Contributions

Contributions to the Wikiracer project are welcome! If you have any improvements, bug fixes, or new features to suggest, please submit a pull request.

## Disclaimer

The Wikiracer tool is provided as-is without any warranty. The developers are not responsible for any misuse or damage caused by the tool. Please use it responsibly and respect the usage policies of Wikipedia.
