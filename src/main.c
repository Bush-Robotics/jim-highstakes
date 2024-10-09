#include "main.h"
#include "pros/misc.h"
#include "pros/motors.h"
#include "utils.h"

// ports
#define LIFT 12
#define INTAKE 11
#define LEFT_DRIVE_A 1
#define LEFT_DRIVE_B 3
#define RIGHT_DRIVE_A 4
#define RIGHT_DRIVE_B 5

// gear ratios
#define INTAKE_RATIO E_MOTOR_GEARSET_18
#define LIFT_RATIO E_MOTOR_GEARSET_06
#define DRIVE_RATIO E_MOTOR_GEARSET_18

#define DEADZONE 0.25
const double DEADZONE_SQUARED = DEADZONE * DEADZONE;
// count1 and count3
int lift_direction = 0; // -1 reverse, 0 stopped, 1, forward
// count2
bool intake = false;

void on_center_button() {
	printf("hello world!\n");
}

/**
 * Runs inijtialization code. This occurs as soon as the program is started.
 *
 * All other competition modes are blocked by initialize; it is recommended
 * to keep execution time for this mode under a few seconds.
 */
void initialize() {}


/**
 * Runs while the robot is in the disabled state of Field Management System or
 * the VEX Competition Switch, following either autonomous or opcontrol. When
 * the robot is enabled, this task will exit.
 */
void disabled() {}

/**
 * Runs after initialize(), and before autonomous when connected to the Field
 * Management System or the VEX Competition Switch. This is intended for
 * competition-specific initialization routines, such as an autonomous selector
 * on the LCD.
 *
 * This task will exit when the robot is enabled and autonomous or opcontrol
 * starts.
 */
void competition_initialize() {}

/**
 * Runs the user autonomous code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the autonomous
 * mode. Alternatively, this function may be called in initialize or opcontrol
 * for non-competition testing purposes.
 *
 * If the robot is disabled or communications is lost, the autonomous task
 * will be stopped. Re-enabling the robot will restart the task, not re-start it
 * from where it left off.
 */
void autonomous() {}

/**
 * Runs the operator control code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the operator
 * control mode.
 *
 * If no competition control is connected, this function will run immediately
 * following initialize().
 *
 * If the robot is disabled or communications is lost, the
 * operator control task will be stopped. Re-enabling the robot will restart the
 * task, not resume it from where it left off.
 */

vec2 drive_input() {
	vec2 input = (vec2){stick_axis(ANALOG_RIGHT_X), stick_axis(ANALOG_LEFT_Y)};
	if (vec2_len_squared(input) < DEADZONE_SQUARED) {
		return (vec2){0.0, 0.0}; // default to zero when stick is not in deadzone
	}
	return input;
}

void drive_train_left(double speed) {
	motor_move_velocity(LEFT_DRIVE_A, speed);
	motor_move_velocity(LEFT_DRIVE_B, speed);
}
void drive_train_right(double speed) {
	motor_move_velocity(RIGHT_DRIVE_A, speed);
	motor_move_velocity(RIGHT_DRIVE_B, speed);
}

void handle_drive(vec2 input) {
	drive_train_right((input.x + input.y) * DRIVE_RATIO);
	drive_train_left((-input.x + input.y) * -DRIVE_RATIO);
}

void opcontrol() {
	while (true) {
		// handle lift
		if ((is_pressed(DIGITAL_A) || is_pressed(DIGITAL_B))) {
			lift_direction = is_pressed(DIGITAL_A) - is_pressed(DIGITAL_B);
		}
		motor_move_velocity(LIFT, lift_direction * LIFT_RATIO);

		if (is_just_pressed(DIGITAL_L1)) {
			intake = !intake; // toggle intake when L1 is pressed
		}
		if (intake) {
			motor_move_velocity(INTAKE, INTAKE_RATIO);
		} else {
			motor_brake(INTAKE);
		}

		handle_drive(drive_input());

		delay(2);
	}
}
