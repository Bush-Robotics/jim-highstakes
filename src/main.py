#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
intake = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
lift = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)
claw = DigitalOut(brain.three_wire_port.a)
right_drive_motor_a = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)
right_drive_motor_b = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
right_drive = MotorGroup(right_drive_motor_a, right_drive_motor_b)
claw2 = Motor(Ports.PORT13, GearSetting.RATIO_36_1, True)
left_drive_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
left_drive_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_6_1, False)
left_drive = MotorGroup(left_drive_motor_a, left_drive_motor_b)
drivetrain = MotorGroup(left_drive_motor_a, left_drive_motor_b, right_drive_motor_a, right_drive_motor_b)
doinker = Motor(Ports.PORT7, GearSetting.RATIO_36_1, False)

# wait for rotation sensor to fully initialize
wait(30, MSEC)


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:
#	Author:
#	Created:
#	Configuration:
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code

def pre_autonomous():
    # actions to do when the program starts
    brain.screen.clear_screen()
    brain.screen.print("pre auton code")
    wait(1, SECONDS)
    

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here
    c=10.21
    claw2.set_velocity(500, PERCENT)
    claw2.set_max_torque(500,PERCENT)
    lift.set_velocity(600,PERCENT)
    right_drive.set_velocity(50,PERCENT)
    left_drive.set_velocity(50, PERCENT)
    #right_drive.spin_for(FORWARD, 19.5/10.21, TURNS, wait=False)
    #left_drive.spin_for(REVERSE, 19.5/10.21, TURNS, wait=True)
    claw.set(True)
    wait(50,MSEC)
    claw2.set_stopping(HOLD)
    claw2.spin(FORWARD)
    wait(1,SECONDS)
    claw2.stop()
    lift.spin(REVERSE)
    wait(3,SECONDS)
    lift.stop()
    
    #starting on right side, block out if we're not
    #right_drive.spin_for(REVERSE, 2.1, TURNS, wait=False)
    #left_drive.spin_for(REVERSE, 2.1, TURNS, wait=True)
    
    #starting on left side, block out if we're not
    #right_drive.spin_for(FORWARD, 2.1, TURNS, wait=False)
    #left_drive.spin_for(FORWARD, 2.1, TURNS, wait=True)

        #turn code: keep on regardless of side ? 
    right_drive.spin_for(REVERSE, 19.5/10.21, TURNS, wait=False)
    left_drive.spin_for(FORWARD, 19.5/10.21, TURNS, wait=True)
    
    wait(1,SECONDS)
    sleep(100,MSEC)



def user_control():
    brain.screen.clear_screen()
    # place driver control in this while loop
    global count
    count = 0
    global count2 
    count2 = 0
    global count3 
    count3 = 0
    global count5 
    count5 = 0
    global myVariable
    doinker.set_velocity(50,PERCENT)
    doinker.set_max_torque(50,PERCENT)
    doinker.set_stopping(COAST)
    intake.set_stopping(COAST)
    intake.set_velocity(100,PERCENT)
    lift.set_stopping(COAST)
    lift.set_velocity(100,PERCENT)
    claw.set(True)
    left_drive.set_velocity(100,PERCENT)
    right_drive.set_velocity(100,PERCENT)
    global speed 
    speed = 0
    global turnspeed
    turnspeed = 0
    global liftspeed
    liftspeed = 100
    global clawspeed
    clawspeed = 100
    claw2.set_velocity(75,PERCENT)
    while True:
        print("Left Drive Temp: ")
        print(left_drive.temperature())
        print("%")
        print("Right Drive Temp: ")
        print(right_drive.temperature())
        print("%")
        print("Axis 1: ")
        print(speed)
        print("Axis 3: ")
        print(turnspeed)
        claw2.set_velocity(clawspeed, PERCENT)
        if controller_1.buttonR1.pressing():
            claw.set(True)
            count5 = 1

        if controller_1.buttonL1.pressing():
            claw.set(False)
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
            claw2.spin(FORWARD)

        if controller_1.buttonRight.pressing():
            claw2.spin(REVERSE)

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
            count2 = 0

        if count2 == 0:
            intake.stop()

        if count2 == 1:
            intake.spin(REVERSE)

        if controller_1.buttonDown.pressing():
            doinker.spin(REVERSE)

        if controller_1.buttonUp.pressing():
            doinker.spin(FORWARD)

        if not controller_1.buttonUp.pressing() and not controller_1.buttonDown.pressing():
            doinker.stop()

        speed = 600*(abs(controller_1.axis3.position())^2)
        turnspeed = 600*(abs(controller_1.axis1.position())^2)

        if controller_1.axis1.position() > 20:
            left_drive.set_velocity(speed,PERCENT)
            right_drive.set_velocity(speed,PERCENT)
            left_drive.spin(FORWARD)
            right_drive.spin(FORWARD)

        if controller_1.axis1.position() < -20:
            right_drive.set_velocity(speed,PERCENT)
            left_drive.set_velocity(speed,PERCENT)
            left_drive.spin(REVERSE)
            right_drive.spin(REVERSE)

        if controller_1.axis3.position() > 20:
            right_drive.set_velocity(turnspeed,PERCENT)
            left_drive.set_velocity(turnspeed,PERCENT)
            left_drive.spin(FORWARD)
            right_drive.spin(REVERSE)

        if controller_1.axis3.position() < -20:
            right_drive.set_velocity(turnspeed,PERCENT)
            left_drive.set_velocity(turnspeed,PERCENT)
            left_drive.spin(REVERSE)
            right_drive.spin(FORWARD)

        if controller_1.axis3.position() < 20 and controller_1.axis3.position()> -20 and controller_1.axis1.position() <20 and controller_1.axis1.position() > -20:
            left_drive.stop()
            right_drive.stop()
        wait(20,MSEC)

# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()
