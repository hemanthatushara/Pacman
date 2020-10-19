# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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

import util


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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    
    possible_states = util.Stack()
    visited_states = []
    possible_route = []
    backtrace=[]
    current_state= problem.getStartState()
    
    possible_states.push((current_state, backtrace))  #Just because we need to start the loop with atleast one point so we can generalize.
    while problem.isGoalState(current_state)!=True:
        info = possible_states.pop()
        #del backtrace[:]
        current_state = info[0]
        backtrace = info[1]
        #print "hello"
        #print backtrace
        #debug statement to see the form of our list
       # print(current_state)
        if current_state not in visited_states:
            #First step is to add the state to visiterd state
            visited_states.append(current_state)
            #backtrace.append(step)
            #Find its successors
            possible_successors = problem.getSuccessors(current_state)
            for i in range(0,len(possible_successors)):
                #path = backtrace + [possible_successors[i][1]]
                action = backtrace + [possible_successors[i][1]]
                possible_states.push((possible_successors[i][0], action))
                #backtrace.pop()

 

    #print backtrace
   # print visited_states
    return backtrace

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    possible_states = util.Queue()
    visited_states = []
    possible_route = []
    backtrace=[]
    current_state= problem.getStartState()
    
    possible_states.push((current_state, backtrace))  #Just because we need to start the loop with atleast one point so we can generalize.
    while problem.isGoalState(current_state)!=True:
        info = possible_states.pop()
        #del backtrace[:]
        current_state = info[0]
        backtrace = info[1]
        
        #print backtrace
        #debug statement to see the form of our list
       # print(current_state)
        if current_state not in visited_states:
            #First step is to add the state to visiterd state
            visited_states.append(current_state)
            #backtrace.append(step)
            #Find its successors
            possible_successors = problem.getSuccessors(current_state)
            for i in range(0,len(possible_successors)):
                #path = backtrace + [possible_successors[i][1]]
                action = backtrace + [possible_successors[i][1]]
                possible_states.push((possible_successors[i][0], action))
                #backtrace.pop()

 

    #print backtrace
   # print visited_states
    return backtrace
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
   
    possible_states =  util.PriorityQueue()
    visited_states = []
    possible_route = []
    backtrace=[]
    current_state= problem.getStartState()
   
    
    possible_states.push((current_state, backtrace),0)  #Just because we need to start the loop with atleast one point so we can generalize.
    while problem.isGoalState(current_state)!=True:
        info = possible_states.pop()
        current_state = info[0]
        backtrace = info[1]

        if (problem.isGoalState(current_state)) :
            return backtrace
        if current_state not in visited_states:
            #First step is to add the state to visiterd state
            visited_states.append(current_state)
            #backtrace.append(step)
            #Find its successors
            
            possible_successors = problem.getSuccessors(current_state)
            for i in range(0,len(possible_successors)):
                #path = backtrace + [possible_successors[i][1]]
                action = backtrace + [possible_successors[i][1]]
                possible_states.push((possible_successors[i][0], action), problem.getCostOfActions(action))
                possible_states.update((current_state, action), problem.getCostOfActions(action) )    

    #print backtrace
   # print visited_states
    return backtrace
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    possible_states =  util.PriorityQueue()
    visited_states = []
    possible_route = []
    backtrace=[]
    current_state= problem.getStartState()
   
    
    possible_states.push((current_state, backtrace),0)  #Just because we need to start the loop with atleast one point so we can generalize.
    while problem.isGoalState(current_state)!=True:
        info = possible_states.pop()
        current_state = info[0]
        backtrace = info[1]
        
        if (problem.isGoalState(current_state)) :
            return backtrace
        if current_state not in visited_states:
            #First step is to add the state to visiterd state
            visited_states.append(current_state)
            #backtrace.append(step)
            #Find its successors
            
            possible_successors = problem.getSuccessors(current_state)
            for i in range(0,len(possible_successors)):

                #path = backtrace + [possible_successors[i][1]]

                action = backtrace + [possible_successors[i][1]]

                #print(problem.getCostOfActions(action))

                cost = problem.getCostOfActions(action) + heuristic(possible_successors[i][0],problem)

                possible_states.push((possible_successors[i][0], action),cost)

                possible_states.update((possible_successors[i][0], action),cost)

                    #print backtrace
                # print visited_states
    return backtrace
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
