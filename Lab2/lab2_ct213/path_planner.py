from grid import Node, NodeGrid
from math import inf
import heapq


class PathPlanner(object):
    """
    Represents a path planner, which may use Dijkstra, Greedy Search or A* to plan a path.
    """
    def __init__(self, cost_map):
        """
        Creates a new path planner for a given cost map.

        :param cost_map: cost used in this path planner.
        :type cost_map: CostMap.
        """
        self.cost_map = cost_map
        self.node_grid = NodeGrid(cost_map)

    @staticmethod
    def construct_path(goal_node):
        """
        Extracts the path after a planning was executed.

        :param goal_node: node of the grid where the goal was found.
        :type goal_node: Node.
        :return: the path as a sequence of (x, y) positions: [(x1,y1),(x2,y2),(x3,y3),...,(xn,yn)].
        :rtype: list of tuples.
        """
        node = goal_node
        # Since we are going from the goal node to the start node following the parents, we
        # are transversing the path in reverse
        reversed_path = []
        while node is not None:
            reversed_path.append(node.get_position())
            node = node.parent
        return reversed_path[::-1]  # This syntax creates the reverse list

    def dijkstra(self, start_position, goal_position):
        """
        Plans a path using the Dijkstra algorithm.

        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """
        # Todo: implement the Dijkstra algorithm
        # The first return is the path as sequence of tuples (as returned by the method construct_path())
        # The second return is the cost of the path
        self.node_grid.reset()#seta todas as distâncias para infinito
        i=start_position[0]
        j=start_position[1]
        self.node_grid.grid[i,j].f=0
        pq=[]
        heapq.heappush(pq,(self.node_grid.grid[i,j].f,self.node_grid.grid[i,j]))
        while True :
            davez= Node(300,300)
            while  len(pq) != 0 : 
                atual=pq.pop(0)
                if atual[1].closed == False :
                    davez=atual[1]
                    break
            
            if davez.i == 300:
                break
           
            self.node_grid.grid[davez.i,davez.j].closed=True
            t=davez.get_position()
            p=self.node_grid.get_successors(t[0],t[1])
            for item in p:
                n=(davez.i,davez.j)
                m=(self.node_grid.grid[item[0],item[1]].i,self.node_grid.grid[item[0],item[1]].j)
                dist=self.cost_map.get_edge_cost(n,m)
                h=item[0]
                k=item[1]
                if self.node_grid.grid[h,k].f >  davez.f +dist and self.node_grid.grid[h,k].closed == False :
                    self.node_grid.grid[h,k].parent=davez
                    self.node_grid.grid[h,k].f = davez.f +dist 
                    heapq.heappush(pq,(self.node_grid.grid[h,k].f,self.node_grid.grid[h,k]))

        pt=self.construct_path(self.node_grid.grid[goal_position[0],goal_position[1]])
        ct=self.node_grid.grid[goal_position[0],goal_position[1]].f
        return pt,ct

    def greedy(self, start_position, goal_position):
        """
        Plans a path using greedy search.

        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """
        # Todo: implement the Greedy Search algorithm
        # The first return is the path as sequence of tuples (as returned by the method construct_path())
        # The second return is the cost of the path
        self.node_grid.reset()#seta todas as distâncias para infinito
        i=start_position[0]
        booleana=1
        j=start_position[1]
        self.node_grid.grid[i,j].f= 0
        pq=[]
        heapq.heappush(pq,(self.node_grid.grid[i,j].f,self.node_grid.grid[i,j]))
        while len(pq) !=0  :     
            atual=heapq.heappop(pq)
            davez=atual[1]
            self.node_grid.grid[davez.i,davez.j].closed=True
            t=davez.get_position()
            p=self.node_grid.get_successors(t[0],t[1])
            
            for item in p:
                node= self.node_grid.grid[item[0] , item[1]]
                dist=node.distance_to(goal_position[0], goal_position[1])
                n=(davez.i,davez.j)
                m=(self.node_grid.grid[item[0],item[1]].i,self.node_grid.grid[item[0],item[1]].j)
                distg=self.cost_map.get_edge_cost(n,m)
                h=item[0]
                k=item[1]
              
                if node.closed == False :
                   self.node_grid.grid[h,k].parent = davez
                   self.node_grid.grid[h,k].f = davez.f + distg
                   self.node_grid.grid[h,k].closed = True
                   heapq.heappush(pq,(dist,self.node_grid.grid[h,k]))

                if node.i==goal_position[0] and node.j == goal_position[1]:
                   booleana=0
                   break
            if booleana == 0:
                break

        pt=self.construct_path(self.node_grid.grid[goal_position[0],goal_position[1]])
        ct=self.node_grid.grid[goal_position[0],goal_position[1]].f
        return pt,ct

    def a_star(self, start_position, goal_position):
        """
        Plans a path using A*.

        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """
        # Todo: implement the A* algorithm
        # The first return is the path as sequence of tuples (as returned by the method construct_path())
        # The second return is the cost of the path
        self.node_grid.reset()
        i=start_position[0]
        j=start_position[1]
        
        self.node_grid.grid[i,j].f= self.node_grid.grid[i,j].distance_to(goal_position[0], goal_position[1])
        self.node_grid.grid[i,j].g=0
        pq=[]
        heapq.heappush(pq,(self.node_grid.grid[i,j].f,self.node_grid.grid[i,j]))
        while len(pq) !=0  :     
            atual=pq.pop(0)
            davez=atual[1]
            self.node_grid.grid[davez.i,davez.j].closed=True
            t=davez.get_position()
            p=self.node_grid.get_successors(t[0],t[1])
            if davez.i==goal_position[0] and davez.j == goal_position[1]:
                   break

            
            for item in p:
                n=(davez.i,davez.j)
                m=(self.node_grid.grid[item[0],item[1]].i,self.node_grid.grid[item[0],item[1]].j)
                distg=self.cost_map.get_edge_cost(n,m)
                node= self.node_grid.grid[item[0] , item[1]]
                dist=node.distance_to(goal_position[0], goal_position[1])
                h=item[0]
                k=item[1]
              
                if node.f > davez.g + dist +distg :
                   self.node_grid.grid[h,k].parent = davez
                   self.node_grid.grid[h,k].f = davez.g + dist +distg
                   self.node_grid.grid[h,k].g= davez.g+distg
                   heapq.heappush(pq,(self.node_grid.grid[h,k].f,self.node_grid.grid[h,k]))

                

        pt=self.construct_path(self.node_grid.grid[goal_position[0],goal_position[1]])
        ct=self.node_grid.grid[goal_position[0],goal_position[1]].f
        return pt,ct
