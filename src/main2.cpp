#include "main.h"

pros::MotorGroup left({-2, -3, 4}, pros::MotorGearset::blue);
	pros::MotorGroup right({15, 16, -17}, pros::MotorGearset::blue);
	pros::Motor intake(11, pros::MotorGearset::green);
	pros::Motor lift(12, pros::MotorGearset::blue);
	pros::Motor lbr(13, pros::MotorGearset::green);
	pros::adi::DigitalOut claw('A', false);
	pros::adi::DigitalOut claw2('B', false);
	pros::adi::DigitalOut doinker('C', false);
	pros::Controller master (pros::E_CONTROLLER_MASTER);
	int liftcount = 0; 
	int ct = 0; 
	int auton = 0;
	int lbt = 0;
	int clkc = 0; 




/**
 * A callback function for LLEMU's center button.
 *
 * When this callback is fired, it will toggle line 2 of the LCD text between
 * "I was pressed!" and nothing.
 */
void on_center_button() {
	static bool pressed = false;
	pressed = !pressed;
	if (pressed) {
		pros::lcd::set_text(2, "I was pressed!");
	} else {
		pros::lcd::clear_line(2);
	}
}

/**
 * Runs initialization code. This occurs as soon as the program is started.
 *
 * All other competition modes are blocked by initialize; it is recommended
 * to keep execution time for this mode under a few seconds.
 */
void initialize() {
	pros::lcd::initialize();
	pros::lcd::set_text(1, "Hello PROS User!");

	pros::lcd::register_btn1_cb(on_center_button);
}



void lady_brown() { 
	while(true) { 
		if (master.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_RIGHT)) { 
			lbt ++; 
		}
		if (lbt == 1) { 
			lbr.move_absolute(150, 200);
			while (!((lbr.get_position() < 148) && (lbr.get_position() > 152))) { 
				pros::delay(2);
			}
			lbt = 2;
		}
		if (lbt == 3) { 
			lift.move_absolute(-90, 300);
			while (!((lift.get_position() > -92) && (lift.get_position() < -88))) { 
				pros::delay(2);
			}
			lift.brake();
			lbr.move_absolute(790, 200);
			while (!((lbr.get_position() > 800) && (lbr.get_position() < 780))) { 
				pros::delay(2);
			lbt = 4;
			}	
		}
		if ((lbt == 4) && (liftcount == 3)) {
			lift.move(127);
		}
		if (lbt == 5) { 
			lbr.move_absolute(0, 200);
			while (!((lbr.get_position() > 5) && (lbr.get_position() < -2))) { 
				pros::delay(2);
			}
		}

		if (master.get_digital(pros::E_CONTROLLER_DIGITAL_UP)) { 
			lbr.move(127); 
		}
		if (master.get_digital(pros::E_CONTROLLER_DIGITAL_DOWN)) { 
			lbr.move(-127);
		}
		if (!(master.get_digital(pros::E_CONTROLLER_DIGITAL_DOWN)) && !(master.get_digital(pros::E_CONTROLLER_DIGITAL_UP)) && (lbt != 1) && (lbt != 3) && (lbt != 5)) { 
			lbr.brake();
		}

		
		
		
	}
}


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
void competition_initialize() {
	pros::screen::erase();
	pros::screen::draw_rect(0,0,240,120);
	pros::screen::fill_rect(0,0,240,120);
	pros::screen_touch_status_s_t status;
	while (auton == 0) {
		//status = pros::screen_touch_status();
		if ((status.x < 240) && (status.y < 120)) {
			auton = 1;
		}
		if ((status.x > 240) && (status.y < 120)) {
			auton = 2; 
		}
	}
	

}

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
void autonomous() {
	
}

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
void opcontrol() {
	pros::Controller master(pros::E_CONTROLLER_MASTER);
	pros::MotorGroup left_mg({1, -2, 3});    // Creates a motor group with forwards ports 1 & 3 and reversed port 2
	pros::MotorGroup right_mg({-4, 5, -6});  // Creates a motor group with forwards port 5 and reversed ports 4 & 6


	while (true) {
		pros::lcd::print(0, "%d %d %d", (pros::lcd::read_buttons() & LCD_BTN_LEFT) >> 2,
		                 (pros::lcd::read_buttons() & LCD_BTN_CENTER) >> 1,
		                 (pros::lcd::read_buttons() & LCD_BTN_RIGHT) >> 0);  // Prints status of the emulated screen LCDs

		// Arcade control scheme
		int dir = master.get_analog(ANALOG_LEFT_Y);    // Gets amount forward/backward from left joystick
		int turn = master.get_analog(ANALOG_RIGHT_X);  // Gets the turn left/right from right joystick
		left_mg.move(dir - turn);                      // Sets left motor voltage
		right_mg.move(dir + turn);                     // Sets right motor voltage
		pros::delay(20);                               // Run for 20 ms then update
	}
}