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
    return [s, s, w, s, w, w, s, w]

def genericSearch(problem, type):
    if type == 'dfs':
        fringe = util.Stack()
    elif type == 'bfs':
        fringe = util.Queue()
    elif type == 'ucs':
        fringe = util.PriorityQueue()
    else:
        print 'Search type not recognized'

    fringe.push((problem.getStartState(), [] ,[]))
    explored = set()
    while fringe.isEmpty == False:
        curr, actions, visited = fringe.pop()
        if problem.isGoalState(curr):
            return actions
        explored.add(curr)
        visited = visited + [curr]
        for pos, dir, cost in problem.getSuccessors(curr):
            if pos not in explored:
                fringe.push(pos, actions + [dir], visited)




def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    """
    "*** YOUR CODE HERE ***"
    #return genericSearch(problem, 'dfs')

    fringe = util.Stack()
    states_in_fringe = []
    fringe.push(
        (problem.getStartState(), [], []))  # Push the start state pos, and create lists for the actions and the visited

    while fringe.isEmpty() == False:  # if the fringe isn't empty

        # pop the state of the top of the stack
        state, actions, visited = fringe.pop()

        # label state as visited
        visited = visited + [state]
        if problem.isGoalState(state):
            return actions

        # add the successors to the fringe.
        for pos, dirs, cost in problem.getSuccessors(state):
            if pos not in visited:
                fringe.push((pos, actions + [dirs], visited + [pos]))



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    #return genericSearch(problem, 'bfs')


    fringe = util.Queue()
    fringe.push((problem.getStartState(), [], []))  # Push the start state pos, and create lists for the actions and the visited

    states_in_fringe = [problem.getStartState()]
    while fringe.isEmpty() == False:  # if the fringe isn't empty

        # pop the state of the top of the stack
        state, actions, visited = fringe.pop()
        if state not in visited:
            # label state as visited
            visited = visited + [state]

            #test if it is a goal state return actions if it is
            if problem.isGoalState(state):
                return actions

            # add the successors that have not been visited to the fringe.
            for pos, dirs, cost in problem.getSuccessors(state):
                if pos not in states_in_fringe:
                    states_in_fringe = states_in_fringe + [pos]
                    fringe.push((pos, actions + [dirs], visited))



def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    #TODO: Figure out why this doesn't pass the dequeueing test.
    "*** YOUR CODE HERE ***"

    #return genericSearch(problem, 'ucs')

    fringe = util.PriorityQueue()

    # Push the start state pos, and create lists for the actions and the visited
    fringe.push((problem.getStartState(), [], []), 0)
    states_in_fringe = []
    while fringe.isEmpty() == False:  # if the fringe isn't empty

        # pop the state of the top of the stack
        state, actions, visited = fringe.pop() #chooses the lowest cost node in fringe.

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            # label state as visited
            visited = visited + [state]

            # add the successors that have not been visited to the fringe.
            for pos, dirs, step in problem.getSuccessors(state):
                if pos not in states_in_fringe:
                    states_in_fringe = states_in_fringe + [pos]
                    fringe.update((pos, actions + [dirs], visited), problem.getCostOfActions(actions +[dirs]))


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def manhattanHeuristic(state, problem):
    """
    A heuristic function that returns the Manhattan distance between the state and the goal. 
    ? Do we have access to the goal state? does problem.goal work??

    """
    #print 'Goal is at (heuristic): ', problem.goal
    #TODO: implement this function



    return util.manhattanDistance(state, problem.goal)


def aStarSearch(problem, heuristic=manhattanHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()

    #print 'The goal is a (astar): ', problem.goal
    # Push the start state pos, and create lists for the actions and the visited
    fringe.push((problem.getStartState(), [], []), 0)  
    states_in_fringe = [problem.getStartState()]

    while fringe.isEmpty() == False:  # if the fringe isn't empty

        # pop the state of the top of the stack
        state, actions, visited = fringe.pop()
        
        if problem.isGoalState(state):
            return actions

        if state not in visited:
            # label state as visited
            visited = visited + [state]

            # add the successors that have not been visited to the fringe.
            for pos, dirs, cost in problem.getSuccessors(state):
                if pos not in states_in_fringe:
                    states_in_fringe = states_in_fringe + [pos]
                    #get the cost of the node, 
                    new_cost = problem.getCostOfActions(actions + [dirs]) + heuristic(state, problem)
                    fringe.update((pos, actions + [dirs], visited), new_cost)




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
