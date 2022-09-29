import numpy as np

class Node:
    def __init__(self, paramGraph, paramPai, paramDepth) -> None:
        self.graph = paramGraph
        self.pai = paramPai
        self.depth = paramDepth
    def printPath(self, Ini):
        Aux = self
        while 1:
            print(Aux.graph, '\n')
            if (Aux.graph == Ini).all():
                break
            Aux = Aux.pai
    def checkExiste(self, Nodes):
        for j in range(np.shape(Nodes)[0]):
            if (Nodes[j].graph == self.graph).all():
                return 1
        return 0

def BFS(inicial, obj):
    X = Node(inicial, -1, -1)
    Abertos = [X]
    Fechados = []
    iter = 0
    while Abertos != []:
        iter += 1
        X = Abertos[0]
        del Abertos[0]
        if (X.graph == obj).all():
            return [X, iter]
        else:
            Aux = geraFilhos(X.graph)
            FilhosX = []
            for i in range(np.shape(Aux)[0]):
                FilhosX = [*FilhosX, Node(Aux[i], X, -1)]
            Fechados.append(X)
            for i in range(len(FilhosX)):
                if not(FilhosX[i].checkExiste(Abertos)) and not(FilhosX[i].checkExiste(Fechados)):
                    Abertos = [*Abertos, FilhosX[i]]
    return [[], iter]

def DFS(inicial, obj, lim):
    X = Node(inicial, -1, -1)
    Abertos = [X]
    Fechados = []
    iter = 0
    while Abertos != []:
        iter += 1
        X = Abertos[0]
        del Abertos[0]
        if (X.graph == obj).all():
            return [X, iter]
        else:
            Aux = geraFilhos(X.graph)
            FilhosX = []
            for i in range(np.shape(Aux)[0]):
                FilhosX = [*FilhosX, Node(Aux[i], X, -1)]
            Fechados.append(X)
            for i in range(len(FilhosX)):
                if not(FilhosX[i].checkExiste(Abertos)) and not(FilhosX[i].checkExiste(Fechados)):
                    Abertos = [*Abertos, FilhosX[i]]
    return [[], iter]

def geraFilhos(graph):
    for i in range( np.shape(graph)[0] ):
        for j in range( np.shape(graph)[1] ):
            if( graph[i][j] == 'X' ):
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
        
################################################## MAIN ##################################################

Obj = np.array([[1,  2 , 3],
                [8, 'X', 4],
                [7,  6 , 5]])

Ini = np.array([[2,  8 , 3],
                [1,  6 , 4],
                [7, 'X', 5]])

BFSres = BFS(Ini, Obj)
print('\nBFS:', BFSres[1], 'iteracoes\n\n',BFSres[0].graph, '\n\nCAMINHO (OBJETIVO -> INICIAL):\n')
BFSres[0].printPath(Ini)

# DFSres = DFS(Ini, Obj)
# print('\nDFS:\n',DFSres, '\n')
