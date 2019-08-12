from enum import Enum
from constants import *
import random
import math


class ExecutionStatus(Enum):
    """
    Represents the execution status of a behavior tree node.
    """
    SUCCESS = 0
    FAILURE = 1
    RUNNING = 2


class BehaviorTree(object):
    """
    Represents a behavior tree.
    """
    def __init__(self, root=None):
        """
        Creates a behavior tree.

        :param root: the behavior tree's root node.
        :type root: TreeNode
        """
        self.root = root

    def update(self, agent):
        """
        Updates the behavior tree.

        :param agent: the agent this behavior tree is being executed on.
        """
        if self.root is not None:
            self.root.execute(agent)


class TreeNode(object):
    """
    Represents a node of a behavior tree.
    """
    def __init__(self, node_name):
        """
        Creates a node of a behavior tree.

        :param node_name: the name of the node.
        """
        self.node_name = node_name
        self.parent = None

    def enter(self, agent):
        """
        This method is executed when this node is entered.

        :param agent: the agent this node is being executed on.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")

    def execute(self, agent):
        """
        Executes the behavior tree node logic.

        :param agent: the agent this node is being executed on.
        :return: node status (success, failure or running)
        :rtype: ExecutionStatus
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")


class LeafNode(TreeNode):
    """
    Represents a leaf node of a behavior tree.
    """
    def __init__(self, node_name):
        super().__init__(node_name)


class CompositeNode(TreeNode):
    """
    Represents a composite node of a behavior tree.
    """
    def __init__(self, node_name):
        super().__init__(node_name)
        self.children = []

    def add_child(self, child):
        """
        Adds a child to this composite node.

        :param child: child to be added to this node.
        :type child: TreeNode
        """
        child.parent = self
        self.children.append(child)


class SequenceNode(CompositeNode):
    """
    Represents a sequence node of a behavior tree.
    """
    def __init__(self, node_name):
        super().__init__(node_name)
        # We need to keep track of the last running child when resuming the tree execution
        self.running_child = None

    def enter(self, agent):
        # When this node is entered, no child should be running
        self.running_child = None

    def execute(self, agent):
        if self.running_child is None:
            # If a child was not running, then the node puts its first child to run
            self.running_child = self.children[0]
            self.running_child.enter(agent)
        loop = True
        while loop:
            # Execute the running child
            status = self.running_child.execute(agent)
            if status == ExecutionStatus.FAILURE:
                # This is a sequence node, so any failure results in the node failing
                self.running_child = None
                return ExecutionStatus.FAILURE
            elif status == ExecutionStatus.RUNNING:
                # If the child is still running, then this node is also running
                return ExecutionStatus.RUNNING
            elif status == ExecutionStatus.SUCCESS:
                # If the child returned success, then we need to run the next child or declare success
                # if this was the last child
                index = self.children.index(self.running_child)
                if index + 1 < len(self.children):
                    self.running_child = self.children[index + 1]
                    self.running_child.enter(agent)
                else:
                    self.running_child = None
                    return ExecutionStatus.SUCCESS


class SelectorNode(CompositeNode):
    """
    Represents a selector node of a behavior tree.
    """
    def __init__(self, node_name):
        super().__init__(node_name)
        # We need to keep track of the last running child when resuming the tree execution
        self.running_child = None

    def enter(self, agent):
        # When this node is entered, no child should be running
        self.running_child = None

    def execute(self, agent):
        if self.running_child is None:
            # If a child was not running, then the node puts its first child to run
            self.running_child = self.children[0]
            self.running_child.enter(agent)
        loop = True
        while loop:
            # Execute the running child
            status = self.running_child.execute(agent)
            if status == ExecutionStatus.FAILURE:
                # This is a selector node, so if the current node failed, we have to try the next one.
                # If there is no child left, then all children failed and the node must declare failure.
                index = self.children.index(self.running_child)
                if index + 1 < len(self.children):
                    self.running_child = self.children[index + 1]
                    self.running_child.enter(agent)
                else:
                    self.running_child = None
                    return ExecutionStatus.FAILURE
            elif status == ExecutionStatus.RUNNING:
                # If the child is still running, then this node is also running
                return ExecutionStatus.RUNNING
            elif status == ExecutionStatus.SUCCESS:
                # If any child returns success, then this node must also declare success
                self.running_child = None
                return ExecutionStatus.SUCCESS


class RoombaBehaviorTree(BehaviorTree):
    """
    Represents a behavior tree of a roomba cleaning robot.
    """
    def __init__(self):
        
        self.select=SelectorNode("select")
        self.seq1=SequenceNode("seq1")
        self.seq2=SequenceNode("seq2")
        self.seq1.add_child(MoveForwardNode())
        self.seq1.add_child(MoveInSpiralNode())
        self.seq2.add_child(GoBackNode())
        self.seq2.add_child(RotateNode())
        self.select.add_child(self.seq1)
        self.select.add_child(self.seq2)
        super().__init__(self.select)
        




class MoveForwardNode(LeafNode):
    def __init__(self):
        super().__init__("MoveForward")
        self.cont=0
        
    

    def enter(self, agent):
      
       agent.set_velocity(FORWARD_SPEED,0)
       agent.move()
        


    def execute(self, agent):
        self.cont=self.cont+1
        
        if agent.get_bumper_state():
            self.cont=0;
            return ExecutionStatus.FAILURE
        elif self.cont*SAMPLE_TIME>MOVE_FORWARD_TIME:
            self.cont=0;
            return ExecutionStatus.SUCCESS
        else :
            self.enter(agent)
            return ExecutionStatus.RUNNING


class MoveInSpiralNode(LeafNode):
    def __init__(self):
        super().__init__("MoveInSpiral")
        self.contador=0

    def enter(self, agent):
        agent.set_velocity(FORWARD_SPEED, FORWARD_SPEED/(INITIAL_RADIUS_SPIRAL+SPIRAL_FACTOR*self.contador*SAMPLE_TIME))
        agent.move()
          

    def execute(self, agent):
        
        self.contador=self.contador+1
        if agent.get_bumper_state():
            self.contador=0
            return ExecutionStatus.FAILURE
        elif self.contador*SAMPLE_TIME>MOVE_IN_SPIRAL_TIME:
            self.contador=0
            return ExecutionStatus.SUCCESS
        else:
            self.enter(agent)
            return ExecutionStatus.RUNNING


class GoBackNode(LeafNode):
    def __init__(self):
        super().__init__("GoBack")
        self.count=0

    def enter(self, agent):
        agent.set_velocity(BACKWARD_SPEED,0)
        agent.move()
        

    def execute(self, agent):
        
        self.count=self.count+1
        if self.count*SAMPLE_TIME>GO_BACK_TIME:
            self.count=0
            return ExecutionStatus.SUCCESS
        else:
            self.enter(agent)
            return ExecutionStatus.RUNNING
        
        


class RotateNode(LeafNode):
    def __init__(self):
        super().__init__("Rotate")
        self.ale=random.randint(-4,4)
        self.mod=abs(self.ale)
        self.count2=0

    def enter(self, agent):
       if self.ale >=0:
            agent.set_velocity(0,ANGULAR_SPEED)
       else:
            agent.set_velocity(0,-1*ANGULAR_SPEED)
       agent.move()
        

    def execute(self, agent):
        self.count2=self.count2+1
        if self.count2*SAMPLE_TIME > self.mod :
            self.count2=0  
            return ExecutionStatus.SUCCESS
        else :
            self.enter(agent)
            return ExecutionStatus.RUNNING
     