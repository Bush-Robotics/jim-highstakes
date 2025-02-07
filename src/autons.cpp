#include "main.h"

/////
// For installation, upgrading, documentations, and tutorials, check out our website!
// https://ez-robotics.github.io/EZ-Template/
/////

// These are out of 127
const int DRIVE_SPEED = 110;
const int TURN_SPEED = 90;
const int SWING_SPEED = 110;
void redsort() { 
  clr.set_integration_time(100);
  clr.set_led_pwm(100);
  while (true) {
    pros::screen::erase();
    pros::screen::print(pros::E_TEXT_LARGE, 1, "COLOR:  %f", clr.get_hue());
    if (clr.get_hue() < 35) {
      enc = lift.get_position();
      pros::screen::erase();
      pros::screen::print(pros::E_TEXT_LARGE, 3, "colorspotted");
      while((lift.get_position() - enc) < 400) { 
        pros::delay(2);
      }
      pros::screen::erase();
      pros::screen::print(pros::E_TEXT_LARGE, 3, "COLORNUKE");
      lift.move(-127);
      pros::delay(50);
      lift.brake();
      pros::delay(1000);
      lift.move(127);
    }
    else { 
      lift.move(127);
    }
  }
}
void bluesort() { 
  clr.set_integration_time(3);
  clr.set_led_pwm(100);
  lift.set_encoder_units(MOTOR_ENCODER_COUNTS);
  while (true) {
    pros::screen::erase();
    pros::screen::print(pros::E_TEXT_LARGE, 3, "lift:  %f", lift.get_position());
    if (clr.get_hue() > 160) {
      enc = lift.get_position();
      pros::screen::erase();
      pros::screen::print(pros::E_TEXT_LARGE, 3, "colorspotted");
      while((lift.get_position() - enc) < 340) { 
        pros::delay(2);
      }
      pros::screen::erase();
      pros::screen::print(pros::E_TEXT_LARGE, 3, "COLORNUKE");
      lift.move(-127);
      pros::delay(50);
      lift.brake();
      pros::delay(1000);
      lift.move(127);
    }
    else { 
      lift.move(127);
    }
    pros::delay(10);
  }
}
///
// Constant
///
void default_constants() {
  // P, I, D, and Start I
  chassis.pid_drive_constants_set(20.0, 0.0, 100.0);         // Fwd/rev constants, used for odom and non odom motions
  chassis.pid_heading_constants_set(11.0, 0.0, 20.0);        // Holds the robot straight while going forward without odom
  chassis.pid_turn_constants_set(3.0, 0.05, 20.0, 15.0);     // Turn in place constants
  chassis.pid_swing_constants_set(6.0, 0.0, 65.0);           // Swing constants
  chassis.pid_odom_angular_constants_set(6.5, 0.0, 52.5);    // Angular control for odom motions
  chassis.pid_odom_boomerang_constants_set(5.8, 0.0, 32.5);  // Angular control for boomerang motions
  
  // Exit conditions
  chassis.pid_turn_exit_condition_set(90_ms, 3_deg, 250_ms, 7_deg, 500_ms, 500_ms);
  chassis.pid_swing_exit_condition_set(90_ms, 3_deg, 250_ms, 7_deg, 500_ms, 500_ms);
  chassis.pid_drive_exit_condition_set(90_ms, 1_in, 250_ms, 3_in, 500_ms, 500_ms);
  chassis.pid_odom_turn_exit_condition_set(90_ms, 3_deg, 250_ms, 7_deg, 500_ms, 750_ms);
  chassis.pid_odom_drive_exit_condition_set(90_ms, 1_in, 250_ms, 3_in, 500_ms, 750_ms);
  chassis.pid_turn_chain_constant_set(3_deg);
  chassis.pid_swing_chain_constant_set(5_deg);
  chassis.pid_drive_chain_constant_set(3_in);

  // Slew constants
  chassis.slew_turn_constants_set(3_deg, 70);
  chassis.slew_drive_constants_set(3_in, 70);
  chassis.slew_swing_constants_set(3_in, 80);

  // The amount that turns are prioritized over driving in odom motions
  // - if you have tracking wheels, you can run this higher.  1.0 is the max
  chassis.odom_turn_bias_set(0.9);

  chassis.odom_look_ahead_set(7_in);           // This is how far ahead in the path the robot looks at
  chassis.odom_boomerang_distance_set(16_in);  // This sets the maximum distance away from target that the carrot point can be
  chassis.odom_boomerang_dlead_set(0.625);     // This handles how aggressive the end of boomerang motions are

  chassis.pid_angle_behavior_set(ez::shortest);  // Changes the default behavior for turning, this defaults it to the shortest path there
}

///
// Drive Example
///
void drive_example() {
  // The first parameter is target inches
  // The second parameter is max speed the robot will drive at
  // The third parameter is a boolean (true or false) for enabling/disabling a slew at the start of drive motions
  // for slew, only enable it when the drive distance is greater than the slew distance + a few inches

  chassis.pid_drive_set(24_in, DRIVE_SPEED, true);
  chassis.pid_wait();

  chassis.pid_drive_set(-12_in, DRIVE_SPEED);
  chassis.pid_wait();

  chassis.pid_drive_set(-12_in, DRIVE_SPEED);
  chassis.pid_wait();
}

///
// Turn Example
///
void turn_example() {
    //Go back
  lbt = 0;
  chassis.pid_drive_set(-30_in, 60, true);
  chassis.pid_wait_until(-20_in);
  chassis.pid_speed_max_set(60);
  chassis.pid_wait_until(-26_in);
  claw.set_value(true);
  claw2.set_value(true);
  chassis.pid_wait();
  
  chassis.pid_speed_max_set(DRIVE_SPEED);
  chassis.pid_drive_set(-5_in, DRIVE_SPEED, false);
  chassis.pid_wait();
  lift.move(127);


}

//RED NEG SIDE SOLO AWP / 2 TOP RING / 8 PT TOTAL
void red_negative() {
  pros::Task clrsort(bluesort);
  intake.move(127);
  //score with lb on alliance stake 
  pros::delay(20);
  lbr.move_absolute(1800, 200);
			while (((lbr.get_position() > 1810) && (lbr.get_position() < 1790))) { 
				pros::delay(2);
			}
  pros::delay(800);
  lbr.move_absolute(0,200);
  while (((lbr.get_position() > 5) && (lbr.get_position() < -2))) { 
				pros::delay(2);
			}
  pros::delay(800);

    
  //swing back and left ~45 deg
  chassis.pid_drive_set(-31_in, DRIVE_SPEED, true);
  chassis.pid_wait();
  chassis.pid_turn_set(108_deg, 70, true);
  chassis.pid_wait();
  //drive backwards to pick up goal
  chassis.pid_drive_set(-25_in, DRIVE_SPEED);
  chassis.pid_wait();
  chassis.pid_drive_set(-15_in, 100);
  chassis.pid_wait_until(-9_in);
  claw.set_value(true);
  claw.set_value(true);
  chassis.pid_wait();
  //spin lift to score ring 

  // turn right > 90 deg, towards ring pile 
  chassis.pid_turn_set(195_deg, TURN_SPEED);
  chassis.pid_wait();
  //chassis.pid_drive_set(-14_in, 55, true);
  //chassis.pid_wait();
  //spin intake 
  intake.move(127);
  chassis.pid_drive_set(20_in, 80,true);
  chassis.pid_wait();
  chassis.pid_turn_relative_set(-33_deg, 80); 
  chassis.pid_wait();
  chassis.pid_drive_set(11_in, 80, false);
  chassis.pid_wait();
  chassis.pid_turn_relative_set(-90_deg, TURN_SPEED);
  chassis.pid_wait();
  chassis.pid_drive_set(20_in, DRIVE_SPEED);
  chassis.pid_wait();
  chassis.pid_turn_relative_set(-90_deg, TURN_SPEED);
  chassis.pid_wait();
  chassis.pid_drive_set(40_in, DRIVE_SPEED, true);
  chassis.pid_wait_until(25_in);
  clrsort.remove();
  lift.brake();
  chassis.pid_wait();
  pros::delay(2000);

}

//RED POSITIVE
void red_positive() {

  lift.move(127);
  //score with lb on alliance stake 
  pros::delay(20);
  lbr.move_absolute(1800, 200);
			while (((lbr.get_position() > 1810) && (lbr.get_position() < 1790))) { 
				pros::delay(2);
			}
  pros::delay(800);
  lbr.move_absolute(0,200);
  while (((lbr.get_position() > 5) && (lbr.get_position() < -2))) { 
				pros::delay(2);
			}
  pros::delay(800);

    
  //swing back and left ~45 deg
  chassis.pid_drive_set(-31_in, DRIVE_SPEED, true);
  chassis.pid_wait();
  chassis.pid_turn_set(-108_deg, 70, true);
  chassis.pid_wait();
  //drive backwards to pick up goal
  chassis.pid_drive_set(-25_in, DRIVE_SPEED);
  chassis.pid_wait();
  chassis.pid_drive_set(-15_in, 100);
  chassis.pid_wait_until(-9_in);
  claw.set_value(true);
  claw.set_value(true);
  chassis.pid_wait();

  //turn to face 2-ring stack
  chassis.pid_turn_relative_set(-35_deg, TURN_SPEED); 
  chassis.pid_wait();
  intake.move(127);
  chassis.pid_drive_set(31_in, DRIVE_SPEED);
  chassis.pid_wait();
  chassis.pid_turn_relative_set(-105_deg, TURN_SPEED); 
  chassis.pid_wait();
  chassis.pid_drive_set(-5_in, DRIVE_SPEED);
  chassis.pid_wait();
  claw2.set_value(false);
  claw.set_value(false);
  chassis.pid_drive_set(5_in, DRIVE_SPEED);
  chassis.pid_wait();
  chassis.pid_turn_relative_set(180_deg, TURN_SPEED);
  chassis.pid_wait();
  chassis.pid_drive_set(-14_in, DRIVE_SPEED);
  chassis.pid_wait_until(-13_in);
  claw.set_value(true);
  claw2.set_value(true);
  chassis.pid_wait();
  chassis.pid_turn_relative_set(90_deg, TURN_SPEED);
  lbr.move_absolute(1400, 200);
  while ((lbr.get_position() < 1390) && (lbr.get_position() > 1410)) { 
    pros::delay(2);
  }
  chassis.pid_drive_set(30_in, 60, true);
  chassis.pid_wait();
}

///
// Swing Example
///
void swing_example() {
  claw.set_value(true);
  claw2.set_value(true);
  pros::Task clrsort(bluesort);
  intake.move(127);
  // // The first parameter is ez::LEFT_SWING or ez::RIGHT_SWING
  // // The second parameter is the target in degrees
  // // The third parameter is the speed of the moving side of the drive
  // // The fourth parameter is the speed of the still side of the drive, this allows for wider arcs

  // chassis.pid_swing_set(ez::LEFT_SWING, 45_deg, SWING_SPEED, 45);
  // chassis.pid_wait();

  // chassis.pid_swing_set(ez::RIGHT_SWING, 0_deg, SWING_SPEED, 45);
  // chassis.pid_wait();

  // chassis.pid_swing_set(ez::RIGHT_SWING, 45_deg, SWING_SPEED, 45);
  // chassis.pid_wait();

  // chassis.pid_swing_set(ez::LEFT_SWING, 0_deg, SWING_SPEED, 45);
  // chassis.pid_wait();
}

///
// Motion Chaining
///
void motion_chaining() {
  // Motion chaining is where motions all try to blend together instead of individual movements.
  // This works by exiting while the robot is still moving a little bit.
  // To use this, replace pid_wait with pid_wait_quick_chain.
  chassis.pid_drive_set(24_in, DRIVE_SPEED, true);
  chassis.pid_wait();

  chassis.pid_turn_set(45_deg, TURN_SPEED);
  chassis.pid_wait_quick_chain();

  chassis.pid_turn_set(-45_deg, TURN_SPEED);
  chassis.pid_wait_quick_chain();

  chassis.pid_turn_set(0_deg, TURN_SPEED);
  chassis.pid_wait();

  // Your final motion should still be a normal pid_wait
  chassis.pid_drive_set(-24_in, DRIVE_SPEED, true);
  chassis.pid_wait();
}

///
// Auto that tests everything
///
void combining_movements() {
  chassis.pid_drive_set(24_in, DRIVE_SPEED, true);
  chassis.pid_wait();

  chassis.pid_turn_set(45_deg, TURN_SPEED);
  chassis.pid_wait();

  chassis.pid_swing_set(ez::RIGHT_SWING, -45_deg, SWING_SPEED, 45);
  chassis.pid_wait();

  chassis.pid_turn_set(0_deg, TURN_SPEED);
  chassis.pid_wait();

  chassis.pid_drive_set(-24_in, DRIVE_SPEED, true);
  chassis.pid_wait();
}

///
// Interference example
///
void tug(int attempts) {
  for (int i = 0; i < attempts - 1; i++) {
    // Attempt to drive backward
    printf("i - %i", i);
    chassis.pid_drive_set(-12_in, 127);
    chassis.pid_wait();

    // If failsafed...
    if (chassis.interfered) {
      chassis.drive_sensor_reset();
      chassis.pid_drive_set(-2_in, 20);
      pros::delay(1000);
    }
    // If the robot successfully drove back, return
    else {
      return;
    }
  }
}

// If there is no interference, the robot will drive forward and turn 90 degrees.
// If interfered, the robot will drive forward and then attempt to drive backward.
void interfered_example() {
  chassis.pid_drive_set(24_in, DRIVE_SPEED, true);
  chassis.pid_wait();

  if (chassis.interfered) {
    tug(3);
    return;
  }

  chassis.pid_turn_set(90_deg, TURN_SPEED);
  chassis.pid_wait();
}

///
// Odom Drive PID
///
void odom_drive_example() {
  // This works the same as pid_drive_set, but it uses odom instead!
  // You can replace pid_drive_set with pid_odom_set and your robot will
  // have better error correction.

  chassis.pid_odom_set(24_in, DRIVE_SPEED, true);
  chassis.pid_wait();

  chassis.pid_odom_set(-12_in, DRIVE_SPEED);
  chassis.pid_wait();

  chassis.pid_odom_set(-12_in, DRIVE_SPEED);
  chassis.pid_wait();
}

///
// Odom Pure Pursuit
///
void odom_pure_pursuit_example() {
  // Drive to 0, 30 and pass through 6, 10 and 0, 20 on the way, with slew
  chassis.pid_odom_set({{{6_in, 10_in}, fwd, DRIVE_SPEED},
                        {{0_in, 20_in}, fwd, DRIVE_SPEED},
                        {{0_in, 30_in}, fwd, DRIVE_SPEED}},
                       true);
  chassis.pid_wait();

  // Drive to 0, 0 backwards
  chassis.pid_odom_set({{0_in, 0_in}, rev, DRIVE_SPEED},
                       true);
  chassis.pid_wait();
}

///
// Odom Pure Pursuit Wait Until
///
void odom_pure_pursuit_wait_until_example() {
  chassis.pid_odom_set({{{0_in, 24_in}, fwd, DRIVE_SPEED},
                        {{12_in, 24_in}, fwd, DRIVE_SPEED},
                        {{24_in, 24_in}, fwd, DRIVE_SPEED}},
                       true);
  chassis.pid_wait_until_index(1);  // Waits until the robot passes 12, 24
  // Intake.move(127);  // Set your intake to start moving once it passes through the second point in the index
  chassis.pid_wait();
  // Intake.move(0);  // Turn the intake off
}

///
// Odom Boomerang
///
void odom_boomerang_example() {
  chassis.pid_odom_set({{0_in, 24_in, 45_deg}, fwd, DRIVE_SPEED},
                       true);
  chassis.pid_wait();

  chassis.pid_odom_set({{0_in, 0_in, 0_deg}, rev, DRIVE_SPEED},
                       true);
  chassis.pid_wait();
}

///
// Odom Boomerang Injected Pure Pursuit
///
void odom_boomerang_injected_pure_pursuit_example() {
  chassis.pid_odom_set({{{0_in, 24_in, 45_deg}, fwd, DRIVE_SPEED},
                        {{12_in, 24_in}, fwd, DRIVE_SPEED},
                        {{24_in, 24_in}, fwd, DRIVE_SPEED}},
                       true);
  chassis.pid_wait();

  chassis.pid_odom_set({{0_in, 0_in, 0_deg}, rev, DRIVE_SPEED},
                       true);
  chassis.pid_wait();
}

///
// Calculate the offsets of your tracking wheels
///
void measure_offsets() {
  // Number of times to test
  int iterations = 10;

  // Our final offsets
  double l_offset = 0.0, r_offset = 0.0, b_offset = 0.0, f_offset = 0.0;

  // Reset all trackers if they exist
  if (chassis.odom_tracker_left != nullptr) chassis.odom_tracker_left->reset();
  if (chassis.odom_tracker_right != nullptr) chassis.odom_tracker_right->reset();
  if (chassis.odom_tracker_back != nullptr) chassis.odom_tracker_back->reset();
  if (chassis.odom_tracker_front != nullptr) chassis.odom_tracker_front->reset();
  
  for (int i = 0; i < iterations; i++) {
    // Reset pid targets and get ready for running an auton
    chassis.pid_targets_reset();
    chassis.drive_imu_reset();
    chassis.drive_sensor_reset();
    chassis.drive_brake_set(MOTOR_BRAKE_HOLD);
    chassis.odom_xyt_set(0_in, 0_in, 0_deg);
    double imu_start = chassis.odom_theta_get();
    double target = i % 2 == 0 ? 90 : 270;  // Switch the turn target every run from 270 to 90

    // Turn to target at half power
    chassis.pid_turn_set(target, 63, ez::raw);
    chassis.pid_wait();
    pros::delay(250);

    // Calculate delta in angle
    double t_delta = util::to_rad(fabs(util::wrap_angle(chassis.odom_theta_get() - imu_start)));

    // Calculate delta in sensor values that exist
    double l_delta = chassis.odom_tracker_left != nullptr ? chassis.odom_tracker_left->get() : 0.0;
    double r_delta = chassis.odom_tracker_right != nullptr ? chassis.odom_tracker_right->get() : 0.0;
    double b_delta = chassis.odom_tracker_back != nullptr ? chassis.odom_tracker_back->get() : 0.0;
    double f_delta = chassis.odom_tracker_front != nullptr ? chassis.odom_tracker_front->get() : 0.0;

    // Calculate the radius that the robot traveled
    l_offset += l_delta / t_delta;
    r_offset += r_delta / t_delta;
    b_offset += b_delta / t_delta;
    f_offset += f_delta / t_delta;
  }

  // Average all offsets
  l_offset /= iterations;
  r_offset /= iterations;
  b_offset /= iterations;
  f_offset /= iterations;

  // Set new offsets to trackers that exist
  if (chassis.odom_tracker_left != nullptr) chassis.odom_tracker_left->distance_to_center_set(l_offset);
  if (chassis.odom_tracker_right != nullptr) chassis.odom_tracker_right->distance_to_center_set(r_offset);
  if (chassis.odom_tracker_back != nullptr) chassis.odom_tracker_back->distance_to_center_set(b_offset);
  if (chassis.odom_tracker_front != nullptr) chassis.odom_tracker_front->distance_to_center_set(f_offset);
}

// . . .
// Make your own autonomous functions here!
// . . .
void fiveRing_LeftRed(){




}