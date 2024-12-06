
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
previoustheta=0
localradius=0
avgtheta=0




def Xfrompolar(r,theta):
    x = r * math.cos(theta)
    return float(x)
def Yfrompolar(r,theta):
    y = r * math.sin(theta)
    return float(y)

def Rfromcartesian(x,y):
    r = math.sqrt(x**2 + y**2) 
    return float(r)
def Thetafromcartesian(x,y):
    theta = math.atan2(y,x)
    return float(theta)
    
def user_control():
    xvector=0
    yvector=0
    global globaltheta, xglobal,yglobal,averagetheta,localradius,avgtheta
    odony.reset_position()
    motor1.reset_position()
    motor2.reset_position()
    while True:
        ypos1=-(motor2.position()/360)*wheelcirc 
        ypos12=(motor1.position()/360)*wheelcirc 
        xpos1 =-(odony.position()/360)*wheelcirc 
        wait(100)
        ypos2=-(motor2.position()/360)*wheelcirc
        ypos22=(motor1.position()/360)*wheelcirc 
        xpos2 =-(odony.position()/360)*wheelcirc 

        deltay1=ypos2-ypos1
        deltay2=ypos22-ypos12
        deltax=xpos2-xpos1


        deltatheta=((deltay1-deltay2)/wheelbase)
        previoustheta=globaltheta
        globaltheta+=deltatheta

        #everything above this works - hooray!

        #this actually works apparently lol
        try:
            radius = (deltay1/deltatheta)+(5)
        except ZeroDivisionError:
            radius = 0


        
        #this works for going straight
        if deltatheta==0:
            yglobal+=deltay1
        
        #rotations
        
        else:
            
            xvector=2*((deltax/deltatheta)+6.25)*(math.sin(deltatheta/2))
            yvector=2*((deltay1/deltatheta)+4.5)*(math.sin(deltatheta/2))

            
            avgtheta=previoustheta+(deltatheta/2)

            localradius=Rfromcartesian(xvector,yvector)
            localtheta=Thetafromcartesian(xvector,yvector)
            localtheta=localtheta-avgtheta
            xglobal+=Xfrompolar(localradius,localtheta)
            yglobal+=Yfrompolar(localradius,localtheta)
            

        
        print(xglobal,xglobal)


user_control()