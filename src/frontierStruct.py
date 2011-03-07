'''
Created on Feb 3, 2011

@author: Administrator
'''

from collections import deque

class FrontierStruct(object):
    '''
    create a universal interface for queue or stack for use in DFS or BFS
    '''
    
    def __init__(self, type):
        '''
        Create the appropriate data structure from the argument
        '''
        self.type = type;
        if type == 'queue':
            self.struct = deque([]);
        elif type == 'stack':
            self.struct = [];
        else:
            raise Exception("Unknown type");
    
    def __iter__(self):
        return self.struct.__iter__();
    
    def append(self, state):
        self.struct.append(state);
        
    def pop(self):
        if (self.type == 'queue'):
            return self.struct.popleft();
        elif (self.type == 'stack'):
            return self.struct.pop();
        
    def empty(self):
        if not self.struct:
            return True;
        else:
            return False;