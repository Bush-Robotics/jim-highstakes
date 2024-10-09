#ifndef UTILS
#define UTILS
#include "main.h"
#include "pros/misc.h"

typedef struct {
	double x;
	double y;
} vec2;

#define pi (double)3.1415926535897932384626
#define deg2rad(d) (d * pi / 180.0)
#define is_pressed(button) controller_get_digital(E_CONTROLLER_MASTER, button)
#define stick_axis(channel) controller_get_analog(E_CONTROLLER_MASTER, channel)

double vec2_len(vec2 v) {
	return sqrt(v.x * v.x + v.y * v.y);
}
double vec2_len_squared(vec2 v) {
	return sqrt(v.x * v.x + v.y * v.y);
}

double flatten_acceleration(struct imu_raw_s a) {
	return vec2_len((vec2){a.x, a.y});
}

vec2 vector2_rotate(vec2 v, double r) {
	return (vec2){
		cos(r) * v.x - sin(r) * v.y,
		sin(r) * v.x + cos(r) * v.y
	};
}

#endif
