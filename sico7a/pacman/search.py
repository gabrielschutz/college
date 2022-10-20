# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from array import array
from re import L
from threading import stack_size
import util

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

################################################ \/\/\/\/\/ EVERYTHING BELOW THIS LINE IS EDITED CODE \/\/\/\/\/ ################################################

class Node:
    """
    This class represents a node (possible state for Pacman)
    Parameters
    ----------
    state : (x:int,y:int)
        the position of the current node where x is the column and y is the row
    depth : int
        how many other nodes to reach the root. Default is -1 when unused
        (bfs and ucs)
    cost : float
        cost to reach this node, can be used to store the cost for ucs,
        or heuristic value for astar, making this the priority value,
        where the lower the better. Default is -1 when unused (dfs and bfs)
    fromRoot : list of Directions
        list containing the directions taken from the root to this node.
        Default is empty list for the root itself
    """

    def __init__(self, state, depth=-1, cost=-1, fromRoot=[]):
        self.state = state
        self.depth = depth
        self.cost = cost
        self.fromRoot = fromRoot

    def __eq__(self, __o):
        """
        Makes possible for 'Node1 == Node2' or 'Node in List' comparisons
        by comparing only their states
        """

        return self.state == __o.state

    def getIndex(self, List):
        """
        Gets the index of the current node in a node list
        Parameters
        ----------
        List : Node list
            list of Nodes to get the index of the current node from
        Returns
        -------
        i : int
            the position index of the current node inside the list
        None
            if the node could not be found in the list
        """
        
        for i in range(len(List)):          # Loops the list
            if List[i].state == self.state: # If the state of the list's current position is the same as the node's...
                return i                    # Returns the current position
        return None                         # If it couldn't be found, returns None

    def insertionSort(self, List):
        """
        Inserts a node in a node list ordering crescently by cost
        Parameters
        ----------
        List : Node list
            list of Nodes to insert the new node in
        """

        for i in range(len(List)):          # Loops the List
            if List[i].cost > self.cost:    # If the cost of the node in the current position is higher than the cost of the new node
                List.insert(i, self)        # Inserts the new node on that position
                return                      # And breaks out of the function
        List.append(self)                   # If it didn't broke out, means that the cost of the new node is higher than all the nodes in the List,
                                            # so it just appends the node to end of the List

def depthFirstSearch(problem):
    """
    Search the deepest List in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    depth = 0                                       # Initiates the depth as 0
    X = Node(problem.getStartState(), depth=depth)  # Creates a node based on the initial state called X with the set depth
    Open = [X]                                      # Creates a list (Open) to hold all the visited, but not finished, with X in it
    Clsd = []                                       # Creates an empty list (Closed) to hold all finished List (List that already had all
                                                    # it's children checked)
    while Open != []:                               # Keeps checking the List until there's no unfinished node left
        X = Open.pop(0)                                 # Pops the first element in Open and store it in X
        if problem.isGoalState(X.state):                # If the state of X is the objective...
            return X.fromRoot                               # Returns its path
        else:                                           # Otherwise...
            Aux = problem.getSuccessors(X.state)            # Generates it's children and stores it in an auxiliary list
                                                            # For instance, getSuccessors generates a list of tuples where the first position (Aux[i][0]) holds
                                                            # the state, the second position (Aux[i][1]) holds the Direction (North, East, South, West) taken
                                                            # from the parent to the child, and the third (Aux[i][2]) holds the cost for such path
                                                            # (default is 1), which is unused by some algorithms
            Children = []                                   # Initiates the Children list as en empty list
            depth = X.depth + 1                             # Makes the children's depth be their parent's depth + 1
            for i in range(len(Aux)):                       # Loops the auxiliary list
                path = []                                       # Initiates a path list as empty in every loop to restart it
                for j in range(len(X.fromRoot)):                # Loops it's parent's path list
                    path.append(X.fromRoot[j])                  # Adds what's in the parent's path list to the newly created list
                                                                # (Tried doing the above outside the loop, then inside it'd append the new path, set the
                                                                # child, and pop that last path for the next child, but was having strange pointer
                                                                # behavior where X.fromRoot was changing altogether)
                path.append(Aux[i][1])                          # Inserts the path from the parent to the child at the end of the list
                Children.append(Node(Aux[i][0], depth=depth, fromRoot=path))# Creates the child Node with the new state, depth and path, then adds it to list
            Clsd.append(X)                                  # Adds the current Node (parent node) to the Closed list
            for i in range(len(Children)):                  # Loops the Children list
                if not(Children[i] in Open) and not(Children[i] in Clsd):# If the current child is neither in Open nor in Closed
                    Open.insert(0, Children[i])                     # Inserts the child at the START of the Open list
    return []                                       # If it broke out of the loop, returns an empty list, meaning it failed

def breadthFirstSearch(problem):
    """Search the shallowest List in the search tree first."""
    
    X = Node(problem.getStartState())               # Creates the initial node
    Open = [X]                                      # Creates the Open list
    Clsd = []                                       # Creates the Closed list
    while Open != []:                               # Loops while Open isn't empty
        X = Open.pop(0)                                 # Pops the first element in Open and store it in X
        if problem.isGoalState(X.state):                # If X is the objective...
            return X.fromRoot                               # Returns its path
        else:                                           # Otherwise...
            Aux = problem.getSuccessors(X.state)            # Generates it's children
            Children = []                                   # Initiates the Children list
            for i in range(len(Aux)):                       # Loops the auxiliary list
                path = []                                       # Initiates the path list
                for j in range(len(X.fromRoot)):                # Loops it's parent's path list
                    path.append(X.fromRoot[j])                      # Adds what's in the parent's path list to the newly created list
                path.append(Aux[i][1])                          # Inserts the path from the parent to the child at the end of the list
                Children.append(Node(Aux[i][0], fromRoot=path)) # Creates the child Node with the new state and path, then adds it to list
            Clsd.append(X)                                  # Puts the parent in Closed
            for i in range(len(Children)):                  # Loops the Children list
                if not(Children[i] in Open) and not(Children[i] in Clsd):# If the current child is neither in Open nor in Closed
                    Open.append(Children[i])                        # Inserts the child at the END of the Open list
    return []                                       # Returns an empty list if it failed

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    X = Node(problem.getStartState())               # Creates the initial node
    Open = [X]                                      # Creates the Open list
    Clsd = []                                       # Creates the Closed list
    while Open != []:                               # Loops while Open isn't empty
        X = Open.pop(0)                                 # Pops the first element in Open and store it in X
        if problem.isGoalState(X.state):                # If X is the objective
            return X.fromRoot                               # Returns its path
        else:                                           # Otherwise
            Aux = problem.getSuccessors(X.state)            # Generates it's children
            Children = []                                   # Initiates the Children list
            for i in range(len(Aux)):                       # Loops the auxiliary list
                path = []                                       # Initiates the path list
                for j in range(len(X.fromRoot)):                # Loops it's parent's path list
                    path.append(X.fromRoot[j])                      # Adds what's in the parent's path list to the newly created list
                path.append(Aux[i][1])                          # Inserts the path from the parent to the child at the end of the list
                Children.append(Node(Aux[i][0], cost=Aux[i][2], fromRoot=path))# Creates the child Node with the new state, cost and path, then adds it to list
            for i in range(len(Children)):                  # Loops the Children list
                if not(Children[i] in Open) and not(Children[i] in Clsd):# If the current child is neither in Open nor in Closed
                    Children[i].insertionSort(Open)                 # Inserts it in the Open list, ordering it crescently by cost
                elif Children[i] in Open:                       # If it's only in the Open list
                    pos = Children[i].getIndex(Open)                # Gets it's position in the list
                    if Children[i].cost < Open[pos].cost:           # If the current child's cost is lower than the cost of the node in the Open list
                        Open.pop(pos)                                   # Removes the node currently inside Open
                        Children[i].insertionSort(Open)                 # And replaces it with the new child
                elif Children[i] in Clsd:                       # If it's only in the Closed list
                    pos = Children[i].getIndex(Clsd)                # Gets it's position in the list
                    if Children[i].cost < Clsd[pos].cost:           # If the current child's cost is lower than the cost of the node in the Open list
                        Clsd.pop(pos)                                   # Removes the node currently inside Closed
                        Children[i].insertionSort(Open)                 # And inserts it in the Open list, ordering it crescently by cost
        Clsd.append(X)                                  # Then, inserts X at the end of the Closed list
    return []                                       # Returns an empty list if it failed

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    depth = 0
    ini = problem.getStartState()
    X = Node(ini,depth=depth,cost=heuristic(ini,problem))# Creates a node based on the initial state called X with a set depth and heuristic (cost)
    Open = [X]                                      # Creates the Open list
    Clsd = []                                       # Creates the Closed list
    while Open != []:                               # Loops while Open isn't empty
        X = Open.pop(0)                                 # Pops the first element in Open and store it in X
        depth = X.depth + 1                             # Makes the children's depth be their parent's depth + 1
        if problem.isGoalState(X.state):                # If X is the objective
            return X.fromRoot                               # Returns its path
        else:                                           # Otherwise
            Aux = problem.getSuccessors(X.state)            # Generates it's children
            Children = []                                   # Initiates the Children list
            for i in range(len(Aux)):                       # Loops the auxiliary list
                path = []                                       # Initiates the path list
                for j in range(len(X.fromRoot)):                # Loops it's parent's path list
                    path.append(X.fromRoot[j])                      # Adds what's in the parent's path list to the newly created list
                path.append(Aux[i][1])                          # Inserts the path from the parent to the child at the end of the list
                Children.append(Node(Aux[i][0],depth=depth,cost=heuristic(Aux[i][0],problem)+depth,fromRoot=path))
                                                                # Creates the child Node with the new state, depth, cost and path, then adds it to list
                                                                # Note that the cost is the heuristic value + its depth. Since the algorithm prioritizes
                                                                # lower costs, shallower nodes will be prioritized as objective
            for i in range(len(Children)):                  # Loops the Children list
                if not(Children[i] in Open) and not(Children[i] in Clsd):# If the current child is neither in Open nor in Closed
                    Children[i].insertionSort(Open)                 # Inserts it in the Open list, ordering it crescently by cost
        Clsd.append(X)                                  # Then, inserts X at the end of the Closed list
    return []                                       # Returns an empty list if it failed

################################################ /\/\/\/\/\ EVERYTHING ABOVE THIS LINE IS EDITED CODE /\/\/\/\/\ ################################################

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
