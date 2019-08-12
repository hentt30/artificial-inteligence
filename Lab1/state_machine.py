import random
import math
from constants import *


class FiniteStateMachine(object):
    """
    A finite state machine.
    """
    def __init__(self, state):
        self.state = state

    def change_state(self, new_state):
        self.state = new_state

    def update(self, agent):
        
        self.state.check_transition(agent, self)
        self.state.execute(agent)
    
 


class State(object):
    """
    Abstract state class.
    """
    def __init__(self, state_name):
        """
        Creates a state.

        :param state_name: the name of the state.
        :type state_name: str
        """
        self.state_name = state_name

    def check_transition(self, agent, fsm):
        """
        Checks conditions and execute a state transition if needed.

        :param agent: the agent where this state is being executed on.
        :param fsm: finite state machine associated to this state.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")

    def execute(self, agent):
        """
        Executes the state logic.

        :param agent: the agent where this state is being executed on.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")


class MoveForwardState(State):
    def __init__(self):
        super().__init__("MoveForward")
        self.cont=0

    def check_transition(self, agent, state_machine):
        self.cont=self.cont+1;
        if self.cont*SAMPLE_TIME > MOVE_FORWARD_TIME:
            self.cont=0
            state_machine.change_state(MoveInSpiralState())         
        if agent.get_bumper_state():
             state_machine.change_state(GoBackState())

        

    def execute(self, agent):
        agent.set_velocity(FORWARD_SPEED,0)
       
        agent.move()


class MoveInSpiralState(State):
    def __init__(self):
        super().__init__("MoveInSpiral")
        self.contador=0
    
    def check_transition(self, agent, state_machine):
        self.contador= self.contador+1
        if self.contador*SAMPLE_TIME > MOVE_IN_SPIRAL_TIME:
             self.contador=0;
             state_machine.change_state( MoveForwardState() )
        if agent.get_bumper_state():
             state_machine.change_state(GoBackState())

    def execute(self, agent):
         agent.set_velocity(FORWARD_SPEED, FORWARD_SPEED/(INITIAL_RADIUS_SPIRAL+SPIRAL_FACTOR*self.contador*SAMPLE_TIME))
         agent.move()


class GoBackState(State):
    def __init__(self):
        super().__init__("GoBack")
        self.count=0

    def check_transition(self, agent, state_machine):
        self.count=self.count+1
        if self.count*SAMPLE_TIME > GO_BACK_TIME :
            self.count=0
            state_machine.change_state(RotateState())

    def execute(self, agent):
        agent.set_velocity(BACKWARD_SPEED,0)
        agent.move()


class RotateState(State):
    def __init__(self):
        super().__init__("Rotate")
        self.ale=random.randint(-4,4)
        self.mod=abs(self.ale)
        self.count2=0

    def check_transition(self, agent, state_machine):
        self.count2=self.count2+1
        if self.count2*SAMPLE_TIME>self.mod:
           state_machine.change_state(MoveForwardState())
    
    def execute(self, agent):
        if self.ale >=0:
            agent.set_velocity(0,ANGULAR_SPEED)
        else:
            agent.set_velocity(0,-1*ANGULAR_SPEED)
        agent.move()
