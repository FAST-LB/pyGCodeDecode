"""WIP gcode Reader""" 
import numpy as np

class gcodeTrajectory:
    def __init__(self,filename):
        """
        This initiates a trajectory object, which saves all positions as an piecewise
        function of time.

        Parameters
        ----------
        filename : string
            .gcode filename, e.g. filename = "test.gcode"

        """

        
        ### set default Values for Machine
        #                G1            M203          M204                  M205
        #               = [[X,Y,Z,E,F  ],[X, Y, Z, E ],[P,   R,   S,   T   ],[X, Y, Z, E ]]
        self.defaults   = [[0,0,0,0,800],[60,60,60,35],[2000,2000,2000,3000],[10,10,10,10]]
        
        self.axisnum    = ["X","Y","Z","E"] #convention used for numerating machine axis
        
        #TIMETABLE
        #dimensions     =  t  u       v       w       q        
        #piecewise def  =  [t,[a1,d1],[a2,d2],[a3,d3],[a4,d4]]
        self.timetable  = [[0,[0,  0],[0,  0],[0,  0],[0,  0]]]

        ################################################################


        self.filename   =   filename
        self.state      =   self.read_GCODE_from_file()     #generate the state array
        self.build_segment_timing()                         #generate the timetable


    def calc_JD_velocity(self,v1,v2):
        """
        Calculates junction deviation velocity with 2 velocity vectors.
        
        Parameters
        ----------
        v1,v2 : float arrays, [1x3]
            3D velocity vectors in xyz base, e.g. v1 = [2.3, 1.2, 0] 

        Returns
        ----------
        float arrays, [[1x3],[1x3]]
            velocity vectors for junction where the norm equals the JD-velocity
        
        Reference
        ----------
        https://onehossshay.wordpress.com/2011/09/24/improving_grbl_cornering_algorithm/

        """
        ### Junction deviation settings
        JD_delta    = 0.01
        JD_acc      = 200 #hardcoded acceleration, to be taken from the state vector, needs restructuring of function #todo1
        JD_minAngle = 18
        JD_maxAngle = 180-18

        #convert [v_x,v_y,v_z,v_e] to [v_x,v_y,v_z] for moving axis only
        v1_mov = v1[0:3]
        v2_mov = v2[0:3]
        #print("Movement velocities: ",v1_mov,v2_mov) #debug
        


        if v1_mov != [] and v2_mov != []:
            JD_cos_theta = (np.dot(-v1_mov,v2_mov)/(np.linalg.norm(v1_mov)*np.linalg.norm(v2_mov))) #cos of theta
            if JD_cos_theta < 1: #catch numerical errors where cos theta is slightly larger one, being an issue with sine conversion
                JD_sin_theta_half = np.sqrt((1 - JD_cos_theta)  /2)
            else:
                JD_sin_theta_half = 0

            #theta represents the small angle between velocity vectors
            #print("theta: ", np.arcsin(JD_sin_theta_half)*2*180/np.pi) #debug

            if JD_sin_theta_half < np.sin(JD_maxAngle*np.pi/(2*180)):       #if angle smaller than max
                if JD_sin_theta_half > np.sin(JD_minAngle*np.pi/(2*180)):   #and larger than min, apply JD
                    JD_Radius = JD_delta * JD_sin_theta_half / (1-JD_sin_theta_half)
                    JD_velocity_scalar = np.sqrt(JD_acc*JD_Radius)
                    #print(JD_velocity_scalar) #debug

                    #scale velocity vectors to calculated JD velocity
                    JD_velocity_vector1 = JD_velocity_scalar * np.asarray(v1) / np.linalg.norm(v1_mov)
                    JD_velocity_vector2 = JD_velocity_scalar * np.asarray(v2) / np.linalg.norm(v2_mov)
                    return [JD_velocity_vector1.tolist(),JD_velocity_vector2.tolist()]
                else:       #angle smaller than min angle, stop completely
                    #print("Angle too Sharp, stopping completely..") #debug
                    return [[0,0,0,0],[0,0,0,0]]
            else:           #angle larger than max angle, full speed pass
                #print("angle too dull, full speed, no JD..") #debug
                v2 = np.linalg.norm(v1_mov)*(v2/np.linalg.norm(v2_mov)) #set junction speed to exit speed
                return [v1,v2]
        else:
            print("no velocity vector received")

    def GCODE_line_dissector(self,line):
        """
        Dissects single Gcode lines into array following convention
        M203 for max axis speed
        M204,P for printing acceleration (R,S,T not yet supported)
        M205, axis Jerk (not yet supported)
            #todo2: fix end of file issue where last input is ignored
        Parameters
        ----------
        line : string
            single Gcode line

        Returns
        ----------
        float array
            array with   G1            M203          M204                  M205
                        [[X,Y,Z,E,F  ],[X, Y, Z, E ],[P,   R,   S,   T   ],[X, Y, Z, E ]]
        """
        def value_getter(line,all_params):
            line = line[:line.find(";")]            #remove comments
            all_params_return = []
            for param_group,i in zip(all_params,range(len(all_params))):
                group_array = []
                if(line.find(param_group[0])!=-1):  #get statement group
                    for param,i in zip(param_group[1],range(len(param_group[1]))):
                        if(line.find(param)!=-1):   #get parameters
                            posA=line.find(param)+len(param)
                            posE=line[posA:].find(" ")+posA
                            if(posE > posA):
                                group_array.insert(i, float(line[posA: posE]))
                            else:
                                group_array.insert(i, float(line[posA:]))
                        else:
                            group_array.insert(i,"None")
                else:
                    group_array.insert(i,"None")
                all_params_return.insert(i,group_array)
            return all_params_return



        G1_params   = ["G1",  ["X","Y","Z","E","F"]]    #G1   params convention
        M203_params = ["M203",["X","Y","Z","E"]]        #M203 params convention
        M204_params = ["M204",["P","R","S","T"]]        #M204 params convention
        M205_params = ["M205",["X","Y","Z","E"]]        #M205 params convention

        all_params  = [G1_params] + [M203_params] + [M204_params] + [M205_params]
        output      = value_getter(line,all_params)
        return output

    def stateUpdater(self,old,new):
        full = []
        for groupOld,groupNew in zip(old,new):
            if groupNew != ["None"]:
                param = []
                for paramOld,paramNew in zip(groupOld,groupNew):
                    if paramNew == "None":
                        param.append(paramOld)
                    else:
                        param.append(paramNew)
                full.append(param)
            else:
                full.append(groupOld)
        #print("State = ",full)
        return full


    def read_GCODE_from_file(self):
        """
        read gcode from .gcode file and fill in a state vector
        
        Parameters
        ----------
        none - hint: gcode file name is set in constructor

        Returns
        ----------
        array with   G1            M203          M204                  M205
                    [[X,Y,Z,E,F  ],[X, Y, Z, E ],[P,   R,   S,   T   ],[X, Y, Z, E ]]
            state vector
        """
        file_gcode  = open(self.filename)
        state       = [self.stateUpdater(self.defaults,[["None"],["None"],["None"]])]
        for line in file_gcode:
            #print("\n-------------- NEW GCODE LINE -------------- \n",line)
            newState = self.stateUpdater(state[-1],self.GCODE_line_dissector(line))
            if state[-1] != newState:
                state.append(newState)
        return state



    def time_calc(self,t0,s,vA,vE,vM,a):
        """
        calculate the times where the piecewise velocity function changes definition
           ________            
          /        \      |     /\          
         /          \     |    /  \     
        /            \    |   /    \        
        t0,t1,    t2,t3   |  t0,t1,t3
        automatically change from trapezoidal to triangular velocity profile if there isn't 
        enough time for the machine to accelerate to maximum velocity

        !!New special Case for only acceleration moves without deceleration

        Parameters
        ----------
        t0  :   float
            start time
        s   :   float
            distance
        vA  :   float  
            velocity at t0 (begin)
        vE  :   float  
            velocity at t3 (end)
        vM  :   float  
            velocity between t1 & t2
        a   :   float  
            acceleration

        Returns
        ----------
        float array [1x4] or [1x3]
            [t0,t1,t2,t3] or [t0,t1,t3] as defined above
        """
        
        def calc_t1():
            return ((a*t0 - vA + vM )/a)

        def calc_t2():
            #print(a,vM) #debug
            return ((2*t0*vM + 2*s)*a + vA*vA - 2*vA*vM + vE*vE)/(2*a*vM)
        
        def calc_t3():
            return (2*vM*vM + (2*a*t0 - 2*vA - 2*vE)*vM + 2*s*a + vA*vA + vE*vE)/(2*a*vM)

        #special cases for short acceleration time, vZ not calculated here (yet, likely not needed)
        #max velocity never reached
        def Scalc_t1():
            return (a*t0 - vA + (np.sqrt(4*s*a + 2*vA*vA + 2*vE*vE))/2 )/a

        def Scalc_t3():
            return (a*t0 - vA +  np.sqrt(4*s*a + 2*vA*vA + 2*vE*vE) - vE)/a

        #special case for very short travel distance without deceleration
        #end velocity never reached
        def S2calc_t1():
            #print("a:",a,"vA:",vA,"s:",s,"t0",t0)
            return (a*t0 - vA + np.sqrt(2*s*a + vA*vA))/(a)

        #abs Values
        vA = abs(vA)
        vE = abs(vE)
        vM = abs(vM)
        s  = abs(s)
        a  = abs(a)
        #print("starting Velocity", vA) #debug

        t1 = calc_t1()
        t2 = calc_t2()
        if t2>t1:
            return [t0,t1,t2,calc_t3()] #standard case
        else:
            t1 = Scalc_t1()
            t3 = Scalc_t3()
            if t1<t3 and t0<t1: #tri case  
                return [t0,t1,t3]
            else: #small single case
                return [t0,S2calc_t1()]


    def build_segment_velocity(self,state0,state1):
        """
        Create the artificial maximum Velocity Vector between two states
        considering max speeds of all axis
        
        Parameters
        ----------
        state0,state1
            state vectors with all required information
            array with   G1            M203          M204                  M205
                        [[X,Y,Z,E,F  ],[X, Y, Z, E ],[P,   R,   S,   T   ],[X, Y, Z, E ]]
                          0,1,2,3,4
        
        Returns
        ----------
        float array [1x4]
            [v_x,v_y,v_z,v_e] as target max speed per axis
            
        """
        def proportionals():
            #calculate proportional velocity coefficients
                        #x                          y                         z                         e
            distances = [state1[0][0]-state0[0][0], state1[0][1]-state0[0][1],state1[0][2]-state0[0][2],state1[0][3]-state0[0][3]]
            
            travel_distance = np.linalg.norm(distances[:3]) #just physical travel no extrusion
            if travel_distance > 0:
                propor = [] #x+y+z=1, e any
                for ax in distances:
                    propor.append(ax/travel_distance)
                
                return propor
            #else:
                #print("no travel move between: ",state0," and ",state1) #handle extrusion only moves here #todo3
        
        def axis_velocity(prop):
            if prop != None:
                ax_vel = np.asarray(prop) * (state1[0][4]/60)
                #check if no axis is overspeeding
                scale = 1
                for vel,i in zip(ax_vel,range(0,4)):
                    if vel > state1[1][i]:
                        #print("Too Fast") #handle overspeed here
                        if (scale > (state1[1][i] / vel)):
                            scale = (state1[1][i] / vel)  #calc scaling for all speeds
                            #print(scale)
                ax_vel=scale*ax_vel #scale so no overspeeding occurs
                return ax_vel


        prop = proportionals() #calc proportionals
        v_prop = axis_velocity(prop) #calc axis speeds
        
        return v_prop

    def build_segment_timing(self):
        """
        This function builds the whole timetable from the state array.
        timetable array as defined in __init__ 
        #dimensions     =  t  u       v       w       q        
        #piecewise def  = [t,[a1,d1],[a2,d2],[a3,d3],[a4,d4]]

        !CURRENTLY NOT SUPPORTED:
            !non travel extrusions
            !check for max acceleration per axis, only accepts global acceleration values
            !edge case handling for end of file condition, see todo2

        """
        def calc_t1(t0,vA,vM,a):
            return ((a*t0 + abs(vA - vM))/a)


        v00 = [0,0,0,0] #starting velocity
        t_curr = 0 #current time
        v0 = None
        v2 = None
        state_i     =   self.state[0]
        state_i1    =   self.state[0+1]
        for i in range(len(self.state)):
            #relevant move is state i to state i+1
            #v00 is starting velocity of the segment
            #v0  is the target velocity of the move
            #v1  is the junction speed, so ending velocity of the segment
            #v2  is the target velocity of the next segment, needed for JD calculation

            #define states as local vars
            #print("###############",i) #debug

            if i+2 < len(self.state):
                if not(v2 is None):
                    state_i     =   self.state[i]
                    state_i1    =   self.state[i+1]

                state_i2    =   self.state[i+2]
            elif i+1 < len(self.state):
                state_i     =   self.state[i]
                state_i1    =   self.state[i+1]
                state_i2    =   self.state[0]
            elif i < len(self.state):
                state_i     =   self.state[i]
                state_i1    =   self.state[0]
                state_i2    =   self.state[0]

            v0 = self.build_segment_velocity(state_i,state_i1)
            v2 = self.build_segment_velocity(state_i1,state_i2)
        
            

            #print("V0: ", v0, "V2: ",v2) #debug

            if not (v0 is None) and not (v2 is None):
                move_JD_vel = self.calc_JD_velocity(v0,v2)
                v1 = move_JD_vel[0]
                #print(v1) #debug
                
                #flag value for never reaching target speeds
                Sv00 = None

                #search largest t1 as the pacemaker for the upcoming travel move
                t1 = 0
                for axis in range(0,4):
                    #distance    = state_i1[0][axis]-state_i[0][axis]
                    vA = v00[axis]
                    vM = v0[axis]
                    t_temp      = calc_t1(t_curr,vA,vM,abs(state_i[2][0]/60)) #todo3 special case 2 here
                    #print(t_temp) #debug
                    if t1 < t_temp: t1 = t_temp; slow_ax = axis
                    #if t1<t_curr: print("ALARM ", t1 , " is smaller than ", t_curr) #debug
                
                #print("T current: ",t_curr,"\t T1: ", t1, "\t SlowAx:", self.axisnum[slow_ax]) #debug

                #time calculations only for the slowest t1
                distance    = state_i1[0][slow_ax]-state_i[0][slow_ax]
                times       = self.time_calc(t_curr,distance,v00[slow_ax],v1[slow_ax],v0[slow_ax],state_i[2][0]/60)
                #print("Times: ", times) #debug

                timetable_seg = [] #single timetable segment

                #build timetable segment
                if len(times) == 4: #if trapezoidal shape
                    ###########ACCELERATING
                    segm = [] #single function segment
                    interval    = times[1]-times[0]
                    #print("(trapz seg, acc) Interval size: ", interval) #debug
                    if interval > 0:
                        for ax in range(0,4):
                            delta_v     = v0[ax]-v00[ax]
                            acc         = delta_v/interval #accel
                            segm.append([v00[ax],acc])
                        full_segm=[times[0]]
                        full_segm.extend(segm) #add all axis segments with time together
                        timetable_seg.extend([full_segm]) #add segment to timetable

                    ###########CONSTANT VELOCITY
                    segm = [] #single function segment
                    for ax in range(0,4):
                        segm.append([v0[ax],0])
                    full_segm=[times[1]]
                    full_segm.extend(segm) #add all axis segments with time together
                    timetable_seg.extend([full_segm]) #add segment to timetable

                    ###########DECELERATING
                    segm = [] #single function segment
                    interval    = times[3]-times[2]
                    #print("(trapz seg dec) Interval size: ", interval) #debug
                    if interval > 0:
                        for ax in range(0,4):
                            delta_v     = v1[ax] - v0[ax]
                            acc         = delta_v/interval #decel
                            segm.append([v0[ax],acc])
                        full_segm=[times[2]]
                        full_segm.extend(segm) #add all axis segments with time together
                        timetable_seg.extend([full_segm]) #add segment to timetable

                elif len(times) == 3: #if triangle shape
                    ###########ACCELERATING
                    segm = [] #single function segment
                    interval    = times[1]-times[0]
                    print("(tri seg acc) Interval size: ", interval) #debug
                    if interval > 0:
                        for ax in range(0,4):
                            delta_v     = v0[ax]-v00[ax]
                            acc         = delta_v/interval #accel tri
                            segm.append([v00[ax],acc])
                        full_segm=[times[0]]
                        full_segm.extend(segm) #add all axis segments with time together
                        timetable_seg.extend([full_segm]) #add segment to timetable             

                    ###########DECELERATING
                    segm = [] #single function segment
                    interval    = times[2]-times[1]
                    print("(tri seg dec) Interval size: ", interval) #debug
                    if interval > 0:
                        for ax in range(0,4):
                            delta_v     = v1[ax] - v0[ax]
                            acc         = delta_v/interval #decel tri
                            segm.append([v0[ax],acc])
                        full_segm=[times[1]]
                        full_segm.extend(segm) #add all axis segments with time together
                        timetable_seg.extend([full_segm]) #add segment to timetable

                elif len(times) ==2: #if only acceleration
                    ###########ACCELERATING WIP
                    segm = [] #single function segment
                    interval    = times[1]-times[0]
                    #print(v0/np.linalg.norm(v0[:3])*interval*(state_i[2][0]/60)) #debug
                    #print("small: ", interval) #debug
                    if interval > 0:
                        Sv00         = [0,0,0,0]    
                        for ax in range(0,4):
                            #delta_v     = (v0[ax]/np.linalg.norm(v0[:3]))*interval*(state_i[2][0]/60) #sieht nur kompliziert aus
                            #acc_old     = delta_v/interval #accel singl
                            acc         = (v0[ax]/np.linalg.norm(v0[:3]))*(state_i[2][0]/60)

                            Sv00[ax]    = v00[ax]+acc*interval
                            #print(acc) #debug
                            segm.append([v00[ax],acc])
                        full_segm=[times[0]]
                        full_segm.extend(segm) #add all axis segments with time together
                        timetable_seg.extend([full_segm]) #add segment to timetable           

                self.timetable.extend(timetable_seg) #add move segments to full timetable
                #print(timetable_seg) #debug
                #update for next cycle
                t_curr = times[-1] #starting time is end time of last move
                if Sv00 == None:
                    v00 = move_JD_vel[1] #starting velocity is JD velocity of last move in direction of next move
                else:
                    v00 = Sv00
            else:
                print("no segment added",v0,v2) #debug
        #print("times: ", times) #debug
        self.timetable.extend([[times[-1],[0,  0],[0,  0],[0,  0],[0,  0]]]) #add the ending time where all moves are completed




    def createVelocityVector(self,state0,state1):
        """ ##############OLD#################
        Create the artificial maximum Velocity Vector between two states
        considering max speeds of all axis
        
        Parameters
        ----------
        state0,state1
            state vectors with all required information
            array with   G1            M203          M204                  M205
                        [[X,Y,Z,E,F  ],[X, Y, Z, E ],[P,   R,   S,   T   ],[X, Y, Z, E ]]
                          0,1,2,3,4
        
        Returns
        ----------
        float array [1x4]
            [v_x,v_y,v_z,v_e] as target max speed per axis
            
        """
        #init return var
        velocity = []

        #calc artificial travel time (these are not real travel times, since the ramp is ignored here)
        travel_distance = np.linalg.norm([state1[0][0]-state0[0][0], state1[0][1]-state0[0][1],state1[0][2]-state0[0][2]])
        travel_time     = travel_distance / (state1[0][4]/60)
        
        print("State0: ", state0)
        print("State1: ", state1)
        #check if speed limits are followed
        if(travel_distance != 0):
            for axis in range(0,4): 
                ax_max_speed = (state1[0][axis]-state0[0][axis])/travel_time
                if state1[1][axis]   <   ax_max_speed: #check if the artificial travel speed is higher than the permitted (M203)
                    print("too fast alarm")
                    #raise ValueError() #handle the downscaled speed >>>>>>>>>>HERE<<<<<<<<<<<<<< todo
                else:
                    #print("i.O.")
                    velocity.append(ax_max_speed)
                    #print("Max Speed axis: ",ax_max_speed)

        #print("Speed vector: ", velocity)
        return velocity

    
    def JD_test(self):
        for i in range(len(self.state)-2):
            #v0 = self.createVelocityVector(self.state[i],self.state[i+1])
            #v1 = self.createVelocityVector(self.state[i+1],self.state[i+2])
            #print(v0)
            #print(self.calc_JD_velocity(v0,v1))
            self.build_segment_velocity(self.state[i],self.state[i+1])


    #def build_timetable(self,state):

        
    def get_values(self,t):
        """
        This function is to read velocity values from the timetable at any point in time.

        Parameters
        ----------
        t   :   float
            point in time in s 

        Returns
        ----------
        float array [1x4]
            velocites as [v_x,v_y,v_z,v_e]
        """
        t_temp = 0
        i=0

        while t_temp < t:
            i += 1
            t_temp = self.timetable[i][0]
        segment         = i-1
        segment_time    = t-self.timetable[segment][0]
        #print(segment,t,segment_time) #debug
        #print(self.timetable[segment]) #debug
        vel = []
        for ax in range(1,5):
            vel.append(self.timetable[segment][ax][0] + self.timetable[segment][ax][1] * segment_time)

        return vel

    def write_timetable_to_file(self,fname="timetable.csv"):
        """
        This is to write the generated timetable to a file for inspection or further use.

        Parameters
        ----------
        fname   :   string (optional)
            filename for the timetable file

        """
        file = open(fname,"w")
        for segm in self.timetable:
            file.write(str(segm))
            file.write("\n")
        file.close()
    
    def get_duration(self):
        """
        This is to quickly calculate the duration of all movements

        Returns
        ----------
        float
            time it takes all moves to complete
        """
        return self.timetable[-1][0]

    def distance_check(self,t):
        """
        Calculate the traveled distance of all axes for a given point in time.
        Use this to check the travel algorithms for accuracy.
        Calculates the analytical integral of the function segments.

        Parameters
        ----------
        t   :   float
            point in time

        Returns
        ----------
        float array [1x4]
            [x,y,z,e] all distances travelled at t 
        """
        distance    = [0,0,0,0]
        t_beg       = 0
        t_end       = 0
        i           = 0

        if t > self.get_duration():         #if t is too large, adjust t to all moves
            t = self.get_duration()

        while t > t_beg and t != t_end:
            
            t_beg   = t_end                 #set beginning to end of last
            t_end   = self.timetable[i+1][0]  #get next end timing
            #print("TIME: ",t_beg,t_end) #debug
            if t > t_beg and t <= t_end:
                t_end = t                   #if in active interval, set end time to current time

            delt_t  = t_end-t_beg           #calc interval time
            #print(delt_t)
            if delt_t > 0:
                for ax in range(1,4):
                    b   =   self.timetable[i][ax][0]
                    m   =   self.timetable[i][ax][1]
                    #print(self.axisnum[ax-1],": ",b,"\t",m)#debug
                    distance[ax-1] += delt_t*(b+(m*delt_t)/2)
                    
                    add = delt_t*(b+(m*delt_t)/2)
                    #print(add)
            

            i      += 1
        return distance
        
    
    def write_state_to_file(self,fname="state_vector.csv"):
        """
        This is to write the state vector to a file for debugging.

        Parameters
        ----------
        fname   :   string (optional)
            filename for the timetable file

        """
        file = open(fname,"w")
        for state in self.state:
            file.write(str(state))
            file.write("\n")
        file.close()

    def continuity_checker(self):
        """
        Test function to check for continuity errors in the Timetable, which are expected due to junction deviation
        """
        t_beg = 0
        t_end = 0
        error = [0,0,0,0]
        for i in range(len(self.timetable)-1):
            t_beg   = t_end                 #set beginning to end of last
            t_end   = self.timetable[i+1][0]
            delt_t  = t_end-t_beg

            for ax in range(1,4):
                b   =   self.timetable[i][ax][0]
                m   =   self.timetable[i][ax][1] #f=mx+b
                error[ax]   +=   abs(self.timetable[i+1][ax][0] - (b + m*delt_t))
        print("continuity error: ", error)
