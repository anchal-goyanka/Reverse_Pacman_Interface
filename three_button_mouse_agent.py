from game import Agent
from game import Directions
from game import Actions
from game import ghosts_in_action
from game import ghosts_at_rest
from game import ghosts_in_action_right
from game import ghosts_in_action_middle
import random
from util import manhattanDistance
from util import euclidianDistance
import util
import layout
from layout import Layout
import copy

class MouseAgent(Agent):
    """
    An agent controlled by the mouse.
    """
    def __init__( self, index = 0 ):

        self.lastMove = Directions.STOP
        self.index = index		

    def getAction( self, state):
        #getAction gets the action for a given index given the object 'state' of gamestatedata class. 
        legal = state.getLegalActions(self.index)
        #print legal
        ghost_indices = [1,2,3,4]
        #print self.index
        if self.index == 0:
            decision_index = 0 
            conf = state.getPacmanState().configuration
            reverse = Actions.reverseDirection( conf.direction )
            for i in ghost_indices:
                if manhattanDistance(state.getPacmanPosition(),state.getGhostPosition(i)) < 3:
                    decision_index+=1
            if decision_index > 0:
                legal = state.getLegalActions(self.index)
            else:
                if reverse in legal and len(legal)>1:
                    legal.remove(reverse)
            depth = 6
            cost_dict = {}
            ghost_successor_dict = {} # 1:state of ghost 1 at depth i
            for i in ghost_indices:
                ghost_successor_dict[i] = [state.getGhostPosition(i)]            
            pacman_dict = {}  # direction:state of pacman with that direciton at depth i
            for i in legal:
                pacman_dict[i] = [(Actions.getSuccessor(state.getPacmanPosition(),i),i)]
            
            for d in range(depth):
                for ghost in ghost_indices: 
                    temp_list = []
                    for stat in ghost_successor_dict[ghost]:
                        temp_list.append(self.getSuccessors_g(stat,state))
                    ghost_successor_dict[ghost] = []
                    for x in temp_list:
                       for y in x:
                           ghost_successor_dict[ghost].append(y)
                break_value = 0
                if d == 1:
                    for t in pacman_dict.keys():
                        for u in pacman_dict[t]:
                            for ghost in ghost_indices:
                                if u[0] in ghost_successor_dict[ghost]:
                                    break_value =1
                                    cost_dict[t] = d
                                    del pacman_dict[t]
                                    break
                            if break_value == 1:
                                break_value = 0
                                break
                    if len(pacman_dict.keys()) == 1:
                        #print '1111'
                        return pacman_dict.keys()[0]
                else:               
                   for i in pacman_dict.keys():
                        temp_list = []  
                        for tupl in pacman_dict[i]:    #tupl = ((2,3),prev_action)
                            temp_list.append(self.getSuccessors_indexo(tupl,state))
                        pacman_dict[i] = []
                        for x in temp_list:
                            for y in x:
                                pacman_dict[i].append(y)
    
                   for i in pacman_dict.keys():
                       for j in pacman_dict[i]:
                           for ghost in ghost_indices:
                               if j[0] in ghost_successor_dict[ghost]:
                                   cost_dict[i] = d
                                   del pacman_dict[i]
                                   break_value =1
                                   break
                           if break_value == 1:
                               break_vlaue = 0
                               break
                   if len(pacman_dict.keys()) == 1:
                       #print '23234'
                       return pacman_dict.keys()[0]
            #print 'returning random'
            return random.choice(legal)
        distance = {}
        distance_right = {}
        assigned_ghost_right = {}
        from graphicsUtils import click_pos
        from graphicsUtils import del_leftclick_loc
        from graphicsUtils import click_pos_right
        from graphicsUtils import del_rightclick_loc
        from graphicsUtils import click_pos_middle
        from graphicsUtils import del_middleclick_loc
        side = 7
        distance_middle = {}
        assigned_ghost_middle = {}
        #print click_pos(),'mouseagent' 


        '''
        For right click list
        '''
        if self.index in ghosts_in_action_right.keys():
            #print ghosts_in_action
            #print self.index, ghosts_in_action
            a = ghosts_in_action_right[self.index][0]            
            del ghosts_in_action_right[self.index][0]
            if len(ghosts_in_action_right[self.index]) == 0:
                del ghosts_in_action_right[self.index]
                ghosts_at_rest.append(self.index)
                return a
            else:
                return a


        '''
        For middle click list
        '''
        if self.index in ghosts_in_action_middle.keys():
            #print ghosts_in_action
            #print self.index, ghosts_in_action
            a = ghosts_in_action_middle[self.index][0]            
            del ghosts_in_action_middle[self.index][0]
            if len(ghosts_in_action_middle[self.index]) == 0:
                del ghosts_in_action_middle[self.index]
                ghosts_at_rest.append(self.index)
                return a
            else:
                return a


        '''
        For left click list
        '''     
        if self.index in ghosts_in_action.keys():
            #print ghosts_in_action
            #print self.index, ghosts_in_action
            a = ghosts_in_action[self.index][0]            
            del ghosts_in_action[self.index][0]
            if len(ghosts_in_action[self.index]) == 0:
                del ghosts_in_action[self.index]
                ghosts_at_rest.append(self.index)
                return a
            else:
                return a





        else:
            if click_pos_right() != None and len(ghosts_at_rest) == 4:
                goal_state = click_pos_right()
                del_rightclick_loc()
                if state.hasWall(goal_state[0],goal_state[1]):
                    temp_a = 0
                    for acti in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
                        ss = Actions.getSuccessor(goal_state,acti)
                        actual_state = (int(ss[0]),int(ss[1]))
                        if not(state.hasWall(actual_state[0],actual_state[1])):
                            goal_state = actual_state
                            temp_a = 1
                            break
                    if temp_a == 0:
                        print "Please provide valid RIGHT co-ordinates"
                        return Directions.STOP
                ghost_positions = self.right_click_function(goal_state,state) # [(3,4),(4,7)]
                for ii in ghost_positions:
                    for jj in ghosts_at_rest: #jj = 1
                        distance_right[jj] = euclidianDistance(ii, state.getGhostPosition(jj))
                        #print jj , distance_right
                    
                    assigned_ghost_right[ii] = min(distance_right.items(), key=lambda x: x[1])[0] #(1,2):3
                    #print assigned_ghost_right[ii]
                    distance_right.clear()
                    ghosts_at_rest.remove(assigned_ghost_right[ii])
                for kk in assigned_ghost_right.keys():
                    start_state = state.getGhostPosition(assigned_ghost_right[kk])                    
                    dist_list = self.uniformCostSearch(start_state, kk,state)
                    ghosts_in_action_right[assigned_ghost_right[kk]] = dist_list
                    #print assigned_ghost_right,'assigneed ghsot'
                    #print ghosts_at_rest, 'at rest list'
                    #ghosts_at_rest.remove(assigned_ghost_right[kk])
                if self.index in ghosts_in_action_right.keys():
                    a = ghosts_in_action_right[self.index][0]
                    del ghosts_in_action_right[self.index][0]
                    if len(ghosts_in_action_right[self.index]) == 0:
                        del ghosts_in_action_right[self.index]
                        ghosts_at_rest.append(self.index)
                    return a
                else:
                    return Directions.STOP
# middle code here
            init_f = []
            final_f = []
            if click_pos_middle() != None and len(ghosts_at_rest) == 4:
                goal_state = click_pos_middle()
                del_middleclick_loc()
                if state.hasWall(goal_state[0],goal_state[1]):
                    temp_a = 0
                    for acti in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
                        ss = Actions.getSuccessor(goal_state,acti)
                        actual_state = (int(ss[0]),int(ss[1]))
                        if not(state.hasWall(actual_state[0],actual_state[1])):
                            goal_state = actual_state
                            temp_a = 1
                            break
                    if temp_a == 0:
                        print "Please provide valid MIDDLE co-ordinates"
                        return Directions.STOP
                a = 0
                b = 0
                c = 0
                d = 0
                a = goal_state[0] - side + 1
                b = goal_state[1] + side - 1
                c = goal_state[0] + side - 1
                d = goal_state[1] - side + 1
                init_f.append((a,b))
                init_f.append((c,d))
                init_f.append((a+2*side-1,b))
                init_f.append((a,b-2*side + 1))
                for h in range(1,(2*side - 2 )+ 1):
                    init_f.append((a+h,b))
                    init_f.append((a,b-h))
                    init_f.append((c-h,d))
                    init_f.append((c,d+h))
                copyy = copy.deepcopy(init_f)
                for i in copyy:
                    if i[0] > 26 or i[0] < 0 :
                        init_f.remove(i)
                        continue
                    if i[1] > 25 or i[1] < 0:
                        init_f.remove(i)
                        continue
                    if state.hasWall(i[0],i[1]):
                        init_f.remove(i)
                        continue
                if len(init_f)<= 4:
                    ghost_positions = init_f   
                
                else:
                    ini = copy.deepcopy(init_f)
                    for i in ini:
                        successors = self.getSuccessors_indexo3(i,state)
                        s_copy = copy.deepcopy(successors)
                        for s in s_copy:
                            if a <= s[0] <= c and d<= s[1] <= b:
                                successors.remove(s)
                        if len(successors) == 0:
                            init_f.remove(i)    
                    if len(init_f) <= 4:
                        ghost_positions = init_f
                    else:
                        #print len(init_f), init_f, 'len of init f but taken first three'
                        ghost_positions = init_f[:4]                 
                #print ghost_positions, 'ghostpositions'
                for ii in ghost_positions:
                    for jj in ghosts_at_rest: #jj = 1
                        distance_middle[jj] = euclidianDistance(ii, state.getGhostPosition(jj))
                        #print jj , distance_right
                    
                    assigned_ghost_middle[ii] = min(distance_middle.items(), key=lambda x: x[1])[0] #(1,2):3
                    #print assigned_ghost_right[ii]
                    distance_middle.clear()
                    #print assigned_ghost_right[ii],assigned_ghost_right,'see if i1 '
                    ghosts_at_rest.remove(assigned_ghost_middle[ii])
                #print assigned_ghost_right, 'assigned_ghost_right fianl'
                #print ghosts_at_rest
                for kk in assigned_ghost_middle.keys():
                    start_state = state.getGhostPosition(assigned_ghost_middle[kk])                    
                    dist_list = self.uniformCostSearch(start_state, kk,state)
                    ghosts_in_action_middle[assigned_ghost_middle[kk]] = dist_list
                if self.index in ghosts_in_action_middle.keys():
                    aa = ghosts_in_action_middle[self.index][0]
                    del ghosts_in_action_middle[self.index][0]
                    if len(ghosts_in_action_middle[self.index]) == 0:
                        del ghosts_in_action_middle[self.index]
                        ghosts_at_rest.append(self.index)
                    return aa
                else:
                    return Directions.STOP
            if click_pos() != None:
                goal_state = click_pos()
                del_leftclick_loc()
                if state.hasWall(goal_state[0],goal_state[1]):
                    temp_a = 0
                    for acti in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
                        actual_state = (int(Actions.getSuccessor(goal_state,acti)[0]),int(Actions.getSuccessor(goal_state,acti)[1]))
                        if not(state.hasWall(actual_state[0],actual_state[1])):
                            goal_state = actual_state
                            temp_a = 1
                            break
                    if temp_a == 0:
                        print "Please provide valid co-ordinates"
                        return Directions.STOP
                for i in ghosts_at_rest:
                    distance[i] = euclidianDistance(goal_state, state.getGhostPosition(i))
                assigned_ghost = min(distance.items(), key=lambda x: x[1])[0]
                start_state = state.getGhostPosition(assigned_ghost)
                dist_list = self.uniformCostSearch(start_state, goal_state,state)
                ghosts_in_action[assigned_ghost] = dist_list
                ghosts_at_rest.remove(assigned_ghost)
                if assigned_ghost == self.index:
                    a = ghosts_in_action[assigned_ghost][0]
                    del ghosts_in_action[assigned_ghost][0]
                    if len(ghosts_in_action[self.index]) == 0:
                        del ghosts_in_action[self.index]
                        ghosts_at_rest.append(self.index)
                    return a
                else:
                    return Directions.STOP
            else:
                return Directions.STOP


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
            n = fringe.heap[0]
            b = fringe.pop()[1]
            if len(b) != 0: 
                prev_action = b[-1]
            else:
                prev_action = None
            if n[2][0] == goal_state:
                return n[2][1]
               
            if n[2][0] not in closed :
                closed.add(n[2][0])
                n[2][1]= tuple(n[2][1])
                s =self.getSuccessors(n[2][0],objj,prev_action)
                for i in s:
                    li = []
                    li.append(i[0])
                    li.append(list(n[2][1]))
                    li[1].append(i[1])
                    cost = n[0] +i[2]
                    fringe.push(li,cost)

    '''
    Takes a position and returns al immediate successors that are also intersections
    '''
    def right_click_function(self,click,objec):
        fringe_right = []
        a = (click,'Stop')
        click = a
        final_pos = []
        fringe_right = self.getSuccessors_indexo2(click,objec)
        for f in range(len(fringe_right)):
            a = 0
            while (a == 0):
                b = self.getSuccessors_right(fringe_right[f][0],objec,fringe_right[f][1])
                if len(b) == 1:
                    fringe_right[f] = b[0]
                else:
                    a = 1
        for l in range(len(fringe_right)):
            final_pos.append(fringe_right[l][0])
        return final_pos

         

    def getSuccessors(self,state_pos,obj,act):     
        successors = []
        d = ['North','South','East','West']
        new_d = []
        direction_list = []
        reverse = Actions.reverseDirection(act)
        if reverse == None:
            direction_list = d
        elif reverse in d:
            for di in d:
                if di != reverse:
                    new_d.append(di)
            direction_list = new_d
        for action in direction_list:
            x,y = state_pos
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not obj.hasWall(nextx,nexty):
                nextState = (nextx, nexty)
                cost = 1
                successors.append( ( nextState, action, cost) )
        return successors


    def getSuccessors_right(self,state_pos,obj,act):     
        successors = []
        d = ['North','South','East','West']
        new_d = []
        direction_list = []
        reverse = Actions.reverseDirection(act)
        if reverse == None:
            direction_list = d
        elif reverse in d:
            for di in d:
                if di != reverse:
                    new_d.append(di)
            direction_list = new_d
        for action in direction_list:
            x,y = state_pos
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not obj.hasWall(nextx,nexty):
                nextState = (nextx, nexty)
                successors.append( ( nextState, action) )
        return successors


    def getSuccessors_indexo(self,tupl,obj):     
        successors = []
        d = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        prevact = Actions.reverseDirection(tupl[1])
        action_list = []
        for k in d:
            if k != prevact:
                action_list.append(k)
        #print state_pos, 'successor fn state'
        for action in action_list:
            x,y = tupl[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not obj.hasWall(nextx,nexty):
                nextState = (nextx, nexty)
                successors.append( ( nextState, action) )
        #print successors, 'successors'
        return successors

    def getSuccessors_g(self,state_pos,obj):     
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state_pos
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not obj.hasWall(nextx,nexty):
            	nextState = (nextx, nexty)
            	successors.append(nextState)
        successors.append(state_pos)
        #print successors, 'successors'Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        return successors

    def getSuccessors_indexo2(self,tupl,obj):     
        successors = []
        d = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        for action in d:
            x,y = tupl[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not obj.hasWall(nextx,nexty):
                nextState = (nextx, nexty)
                successors.append( ( nextState, action) )
        return successors

    def getSuccessors_indexo3(self,tupl,obj):     
        successors = []
        d = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        for action in d:
            x,y = tupl
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not obj.hasWall(nextx,nexty):
                nextState = (nextx, nexty)
                successors.append(nextState)
        return successors


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
