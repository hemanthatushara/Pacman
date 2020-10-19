# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #print "Current game state : " ,successorGameState
        #print "New position : ", newPos
        #print "New Food : ", newFood
        #print "New ghost states :", newGhostStates
        #print "New scared times : ", newScaredTimes
        #print "currentGameState:", currentGameState
        foodList = newFood.asList()
        currentPosition = currentGameState.getPacmanPosition()
        #print "current game state", currentGameState
        currentFood = currentGameState.getFood()
        #print "current food state", currentFood
        ghostPosition = successorGameState.getGhostPositions()
        #print"ghost position", ghostPosition
        max_dist = ((newFood.height-1) + (newFood.width -1))
        #print "Maximum distance between pacman and food",max_dist
        gameScore = 0

        if currentFood[newPos[0]][newPos[1]]:
            gameScore = gameScore+10            #awards getting to food

        distance_to_food = 9999
        distance_to_ghost = 9999
        for food in foodList:
            distance_to_food = min([manhattanDistance(food,newPos),distance_to_food])
        for ghost in ghostPosition:
            distance_to_ghost= min([manhattanDistance(ghost,newPos),distance_to_ghost])

        if distance_to_ghost < 2:
            gameScore = gameScore -500         #disincentivises colliding with ghosts at any point
        distance_to_food_inverse = 1.0/distance_to_food
        distance_to_ghost_inverse = 1/(distance_to_ghost+1)
        #gameScore = gameScore + distance_to_food + distance_to_ghost/max_dist
        gameScore = gameScore + distance_to_food_inverse + distance_to_ghost_inverse

        return gameScore


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def minimax(state):
            value = float('-inf')
            best_move =  state.getLegalActions(0)[0]
            alpha =float('-inf')
            beta= float('inf')
            for action in state.getLegalActions(0):
                value = max(value,minValue(state.generateSuccessor(0, action), 1, 1, alpha, beta))
                if value > alpha:
                    bestAction = action
                alpha = max(alpha, value)

            return bestAction

        def maxValue(state, index, depth, alpha, beta):
            if state.isWin() or state.isLose() or depth > self.depth:
                return self.evaluationFunction(state)
            v = float('-inf')

            for action in state.getLegalActions(0):
                v = max(v, minValue(state.generateSuccessor(0, action),1,depth,alpha,beta))

                alpha = max(alpha, v)

            return v
        def minValue(state, index, depth, alpha, beta):
            ##Dealing with the end case
            if index == state.getNumAgents():
                return maxValue(state,0,depth+1,alpha,beta)

            if state.isWin() or state.isLose() or depth > self.depth+1:
                return self.evaluationFunction(state)
            v = float('inf')
            for action in state.getLegalActions(index):
                v = min(v, minValue(state.generateSuccessor(index,action),index+1,depth,alpha,beta))

                beta = min(beta, v)
            return v
        return minimax(gameState)

        #util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #til.raiseNotDefined()

        def alphabeta_pruning(state):
            value = float('-inf')
            best_move =  state.getLegalActions(0)[0]
            alpha =float('-inf')
            beta= float('inf')
            for action in state.getLegalActions(0):
                value = max(value,minValue(state.generateSuccessor(0, action), 1, 1, alpha, beta))
                if value > alpha:
                    bestAction = action
                alpha = max(alpha, value)

            return bestAction

        def maxValue(state, index, depth, alpha, beta):
            if state.isWin() or state.isLose() or depth > self.depth:
                return self.evaluationFunction(state)
            v = float('-inf')
            terminal_state =0
            for action in state.getLegalActions(0):
                v = max(v, minValue(state.generateSuccessor(0, action),1,depth,alpha,beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
                terminal_state+=1
            return v
        def minValue(state, index, depth, alpha, beta):
            ##Dealing with the end case
            if index == state.getNumAgents():
                return maxValue(state,0,depth+1,alpha,beta)

            if state.isWin() or state.isLose() or depth > self.depth+1:
                return self.evaluationFunction(state)
            v = float('inf')
            for action in state.getLegalActions(index):
                v = min(v, minValue(state.generateSuccessor(index,action),index+1,depth,alpha,beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v
        return alphabeta_pruning(gameState)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expectimax(state, index, depth):

            possible_actions = state.getLegalActions(0)
            if len(possible_actions) == 0:
                return self.evaluationFunction(state)
            else:
                expecti_value = []
                best_action = possible_actions[0]
                v = float('-inf')
                for action in possible_actions:
                    value = calculate(state.generateSuccessor(0,action),1,1)
                    if value > v:
                        v = value
                        #print v
                        best_action = action
                        #print best_action
                        #print best_action
            #print best_action
            return best_action
        def calculate(state, index, depth):
            if depth > self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            if index==state.getNumAgents():
                return calculate(state,0,depth+1)
            else:
                total = 0.0
                length = 0.0
                v = float('-inf')
                for action in state.getLegalActions(index):
                    v = max(v,calculate(state.generateSuccessor(index,action), index+1, depth))
                    total += calculate(state.generateSuccessor(index,action), index+1, depth)
                    length += 1.0
                if index == 0:
                    return v
                else:
                    return total/length

        return expectimax(gameState,0,0)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()



# Abbreviation
better = betterEvaluationFunction
