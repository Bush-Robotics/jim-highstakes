
# Library imports
from vex import *
import math

WHEEL_CIRC = 4.5 * 2 * math.pi

brain = Brain()
ctrl = Controller()
motor_r=Motor(Ports.PORT1)
motor_l=Motor(Ports.PORT10)
motor_t=Rotation(Ports.PORT12)

# set to 90 degrees
global_rot=math.pi/2

wheelbase=10
x_global=0
y_global=0
prev_theta=0
local_arc_rad=0
avg_theta=0




def x_from_polar(r,theta):
    x = r * math.cos(theta)
    return float(x)
def y_from_polar(r,theta):
    y = r * math.sin(theta)
    return float(y)

def r_from_cartisian(x,y):
    r = math.sqrt(x**2 + y**2) 
    return float(r)
def r_from_cartesian(x,y):
    theta = math.atan2(y,x)
    return float(theta)
    
def user_control():
    arc_x=0
    arc_y=0
    global global_rot, x_global,y_global,averagetheta,local_arc_rad,avg_theta
    motor_t.reset_position()
    motor_r.reset_position()
    motor_l.reset_position()
    while True:
        ypos1=-(motor_l.position()/360)*WHEEL_CIRC 
        ypos12=(motor_r.position()/360)*WHEEL_CIRC 
        xpos1 =-(motor_t.position()/360)*WHEEL_CIRC 
        wait(10)
        ypos2=-(motor_l.position()/360)*WHEEL_CIRC
        ypos22=(motor_r.position()/360)*WHEEL_CIRC 
        xpos2 =-(motor_t.position()/360)*WHEEL_CIRC 

        deltay1=ypos2-ypos1
        deltay2=ypos22-ypos12
        deltax=xpos2-xpos1


        delta_theta=((deltay1-deltay2)/wheelbase)
        previoustheta=global_rot
        global_rot+=delta_theta

        
        #this does not work for going straight
        if delta_theta==0:
            y_global+=2*((deltay1/0.0000000000001)+4.5)*(math.sin(delta_theta/2))
        # arcs
        elif (deltay1>0 and deltay2>0) or (deltay1<0 and deltay2<0):
            arc_x=2*((deltax/delta_theta)+6.25)*(math.sin(delta_theta/2))
            arc_y=2*((deltay1/delta_theta)+4.5)*(math.sin(delta_theta/2))

            
            avg_theta=previoustheta+(delta_theta/2)

            local_arc_rad=r_from_cartisian(arc_x,arc_y)
            
            # Rotating to match global pos
            local_theta=r_from_cartesian(arc_x,arc_y)
            local_theta=local_theta-avg_theta
            
            x_global+=x_from_polar(local_arc_rad,local_theta)
            y_global+=y_from_polar(local_arc_rad,local_theta)
        print(x_global,x_global)

user_control()
