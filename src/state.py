'''
Created on Feb 3, 2011

@author: Administrator
'''

from sets import Set

class State(object):
    '''
    Represents the state of the original end of the shore and edges to other states
    '''

    def __str__(self):
        return self._string_representation();
    def __repr__(self):
        return self._string_representation();
    
    def _string_representation(self):
        return "m:%d c:%d b:%d" % (self.missionaries, self.cannibals, self.boat);
    
    def __init__(self, missionaries, cannibals, boat):
        '''
        Initialize # of missionaries cannibals and boat location
        '''
        self.missionaries = missionaries;
        self.cannibals = cannibals
        self.boat = boat;
        self.arcs = Set([]);
        
    def associate(self, state, recipricate = True):
        self.arcs.add(state);
        if (recipricate):
            state.associate(self, False);
        
        
        