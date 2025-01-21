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

lbMotor = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)
intake = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
lift = Motor(Ports.PORT12, GearSetting.RATIO_6_1, True)
claw = DigitalOut(brain.three_wire_port.a)
claw2 = DigitalOut(brain.three_wire_port.b)
lbRotation = Rotation(Ports.PORT20, True)
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
    circumference=10.21

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

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
    global lbCount
    lbCount = 0
    global clk 
    clk = 0
    global clkc
    clkc = 0
    

    #initialize motors correctly
    lbMotor.set_velocity(100,PERCENT)
    lbMotor.set_max_torque(1000,PERCENT)
    lbMotor.set_stopping(COAST)
    intake.set_stopping(COAST)
    intake.set_velocity(100,PERCENT)
    lift.set_stopping(COAST)
    lift.set_velocity(100,PERCENT)
    claw.set(False)
    claw2.set(False)
    left_drive.set_velocity(100,PERCENT)
    right_drive.set_velocity(100,PERCENT)
    global liftspeed
    liftspeed = 100
    lbMotor.set_position(0, DEGREES)
    lbRotation.set_position(0,DEGREES)
    lbMotor.set_velocity(100,PERCENT)
    lbMotor.set_stopping(HOLD)
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
        #count clock cycles 
        if (clk % 10 == 0):
            clkc +=1
        
        #toggle clamp 
        if controller_1.buttonR1.pressing():
            claw.set(True)
            claw2.set(True)

        if controller_1.buttonL1.pressing():
            claw.set(False)
            claw2.set(False)

        #toggle hooks/lift
        if controller_1.buttonA.pressing():
            count = 1
        if controller_1.buttonB.pressing():
            count = 0
        if controller_1.buttonX.pressing():
            count = 2

        if count == 1:
            lift.spin(FORWARD)
        if count == 2: 
            lift.spin(REVERSE)
        if count == 0:
            lift.stop()
            

        #reset lbRotation position with double click
        if controller_1.buttonLeft.pressing(): 
            lbCount = 0
            lbMotor.stop() 
            clkc = 0 
        if controller_1.buttonLeft.pressing() and clkc < 1: 
            lbRotation.set_position(0, DEGREES) 
        

        #lady brown control/macros
        if controller_1.buttonRight.pressing() and clkc > 1:
            lbCount += 1
            clkc = 0
        
        if (lbCount == 1): 
            lbMotor.spin(FORWARD)
            lbCount = 1
            if lbRotation.position() > 90:
                lbMotor.stop()
                lbCount = 2
        if lbCount == 2: 
            if not (controller_1.buttonDown.pressing()) and not (controller_1.buttonUp.pressing()):
                lbMotor.stop()
        if lbCount == 3: 
            lift.set_velocity(50,PERCENT)
            lift.spin_for(REVERSE, 90, DEGREES, wait=True)
            lift.set_velocity(100,PERCENT)
            lbCount = 4

        if lbCount == 4: 
            lbMotor.spin(FORWARD)
            if lbRotation.position() > 720: 
                lbMotor.stop() 
    
        if lbCount == 5: 
            lbMotor.spin(REVERSE)
            if lbRotation.position() < 1: 
                lbMotor.stop()
                lbCount = 0

        if controller_1.buttonDown.pressing():
            lbMotor.spin(REVERSE)

        if controller_1.buttonUp.pressing():
            lbMotor.spin(FORWARD)

        if not controller_1.buttonUp.pressing() and not controller_1.buttonDown.pressing() and (lbCount == 0):
            lbMotor.stop()
        
        #toggle front intake 
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
        print("lbRotation Angle: ")
        print(lbRotation.position())
        #print("lbCount: ")
        #print(lbCount)
        clk +=1
        wait(20,MSEC)

# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()