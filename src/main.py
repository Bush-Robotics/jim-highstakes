
# Library imports
from vex import *
import math

brain = Brain()
cntrl = Controller()
motor1=Motor(Ports.PORT1)
motor2=Motor(Ports.PORT10)
odony=Rotation(Ports.PORT12)
wheelcirc = 13
robotxposition=0
globaltheta=math.pi/2
wheelbase=10
xglobal=0
yglobal=0





def polar_to_cartesian(r,theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y
def cartesian_to_polar(x,y):
    r = math.sqrt(x**2 + y**2) 
    theta = math.atan2(y, x)
    return r, theta
    
def user_control():

    global globaltheta, xglobal,yglobal,counter
    odony.reset_position()
    motor1.reset_position()
    motor2.reset_position()
    while True:
        counter+=1
        ypos1=(motor2.position()/360)*wheelcirc 
        ypos12=-(motor1.position()/360)*wheelcirc 
        xpos1 =(odony.position()/360)*wheelcirc 
        wait(10)
        ypos2=(motor2.position()/360)*wheelcirc
        ypos22=-(motor1.position()/360)*wheelcirc 
        xpos2 =(odony.position()/360)*wheelcirc 

        deltay1=ypos2-ypos1
        deltay2=ypos22-ypos12
        deltax=xpos2-xpos1


        deltatheta=((deltay2-deltay1)/wheelbase)
        globaltheta+=deltatheta

        #everything above this works - hooray!

        #this is where it gets weird, the code is supposed to calculate the radius of the arc and use that in the math but it is wildly wrong
        
        try:
            radius = (deltay2/deltatheta)+(5)
        except ZeroDivisionError:
            radius = 0



        #sorry these variable names are horrid, this is part of the x,y local positioning vector
        try:
            vectordeltax=2*math.sin(globaltheta/2)*(deltax/deltatheta)-7
        except ZeroDivisionError:
            vectordeltax=0

        #this is the part that turns it into polar and converts it into the global scope and then turns it back into cartesian
        polar_theta_delta=float(cartesian_to_polar(vectordeltax,radius)[1])-(globaltheta+(deltatheta/2))
        polar_radius_delta=float(cartesian_to_polar(vectordeltax,radius)[0])
        xglobal+=float(polar_to_cartesian(polar_radius_delta,polar_theta_delta)[0])
        yglobal+=float(polar_to_cartesian(polar_radius_delta,polar_theta_delta)[1])
        
        

        print(radius, deltay2,deltatheta)

user_control()