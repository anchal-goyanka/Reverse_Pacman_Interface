from game import Agent
from game import Directions
from game import Actions
from game import ghosts_in_action
from game import ghosts_at_rest
from game import ghost_goal_position
import random
from util import manhattanDistance
from util import euclidianDistance
import util
import layout
from layout import Layout

class MouseAgent(Agent):
    """
    An agent controlled by the mouse.
    """
    def __init__( self, index = 0 ):

        self.lastMove = Directions.STOP
        self.index = index	

    def getAction( self, state):

        legal = state.getLegalActions(self.index)
        #print legal,'legal',self.index
              
        if self.index == 0:
            '''
            Where pacman knows ghosts end positions
        
            cheat_dic = {}
            for i in [1,2,3,4]:
                if i in ghosts_in_action.keys():
                    cheat_dic[i] = ghosts_in_action[i][] 
            '''    
            cost = {}  #stores cost for taking various actions
            pacman_pos = state.getPacmanPosition()
            #print pacman_pos,'old_pos'
            ghost_pos_dic = {}
            ghosts = [1,2,3,4]
            for i in ghosts:
                ghost_pos_dic[i] = state.getGhostPosition(i)
            for action in legal:
                successor_state = state.generatePacmanSuccessor(action)
                new_pos = successor_state.getPacmanPosition()
                #print new_pos,'new_pos'
                value = 0
                for i in ghost_pos_dic:
                    distance = util.manhattanDistance(new_pos, ghost_pos_dic[i])
                    #print i,action,distance
                    if distance == 0 : distance = 0.1000
                    value += 1.0/distance
                    #print value, 'value'
                cost[action] = value
            minvalue = min(cost.values())
            #print minvalue,'min val'
            #print cost, 'cost'
            for i in cost.keys():
                if cost[i] == minvalue:
                    #print i
                    return i            
                                
            #return random.choice(legal) 
            
        distance = {}
        from graphicsUtils import click_pos
        from graphicsUtils import del_leftclick_loc
        #print click_pos(),'mouseagent' 
             
        if self.index in ghosts_in_action.keys():
            #print ghosts_in_action
            #print self.index, ghosts_in_action
            a = ghosts_in_action[self.index][0]            
            del ghosts_in_action[self.index][0]
            if len(ghosts_in_action[self.index]) == 0:
                del ghosts_in_action[self.index]
                ghosts_at_rest.append(self.index)
                #print 'action returned for index and list already present'
                return a
            else:
                return a 
        else:
            if click_pos() != None:
                goal_state = click_pos()
                del_leftclick_loc()
                if state.hasWall(goal_state[0],goal_state[1]):
                    print "Please give valid co-ordinates"
                    return Directions.STOP
                for i in ghosts_at_rest:
                    distance[i] = euclidianDistance(goal_state, state.getGhostPosition(i))
                assigned_ghost = min(distance.items(), key=lambda x: x[1])[0]
                start_state = state.getGhostPosition(assigned_ghost)
                #print start_state, 'start'
                #print goal_state, 'goal'
                #dist_list = self.depthFirstSearch(start_state, goal_state,state)
                dist_list = self.uniformCostSearch(start_state, goal_state,state)
                ghosts_in_action[assigned_ghost] = dist_list
                ghosts_at_rest.remove(assigned_ghost)
                #print ghosts_in_action, assigned_ghost, ghosts_at_rest, 'after one dfs '
                if assigned_ghost == self.index:
                    a = ghosts_in_action[assigned_ghost][0]
                    del ghosts_in_action[assigned_ghost][0]
                    if len(ghosts_in_action[self.index]) == 0:
                        del ghosts_in_action[self.index]
                        ghosts_at_rest.append(self.index)
                    #print 'action returned for newly formed ghost tree'
                    return a
                else:
                    #print 'action returned after dfs for other ghost'
                    return Directions.STOP
            else:
                #print 'action returned since no clicks'
                return Directions.STOP

    def depthFirstSearch(self,start_state, goal_state,objj):    
        closed = set()
        fringe = util.Stack()
        from game import Directions
        South = Directions.SOUTH
        West = Directions.WEST
        North = Directions.NORTH
        East = Directions.EAST
        South = Directions.STOP
        l=[start_state,[]]
        fringe.push(l) 
        while (not(fringe.isEmpty())):        
            fringe.pop()	
            if (n[0] == goal_state):
                return n[1]
            if n[0] not in closed :
                closed.add(n[0])
                n[1]= tuple(n[1])
                s =self.getSuccessors(n[0],objj)
                for successor in s:
                    li = []
                    li.append(successor[0])
                    li.append(list(n[1]))
                    li[1].append(successor[1])
                    fringe.push(li)
    def uniformCostSearch(self,start_state, goal_state,objj):
        """Search the node of least total cost first."""
        closed = set()
        fringe = util.PriorityQueue()
        from game import Directions
        South = Directions.SOUTH
        West = Directions.WEST
        North = Directions.NORTH
        East = Directions.EAST
        Stop = Directions.STOP
        l=[start_state,[]]
        fringe.push(l,0)
        if start_state == goal_state:
            return [Directions.STOP]
        while (not(fringe.isEmpty())):
            #print ("list",fringe.heap)
            n = fringe.heap[0]
            fringe.pop()
            if n[2][0] == goal_state:
                return n[2][1]
               
            if n[2][0] not in closed :
                closed.add(n[2][0])
                n[2][1]= tuple(n[2][1])
                s =self.getSuccessors(n[2][0],objj)
                #print ("s",s)
                for i in s:
                    li = []
                    li.append(i[0])
                    li.append(list(n[2][1]))
                    li[1].append(i[1])
                    cost = n[0] +i[2]
                    fringe.push(li,cost)

    def getSuccessors(self,state_pos,obj):     
        successors = []
        #print state_pos, 'successor fn state'
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state_pos
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not obj.hasWall(nextx,nexty):
            	nextState = (nextx, nexty)
            	cost = 1
            	successors.append( ( nextState, action, cost) )
        #print successors, 'successors'
        return successors

    

'''
def getSuccessors(state_pos):     
    successors = []
    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
        x,y = state_pos
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        #print state.getWalls(), 'walls'
        if not (([nextx],[nexty])):
        	nextState = (nextx, nexty)
        	cost = 1
        	successors.append( ( nextState, action, cost) )
    return successors


def depthFirstSearch(start_state, goal_state):    
    closed = set()
    fringe = util.Stack()
    from game import Directions
    South = Directions.SOUTH
    West = Directions.WEST
    North = Directions.NORTH
    East = Directions.EAST
    l=[start_state,[]]
    fringe.push(l)
    while (not(fringe.isEmpty())):
        n = fringe.list[-1]
        fringe.pop()	
        if (n[0] == goal_state):
            print n[1], 'ini'
            return n[1]
        if n[0] not in closed :
            closed.add(n[0])
            n[1]= tuple(n[1])
            s =getSuccessors(n[0])
            for i in s:
            	li = []
            	li.append(i[0])
            	li.append(list(n[1]))
            	li[1].append(i[1])
            	fringe.push(li)
		
'''
                     
''' 
    def getMove(self, legal):
        move = Directions.STOP
        if   (self.WEST_KEY in self.keys or 'Left' in self.keys) and Directions.WEST in legal:  move = Directions.WEST
        if   (self.EAST_KEY in self.keys or 'Right' in self.keys) and Directions.EAST in legal: move = Directions.EAST
        if   (self.NORTH_KEY in self.keys or 'Up' in self.keys) and Directions.NORTH in legal:   move = Directions.NORTH
        if   (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move

class KeyboardAgent2(KeyboardAgent):
    """
    A second agent controlled by the keyboard.
    """
    # NOTE: Arrow keys also work.
    WEST_KEY  = 'j'
    EAST_KEY  = "l"
    NORTH_KEY = 'i'
    SOUTH_KEY = 'k'
    STOP_KEY = 'u'

    def getMove(self, legal):
        move = Directions.STOP
        if   (self.WEST_KEY in self.keys) and Directions.WEST in legal:  move = Directions.WEST
        if   (self.EAST_KEY in self.keys) and Directions.EAST in legal: move = Directions.EAST
        if   (self.NORTH_KEY in self.keys) and Directions.NORTH in legal:   move = Directions.NORTH
        return move


        if move == Directions.STOP:     #when keys = [] (keys is empty, i.e no input from the user)
            # Try to move in the same direction as before
            if self.lastMove in legal:
                move = self.lastMove

        if (self.STOP_KEY in self.keys) and Directions.STOP in legal: move = Directions.STOP

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        return move
'''
