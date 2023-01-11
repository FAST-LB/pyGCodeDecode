"""
Utils for the GCode Reader contains:
-Velocity as Class
-Segment
"""
from typing import List, Type
import numpy as np
from .state import state

class velocity:
    """4D - Velocity object for (cartesian) 3D Printer
    Supports
        str, add, sub, mul (scalar), truediv (scalar),eq
    Additional methods 
        get_vec:        returns Velocity as a 1x3 or 1x4 list [Vx,Vy,Vz(,Ve)], optional argument withExtrusion: default = False
        get_abs:        returns the absolute 3D movement Velocity, extrusion is ignored
        get_norm dir:   returns the normalized direction as 1x3 or 1x4 list [Vx,Vy,Vz(,Ve)], optional argument withExtrusion: default = False
        avoid_overspeed:returns Velocity with all axis kept below their max travel speed
    Class method
        convert_vector_to_velocity: returns a Velocity object with a 1x4 list as input [Vx,Vy,Vz,Ve]
    """
    def __init__(self,Vx:float,Vy:float,Vz:float,Ve:float):
         self.Vx    = Vx
         self.Vy    = Vy
         self.Vz    = Vz
         self.Ve    = Ve
    def __str__(self) -> str:
        return "Velocity: [Vx:" + str(self.Vx) +", Vy:" + str(self.Vy) + ", Vz:" + str(self.Vz) + ", Ve:" + str(self.Ve) + "]"
    def __add__(self,other:'velocity') -> 'velocity':
            Vx   = self.Vx + other.Vx
            Vy   = self.Vy + other.Vy
            Vz   = self.Vz + other.Vz
            Ve   = self.Ve + other.Ve
            return velocity(Vx=Vx,Vy=Vy,Vz=Vz,Ve=Ve)
    def __sub__(self,other:'velocity') -> 'velocity':
            Vx   = self.Vx - other.Vx
            Vy   = self.Vy - other.Vy
            Vz   = self.Vz - other.Vz
            Ve   = self.Ve - other.Ve
            return velocity(Vx=Vx,Vy=Vy,Vz=Vz,Ve=Ve)
    def __mul__(self,other):
        #ggfs problem hier, nochmal prüfen ob mul so richtig ist
        if type(other) is float or type(other) is np.float64 or type(other) is int:
            Vx   = self.Vx * other
            Vy   = self.Vy * other
            Vz   = self.Vz * other
            Ve   = self.Ve * other
        else: raise TypeError("mutiplication of Velocities only supports float")
        return velocity(Vx=Vx,Vy=Vy,Vz=Vz,Ve=Ve)
    def __truediv__(self,other):
        if type(other) is float or type(other) is np.float64:
            Vx   = self.Vx / other
            Vy   = self.Vy / other
            Vz   = self.Vz / other
            Ve   = self.Ve / other
        else: raise TypeError("division of Velocities only supports float")
        return velocity(Vx=Vx,Vy=Vy,Vz=Vz,Ve=Ve)
    def __eq__(self,other:'velocity'):
        equal = True
        equal = False if self.Vx != other.Vx else equal
        equal = False if self.Vy != other.Vy else equal
        equal = False if self.Vz != other.Vz else equal
        equal = False if self.Ve != other.Ve else equal
        return equal
    def get_vec(self,withExtrusion=False):
        if withExtrusion: return [self.Vx,self.Vy,self.Vz,self.Ve]
        else: return [self.Vx,self.Vy,self.Vz]
    def get_abs(self):
        return np.linalg.norm(self.get_vec())
    def get_norm_dir(self,withExtrusion=False):
        abs_val = self.get_abs()
        return self.get_vec(withExtrusion=withExtrusion)/abs_val if abs_val > 0 else None
    def avoid_overspeed(self,p_settings:state.p_settings):
        """Returns velocity without any axis overspeed"""
        scale = 1.0
        scale = p_settings.Vx / self.Vx if self.Vx > 0 and p_settings.Vx / self.Vx < scale else scale
        scale = p_settings.Vy / self.Vy if self.Vy > 0 and p_settings.Vy / self.Vy < scale else scale
        scale = p_settings.Vz / self.Vz if self.Vz > 0 and p_settings.Vz / self.Vz < scale else scale
        scale = p_settings.Ve / self.Ve if self.Vz > 0 and p_settings.Ve / self.Ve < scale else scale

        return self * scale
    def not_zero(self):
        return True if np.linalg.norm(self.get_vec(withExtrusion=True)) > 0 else False

    @classmethod
    def convert_vector_to_velocity(cls,vector:List[float]):
        return cls(Vx=vector[0], Vy=vector[1], Vz=vector[2],Ve=vector[3])

class segment:
    """stores Segment data for linear 4D Velocity function segment, contains: time,position,velocity
    Supports
        str
    Additional methods 
        move_segment_time:      moves Segment in time by a specified interval
        get_velocity:           returns the calculated Velocity for all axis at a given point in time
        get_position:           returns the calculated Position for all axis at a given point in time
    Class method
        create_initial:         returns the artificial initial segment where everything is at standstill, intervall length = 0
        self_check:             returns True if all self checks have been successfull
    """    
    def __init__(self,t_begin:float, t_end:float, pos_begin:state.position, vel_begin:velocity, pos_end:state.position=None, vel_end:velocity=None):
        self.t_begin    = t_begin
        self.t_end      = t_end
        self.pos_begin  = pos_begin
        self.pos_end    = pos_end
        self.vel_begin  = vel_begin
        self.vel_end    = vel_end
        self.self_check()
    def __str__(self) -> str:
        distance = self.pos_end.get_t_distance(old_position=self.pos_begin) if not self.pos_end is None else 0 
        #return f"Segment length: {distance} mm from {self.t_begin}s to {self.t_end}s\nv_begin: {self.vel_begin}\tv_end: {self.vel_end}\n"
        return f"\nSegment from: \n{self.pos_begin} to \n{self.pos_end} Self check: {self.self_check()}.\n"    
    def __repr__(self):
        return self.__str__()
    def move_segment_time(self,delta_t:float):
        self.t_begin    = self.t_begin + delta_t
        self.t_end      = self.t_end   + delta_t
    def get_velocity(self,t):
        if t<self.t_begin or t>self.t_end:
            raise ValueError("Segment not defined for this point in time.")
        else:
            #linear interpolation of velocity in Segment
            delt_vel    = self.vel_end  - self.vel_begin
            delt_t      = self.t_end    - self.t_begin
            slope       = delt_vel/delt_t if delt_t > 0 else velocity(0,0,0,0)
            current_vel = self.vel_begin + slope * (t - self.t_begin)
            return current_vel
    def get_position(self,t):
        if t<self.t_begin or t>self.t_end:
            raise ValueError("Segment not defined for this point in time.")
        else:
            current_vel = self.get_velocity(t=t)
            position    = self.pos_begin + ((self.vel_begin + current_vel) * (t - self.t_begin) / 2.0).get_vec(withExtrusion=True)
            return position
    def self_check(self):#,tolerance=float("e-13"), state:state=None):
        # WIP, check for self consistency
        # > travel distance
        position        = self.pos_begin + ((self.vel_begin + self.vel_end) * (self.t_end - self.t_begin) / 2.0).get_vec(withExtrusion=True)
        pos_check       = self.pos_end == position
        if pos_check:
            return pos_check
        else:
            error_distance = np.linalg.norm(np.asarray(self.pos_end.get_vec())-np.asarray(position.get_vec()))
            return "Error distance: " + str(error_distance)
        # > max acceleration
        # > max velocity
        # ..more?
    
    @classmethod
    def create_initial(cls,initial_position:state.position=None):
        velocity_0 = velocity(Vx=0,Vy=0,Vz=0,Ve=0)
        pos_0      = state.position(x=0,y=0,z=0,e=0) if initial_position is None else initial_position
        return cls(t_begin=0,t_end=0,pos_begin=pos_0,vel_begin=velocity_0,pos_end=pos_0,vel_end=velocity_0)
