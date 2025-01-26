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
intake = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
lift = Motor(Ports.PORT12, GearSetting.RATIO_6_1, True)
claw = DigitalOut(brain.three_wire_port.a)
claw2 = DigitalOut(brain.three_wire_port.b)
clr = Optical(Ports.PORT10)

lb = Rotation(Ports.PORT20, True)
wait(30,MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")
liftcount = 0 
def lady_brown(): 
    global lbt, lbr, clkc, lift, liftcount
    while True: 
        if controller_1.buttonLeft.pressing(): 
            lbt = 0
            lbr.stop() 
            clkc = 0 
        if controller_1.buttonLeft.pressing() and clkc < 1: 
            lb.set_position(0, DEGREES) 
        if controller_1.buttonRight.pressing() and clkc > 1:
            lbt += 1
            clkc = 0
        if (lbt == 1): 
            lbr.spin_to_position(150, DEGREES, wait = True)
            lbt = 2
        if lbt == 3: 
            lift.set_velocity(50,PERCENT)
            liftcount = 0
            lift.spin_for(REVERSE, 90,DEGREES)
            lift.stop()
            lift.set_velocity(100, PERCENT)
            lbr.spin_to_position(790, DEGREES, wait = True)
            lbt = 4
        if lbt == 4 and liftcount == 3: 
            lift.spin(FORWARD)
        if lbt == 5: 
            lbr.spin(REVERSE)
            if lbr.position() < 5: 
                lbr.stop() 
                lbt = 0 

        #print(lbr.position())

        if controller_1.buttonDown.pressing():
            lbr.spin(REVERSE)

        if controller_1.buttonUp.pressing():
            lbr.spin(FORWARD)

        if not controller_1.buttonUp.pressing() and not controller_1.buttonDown.pressing() and lbt != 1 and lbt != 3 and lbt != 5:
            lbr.stop()
        print(lbt)
        '''
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
        '''

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
    claw2.set(True)
    right_drive.spin_for(REVERSE, 2/ratio, TURNS, wait=False)
    left_drive.spin_for(REVERSE, 2/ratio, TURNS, wait=True)
    lift.spin_for(FORWARD, 5, TURNS)
    ct = 1
    
    wait(1,SECONDS)
    sleep(100,MSEC)

def user_control():
    brain.screen.clear_screen()
    global lbt, lbr, clkc
    #liftcountvariables for toggles
    liftcount= 0
    intakecount = 0
    count3 = 0
    lbt = 0
    lbt2 = 0
    clk = 0
    clkc = 0
    

    #initialize motors correctly
    lbr.set_velocity(100,PERCENT)
    lbr.set_max_torque(1000,PERCENT)
    intake.set_stopping(COAST)
    intake.set_velocity(100,PERCENT)
    lift.set_stopping(COAST)
    lift.set_velocity(100,PERCENT)
    '''
    ct = 0
    if ct == 1: 
        claw.set(True)
        claw2.set(True)
    else:
        claw.set(False)
        claw2.set(False)
    '''
    claw.set(False)
    claw2.set(False)
    left_drive.set_velocity(100,PERCENT)
    right_drive.set_velocity(100,PERCENT)
    liftspeed = 100
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

    #call lb function on a separate thread 
    lbr.set_position(0,DEGREES)
    ladybrown = Thread(lady_brown)
    while True:
        lbr.set_velocity(100,PERCENT)
        lbr.set_stopping(HOLD)

        if (clk % 10 == 0):
            clkc +=1
        
        if controller_1.buttonR1.pressing():
            claw.set(True)
            claw2.set(True)
    
        if controller_1.buttonL1.pressing():
            claw.set(False)
            claw2.set(False)

        if controller_1.buttonA.pressing():
            liftcount= 1

        if controller_1.buttonB.pressing():
            liftcount= 0
            count3 = 0

        if liftcount== 0 and count3 == 0 and lbt != 3:
            lift.stop()

        if liftcount== 1 and lbt != 3:
            lift.spin(FORWARD)

        

        

        if controller_1.buttonX.pressing():
            count3 = 1

        if count3== 0 and liftcount== 0 and lbt !=3:
            lift.stop()

        if count3 == 1 and lbt != 3:
            lift.spin(REVERSE)
        
        if controller_1.buttonR2.pressing(): 
            intakecount = 1
        if controller_1.buttonL2.pressing():
            intakecount = 2 
        if controller_1.buttonY.pressing():
            intakecount = 0 
        if intakecount == 1: 
            intake.spin(FORWARD)
        if intakecount == 2: 
            intake.spin(REVERSE)
        if intakecount == 0: 
            intake.stop()
            

        

        #assign stick position to initial variables
        ithrottle = controller_1.axis3.position()
        iturn = controller_1.axis1.position()
        #throwaway to bind variables
        throttle = ithrottle
        turn = iturn

        #smooth throttle and turn curve based on stick position
        if ithrottle > deadzone: 
            throttle = 50 * math.cos(b*ithrottle - c)+50
        if ithrottle < -deadzone: 
            throttle = -1 * (50 * math.cos(b*ithrottle - c)+50)
        if iturn > deadzone: 
            turn = 50 * math.cos(b*iturn - c)+50
        if iturn < -deadzone: 
             turn = -1 * (50 * math.cos(b*iturn - c)+50)

        #assign variables to motor speeds
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
            liftcount= 1
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