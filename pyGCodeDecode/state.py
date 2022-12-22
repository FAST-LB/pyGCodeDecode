from typing import List, Type
import numpy as np

class state:
    class position:
        """The Position stores 4D spatial data in x,y,z,e
        Supports
            str, add (pos+pos, pos+(list 1x4), pos+(numpy.ndarray 1x4))
        Additional methods 
            is_travel:      returns True if there is a travel move between self and another given Position
            is_extruding:   returns True if there is an extrusion between self and another given Position
            get_vec:        returns Position as a 1x3 or 1x4 list [x,y,z(,e)], optional argument withExtrusion: default = False
            get_t_distance: returns the absolute travel distance between self and another given Position (3D)
        Class method
            new:            returns an updated Position from given old Position and optional changing positional values
            convert_vector_to_position: returns a Position object with a 1x4 list as input [Vx,Vy,Vz,Ve]
        """
        def __init__(self,x,y,z,e):
            self.x = x
            self.y = y
            self.z = z
            self.e = e
        def __str__(self) -> str:
            return ">>> Position\nx: "+str(self.x)+"\ny: "+str(self.y)+"\nz: "+str(self.z)+"\ne: "+str(self.e)+"\n"
        def __add__(self,other:'state.position') -> 'state.position':
            if isinstance(other,state.position):
                x   = self.x + other.x
                y   = self.y + other.y
                z   = self.z + other.z
                e   = self.e + other.e
                return state.position(x=x,y=y,z=z,e=e)
            elif isinstance(other, np.ndarray) and len(other) == 4:
                x   = self.x + other[0]
                y   = self.y + other[1]
                z   = self.z + other[2]
                e   = self.e + other[3]
                return state.position(x=x,y=y,z=z,e=e)
            elif isinstance(other, list) and len(other) == 4:
                x   = self.x + other[0]
                y   = self.y + other[1]
                z   = self.z + other[2]
                e   = self.e + other[3]
                return state.position(x=x,y=y,z=z,e=e)
            else: raise ValueError("Addition with __add__ is only possible with other Position, 1x4 'list' or 1x4 'numpy.ndarray'")
        def __sub__(self,other:'state.position') -> 'state.position':
            if isinstance(other,state.position):
                x   = self.x - other.x
                y   = self.y - other.y
                z   = self.z - other.z
                e   = self.e - other.e
                return state.position(x=x,y=y,z=z,e=e)
            elif isinstance(other, np.ndarray) and len(other) == 4:
                x   = self.x - other[0]
                y   = self.y - other[1]
                z   = self.z - other[2]
                e   = self.e - other[3]
                return state.position(x=x,y=y,z=z,e=e)
            elif isinstance(other, list) and len(other) == 4:
                x   = self.x - other[0]
                y   = self.y - other[1]
                z   = self.z - other[2]
                e   = self.e - other[3]
                return state.position(x=x,y=y,z=z,e=e)
            else: raise ValueError("Subtraction with __sub__ is only possible with other Position, 1x4 'list' or 1x4 'numpy.ndarray'")
        def __eq__(self,other:'state.position'):
            if self.x == other.x and self.y == other.y and self.z == other.z and self.e == other.e: return True
            else: return False
        def is_travel(self,old_position:'state.position') -> bool:
            if abs(old_position.x-self.x)+abs(old_position.y-self.y)+abs(old_position.z-self.z) > 0: return True
            else: return False
        def is_extruding(self,old_position:'state.position') -> bool:
            if abs(old_position.e-self.e)>0: return True
            else: return False
        def get_vec(self,withExtrusion=False):
            if withExtrusion: return [self.x,self.y,self.z,self.e]
            else: return [self.x,self.y,self.z]
        def get_t_distance(self,old_position:'state.position'=None,withExtrusion=False) -> float:
            if old_position is None: old_position = state.position(0,0,0,0)
            return np.linalg.norm(np.subtract(self.get_vec(withExtrusion=withExtrusion),old_position.get_vec(withExtrusion=withExtrusion)))
        @classmethod
        def new(cls,old_position,x:float=None,y:float=None,z:float=None,e:float=None,absMode=True):
            if x is None:
                x = old_position.x
            if y is None:
                y = old_position.y
            if z is None:
                z = old_position.z
            if e is None:
                e = old_position.e
            if not absMode and not e is None: #if rel mode, extrusion needs to be summed
                e = old_position.e + e
            return cls(x,y,z,e)
        @classmethod
        def convert_vector_to_position(cls,vector:List[float]):
            return cls(x=vector[0], y=vector[1], z=vector[2],e=vector[3])
            
    class p_settings:
        """Store Printing Settings
        Supports
            str,repr
        Class method
            new:            returns an updated p_settings from given old p_settings and optional changing values
        """
        def __init__(self,p_acc,jerk,Vx,Vy,Vz,Ve,speed,absMode=True):
            self.p_acc  = p_acc     #printing acceleration
            self.jerk   = jerk      #jerk settings
            self.Vx     = Vx        #max axis speed X
            self.Vy     = Vy        #max axis speed Y
            self.Vz     = Vz        #max axis speed Z
            self.Ve     = Ve        #max axis speed E
            self.speed  = speed     #travel speed for move
            self.absMode= absMode
        def __str__(self) -> str:
            return ">>> Print Settings:\nJerk: "+str(self.jerk)+"\nPrinting Acceleration: "+str(self.p_acc)+"\nMaximum Axis Speeds: [Vx:" + str(self.Vx) +", Vy:" + str(self.Vy) + ", Vz:" + str(self.Vz) + ", Ve:" + str(self.Ve) + "]\n" + "Printing speed: " + str(self.speed) +"\n"
        def __repr__(self) -> str:
            return self.__str__()
        @classmethod
        def new(cls,old_settings:'state.p_settings', p_acc:float=None, jerk:float=None,Vx:float=None,Vy:float=None,Vz:float=None,Ve:float=None,speed:float=None,absMode:bool=None):
            if p_acc is None:
                p_acc   = old_settings.p_acc    
            if jerk is None:
                jerk    = old_settings.jerk     
            if Vx is None:                  
                Vx      = old_settings.Vx       
            if Vy is None:
                Vy      = old_settings.Vy       
            if Vz is None:
                Vz      = old_settings.Vz       
            if Ve is None:
                Ve      = old_settings.Ve       
            if speed is None:
                speed = old_settings.speed
            if absMode is None:
                absMode = old_settings.absMode
            return cls(p_acc=p_acc,jerk=jerk,Vx=Vx,Vy=Vy,Vz=Vz,Ve=Ve,speed=speed,absMode=absMode)

    """State contains a Position and the gcode-defined Printing Settings (p_settings) to apply for the corresponding move to the Position
    Supports
        str
    Class method
        new: returns new State from old State and given optional changing Position and/or Print Settings
    """
    def __init__(self,state_position:position,state_p_settings:p_settings):
        self.state_position   = state_position
        self.state_p_settings = state_p_settings
        self.next_state = None
        self.prev_state = None
        self.line_nmbr  = None
    
    @property
    def state_position(self):
        return self._state_position
    @state_position.setter
    def state_position(self,set_position:position):
        self._state_position = set_position
    
    @property
    def state_p_settings(self):
        return self._state_p_settings
    @state_p_settings.setter
    def state_p_settings(self,set_p_settings:p_settings):
        self._state_p_settings = set_p_settings
    
    @property
    def line_nmbr(self):
        return self._line_nmbr
    @line_nmbr.setter
    def line_nmbr(self,nmbr):
        self._line_nmbr = nmbr

    #Neighbor list
    @property
    def next_state(self):
        return self._next_state
    @next_state.setter
    def next_state(self,state:'state'):
        self._next_state = state
    
    @property
    def prev_state(self):
        return self._prev_state
    @prev_state.setter
    def prev_state(self,state:'state'):
        self._prev_state = state

    def __str__(self) -> str:
        return f"<<< State Information line: {self.line_nmbr} >>>\n {self.state_position} {self.state_p_settings}"
    def __repr__(self) -> str:
            return self.__str__()
    @classmethod
    def new(cls,old_state:'state',position:position=None,p_settings:p_settings=None):
        if position     is None:
            position    = old_state.position
        if p_settings   is None:
            p_settings  = old_state.p_settings
        return cls(state_position=position,state_p_settings=p_settings)
