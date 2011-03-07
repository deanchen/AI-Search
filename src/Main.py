'''
Created on Feb 3, 2011

@author: Administrator
'''

from state import State;
from frontierStruct import FrontierStruct;
import timeit;

'''
graph to be processed by BFS, DFS IDDFS

populated by generate_legal_states() in main

first element of list is the goal state
last element of list is the start state
'''
STATES = [];

def bfs_dfs(type, depth = None):
    global STATES;
    start_state = STATES[len(STATES)-1];
    goal_state = STATES[0];
    
    shortest_dfs_length = None;
    max_depth = 0;
    # reset markings on states
    for state in STATES:
        state.visited = False;
        state.prev = None;
        state.depth = None;
        
    # create appropriate data structure based on search type
    if (type == "bfs"):
        frontier = FrontierStruct('queue');
    elif (type == "dfs"):
        frontier = FrontierStruct('stack');
    else:
        raise Exception("Unknown type");
    
    found = False;
    # add source state on to frontier
    frontier.append(start_state);
    start_state.depth = 0;
    start_state.visited = True;
    
    # run search 
    while (not frontier.empty()):
        state = frontier.pop();
        if (state.depth > max_depth):
            max_depth = state.depth;
        # expand node if not goal state
        if (state != goal_state and (depth == None or state.depth < depth)):
            for child_state in state.arcs:
                if (child_state.visited == False):
                    child_state.depth = state.depth + 1;
                    child_state.prev = state;
                    child_state.visited = True;
                    frontier.append(child_state);
        elif (state == goal_state):
            found = True;
            save_path(state);
            if (type == "bfs"):
                return state;
            else:
                if (shortest_dfs_length == None or shortest_dfs_length > state.depth):
                    shortest_dfs_length = state.depth;
    if not found:
        if (depth == None or max_depth < depth):    
            raise Exception("Search failed");
        else:
            return None;
    else:
        return goal_state;
    
def iddfs():
    depth = 1;
    result = None;
    while (result == None):
        result = bfs_dfs("dfs", depth);
        depth += 1;
                  

def save_path(goal_state):
    state = goal_state;
    start_state = STATES[len(STATES)-1];
    while (state != start_state):
        state.prev_optimal = state.prev;
        state = state.prev;
        
'''
boat
generate legal states for each boat location where:
    all 3 missionaries on left shore
    all 3 missionaries on right shore
    # of missionaries = # of cannibals
'''
def generate_legal_states():
    states = []
    for b in range(0, 2):
        for i in range(0,4):
            for j in range(0,4):
                if (0 == i or 3 == i or i == j):
                    states.append(State(i, j, b));
    
    associate_states(states);    
    return states;             

'''
form association between states with legal transitions
'''
def associate_states(states):
    '''
    split the states in half since only one half needs to be processed
    '''
    split_index = len(states)/2
    right_states = states[0:split_index];
    left_states = states[split_index:len(states)];

    for left_state in left_states:
        
        m = left_state.missionaries;
        c = left_state.cannibals;
        '''
        check for 3 possible transitions:
            empty ship
            1 missionary 1 cannibal
            1 missionary
            1 cannibal
            2 missionaries
            2 cannibals
        '''
        transition_values = [[m-1,c-1], [m-1,c], [m,c-1], [m-2, c], [m, c-2]];
        
        for right_state in right_states:
            m = right_state.missionaries;
            c = right_state.cannibals;
            if [m, c] in transition_values:
                left_state.associate(right_state);

'''
find and return a state given attributes
'''
def find_state(states, m, c, b = None):
    for state in STATES:
        if (state.missionaries == m and state.cannibals == c):
            if ((b == None) or (state.boat == b)):
                return state;

def print_solution(goal_state, start_state):
    steps = [goal_state];
    state = goal_state;
    while (state != start_state):
        state = state.prev_optimal;
        steps.append(state);
    
    state = None;
    while (len(steps)>0):
        state = steps.pop();
        print "%i %s" % (state.depth, state);
    
if __name__ == '__main__':
    STATES = generate_legal_states();
    
    print "BFS Solution";
    bfs_dfs("bfs");
    print_solution(STATES[0], STATES[len(STATES)-1]);
    print "";
    
    print "DFS Solution";
    bfs_dfs("dfs");
    print_solution(STATES[0], STATES[len(STATES)-1]);
    print "";
    
    print "IDDFS Solution";
    iddfs();
    print_solution(STATES[0], STATES[len(STATES)-1]);
    print "";
    
    trials = 3;
    iterations = 100;
    #bfs_dfs("bfs");
    
    for i in range(0, trials):
        t = timeit.Timer('bfs_dfs("bfs")', 'from __main__ import bfs_dfs');
        print("%d Iterations of BFS: %f" % (iterations, t.timeit(number=iterations)));
        
        t = timeit.Timer('bfs_dfs("dfs")', 'from __main__ import bfs_dfs');
        print("%d Iterations of DFS: %f" % (iterations, t.timeit(number=iterations)));
        
        t = timeit.Timer('iddfs()', 'from __main__ import iddfs');
        print("%d Iterations of IDDFS: %f" % (iterations, t.timeit(number=iterations)));
        print "";
    
    

