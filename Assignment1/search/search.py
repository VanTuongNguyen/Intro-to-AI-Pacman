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
    "*** YOUR CODE HERE ***"
    from util import Stack

    stack = Stack() #[(x,y),[path]]
    visitedState = []

    if problem.isGoalState(problem.getStartState()):
        return []
    stack.push((problem.getStartState(),[]))

    while(True):
        if stack.isEmpty():
            return []
        
        state,path = stack.pop()

        if problem.isGoalState(state):
            return path
        
        visitedState.append(state)

        succ = problem.getSuccessors(state)

        if succ:
            for i in succ:
                if i[0] not in visitedState:
                    newPath = path + [i[1]]
                    stack.push((i[0],newPath))
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    queue = Queue() #[(x,y),[path]]
    visitedState = []
    if problem.isGoalState(problem.getStartState()):
        return []
    queue.push((problem.getStartState(),[]))

    while(True):
        if queue.isEmpty():
            return []
        
        state,path = queue.pop()

        if problem.isGoalState(state):
            return path
        
        visitedState.append(state)

        succ = problem.getSuccessors(state)

        if succ:
            for i in succ:
                if i[0] not in visitedState and i[0] not in (j[0] for j in queue.list) :
                    newPath = path + [i[1]]
                    queue.push((i[0],newPath))


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    heap = PriorityQueue() #[(((x,y),[path]),cost)]
    visitedState = []
    if problem.isGoalState(problem.getStartState()):
        return []
    heap.push((problem.getStartState(),[]),0)

    while(True):
        if heap.isEmpty():
            return []
        
        state,path = heap.pop()

        if problem.isGoalState(state):
            return path
        
        visitedState.append(state)

        succ = problem.getSuccessors(state)

        if succ:
            for i in succ:
                if i[0] not in visitedState and i[0] not in (j[2][0] for j in heap.heap):

                    newPath = path + [i[1]]
                    pri = problem.getCostOfActions(newPath)
                    heap.push((i[0],newPath),pri)
                elif i[0] not in visitedState:
                    for j in heap.heap:
                        if j[2][0] == i[0]:
                            oldPri = problem.getCostOfActions(j[2][1])

                    newPri = problem.getCostOfActions(path + [i[1]])
                    if oldPri > newPri:
                        newPath = path + [i[1]]
                        heap.push((i[0],newPath),newPri)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

from util import PriorityQueue

class NewPriorityQueueWithFunction(PriorityQueue):
    def __init__(self, problem, func):
        self.problem = problem
        PriorityQueue.__init__(self)
        self.func = func
    def push(self, item, heuristic):
        PriorityQueue.push(self, item, self.func(self.problem, item, heuristic))

def f(problem, state, heuristic):
    return problem.getCostOfActions(state[1]) + heuristic(state[0],problem)

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    queueAStar = NewPriorityQueueWithFunction(problem,f)
    visitedState = []

    if problem.isGoalState(problem.getStartState()):
        return []

    queueAStar.push((problem.getStartState(),[]),heuristic)

    while (True):
        if queueAStar.isEmpty():
            return []
        state, path = queueAStar.pop()

        if problem.isGoalState(state):
            return path
        if state in visitedState:
            continue
        visitedState.append(state)

        succ = problem.getSuccessors(state)
        if succ:
            for i in succ:
                if i[0] not in visitedState:
                    newPath = path + [i[1]]
                    queueAStar.push((i[0],newPath),heuristic)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
