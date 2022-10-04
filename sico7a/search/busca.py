import numpy as np

class Node:
    """
    Class for a node from the tree created from search algorithms

    Attributes
    ---------

    graph : object matrix
        the main object of the node which holds the current position of the
        objects in the puzzle
    pai : Node
        the parent node of the current node
    depth : int
        depth of the node only used for limited Depth-First Search
    heur : int
        heuristic of the node for the Best Match Search algorith
    path : Node array
        array the holds the path from the current node to the root
        in order = [current node, it's parent, it's parent's parent,..., root]

    Methods
    -------

    setPath()
        sets the path from the node to the root
    setHeur(obj)
        sets the heuristic value of the node based on the objective
    printPath()
        prints the path from the root to the node
    checkExiste(Nodes)
        checks if the node is present in an array of nodes
    getIndex(Nodes)
        gets the position of the node in an array of nodes
    findX()
        finds the position of the movable object from the main object
        of the node
    """

    def __init__(self, paramGraph, paramPai=-1, paramDepth=-1, paramHeur=-1, paramPath=[]) -> None:
        """
        Parameters
        ----------

        graph : object matrix
            the main object of the node which holds the current position of the
            objects in the puzzle
        pai : Node
            the parent node of the current node (default is -1 for the root [no parent])
        depth : int
            depth of the node only used for limited Depth-First Search
            (default is -1 since only one algorithm uses it)
        heur : int
            heuristic of the node for the Best Match Search algorith
            (default is -1 since only one algorithm uses it)
        path : Node array
            array the holds the path from the current node to the root
            in order = [current node, it's parent, it's parent's parent,..., root]
            (default is an empty array)
        """

        self.graph = paramGraph
        self.pai = paramPai
        self.depth = paramDepth
        self.heur = paramHeur
        self.path = paramPath

    def setPath(self):
        """
        Sets the path from the node in it's path attribute. Starts at the
        desired node, adds it to the path's array, then moves to the node's
        parent, adding each parent until it reaches the root where the parent
        is -1
        """

        Aux = self
        while 1:
            self.path = [*self.path, Aux.graph]
            if Aux.pai == -1:
                break
            Aux = Aux.pai

    def setHeur(self, obj):
        """
        Sets the heuristic of the current by comparing the node with the objective.
        The lower the better. Starts at row*columns and subtracts 1 for each object
        in the correct position except for the movable object

        Parameters
        ----------

        obj : object matrix
            objective matrix for the puzzle
        """

        lin = np.shape(self.graph)[0]
        col = np.shape(self.graph)[1]
        self.heur = lin*col
        for i in range(lin):
            for j in range(col):
                if(self.graph[i][j] != 'X') and (self.graph[i][j] == obj[i][j]):
                    self.heur -= 1

    def printPath(self):
        """
        Prints the path by looping backwards the node's path array and printing
        each node's main object
        """

        for i in range(len(self.path)-1, -1, -1):
            print(self.path[i], '\n')

    def checkExiste(self, Nodes):
        """
        Checks if the current node is present in a node array

        Parameters
        ----------

        Nodes : Node array
            array of nodes to check if the current node is present within

        Returns
        -------

        1 
            if the node is present
        0
            if the node is not present
        """

        for j in range(len(Nodes)):
            if (Nodes[j].graph == self.graph).all():
                return 1
        return 0

    def getIndex(self, Nodes):
        """
        Gets the index of the current node in a node array

        Parameters
        ----------

        Nodes : Node array
            array of nodes to get the index of the current node from

        Returns
        -------

        j
            which is the position index of the current node
            inside the array
        -1
            if the node could not be found in the array
        """
        
        for j in range(len(Nodes)):
            if (Nodes[j].graph == self.graph).all():
                return j
        return -1

    def findX(self):
        """
        Finds the position index of the movable object inside the current
        node's main object

        Returns
        -------

        two position int array with the row and column of the movable object
        """

        for i in range(np.shape(self.graph)[0]):
            for j in range(np.shape(self.graph)[1]):
                if(self.graph[i][j] == 'X'):
                    return [i, j]

def BFS(inicial, obj):
    X = Node(inicial)
    Abertos = [X]
    Fechados = []
    iter = 0
    while Abertos != []:
        iter += 1
        X = Abertos[0]
        del Abertos[0]
        if (X.graph == obj).all():
            X.setPath()
            return [X, iter]
        else:
            Aux = geraFilhos(X.graph)
            FilhosX = []
            for i in range(len(Aux)):
                FilhosX = [*FilhosX, Node(Aux[i], X)]
            Fechados.append(X)
            for i in range(len(FilhosX)):
                if not(FilhosX[i].checkExiste(Abertos)) and not(FilhosX[i].checkExiste(Fechados)):
                    Abertos = [*Abertos, FilhosX[i]]
    return [[], iter]

def DFS(inicial, obj, lim):
    depth = 0
    X = Node(inicial, paramDepth=depth)
    Abertos = [X]
    Fechados = []
    iter = 0
    while Abertos != []:
        iter += 1
        X = Abertos[0]
        del Abertos[0]
        if (X.graph == obj).all():
            X.setPath()
            return [X, iter]
        elif X.depth < lim:
            Aux = geraFilhos(X.graph)
            FilhosX = []
            depth = X.depth + 1
            for i in range(len(Aux)):
                FilhosX = [*FilhosX, Node(Aux[i], X, depth)]
            Fechados.append(X)
            for i in range(len(FilhosX)-1,-1,-1):
                if not(FilhosX[i].checkExiste(Abertos)) and not(FilhosX[i].checkExiste(Fechados)):
                    Abertos = [FilhosX[i], *Abertos]
    return [[], iter]

def BME(inicial, obj):
    X = Node(inicial)
    Abertos = [X]
    Fechados = []
    iter = 0
    while Abertos != []:
        iter += 1
        X = Abertos[0]
        del Abertos[0]
        if(X.graph == obj).all():
            X.setPath()
            return [X, iter]
        else:
            Aux = geraFilhos(X.graph)
            FilhosX = []
            for i in range(len(Aux)):
                FilhosX = [*FilhosX, Node(Aux[i], X)]
            for i in range(len(FilhosX)):
                if not(FilhosX[i].checkExiste(Abertos)) and not(FilhosX[i].checkExiste(Fechados)):
                    FilhosX[i].setHeur(obj)
                    Abertos = insertionSort(Abertos, FilhosX[i])
                elif FilhosX[i].checkExiste(Abertos):
                    pos = FilhosX[i].getIndex(Abertos)
                    if (len(FilhosX[i].path) < len(Abertos[pos].path)):
                        Abertos[pos] = FilhosX[i]
                elif FilhosX[i].checkExiste(Fechados):
                    pos = FilhosX[i].getIndex(Fechados)
                    if (len(FilhosX[i].path) < len(Fechados[pos].path)):
                        del Fechados[pos]
                        Abertos = insertionSort(Abertos, FilhosX[i])
        Fechados = [*Fechados, X]
    return [[], iter]

def geraFilhos(graph):
    for i in range(np.shape(graph)[0]):
        for j in range(np.shape(graph)[1]):
            if(graph[i][j] == 'X'):
                posX = [i, j]
    Aux = np.ndarray(shape=(4,np.shape(graph)[0],np.shape(graph)[1]), dtype=object)
    k = 0
    if(posX[1]-1 >= 0):
        Aux[k] = graph
        Aux[k][posX[0]][posX[1]-1] = graph[posX[0]][posX[1]]
        Aux[k][posX[0]][posX[1]] = graph[posX[0]][posX[1]-1]
        k += 1
    if(posX[0]-1 >= 0):
        Aux[k] = graph
        Aux[k][posX[0]-1][posX[1]] = graph[posX[0]][posX[1]]
        Aux[k][posX[0]][posX[1]] = graph[posX[0]-1][posX[1]]
        k += 1
    if(posX[1]+1 <= np.shape(graph)[1]-1):
        Aux[k] = graph
        Aux[k][posX[0]][posX[1]+1] = graph[posX[0]][posX[1]]
        Aux[k][posX[0]][posX[1]] = graph[posX[0]][posX[1]+1]
        k += 1
    if(posX[0]+1 <= np.shape(graph)[1]-1):
        Aux[k] = graph
        Aux[k][posX[0]+1][posX[1]] = graph[posX[0]][posX[1]]
        Aux[k][posX[0]][posX[1]] = graph[posX[0]+1][posX[1]]
        k += 1
    return Aux[0:k]

def insertionSort(A, ins):
    n = len(A)
    for i in range(n):
        if A[i].heur > ins.heur:
            return [*A[0:i], ins, *A[i:n]]
    return [*A, ins]

################################################## MAIN ##################################################

Obj = np.array([[1,  2 , 3],
                [8, 'X', 4],
                [7,  6 , 5]])

Ini = np.array([[2,  8 , 3],
                [1,  6 , 4],
                [7, 'X', 5]])

BFSres = BFS(Ini, Obj)
print('\nBFS:', BFSres[1], 'iteracoes\n\n',BFSres[0].graph, '\n\nCAMINHO:\n')
BFSres[0].printPath()

DFSres = DFS(Ini, Obj, 5)
print('\nDFS:', DFSres[1], 'iteracoes\n\n',DFSres[0].graph, '\n\nCAMINHO:\n')
DFSres[0].printPath()

BMEres = BME(Ini, Obj)
print('\nBusca Melhor Escolha:', BMEres[1], 'iteracoes\n\n',BMEres[0].graph, '\n\nCAMINHO:\n')
BMEres[0].printPath()
