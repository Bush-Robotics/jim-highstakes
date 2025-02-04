#pragma once

#include "EZ-Template/api.hpp"
#include "api.h"

extern Drive chassis;

// Your motors, sensors, etc. should go here.  Below are examples
inline pros::Motor intake(-11, pros::MotorGearset::green);
inline pros::Motor lift(-12, pros::MotorGearset::blue);
inline pros::Motor lbr(13, pros::MotorGearset::green);
inline pros::adi::DigitalOut claw('A', false);
inline pros::adi::DigitalOut claw2('B', false);
inline pros::adi::DigitalOut doinker('C', false);
inline pros::Controller master (pros::E_CONTROLLER_MASTER);
inline int lbt;
// inline pros::Motor intake(1);
// inline pros::adi::DigitalIn limit_switch('A');