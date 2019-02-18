import Player
import Fountain
import Rival

import numpy as np

class FarmTile(object):
    def __init__(self, unit = None):
        self._unit = unit
        
    def __repr__(self):
        if self._unit is None:
            return " "
        else:
            return str(self._unit)
        
    def __str__(self):
        return self.__repr__()
        
    def __eq__(self, other): 
        return str(self._unit) == str(other._unit)
        
    def update_unit(self, new_unit):
        self._unit = new_unit

def _contains_unit(farmtile, unit):
    if isinstance(farmtile._unit, unit):
        return True
    else:
        return False

contains_unit = np.vectorize(_contains_unit)

class FarmMap(object):
    def __init__(self):
        # Meta-data
        self._start = (0, 0)
        self._end = (2, 2)
        self._layout = np.array([FarmTile() for _ in range(9)]).reshape((3, 3))
        
        # Fill in layout
        self._layout[self._start].update_unit(Player.Player())
        self._layout[(1, 1)].update_unit(Rival.Rival())
        self._layout[self._end].update_unit(Fountain.Fountain())
        self.outcome = None
    
    def __repr__(self):
        return '%s|%s|%s\n-----\n%s|%s|%s\n-----\n%s|%s|%s' % (self._layout[0,0],
                                                               self._layout[0,1],
                                                               self._layout[0,2],
                                                               self._layout[1,0],
                                                               self._layout[1,1],
                                                               self._layout[1,2],
                                                               self._layout[2,0],
                                                               self._layout[2,1],
                                                               self._layout[2,2])
        
    def __str__(self):
        return self.__repr__()
        
    def find_player(self):
        out_tuple_arrays = np.nonzero(contains_unit(self._layout, Player.Player))
        loc = tuple([a[0] for a in out_tuple_arrays])
        return(loc)
        
    def find_fountain(self):
        out_tuple_arrays = np.nonzero(contains_unit(self._layout, Fountain.Fountain))
        loc = tuple([a[0] for a in out_tuple_arrays])
        return(loc)
        
    def find_rival(self):
        out_tuple_arrays = np.nonzero(contains_unit(self._layout, Rival.Rival))
        loc = tuple([a[0] for a in out_tuple_arrays])
        return(loc)
        
    def find_possible_directions(self):
        current_location = self.find_player()
        possible_directions = []
        # Up?
        if current_location[0] > 0:
            possible_directions.append("Up")
        # Down?
        if current_location[0] < np.shape(self._layout)[0] - 1:
            possible_directions.append("Down")
        # Left?
        if current_location[1] > 0:
            possible_directions.append("Left")
        # Right?
        if current_location[1] < np.shape(self._layout)[1] - 1:
            possible_directions.append("Right")
        return(possible_directions)
        
    def move(self, direction):
        if direction not in self.find_possible_directions():
            raise ValueError('Invalid move')
        current_tile = self.find_player()
        if direction == 'Up':
            new_tile = tuple([a + b for a, b in zip(current_tile, [-1, 0])])
        elif direction == 'Down':
            new_tile = tuple([a + b for a, b in zip(current_tile, [1, 0])])
        elif direction == 'Left':
            new_tile = tuple([a + b for a, b in zip(current_tile, [0, -1])])
        else:
            new_tile = tuple([a + b for a, b in zip(current_tile, [0, 1])])
        self.resolve_collision(current_tile, new_tile)
        return
        
    def resolve_collision(self, current_tile, new_tile):
        if self._layout[new_tile]._unit is None:
            self._layout[new_tile].update_unit(self._layout[current_tile]._unit)
            self._layout[current_tile].update_unit(None)
        elif isinstance(self._layout[new_tile]._unit, Fountain.Fountain):
            self._layout[new_tile]._unit._discovered = True
            raise Fountain.FountainCollision()
        elif isinstance(self._layout[new_tile]._unit, Rival.Rival):
            self._layout[new_tile]._unit._discovered = True
            raise Rival.RivalCollision()
        return            
        
#x = FarmMap()
#print(x)
#print(x.find_player())
#print(x.find_possible_directions())
#print()
#x.move('Down')
#print(x)
#print(x.find_player())
#print(x.find_possible_directions())
#x.move('Right')
#print(x)
#print(x.find_player())
#print(x.find_possible_directions())
#x.move('Down')
#print(x)
#print(x.find_player())
#print(x.find_possible_directions())
#x.move('Right')
#print(x)
#print(x.find_player())
#print(x.find_possible_directions())
#x.move('Up')
#print(x)
#print(x.find_player())
#print(x.find_possible_directions())