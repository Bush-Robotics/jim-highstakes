from vex import *

brain=Brain()
controller_1 = Controller(PRIMARY)
left_drive_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
left_drive_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_6_1, False)
right_drive_motor_a = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)
right_drive_motor_b = Motor(Ports.PORT5, GearSetting.RATIO_6_1, True)
right_drive = MotorGroup(right_drive_motor_a, right_drive_motor_b)
left_drive = MotorGroup(left_drive_motor_a, left_drive_motor_b)
doinker = Motor(Ports.PORT7, GearSetting.RATIO_36_1, False)
claw2 = Motor(Ports.PORT13, GearSetting.RATIO_36_1, True)
intake = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
lift = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)
claw = DigitalOut(brain.three_wire_port.a)



def when_started1():
    #control points
    #graph: https://www.desmos.com/calculator/vigixi45si
    right_drive.set_stopping(COAST)
    left_drive.set_stopping(COAST)
    global deadzone
    deadzone = 10
    x1 = 0
    y1 = 0
    x2 = 70
    y2 = 0
    x3 = 30 
    y3 = 100
    x4 = 100 
    y4 = 100
    t= 0
    x5 = []
    y5 = []

    #velocity multiplier - speed percent or ratio (0-1)
    global velocity_multiplier
    velocity_multiplier = 1

    while True:
        global deadzone
        #assign initial stick values
        ithrottle = (controller_1.axis3.position() / 100)
        iturn = (controller_1.axis1.position() / 100)
        global throttle
        global turn 

        #apply bezier curve to stick inputs (redundant)
        throttle = ((1-ithrottle)**3 * x1 + 3*(1-ithrottle)**2*ithrottle * x2 + 3*(1-ithrottle)*ithrottle**2 * x3 + ithrottle**3 * x4)
        turn = ((1-iturn)**3 * x1 + 3*(1-iturn)**2*iturn * x2 + 3*(1-iturn)*iturn**2 * x3 + iturn**3 * x4)

        #apply bezier curve to stick inputs if outside of deadzone
        if ithrottle > deadzone: 
            global throttle
            throttle = ((1-ithrottle)**3 * x1 + 3*(1-ithrottle)**2*ithrottle * x2 + 3*(1-ithrottle)*ithrottle**2 * x3 + ithrottle**3 * x4)
        if ithrottle < -deadzone: 
            global throttle
            throttle = -1 * ((1-ithrottle)**3 * x1 + 3*(1-ithrottle)**2*ithrottle * x2 + 3*(1-ithrottle)*ithrottle**2 * x3 + ithrottle**3 * x4)
        if iturn > deadzone: 
            global turn
            turn = ((1-iturn)**3 * x1 + 3*(1-iturn)**2*iturn * x2 + 3*(1-iturn)*iturn**2 * x3 + iturn**3 * x4)
        if iturn < -deadzone: 
             global turn 
             turn = -1 * ((1-iturn)**3 * x1 + 3*(1-iturn)**2*iturn * x2 + 3*(1-iturn)*iturn**2 * x3 + iturn**3 * x4)

        #assign remapped stick positions to motor speeds
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

        
        #y = ((1-t)**3 * y1 + 3*(1-t)**2*t * y2 + 3*(1-t)*t**2 * y3 + t**3 * y4)





