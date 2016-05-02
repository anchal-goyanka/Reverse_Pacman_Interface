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
from game import Grid
from game import Agent
from game import Actions

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
	oldPos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
	newG = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
	food = newFood.asList()
	a = [util.manhattanDistance(newPos,df) for df in food]
	b = [util.manhattanDistance(oldPos,df) for df in food]
	g = min([util.manhattanDistance(newG[i],newPos) for i in range(len(newG))])
	#print action
	if (len(a) ==len(b)):
		return -1/g + 1
	else:
		return 1/a -1/g	
	'''if b in set(newG):
		return -500
	elif newFood[newPos[0]][newPos[1]]:
		return 500'''

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
	
    def value(self,state,i,d,t):	
		if state.isWin():
			return self.evaluationFunction(state)
		if state.isLose():
			return self.evaluationFunction(state)
		if (not(i%t == 0) and (i<=(d*t)-1)):
			v = float("inf")
			i = i+1
			for action in state.getLegalActions((i-1)%t):
				s = state.generateSuccessor((i-1)%t, action)
				v = min(v,self.value(s,i,d,t))
			return v
		if ((i%t == 0) and (i<=(d*t)-1)):
			v = float("-inf")
			i = i+1
			for action in state.getLegalActions(0):
				s = state.generateSuccessor(0, action)
				v = max(v,self.value(s,i,d,t))
			return v
		if i>(d*t-1):
			return self.evaluationFunction(state)


			
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
	t = gameState.getNumAgents()
	li =[]
	#print gameState
	ll = gameState.getLegalActions()
	for a in ll :
	
		s = gameState.generateSuccessor(0,a)
		val = self.value(s,1,self.depth,t)
		li.append(val)
		#print a,val
	#print (li)
	return ll[li.index(max(li))]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def value(self,state,i,d,t,a,b):	
		if state.isWin():
			return self.evaluationFunction(state)
		if state.isLose():
			return self.evaluationFunction(state)
		if (not(i%t == 0) and (i<=(d*t)-1)):
			v = float("inf")
			i = i+1
			for action in state.getLegalActions((i-1)%t):
				s = state.generateSuccessor((i-1)%t, action)
				v = min(v,self.value(s,i,d,t,a,b))
				if v < a :
					return v
				b = min(b,v)
			return v
		if ((i%t == 0) and (i<=(d*t)-1)):
			v = float("-inf")
			i = i+1
			for action in state.getLegalActions(0):
				s = state.generateSuccessor(0, action)
				v = max(v,self.value(s,i,d,t,a,b))
				if v > b :
					return v
				a = max(a,v)
			return v
		if i>(d*t-1):
			return self.evaluationFunction(state)


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
	t = gameState.getNumAgents()
	li =[]
	ll = gameState.getLegalActions()
	c = float("-inf")
	e = float("inf")
	for a in ll :	
		s = gameState.generateSuccessor(0,a)
		val = self.value(s,1,self.depth,t,c,e)
		li.append(val)
		if val > e:
			c = max(c,val)
	return ll[li.index(max(li))]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def value(self,state,i,d,t):	
		if state.isWin():
			return self.evaluationFunction(state)
		if state.isLose():
			return self.evaluationFunction(state)
		if (not(i%t == 0) and (i<=(d*t)-1)):
			v = 0.0
			i = i+1
			for action in state.getLegalActions((i-1)%t):
				s = state.generateSuccessor((i-1)%t, action)
				p = float(1.0/len(state.getLegalActions((i-1)%t)))
				v = v + float((p*self.value(s,i,d,t)))
			return v
		if ((i%t == 0) and (i<=(d*t)-1)):
			v = float("-inf")
			i = i+1
			for action in state.getLegalActions(0):
				s = state.generateSuccessor(0, action)
				v = max(v,self.value(s,i,d,t))
			return v
		if i>(d*t-1):
			return self.evaluationFunction(state)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
	t = gameState.getNumAgents()
	li =[]
	#print gameState
	ll = gameState.getLegalActions()
	for a in ll :	
		s = gameState.generateSuccessor(0,a)
		val = self.value(s,1,self.depth,t)
		li.append(val)
		#print a,val
	#print (li)
	return ll[li.index(max(li))]
        util.raiseNotDefined()
	      
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    pos = currentGameState.getPacmanPosition()
    lfood = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    gpos =currentGameState.getGhostPositions()
    nfood=currentGameState.getNumFood()
    caps=currentGameState.getCapsules()
    st = [ghostState.scaredTimer for ghostState in ghostStates]
    food = lfood.asList()
    minfoodd = min([util.manhattanDistance(pos,df) for df in food])
    mincapsd=min([util.manhattanDistance(pos,d) for d in caps])
    g =sum([1.0/(util.manhattanDistance(gpos[i],pos)+0.1) for i in range(len(gpos))])
    numOfScaredGhosts = 0
    m = 0
    print nfood,minfoodd,mincapsd
    for ghostState in ghostStates: 
        if ghostState.scaredTimer is 0:
            numOfScaredGhosts += 1
    if numOfScaredGhosts > 0 :
	m = -300.0
    else:
	m = 300.0
    return -100.0*len(caps) -20.0*len(food) +1.0/minfoodd +m*g	
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
'''
 if st[0] >1 :
	m = 3.0
    else :
	m = -3.0
    if not(nfood ==0) and (minfoodd == 0):
	print 2.0/nfood + 5.0 + m*g + 4.0/(mincapsd + 0.1)

	return 2.0/nfood + 5.0 + m*g + 4.0/(mincapsd + 0.1)
    if not(nfood ==0) and not(minfoodd == 0):
	print 2.0/nfood + 2.0/minfoodd + m*g + 4.0/(mincapsd + 0.1)
	return 2.0/nfood + 2.0/minfoodd + m*g + 4.0/(mincapsd + 0.1)

    else :
	print m*g + 4.0/(mincapsd + 0.1)
	return m*g + 4.0/(mincapsd + 0.1)'''

