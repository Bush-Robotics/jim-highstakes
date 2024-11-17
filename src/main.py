#region VEXcode Generated Robot Configuration
import math
from vex import *


# Brain should be defined by default
brain=Brain()
controller_1 = Controller(PRIMARY)
left_drive_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
left_drive_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_6_1, False)
right_drive_motor_a = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)
right_drive_motor_b = Motor(Ports.PORT5, GearSetting.RATIO_6_1, True)
right_drive = MotorGroup(right_drive_motor_a, right_drive_motor_b)
left_drive = MotorGroup(left_drive_motor_a, left_drive_motor_b)
# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------


# Begin project code
def when_started1():
    #constants for controller stick smoothing math
    pi = 3.14159265359
    d2r = pi / 180
    b = 0.0314159265359
    c = 3.14159265359

    #stick deadzone 
    deadzone = 10 
    #velocity multiplier (speed fraction)
    velocity_multiplier = .75

    while True:
        #assign stick position to initial variables
        ithrottle = controller_1.axis3.position()
        iturn = controller_1.axis1.position()
        global throttle 
        global turn 
        #throwaway to bind variables
        throttle = ithrottle
        turn = iturn

        #smooth throttle and turn curve based on stick position
        if ithrottle > deadzone: 
            global throttle
            throttle = 50 * math.cos(b*ithrottle - c)+50
        if ithrottle < -deadzone: 
            global throttle
            throttle = -1 * (50 * math.cos(b*ithrottle - c)+50)
        if iturn > deadzone: 
            global turn
            turn = 50 * math.cos(b*iturn - c)+50
        if iturn < -deadzone: 
             global turn 
             turn = -1 * (50 * math.cos(b*iturn - c)+50)

        #assign variables to motor speeds
        global throttle
        global turn
        global left
        global right
        left = throttle + turn
        right = throttle - turn 

        #turn in place code 
        if ithrottle < deadzone and ithrottle > -deadzone: 
            throttle = 0
            left = turn
            right = -turn
            right_drive.set_velocity(velocity_multiplier*right, PERCENT)
            left_drive.set_velocity(velocity_multiplier*left, PERCENT)
            right_drive.spin(FORWARD)
            left_drive.spin(FORWARD)
        else:
        #set motor velocities if not turning in place
            right_drive.set_velocity(velocity_multiplier*right, PERCENT)
            left_drive.set_velocity(velocity_multiplier*left, PERCENT)

        #spin motors if stick is out of deadzone
        if throttle > deadzone or throttle < -deadzone: 
            right_drive.spin(FORWARD)
            left_drive.spin(FORWARD)
        #stop motors when no inputs or in deadzone
        if throttle < deadzone and throttle > -deadzone and turn < deadzone and turn > -deadzone:
            right_drive.stop()
            left_drive.stop()
        
        #print values for debugging
        print('turn: ')
        print(turn)
        print('throttle: ')
        print(throttle)
        print('left: ')
        print(left)
        print('right: ')
        print(right)

when_started1()

            
