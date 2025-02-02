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
doinker = DigitalOut(brain.three_wire_port.c)
clr = Optical(Ports.PORT10)
timer = Timer()
lb = Rotation(Ports.PORT20, True)
wait(30,MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")
liftcount = 0 
objectDetected = False
ct = 0 
auton = 2
stopped = 0 

def colorsort(): 
    global clr, lift, liftcount, objectDetected
    clr.integration_time(9)
    clr.set_light(LedStateType.ON)
    clr.set_light(100)
    clr.set_light_power(100)
    print("STARTED!")
    while True: 
     #if objectDetected == False: 
            #print(clr.hue())
     #if clr.is_near_object():
        if clr.hue() < 20:
            wait(.5, SECONDS)
            liftcount=0
            objectDetected = True
            lift.stop()
            print("SPOTTED RED!!!!!!!!")
            '''wait(.2, SECONDS) 
            liftcount = 2 
            lift.stop() 
            wait(1, SECONDS) 
            liftcount = 1
            lift.spin(FORWARD)'''
        elif clr.hue()>=200:
             liftcount=0
             wait(.5, SECONDS)
             objectDetected = True
             print("SPOTTED BLUE !!!!!!!!")
             lift.stop()

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

def pre_autonomous():
    global auton, stopped
    stopped = 0
    # actions to do when the program starts
    brain.screen.clear_screen()
    brain.screen.print("pre auton code")
    wait(.1, SECONDS)
    brain.screen.draw_rectangle(0,0,240,120,Color.BLUE)
    brain.screen.draw_rectangle(240,0,240,120, Color.BLUE)
    brain.screen.draw_rectangle(0,120,240,120, Color.RED)
    brain.screen.draw_rectangle(240,120,240,120, Color.RED)
    while auton == 0: 
        if brain.screen.pressing():
            if brain.screen.x_position() < 240 and brain.screen.y_position() < 120: 
                print("pressed 1")
                auton = 1
            if brain.screen.x_position() > 240 and brain.screen.y_position() < 120: 
                print("pressed 2")
                auton = 2
            if brain.screen.x_position() < 240 and brain.screen.y_position() > 120: 
                print("pressed 3")
                auton = 3
            if brain.screen.x_position() > 240 and brain.screen.y_position() > 120: 
                print("pressed 4")
                auton = 4 
            controller_1.screen.clear_screen()
            controller_1.screen.print("auton: ")
            if auton == 1: 
                controller_1.screen.print("left side blue")
            if auton == 2: 
                controller_1.screen.print("right side blue")
            if auton == 3: 
                controller_1.screen.print("left side red")
            if auton == 4: 
                controller_1.screen.print("right side red")
        


def autonomous():
    global ct, auton, doinkcount, stopped
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    
    # place automonous code here
    circumference=10.21
    ratio = 48 / 36 * circumference
    intake.set_velocity(100,PERCENT)
    lift.set_velocity(600,PERCENT)
    right_drive.set_velocity(50,PERCENT)
    left_drive.set_velocity(50, PERCENT)

    right_drive_motor_a.set_position(0,DEGREES)
    left_drive_motor_a.set_stopping(COAST)
    left_drive_motor_b.set_stopping(COAST)
    left_drive_motor_c.set_stopping(COAST)
    right_drive_motor_a.set_stopping(COAST)
    right_drive_motor_b.set_stopping(COAST)
    right_drive_motor_c.set_stopping(COAST)

    
    if auton == 1: 
        #left side blue 
        right_drive.set_velocity(4.8, VOLT)
        left_drive.set_velocity(4.8, VOLT)
        right_drive.spin_for(REVERSE, 30/ratio, TURNS, wait=False)
        left_drive.spin_for(REVERSE, 30/ratio, TURNS, wait=True)
        right_drive.set_velocity(4.8, VOLT)
        left_drive.set_velocity(4.2, VOLT)
        right_drive.spin_for(REVERSE, 18/ratio, TURNS, wait=False)
        left_drive.spin_for(REVERSE, 18/ratio, TURNS, wait=True)
        right_drive.set_velocity(7.2, VOLT)
        left_drive.set_velocity(4.8, VOLT)
        right_drive.spin_for(REVERSE, 6/ratio, TURNS, wait=False)
        left_drive.spin_for(REVERSE, 6/ratio, TURNS, wait=True)
        claw.set(True)
        claw2.set(True)
        right_drive.spin_for(REVERSE, 10/ratio, TURNS, wait=False)
        left_drive.spin_for(REVERSE, 10/ratio, TURNS, wait=True)
        wait(.5,SECONDS)
        lift.spin(FORWARD)
        right_drive.spin_for(REVERSE, 6/ratio, TURNS, wait=False)
        left_drive.spin_for(FORWARD, 6/ratio, TURNS, wait=True)
        intake.spin(FORWARD)
        right_drive.spin_for(FORWARD, 40/ratio, TURNS, wait=False)
        left_drive.spin_for(FORWARD, 40/ratio, TURNS, wait=True)
        wait(2,SECONDS)
        lift.stop()
        lbr.spin_to_position(500, wait = True)
        right_drive.spin_for(REVERSE, 2/ratio, TURNS, wait=False)
        left_drive.spin_for(FORWARD, 2/ratio, TURNS, wait=True)
        left_drive.spin_for(REVERSE, 75/ratio, TURNS, wait= False)
        right_drive.spin_for(REVERSE, 75/ratio, TURNS, wait= True)


    if auton == 2: 
        #right side blue 

        
        '''left_drive_motor_a.spin(REVERSE, 6, VOLT)
        left_drive_motor_b.spin(REVERSE, 6, VOLT)
        left_drive_motor_c.spin(REVERSE, 6, VOLT)
        right_drive_motor_a.spin(REVERSE, 8, VOLT)
        right_drive_motor_b.spin(REVERSE, 8, VOLT)
        right_drive_motor_c.spin(REVERSE, 8, VOLT)
        while stopped == 0: 
            if right_drive_motor_a.position() < -850: 
                left_drive_motor_a.spin(REVERSE, 5.5, VOLT)
                left_drive_motor_b.spin(REVERSE, 5.5, VOLT)
                left_drive_motor_c.spin(REVERSE, 5.5, VOLT)
                right_drive_motor_a.spin(REVERSE, 8, VOLT)
                right_drive_motor_b.spin(REVERSE, 8, VOLT)
                right_drive_motor_c.spin(REVERSE, 8, VOLT)
            if right_drive_motor_a.position() < -1050: 
                claw.set(True)
                claw2.set(True)
            if right_drive_motor_a.position() < -1300: 
                right_drive.stop()
                left_drive.stop()
                left_drive.set_stopping(BRAKE)
                right_drive.set_stopping(BRAKE)
                stopped = 1
            else: 
                print(right_drive_motor_a.position())
        if stopped == 1: 
            right_drive_motor_a.reset_position()
            stopped = 2
        while stopped == 2:
            
            left_drive_motor_a.spin(REVERSE, 6, VOLT)
            left_drive_motor_b.spin(REVERSE, 6, VOLT)
            left_drive_motor_c.spin(REVERSE, 6, VOLT)
            right_drive_motor_a.spin(FORWARD, 8, VOLT)
            right_drive_motor_b.spin(FORWARD, 8, VOLT)
            right_drive_motor_c.spin(FORWARD, 8, VOLT)
            
            if right_drive_motor_a.position() >= 35:
                right_drive.stop()
                left_drive.stop()
                stopped = 2  
            else: 
                print(right_drive_motor_a.position())

            
        wait(2, SECONDS) 
        right_drive.stop()
        left_drive.stop()'''
        
        right_drive.spin_for(REVERSE, 35/ratio, TURNS, wait=False)
        left_drive.spin_for(REVERSE, 35/ratio, TURNS, wait=True)
        right_drive.set_velocity(30, PERCENT)
        left_drive.set_velocity(40, PERCENT)
        right_drive.spin_for(REVERSE, 17/ratio, TURNS, wait=False)
        left_drive.spin_for(REVERSE, 17/ratio, TURNS, wait=True)
        claw.set(True)
        claw2.set(True)
        right_drive.spin_for(REVERSE, 5/ratio, TURNS, wait=False)
        left_drive.spin_for(REVERSE, 5/ratio, TURNS, wait=True)
        wait(.5,SECONDS)
        lift.spin(FORWARD)
        right_drive.spin_for(FORWARD, 10/ratio, TURNS, wait=False)
        left_drive.spin_for(REVERSE, 10/ratio, TURNS, wait=True)
        intake.spin(FORWARD)
        right_drive.spin_for(FORWARD, 45/ratio, TURNS, wait=False)
        left_drive.spin_for(FORWARD, 45/ratio, TURNS, wait=True)
        wait(2,SECONDS)
        lbr.spin_to_position(500,DEGREES)
        right_drive.set_velocity(50, PERCENT)
        left_drive.set_velocity(50, PERCENT)
        right_drive.spin_for(REVERSE, 2/ratio, TURNS, wait=False)
        left_drive.spin_for(FORWARD, 2/ratio, TURNS, wait=True)
        right_drive.spin_for(REVERSE,75/ratio,TURNS, wait = False)
        left_drive.spin_for(REVERSE,75/ratio,TURNS, wait = False)

    

   
    ct = 1
    
    wait(1,SECONDS)
    sleep(100,MSEC)

def user_control():
    right_drive.set_stopping(COAST)
    left_drive.set_stopping(COAST)
    brain.screen.clear_screen()
    global lbt, lbr, clkc
    #liftcountvariables for toggles
    liftcount= 0
    intakecount = 0
    lbt = 0
    clk = 0
    clkc = 0
    doinkcount = 0
    last_timer = 0

    #initialize motors correctly
    lbr.set_velocity(100,PERCENT)
    lbr.set_max_torque(1000,PERCENT)
    intake.set_stopping(COAST)
    intake.set_velocity(100,PERCENT)
    lift.set_stopping(COAST)
    lift.set_velocity(100,PERCENT)


    if ct == 1: 
        claw.set(True)
        claw2.set(True)
    else:
        claw.set(False)
        claw2.set(False)

    
    #claw.set(False)
    #claw2.set(False)
    #claw.set(True)
    #claw2.set(True)
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
    #sortclr = Thread(colorsort)
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
            intakecount = 0

        if liftcount== 0 and lbt != 3:
            lift.stop()

        if liftcount== 1 and lbt != 3:
            lift.spin(FORWARD)



        if doinkcount == 0: 
            doinker.set(False)
        
        if doinkcount == 1: 
            doinker.set(True)
        
        if doinkcount == 2: 
            doinker.set(False) 
            doinkcount  = 0

        if controller_1.buttonY.pressing() and (brain.timer.time(SECONDS) - last_timer > .5): 
            last_timer = brain.timer.time(SECONDS)
            doinkcount += 1 
        
        

        if controller_1.buttonX.pressing():
            liftcount = 2

        if liftcount== 0 and lbt !=3:
            lift.stop()

        if liftcount == 2 and lbt != 3:
            lift.spin(REVERSE)
        
        if controller_1.buttonR2.pressing(): 
            intakecount = 1
        if controller_1.buttonL2.pressing():
            intakecount = 2 
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
            throttle = (50 * math.cos(b*ithrottle - c)+50) * 1 / 100
        if ithrottle < -deadzone: 
            throttle = -1 * (50 * math.cos(b*ithrottle - c)+50) * 1 / 100
        if iturn > deadzone: 
            turn = 50 * math.cos(b*iturn - c)+50 * 1 / 100
        if iturn < -deadzone: 
             turn = -1 * (50 * math.cos(b*iturn - c)+50) * 1 / 100

        #assign variables to motor speeds
        left = (throttle + turn) * 12 
        right = (throttle - turn) * 12 

        #turn in place code 
        '''if ithrottle < deadzone and ithrottle > -deadzone: 
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
            left_drive.set_velocity(velocity_multiplier*left, PERCENT)'''
        
        if ithrottle < deadzone and ithrottle > -deadzone: 
            throttle = 0 
            left = turn 
            right = -turn 
            left_drive_motor_a.spin(FORWARD, left, VOLT)
            left_drive_motor_b.spin(FORWARD, left, VOLT)
            left_drive_motor_c.spin(FORWARD, left, VOLT)
            right_drive_motor_a.spin(FORWARD, right, VOLT)
            right_drive_motor_b.spin(FORWARD, right, VOLT)
            right_drive_motor_c.spin(FORWARD, right, VOLT)


        #spin motors if stick is out of deadzone
        if throttle > deadzone or throttle < -deadzone: 
            left_drive_motor_a.spin(FORWARD, left, VOLT)
            left_drive_motor_b.spin(FORWARD, left, VOLT)
            left_drive_motor_c.spin(FORWARD, left, VOLT)
            right_drive_motor_a.spin(FORWARD, right, VOLT)
            right_drive_motor_b.spin(FORWARD, right, VOLT)
            right_drive_motor_c.spin(FORWARD, right, VOLT)
        #stop motors when no inputs or in deadzone  
        if throttle < deadzone and throttle > -deadzone and turn < deadzone and turn > -deadzone:
            right_drive.stop()
            left_drive.stop()

        clk +=1
        wait(20,MSEC)
        

# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()