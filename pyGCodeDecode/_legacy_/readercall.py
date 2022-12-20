from reader import gcodeTrajectory
import matplotlib.pyplot as plt
import numpy as np

obj = gcodeTrajectory("test.gcode")
obj.write_timetable_to_file()
obj.write_state_to_file()
end_time = obj.get_duration()
obj.distance_check(120)
print("(readercall.py) end time is: ", end_time)

x= np.linspace(0,end_time,5000)
#x= np.linspace(20,35,500)
u = []
v = []
w = []
q = []
abs         = []
x_travel    = []
y_travel    = []

for xx in x:
    u.append(obj.get_values(xx)[0])
    v.append(obj.get_values(xx)[1])
    w.append(obj.get_values(xx)[2])
    q.append(obj.get_values(xx)[3])
    abs.append(np.linalg.norm([u[-1],v[-1],w[-1]]))
    distance = obj.distance_check(xx)
    x_travel.append(distance[0])
    #y_travel.append(distance[1])

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(x,u,x,v,x,w,x,q) #,marker="x"
ax1.plot(x,abs, linestyle = "--",linewidth=2)
ax2.plot(x,x_travel,linewidth = 2,color="c")
#ax2.plot(x,y_travel,linewidth = 2,color="b")

plt.show()
plt.savefig("velplot.png",dpi=500)
