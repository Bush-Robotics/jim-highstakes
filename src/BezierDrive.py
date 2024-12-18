from vex import *

brain=Brain()
controller_1 = Controller(PRIMARY)
left_drive_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
left_drive_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)
left_drive_motor_c = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)

right_drive_motor_a = Motor(Ports.PORT15, GearSetting.RATIO_6_1, False)
right_drive_motor_b = Motor(Ports.PORT16, GearSetting.RATIO_6_1, False)
right_drive_motor_c = Motor(Ports.PORT17, GearSetting.RATIO_6_1, False)

right_drive = MotorGroup(right_drive_motor_a, right_drive_motor_b)
left_drive = MotorGroup(left_drive_motor_a, left_drive_motor_b)
doinker = Motor(Ports.PORT7, GearSetting.RATIO_36_1, False)
claw2 = Motor(Ports.PORT13, GearSetting.RATIO_36_1, True)
intake = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
lift = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)
claw = DigitalOut(brain.three_wire_port.a)



def when_started1():
    #control points
    #graph: https://www.desmos.com/calculator/0a5farialg 
    right_drive.set_stopping(COAST)
    left_drive.set_stopping(COAST)
    ithrottle = 0
    iturn = 0
    global deadzone
    deadzone = 0.1
    x1 = 0
    y1 = 0
    x2 = 70
    y2 = 0
    x3 = 30 
    y3 = 100
    x4 = 100 
    y4 = 100
    t= 0

    #velocity multiplier - speed percent or ratio (0-1)
    global velocity_multiplier
    velocity_multiplier = 1

    while True:
        #assign initial stick values
        
        global throttle
        global turn 

        #apply bezier curve to stick inputs (redundant)
        throttle = ((1-ithrottle)**3 * x1 + 3*(1-ithrottle)**2*ithrottle * x2 + 3*(1-ithrottle)*ithrottle**2 * x3 + ithrottle**3 * x4)
        turn = ((1-iturn)**3 * x1 + 3*(1-iturn)**2*iturn * x2 + 3*(1-iturn)*iturn**2 * x3 + iturn**3 * x4)

        #divide stick values by 100 so 0<t<1
        ithrottle = (controller_1.axis3.position() / 100)
        iturn = (controller_1.axis1.position() / 100)
        #apply bezier curve to stick inputs if outside of deadzone
        if ithrottle > deadzone: 
            global throttle
            throttle = ((1-ithrottle)**3 * x1 + 3*(1-ithrottle)**2*ithrottle * x2 + 3*(1-ithrottle)*ithrottle**2 * x3 + ithrottle**3 * x4)
        if ithrottle < -deadzone: 
            global throttle
            ithrottle = -1 * ithrottle
            throttle = -1 * ((1-ithrottle)**3 * x1 + 3*(1-ithrottle)**2*ithrottle * x2 + 3*(1-ithrottle)*ithrottle**2 * x3 + ithrottle**3 * x4)
        if iturn > deadzone and (ithrottle > deadzone or ithrottle < -deadzone): 
            global turn
            turn = ((1-iturn)**3 * x1 + 3*(1-iturn)**2*iturn * x2 + 3*(1-iturn)*iturn**2 * x3 + iturn**3 * x4)
        if iturn < -deadzone and (ithrottle > deadzone or ithrottle < -deadzone): 
            global turn 
            iturn = -1 * iturn
            turn = -1 * ((1-iturn)**3 * x1 + 3*(1-iturn)**2*iturn * x2 + 3*(1-iturn)*iturn**2 * x3 + iturn**3 * x4)
            print(turn)

        
        #assign remapped stick positions to motor speeds
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
        if throttle > deadzone:
            right_drive.spin(FORWARD)
            left_drive.spin(FORWARD)
        if throttle < -deadzone:
            right_drive.spin(FORWARD)
            left_drive.spin(FORWARD)
        #stop motors when no inputs or in deadzone
        if throttle < deadzone and throttle > -deadzone and turn < deadzone and turn > -deadzone:
            right_drive.stop()
            left_drive.stop()
        #print values for debugging
        
        print('turn: ')
        print(iturn)
        print('throttle: ')
        print(ithrottle)
        print('left: ')
        print(left)
        print('right: ')
        print(right)
        wait(30,MSEC)
        
        

when_started1()

        
        #y = ((1-t)**3 * y1 + 3*(1-t)**2*t * y2 + 3*(1-t)*t**2 * y3 + t**3 * y4)





