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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        The evaluation function takes in the current and[] proposed successor
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
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()

        score = successorGameState.getScore()
        
        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            ghostDist = util.manhattanDistance(ghostPos, newPos)
            scaredTime = ghost.scaredTimer
            # be afraid (not scared, close ghost)
            if scaredTime < 2 and ghostDist < 2:
                return -9999
            # don't be afraid (ghosts are scared, location doesn't matter)
            if scaredTime >= 2:
                score += 100
                
        minFood = 9999
        for food in newFood:
            currentFood = util.manhattanDistance(food, newPos)
            if currentFood < minFood:
                minFood = currentFood
        score += 1/minFood

        return score

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
    
        return self.minimax(gameState, 0, 0)[1]

    def findMax(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        result = []
        for action in actions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            result.append((self.minimax(successorState, agentIndex + 1, depth)[0], action)) 
        return max(result)
    
    def findMin(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        result = []
        for action in actions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            result.append((self.minimax(successorState, agentIndex + 1, depth)[0], action))
        return min(result)
    
    def minimax(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (self.evaluationFunction(gameState), "Stop")
        
        agentsNum = gameState.getNumAgents()
        # reset agent count after last agent
        if agentIndex == agentsNum:
            agentIndex = 0
        # move to next depth if last agent
        elif agentIndex == agentsNum - 1:
            depth += 1

        if agentIndex == 0:
            return self.findMax(gameState, agentIndex, depth)
        else:
            return self.findMin(gameState, agentIndex, depth)

        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
    
        # same as minimax agent but start with very small alpha and very large beta
        return self.minimax(gameState, 0, 0, -9999, 9999)[1]

    def findMax(self, gameState, agentIndex, depth, alpha, beta):
        actions = gameState.getLegalActions(agentIndex)
        result = []
        for action in actions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            res = self.minimax(successorState, agentIndex + 1, depth, alpha, beta)[0]
            result.append((res, action))
            if res > beta:
                return (res, action)
            alpha = max(alpha, res)
        return max(result)
    
    def findMin(self, gameState, agentIndex, depth, alpha, beta):
        actions = gameState.getLegalActions(agentIndex)
        result = []
        for action in actions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            res = self.minimax(successorState, agentIndex + 1, depth, alpha, beta)[0]
            result.append((res, action))
            if res < alpha:
                return (res, action)
            beta = min(beta, res)
        return min(result)
    
    def minimax(self, gameState, agentIndex, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (self.evaluationFunction(gameState), "Stop")
        
        agentsNum = gameState.getNumAgents()
        if agentIndex == agentsNum:
            agentIndex = 0
        elif agentIndex == agentsNum - 1:
            depth += 1

        if agentIndex == 0:
            return self.findMax(gameState, agentIndex, depth, alpha, beta)
        else:
            return self.findMin(gameState, agentIndex, depth, alpha, beta)

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
        return self.expectimax(gameState, 0, 0)[1]

    def findMax(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        result = []
        for action in actions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            result.append((self.expectimax(successorState, agentIndex + 1, depth)[0], action)) 
        return max(result)
    
    def findRandom(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        result = []
        total = 0
        for action in actions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            res = self.expectimax(successorState, agentIndex + 1, depth)[0]
            total += res
            result.append((res, action))
        return (total / len(result), )
    
    def expectimax(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (self.evaluationFunction(gameState), "Stop")
        
        agentsNum = gameState.getNumAgents()
        if agentIndex == agentsNum:
            agentIndex = 0
        elif agentIndex == agentsNum - 1:
            depth += 1

        if agentIndex == 0:
            return self.findMax(gameState, agentIndex, depth)
        else:
            return self.findRandom(gameState, agentIndex, depth)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: My better evaluation function is mostly the same as the
    first one.

    I considered the ghost distance and whether or not the ghost is scared.
    If there is little remaining scare time and the ghost is nearby, then a
    large negative value is immediately returned. If there is a lot of 
    remaining scared time, then a positive value is added to the score.

    For food, the food with the minimum distance is found. The reciprocal of
    that food distance is added to the score. The total number of food is also
    subtracted, so that Pacman chooses states with less remaining food.

    The reciprocal number of capsules is a new addition that adds a small
    value for the number of remaining capsules.
    """
    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood().asList()
    currentGhost = currentGameState.getGhostStates()
    currentCapsule = currentGameState.getCapsules()

    score = currentGameState.getScore()
    
    for ghost in currentGhost:
        ghostPos = ghost.getPosition()
        ghostDist = util.manhattanDistance(ghostPos, currentPos)
        scaredTime = ghost.scaredTimer
        # be afraid (not scared, close ghost)
        if scaredTime < 2 and ghostDist < 2:
            return -9999
        # don't be afraid (ghosts are scared, location doesn't matter)
        if scaredTime >= 2:
            score += 100
                
    minFood = 9999
    count = 0
    for food in currentFood:
        foodDist = util.manhattanDistance(food, currentPos)
        if foodDist < minFood:
            minFood = foodDist
        count += 1
    score -= count
    score += 1/minFood

    if len(currentCapsule) > 0:
        score += 1/len(currentCapsule)

    return score

# Abbreviation
better = betterEvaluationFunction
