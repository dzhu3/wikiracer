from py_wikiracer.internet import Internet
from typing import List
from html.parser import HTMLParser
import heapq

class Parser:

    @staticmethod
    def get_links_in_page(html: str) -> List[str]:
        """
        In this method, we should parse a page's HTML and return a list of links in the page.
        Be sure not to return any link with a DISALLOWED character.
        All links should be of the form "/wiki/<page name>", as to not follow external links.

        To do this, you can use str.find, regex, or you can
            instantiate your own subclass of HTMLParser in this function and feed it the html.
        """
        disallowed = Internet.DISALLOWED

        class MyHTMLParser(HTMLParser):

            lsLinks = list()

            def handle_starttag(self, tag, attributes):
                if tag == "a":  # anchor tag
                    for name, value in attributes:
                        if name == "href" and value[:6] == "/wiki/" and not any(
                                x in value[6:] for x in disallowed):
                            if value not in self.lsLinks:  # no duplicates
                                self.lsLinks.append(value)

        parser = MyHTMLParser()
        parser.feed(html)

        return parser.lsLinks

# In these methods, we are given a source page and a goal page, and we should return
#  the shortest path between the two pages. Be careful! Wikipedia is very large.

# These are all very similar algorithms, so it is advisable to make a global helper function that does all of the work, and have
#  each of these call the helper with a different data type (stack, queue, priority queue, etc.)

class BFSProblem:
    def __init__(self, internet: Internet):
        self.internet = internet
    # Example in/outputs:
    #  bfs(source = "/wiki/Computer_science", goal = "/wiki/Computer_science") == ["/wiki/Computer_science", "/wiki/Computer_science"]
    #  bfs(source = "/wiki/Computer_science", goal = "/wiki/Computation") == ["/wiki/Computer_science", "/wiki/Computation"]
    # Find more in the test case file.

    # Do not try to make fancy optimizations here. The autograder depends on you following standard BFS and will check all of the pages you download.
    # Links should be inserted into the queue as they are located in the page, and should be obtained using Parser's get_links_in_page.
    # Be very careful not to add things to the "visited" set of pages too early. You must wait for them to come out of the queue first. See if you can figure out why.
    #  This applies for bfs, dfs, and dijkstra's.
    # Download a page with self.internet.get_page().
    def bfs(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia"):

        def backtrack(start, end):
            if start == end:
                return [start, end]
            path = [end]
            while path[-1] != start:
                path.append(parent_pointer[path[-1]])
            path.reverse()
            return path

        visited = [source]
        parent_pointer = {}
        queue = [source]
        while queue:
            v = queue.pop(0)
            visited.append(v)
            v_html = self.internet.get_page(v)
            v_links = Parser.get_links_in_page(v_html)
            for i in v_links:
                if i == goal:
                    parent_pointer[i] = v
                    return backtrack(source, goal)
                if i not in visited:
                    if i not in queue:
                        queue.append(i)
                        parent_pointer[i] = v
        return None  # no path detected


class DFSProblem:
    def __init__(self, internet: Internet):
        self.internet = internet

    # Links should be inserted into a stack as they are located in the page. Do not add things to the visited list until they are taken out of the stack.
    def dfs(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia"):

        def backtrack(start, end):
            if start == end:
                return [start, end]
            path = [end]
            while path[-1] != start:
                path.append(parent_pointer[path[-1]])
            path.reverse()
            return path

        stack = [source]
        parent_pointer = {}
        visited = [source]
        while stack:
            v = stack.pop()
            visited.append(v)
            v_html = self.internet.get_page(v)
            v_links = Parser.get_links_in_page(v_html)
            for i in v_links:
                if i == goal:
                    parent_pointer[i] = v
                    return backtrack(source, goal)
                elif i not in visited:
                    parent_pointer[i] = v
                    stack.append(i)

        return None  # if no path exists, return None

class DijkstrasProblem:
    def __init__(self, internet: Internet):
        self.internet = internet
        self.priorityqueue = {}
        self.visited = []
    # Links should be inserted into the heap as they are located in the page.
    # By default, the cost of going to a link is the length of a particular destination link's name. For instance,
    #  if we consider /wiki/a -> /wiki/ab, then the default cost function will have a value of 8.
    # This cost function is overridable and your implementation will be tested on different cost functions. Use costFn(node1, node2)
    #  to get the cost of a particular edge.
    # You should return the path from source to goal that minimizes the total cost. Assume cost > 0 for all edges.
    def removeMin(self):
        heap_dict = []
        for key, value in self.priorityqueue.items():
            heap_dict.append((value, key))
        heapq.heapify(heap_dict)
        min_value = heapq.heappop(heap_dict)
        self.visited.append(min_value[1])  # append the vertex you just popped, added to set
        new_dict = []
        for value, key in heap_dict:
            new_dict.append((key, value))
        self.priorityqueue = dict(new_dict)
        return min_value  # 2-tuple with (cost, link)

    def dijkstras(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia", costFn = lambda x, y: len(y)):

        self.priorityqueue = {}
        parent_pointer = {}
        self.visited = [source]

        def backtrack(start, end):
            if start == end:
                return [start, end]
            path = [end]
            while path[-1] != start:
                path.append(parent_pointer[path[-1]])
            path.reverse()
            return path

        source_links = Parser.get_links_in_page(self.internet.get_page(source))
        for i in source_links:
            if i == goal:
                return [source, i]
            elif i not in self.visited:
                parent_pointer[i] = source
                self.priorityqueue[i] = costFn(source, i)

        while self.priorityqueue:
            v_distance, v = self.removeMin()
            v_links = Parser.get_links_in_page(self.internet.get_page(v))
            for v_adj in v_links:
                if v_adj == goal:
                    parent_pointer[v_adj] = v
                    return backtrack(source, goal)
                if v_adj not in self.visited:
                    if v_adj not in self.priorityqueue:
                        self.priorityqueue[v_adj] = costFn(v, v_adj) + v_distance
                        parent_pointer[v_adj] = v
                    elif costFn(v, v_adj) + v_distance < self.priorityqueue[v_adj]:  # compare costs and update if needed
                        parent_pointer[v_adj] = v
                        self.priorityqueue[v_adj] = costFn(v, v_adj) + v_distance

        return None  # if no path exists, return None


class WikiracerProblem:
    def __init__(self, internet: Internet):
        self.internet = internet

    # Time for you to have fun! Using what you know, try to efficiently find the shortest path between two wikipedia pages.
    # Your only goal here is to minimize the total amount of pages downloaded from the Internet, as that is the dominating time-consuming action.

    # Your answer doesn't have to be perfect by any means, but we want to see some creative ideas.
    # One possible starting place is to get the links in `goal`, and then search for any of those from the source page, hoping that those pages lead back to goal.

    # Note: a BFS implementation with no optimizations will not get credit, and it will suck.
    # You may find Internet.get_random() useful, or you may not.

    def wikiracer(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia"):  # try double ended BFS

        if source == goal:
            return [source, goal]
        def backtrack(start, end):
            if start == end:
                return [start, end]
            path = [end]
            while path[-1] != start:
                path.append(parent_pointer[path[-1]])
            path.reverse()
            return path

        goal_links = Parser.get_links_in_page(self.internet.get_page(goal))

        visited = []
        parent_pointer = {}
        queue = [source]
        while queue:
            v = queue.pop(0)
            visited.append(v)
            v_links = Parser.get_links_in_page(self.internet.get_page(v))

            for i in v_links:
                if i == goal:
                    parent_pointer[i] = v
                    return backtrack(source, goal)
                elif i in goal_links and i not in visited:
                    parent_pointer[i] = v
                    visited.append(i)
                    i_links = Parser.get_links_in_page(self.internet.get_page(i))
                    for i_link in i_links:
                        if i_link == goal:
                            parent_pointer[goal] = i
                            return backtrack(source, goal)
                elif i not in visited:
                    if i not in queue:
                        queue.append(i)
                        parent_pointer[i] = v
        return None

# KARMA
class FindInPageProblem:
    def __init__(self, internet: Internet):
        self.internet = internet
    # This Karma problem is a little different. In this, we give you a source page, and then ask you to make up some heuristics that will allow you to efficiently
    #  find a page containing all of the words in `query`. Again, optimize for the fewest number of internet downloads, not for the shortest path.

    def find_in_page(self, source = "/wiki/Calvin_Li", query = ["ham", "cheese"]):

        raise NotImplementedError("Karma method find_in_page")

        path = [source]

        # find a path to a page that contains ALL of the words in query in any place within the page
        # path[-1] should be the page that fulfills the query.
        # YOUR CODE HERE

        return path # if no path exists, return None
