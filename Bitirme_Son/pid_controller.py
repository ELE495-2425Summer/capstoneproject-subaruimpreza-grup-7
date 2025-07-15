import math
import time

BETA = 7.0

class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint, output_limits=(0, 255)):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.min_out, self.max_out = output_limits
        self._integral = 0.0
        self._last_error = 0.0
        self._last_time = time.time()

    def reset(self):
        self._integral = 0.0
        self._last_error = 0.0
        self._last_time = time.time()

    def update(self, measurement):
        now = time.time()
        dt = now - self._last_time
        error = measurement - self.setpoint

        self._integral += error * dt
        derivative = (error - self._last_error) / dt if dt > 0 else 0.0
        raw_output = (self.Kp * error) + (self.Ki * self._integral) + (self.Kd * derivative)

        # PWM limitlemesi (pozitif/negatif işaret korunarak)
        clipped = max(self.min_out, min(self.max_out, raw_output)) if self.min_out < self.max_out else raw_output

        # PWM ölçekleme (mutlak değeriyle normalize edip exponential rampa uygula)
        norm = abs(clipped) / float(self.max_out)
        exp_ramp = (1 - math.exp(-BETA * norm)) / (1 - math.exp(-BETA))
        pwm = int(self.max_out * exp_ramp)

        # PWM işaretini koru (negatifse negatif kalacak)
        pwm = pwm if clipped >= 0 else -pwm

        self._last_error = error
        self._last_time = now
        return pwm
