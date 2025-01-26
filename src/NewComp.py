from vex import * 

brain=Brain()
controller_1 = Controller(PRIMARY)
left_drive_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
left_drive_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)
left_drive_motor_c = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)
right_drive_motor_a = Motor(Ports.PORT15, GearSetting.RATIO_6_1, False)
right_drive_motor_b = Motor(Ports.PORT16, GearSetting.RATIO_6_1, False)
right_drive_motor_c = Motor(Ports.PORT17, GearSetting.RATIO_6_1, True)

right_drive = MotorGroup(right_drive_motor_a, right_drive_motor_b, right_drive_motor_c)
left_drive = MotorGroup(left_drive_motor_a, left_drive_motor_b, left_drive_motor_c)
lbr = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)
claw2 = Motor(Ports.PORT7, GearSetting.RATIO_36_1, True)
intake = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
lift = Motor(Ports.PORT12, GearSetting.RATIO_6_1, True)
claw = DigitalOut(brain.three_wire_port.a)
claw3 = DigitalOut(brain.three_wire_port.b)
clr = Optical(Ports.PORT10)

lb = Rotation(Ports.PORT20, True)
wait(30,MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

def pre_autonomous():
    # actions to do when the program starts
    brain.screen.clear_screen()
    brain.screen.print("pre auton code")
    wait(1, SECONDS)

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here
    circumference=10.21
    ratio = 48 / 36 * circumference
    
    lift.set_velocity(600,PERCENT)
    right_drive.set_velocity(50,PERCENT)
    left_drive.set_velocity(50, PERCENT)
    
    
    #starting on right side, block out if we're not
    #right_drive.spin_for(REVERSE, 2.1, TURNS, wait=False)
    #left_drive.spin_for(REVERSE, 2.1, TURNS, wait=True)
    
    #starting on left side, block out if we're not
    #right_drive.spin_for(FORWARD, 2.1, TURNS, wait=False)
    #left_drive.spin_for(FORWARD, 2.1, TURNS, wait=True)

        #turn code: keep on regardless of side ? 
    right_drive.spin_for(REVERSE, 15/ratio, TURNS, wait=False)
    left_drive.spin_for(REVERSE, 15/ratio, TURNS, wait=True)
    claw.set(True)
    claw3.set(True)
    right_drive.spin_for(REVERSE, 2/ratio, TURNS, wait=False)
    left_drive.spin_for(REVERSE, 2/ratio, TURNS, wait=True)
    lift.spin_for(FORWARD, 5, TURNS)
    global ct
    ct = 1
    
    wait(1,SECONDS)
    sleep(100,MSEC)

def user_control():
    brain.screen.clear_screen()
    #count variables for toggles
    global count
    count = 0
    global count2 
    count2 = 0
    global count3 
    count3 = 0
    global count5 
    count5 = 0
    global lbt
    lbt = 0
    global lbt2 
    lbt2 = 0
    global clk 
    clk = 0
    global clkc
    clkc = 0
    

    #initialize motors correctly
    lbr.set_velocity(100,PERCENT)
    lbr.set_max_torque(1000,PERCENT)
    lbr.set_stopping(HOLD)
    intake.set_stopping(COAST)
    intake.set_velocity(100,PERCENT)
    lift.set_stopping(COAST)
    lift.set_velocity(100,PERCENT)
    '''
    global ct
    ct = 0
    if ct == 1: 
        claw.set(True)
        claw3.set(True)
    else:
        claw.set(False)
        claw3.set(False)
    '''
    claw.set(False)
    claw3.set(False)
    left_drive.set_velocity(100,PERCENT)
    right_drive.set_velocity(100,PERCENT)
    global liftspeed
    liftspeed = 100
    global clawspeed
    clawspeed = 100
    lbr.set_position(0, DEGREES)
    lb.set_position(0,DEGREES)
    #constants for controller stick smoothing math
    pi = 3.14159265359
    d2r = pi / 180
    b = 0.0314159265359
    c = 3.14159265359

    #stick deadzone 
    deadzone = 2 
    #velocity multiplier (speed fraction)
    velocity_multiplier = 1

    while True:
        lbr.set_velocity(400,PERCENT)
        claw2.set_velocity(clawspeed, PERCENT)
        lbr.set_stopping(HOLD)

        if (clk % 10 == 0):
            clkc +=1
        
        if controller_1.buttonR1.pressing():
            claw.set(True)
            claw3.set(True)
            count5 = 1

        if controller_1.buttonL1.pressing():
            claw.set(False)
            claw3.set(False)
            count5 = 0

        if controller_1.buttonA.pressing():
            count = 1

        if controller_1.buttonB.pressing():
            count = 0
            count3 = 0

        if count == 0 and count3 == 0:
            lift.stop()

        if count == 1:
            lift.spin(FORWARD)

        
        if controller_1.buttonLeft.pressing(): 
            lbt = 0
            lbr.stop() 
            clkc = 0 
        if controller_1.buttonLeft.pressing() and clkc < 1: 
            lb.set_position(0, DEGREES) 
        

        #lady brown macros
        if controller_1.buttonRight.pressing() and clkc > 1:
            lbt += 1
            clkc = 0
            
        
        if (lbt == 1): 
            lbr.spin(FORWARD)
            lbt = 1
            if lb.position() > 90:
                lbr.stop()
                lbt = 2
        if lbt == 2: 
            if not (controller_1.buttonDown.pressing()) and not (controller_1.buttonUp.pressing()):
                lbr.stop()
        if lbt == 3: 
            lift.set_velocity(50,PERCENT)
            lift.spin_for(REVERSE, 90, DEGREES, wait=True)
            lift.set_velocity(100,PERCENT)
            lbt = 4

        if lbt == 4: 
            lbr.spin(FORWARD)
            if lb.position() > 720: 
                lbr.stop() 
                lbt = 5
        
        if lbt == 5 and not controller_1.buttonUp.pressing() and not controller_1.buttonDown.pressing():
            lbr.stop()
        if lbt == 6: 
            lbr.spin(REVERSE)
            if lb.position() < 1: 
                lbr.stop()
                lbt = 0
        
        
            

        if not controller_1.buttonLeft.pressing() and not controller_1.buttonRight.pressing() and not controller_1.buttonR1.pressing() and not controller_1.buttonL1.pressing():
            claw2.stop()

        if count5 == 1:
            claw2.set_stopping(HOLD)

        if count5 ==0: 
            claw2.set_stopping(COAST)

        if controller_1.buttonX.pressing():
            count3 = 1

        if count3== 0 and count == 0:
            lift.stop()

        if count3 == 1:
            lift.spin(REVERSE)
        
        if controller_1.buttonR2.pressing(): 
            count2 = 1
        if controller_1.buttonL2.pressing():
            count2 = 2 
        if controller_1.buttonY.pressing():
            count2 = 0 
        if count2 == 1: 
            intake.spin(FORWARD)
        if count2 == 2: 
            intake.spin(REVERSE)
        if count2 == 0: 
            intake.stop()
            

        if controller_1.buttonDown.pressing():
            lbr.spin(REVERSE)

        if controller_1.buttonUp.pressing():
            lbr.spin(FORWARD)

        if not controller_1.buttonUp.pressing() and not controller_1.buttonDown.pressing() and (lbt == 0) and (lbt2 == 0):
            lbr.stop()

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

        #wip color sort 
        '''
        if clr.hue() <= 20: 
            print("RED!!! ")
            

        if clr.hue() >= 195: 
            #print("BLUE!!!")
            lift.stop()
            print("STOPPED!")
            if clkc > 1: 
                clkc = 0
        if clkc < 1: 
            count = 1
            print("RESTARTED!") 
        ''' 
        
        #print values for debugging
        '''
        print('turn: ')
        print(turn)
        print('throttle: ')
        print(throttle)
        print('left: ')
        print(left)
        print('right: ')
        print(right)
        '''
        '''
        print('Left Temp: ')
        print(left_drive_motor_a.temperature())
        print(left_drive_motor_b.temperature())
        print('Right Temp: ')
        print(right_drive.temperature())
        print(right_drive_motor_a.temperature())
        '''
        #print("LB Angle: ")
        #print(lb.position())
        #print("LBT: ")
        #print(lbt)
        #print(clr.hue())
        clk +=1
        wait(20,MSEC)

# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()