"""
Este programa lo que hace es implementar el objeto de nodo, ademas de una clase Stackfrontier, donde los metodos
add, contains_state,empty,remove, se encargan de la administracion de los nodos,notese que para stackfrontires es una pila 
de tipo lifo"""


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

# verificamos si el nodo en el que estamos no esta dentro de la frontera, para no caer en el bucle
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


#este objeto tomas los metodos de stackfrontier, solo modifica el metodo de remover, ya que esta sera de tipo 
#fifo (first input first output)
class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

if __name__=="__main__":
    node1=Node(1,None,None)
    print(node1.state)