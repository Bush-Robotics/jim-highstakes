#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
intake = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
lift = Motor(Ports.PORT12, GearSetting.RATIO_6_1, True)
claw = DigitalOut(brain.three_wire_port.a)
left_drive_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
left_drive_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
left_drive = MotorGroup(left_drive_motor_a, left_drive_motor_b)
right_drive_motor_a = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
right_drive_motor_b = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
right_drive = MotorGroup(right_drive_motor_a, right_drive_motor_b)


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
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *
myVariable = 0
# Begin project code
count = 0
count2 = 0
def when_started1():
    global count
    count = 0
    global count2 
    count2 = 0
    global count3 
    count3 = 0
    global myVariable
    #drivetrain.set_drive_velocity(100,PERCENT)
    #drivetrain.set_turn_velocity(100,PERCENT)
    intake.set_stopping(COAST)
    intake.set_velocity(100,PERCENT)
    #clamp.set_velocity(100,PERCENT)
    #clamp.set_stopping(HOLD)
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
    while True:
        print("Left Drive: ")
        print(left_drive.temperature())
        print("Right Drive: ")
        print(right_drive.temperature())
        if controller_1.buttonL1.pressing():
            claw.set(True)
        if controller_1.buttonR1.pressing():
            claw.set(False)
        if controller_1.buttonA.pressing():
            count = 1
        if controller_1.buttonB.pressing():
            count = 0
            count3 = 0
        if count == 0 and count3 == 0:
            lift.stop()
        if count == 1:
            lift.spin(FORWARD)

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
            lift.set_velocity(25,PERCENT)
        if controller_1.buttonUp.pressing():
            lift.set_velocity(100,PERCENT)
        speed = (abs(controller_1.axis3.position())^2)
        turnspeed = (abs(controller_1.axis1.position())^2)
        if controller_1.axis3.position() > 10:
            #drivetrain.set_drive_velocity((controller_1.axis3)^2)
            #drivetrain.drive(REVERSE)
            left_drive.set_velocity(speed,PERCENT)
            right_drive.set_velocity(speed,PERCENT)
            left_drive.spin(FORWARD)
            right_drive.spin(FORWARD)
        if controller_1.axis3.position() < -10:
            #drivetrain.set_drive_velocity((controller_1.axis3)^2)
            #drivetrain.drive(FORWARD)left_drive.set_velocity(speed,PERCENT)
            right_drive.set_velocity(speed,PERCENT)
            left_drive.set_velocity(speed,PERCENT)
            left_drive.spin(REVERSE)
            right_drive.spin(REVERSE)
        if controller_1.axis1.position() > 10:
            #drivetrain.set_turn_velocity((controller_1.axis1)^2)
            #drivetrain.turn(RIGHT)
            right_drive.set_velocity(turnspeed,PERCENT)
            left_drive.set_velocity(turnspeed,PERCENT)
            left_drive.spin(FORWARD)
            right_drive.spin(REVERSE)
        if controller_1.axis1.position() < -10:
            #drivetrain.set_turn_velocity((controller_1.axis1)^2)
            #drivetrain.turn(LEFT)
            right_drive.set_velocity(turnspeed,PERCENT)
            left_drive.set_velocity(turnspeed,PERCENT)
            left_drive.spin(REVERSE)
            right_drive.spin(FORWARD)
        if controller_1.axis3.position() < 10 and controller_1.axis3.position()> -10 and controller_1.axis1.position() <10 and controller_1.axis1.position() > -10:
            #drivetrain.stop()
            left_drive.stop()
            right_drive.stop()
        #if controller_1.buttonR2.pressing():
            #intake.spin(REVERSE)
        #if controller_1.buttonL1.pressing():
            #clamp.spin(FORWARD)
        #if not controller_1.buttonR1.pressing() and not controller_1.buttonL1.pressing():
            #clamp.stop()
        #if controller_1.buttonR1.pressing():
            #clamp.spin(REVERSE)
        #if controller_1.buttonL2.pressing():
            #intake.spin(FORWARD)
        #if not controller_1.buttonL2.pressing() and not controller_1.buttonR2.pressing():
            #intake.stop()
        #if controller_1.buttonA.pressing():
            #lift.spin(FORWARD)
        #if controller_1.buttonB.pressing():
            #lift.spin(REVERSE)
        #if not controller_1.buttonA.pressing() and not controller_1.buttonB.pressing():
            #lift.stop()
        
        
        wait(5,MSEC)
when_started1()