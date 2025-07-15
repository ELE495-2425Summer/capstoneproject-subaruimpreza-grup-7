from gpiozero import DistanceSensor
from gpio_config import TRIG_PIN, ECHO_PIN, TRIG_ARKA_PIN, ECHO_ARKA_PIN

ultrasonic_sensor_on = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, max_distance=5.0)
ultrasonic_sensor_arka = DistanceSensor(echo=ECHO_ARKA_PIN, trigger=TRIG_ARKA_PIN, max_distance=5.0)

def mesafe_oku():
    return ultrasonic_sensor_on.distance

def mesafe_oku_arka():
    return ultrasonic_sensor_arka.distance
