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
        score = successorGameState.getScore()

        if action == Directions.STOP:
            score -= 20

        ghostPos = currentGameState.getGhostPosition(1)
        distToGhost = util.manhattanDistance(ghostPos, newPos)


        score += max(distToGhost, 3)

        foodlist = newFood.asList()

        closestfood = 100
        for foodpos in foodlist:
            thisdist = util.manhattanDistance(foodpos, newPos)
            if (thisdist < closestfood):
                closestfood = thisdist
        score -=  5* closestfood


        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            score += 200

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
      """
      "*** YOUR CODE HERE ***"

      def minimax(state, depth, agent):
        if agent == state.getNumAgents():

          if depth ==self.depth or state.isWin() or state.isLose():   #check if terminal
            return self.evaluationFunction(state)
          else:
            return minimax(state, depth + 1, 0) #wrap around back to pacman's turn

        else:
          actions = state.getLegalActions(agent)
          if len(actions) == 0:     #it's a terminal state
            return self.evaluationFunction(state)

          successors = [] 
          for action in actions:
            successors.append((minimax(state.generateSuccessor(agent, action), depth, agent +1),action))
          return (max if agent ==0 else min)(successors)

      #intitial run through
      
      actions = gameState.getLegalActions(0)
      successors = [
        (minimax(gameState.generateSuccessor(0,action), 1, 1), action)
        for action in actions
      ]
      best = max(successors)
      return best[1]
            



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        def max_node(state, depth, agent, alpha, beta):
            curr = None
            if depth > self.depth:
                return self.evaluationFunction(state)


            for action in state.getLegalActions(agent):
                successor = min_node(state.generateSuccessor(agent, action), depth, agent + 1, alpha, beta)
                curr = max(curr, successor)

                if beta is not None and curr > beta:
                    return curr

                alpha = max(alpha, curr)

            if curr is None:
                return self.evaluationFunction(state)

            return curr
        def min_node(state, depth, agent, alpha, beta):
          curr = None
          if agent == state.getNumAgents():
              return max_node(state, depth + 1, 0, alpha, beta)

          for action in state.getLegalActions(agent):
              next = min_node(state.generateSuccessor(agent, action), depth, agent + 1, alpha, beta)
              if curr is None:
                curr = next
              else:
                curr = min(curr, next)
              
              if curr < alpha and alpha is not None:
                  return curr

              if beta is None:
                beta = curr
              else:
                beta = min(beta, curr)
              
          if curr is None:
              return self.evaluationFunction(state)

          return curr

        curr, alpha, beta, move = None, None, None, None
        for action in gameState.getLegalActions(0):
            curr = max(curr, min_node(gameState.generateSuccessor(0, action), 1, 1, alpha, beta))
            # if val >= beta: return action
            if alpha is None:
              alpha, move = curr, action
            else:
              alpha, move = max(curr, alpha), action if curr > alpha else move

        return move

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
        #back to using the code from minimax, but instead of returning min/max, we will return teh average. 


        def expectimax(state, depth, agent):
          if agent == state.getNumAgents():

            if depth ==self.depth or state.isWin() or state.isLose():   #check if terminal
              return self.evaluationFunction(state)
            else:
              return expectimax(state, depth + 1, 0) #wrap around back to pacman's turn

          else:
            actions = state.getLegalActions(agent)
            if len(actions) == 0:     #it's a terminal state
              return self.evaluationFunction(state)

            successors = []
            value_sum=0
            for action in actions:
              value = expectimax(state.generateSuccessor(agent, action), depth, agent +1)
              successors.append((value,action))

              if type(value) is tuple:
                value = value[0]
              value_sum +=value
            if agent == 0:
              return max(successors)
            else:
              return value_sum/len(actions)

      #intitial run through
        actions = gameState.getLegalActions(0)
        successors = [
          (expectimax(gameState.generateSuccessor(0,action), 1, 1), action)
          for action in actions
          ]
        best = max(successors)
        return best[1]

def dist_closestGhostie(newPos, newGhostStates):
    dist = []
    for ghost in newGhostStates:
        ghostPos = ghost.getPosition()
        dist.append(manhattanDistance(newPos, ghostPos))
    if dist and min(dist) != 0:
        return min(dist)
    return 1

def howMuchNomzLeft(newFood):
    return sum([len(filter(lambda y: y, x)) for x in newFood])

def avgDistToNomz( newPos, newFood):
  dist = []
  for i, row in enumerate(newFood):
    for j, column in enumerate(newFood[i]):
      if newFood[i][j]:
        dist.append(util.manhattanDistance(newPos, (i,j)))
  return sum(dist)/float(len(dist)) if (dist and sum(dist) != 0) else 1


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghosties = currentGameState.getGhostStates()
    value = currentGameState.getScore()+ 7.0/dist_closestGhostie(pos, ghosties) + 15.0/avgDistToNomz(pos, food)
    return value

# Abbreviation
better = betterEvaluationFunction

