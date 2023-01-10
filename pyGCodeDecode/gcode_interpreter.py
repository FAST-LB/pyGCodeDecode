"""WIP gcode Reader""" 
import numpy as np
from typing import List
from .planner_block import planner_block
from .state import state
from .state_generator import read_GCODE_from_file
from .utils import segment
from timeit import default_timer as timer


def generate_planner_blocks(states:List[state]):
    """
    converts list of states to trajectory segments

    Parameters
    ----------
    states  :   List[state]
        list of states

    Returns
    ----------
    blck_list[planner_block]
        list of all plannerblocks to complete travel between all states
    """
    blck_list   = []
    for state in states:
        prev_blck           = blck_list[-1] if len(blck_list) > 0 else None         #grab prev blck from blck_list
        new_blck            = planner_block(state=state,prev_blck=prev_blck)        #generate new blck 
        if len(new_blck.get_segments())>0:
            if not new_blck.prev_blck is None:
                new_blck.prev_blck.next_blck = new_blck  #update nb list
            blck_list.extend([new_blck])
    return blck_list

def find_current_segm(path:List[segment],t:float,last_index:int=None):
    """
    finds the current segment

    Parameters
    ----------
    path    :   List[segment]
        all segments to be searched
    t       :   float
        time of search
    last_index: int
        last found index for optimizing search

    Returns
    ----------
    segment
        the segment which defines movement at that point in time
    """
    #some robustness checks
    if path[-1].t_end < t:
        print("No movement at this time in Path!")
        return None,None
    elif last_index is None or len(path)-1 < last_index or path[last_index].t_begin > t:
        #print(f"unoptimized Search, last index: {last_index}")
        for last_index,segm in enumerate(path):
            if t >= segm.t_begin and t < segm.t_end: return segm,last_index
    else:
        for id,segm in enumerate(path[last_index:]):
            if t >= segm.t_begin and t <= segm.t_end: 
                return segm,last_index+id
        raise ValueError("nothing found")

def unpack_blocklist(blocklist:List[planner_block])->List[segment]:
    """
    Returns list of segments by unpacking list of plannerblocks.
    """
    path = []
    for block in blocklist:
        path.extend(block.get_segments()[:])
    return path

class gcode_interpreter:

    def plot_2d_position(self,filename="trajectory.png",show_points=True,dpi=400):
        import matplotlib.pyplot as plt
        
        segments = unpack_blocklist(blocklist=self.blocklist)
        x,y = [],[]
        x.append(segments[0].pos_begin.get_vec()[0])
        y.append(segments[0].pos_begin.get_vec()[1])
        for segm in segments:
            x.append(segm.pos_end.get_vec()[0])
            y.append(segm.pos_end.get_vec()[1])
        
        new = plt.subplot()
        new.plot(x,y,color="red")

        if show_points:
            for blck in self.blocklist:
                new.scatter(blck.get_segments()[-1].pos_end.get_vec()[0],blck.get_segments()[-1].pos_end.get_vec()[1],color="blue",marker="x")
        
        plt.xlabel("x position")
        plt.ylabel("y position")
        plt.title("2D Position")
        plt.savefig(filename,dpi=dpi)
        plt.close()

    def plot_vel(self,axis=("x","y","z","e"),show_plannerblocks=True,show_segments=False,show_JD=True,timesteps=2000,filename="velplot.png",dpi=400):
        import matplotlib.pyplot as plt
        axis_dict = {"x":0,"y":1,"z":2,"e":3}
        
        segments = unpack_blocklist(blocklist=self.blocklist) #unpack

        ##timesteps
        if type(timesteps) == int: #evenly distributed timesteps
            times = np.linspace(0,self.blocklist[-1].get_segments()[-1].t_end,timesteps,endpoint=False)
        elif timesteps == "constrained": #use segment timepoints as plot constrains
            times = [0]
            for segm in segments:
                times.append(segm.t_end)
        else: raise ValueError("Invalid value for Timesteps, either use Integer or \"constrained\" as argument.")

        ##gathering values
        pos     = [[],[],[],[]]
        vel     = [[],[],[],[]]
        abs     = [] #initialize value arrays
        index_saved = 0
        for t in times:
            segm, index_saved = find_current_segm(path=segments,t=t,last_index=index_saved)
            

            tmp_vel = segm.get_velocity(t=t).get_vec(withExtrusion=True)
            tmp_pos = segm.get_position(t=t).get_vec(withExtrusion=True)
            for ax in axis:
                pos[axis_dict[ax]].append(tmp_pos[axis_dict[ax]])
                vel[axis_dict[ax]].append(tmp_vel[axis_dict[ax]])
            
            abs.append(np.linalg.norm(tmp_vel[:3]))

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        #plot JD-Limits
        for blck in self.blocklist:
            
            #plannerblocks vertical line plot
            if show_plannerblocks:  
                ax1.axvline(x=blck.get_segments()[-1].t_end,color="black",lw=0.5)
            
            #segments vertical line plot
            if show_segments:       
                for segm in blck.get_segments():
                    ax1.axvline(x=segm.t_end,color="green",lw=0.25)

            if show_JD:
                #absolute JD Marker
                absJD = np.linalg.norm([blck.JD[0],blck.JD[1],blck.JD[2]]) 
                ax1.scatter(x=blck.get_segments()[-1].t_end,y=absJD,color="red",marker="x")
                for ax in axis:
                    ax1.scatter(x=blck.get_segments()[-1].t_end,y=blck.JD[axis_dict[ax]],marker="x",color="black",lw=0.5)

        #plot all axis in velocity and position
        for ax in axis:
            ax1.plot(times,vel[axis_dict[ax]],label=ax) #velocity
            ax2.plot(times,pos[axis_dict[ax]],linestyle="--") #position w/ extrusion
            #if not ax == "e": ax2.plot(times,pos[axis_dict[ax]],linestyle="--") #position ignoring extrusion
        ax1.plot(times,abs,color="black",label="abs") #absolute velocity


        ax1.set_xlabel("time in s")
        ax1.set_ylabel("velocity in mm/s")
        ax2.set_ylabel("position in mm")
        ax1.legend(loc="lower left")
        plt.title("Velocity and Position over Time")
        plt.savefig(filename,dpi=400)
        plt.close()

    def trajectory_self_correct(self):
        ###self correction
        for block in self.blocklist:
            block.self_correction()
    
    def get_values(self,t):
        segments                = unpack_blocklist(blocklist=self.blocklist)
        segm, self.last_index   = find_current_segm(path=segments,t=t,last_index=self.last_index)
        tmp_vel = segm.get_velocity(t=t).get_vec(withExtrusion=True)
        tmp_pos = segm.get_position(t=t).get_vec(withExtrusion=True)
        
        return tmp_vel,tmp_pos
    
    def check_printer(self,printer):
        """
        Method to check the printer Dict for typos or missing parameters.
        """
        printer_keys = [
        "nozzle_diam",
        "filament_diam",
        "velocity",
        "acceleration",
        "jerk",
        "Vx",
        "Vy",
        "Vz",
        "Ve"
        ]
        
        #Following code could be improved i guess..

        ##check if all provided keys are valid
        for key in printer:
            if not key in printer_keys:
                raise ValueError(f"Invalid Key: \"{key}\" in Printer Dictionary, check for typos. Valid keys are: {printer_keys}")
        
        ##check if every required key is proivded
        for key in printer_keys:
            if not key in printer:
                raise ValueError(f"Key: \"{key}\" is not provided in Printer Dictionary, check for typos. Required keys are: {printer_keys}")



    def __init__(self,filename,initial_position,printer):
        self.last_index = None #used to optimize search in segment list
        ###SET INITIAL SETTINGS
        self.check_printer(printer=printer)

        initial_p_settings  =  state.p_settings(p_acc=printer["acceleration"],jerk=printer["jerk"],Vx=printer["Vx"],Vy=printer["Vy"],Vz=printer["Vz"],Ve=printer["Ve"],speed=printer["velocity"])

        self.states         = read_GCODE_from_file(filename=filename,initial_p_settings=initial_p_settings,initial_position=initial_position)
        
        self.blocklist      = generate_planner_blocks(states=self.states)

        self.trajectory_self_correct()
        
