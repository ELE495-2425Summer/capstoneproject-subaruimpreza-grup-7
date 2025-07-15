from gpiozero import OutputDevice, PWMOutputDevice
from gpio_config import IN1_PIN, IN2_PIN, IN3_PIN, IN4_PIN, ENA_PIN, ENB_PIN

IN1 = OutputDevice(IN1_PIN)
IN2 = OutputDevice(IN2_PIN)
IN3 = OutputDevice(IN3_PIN)
IN4 = OutputDevice(IN4_PIN)
ENA = PWMOutputDevice(ENA_PIN, frequency=1000)
ENB = PWMOutputDevice(ENB_PIN, frequency=1000)

def motor_calistir(hiz, yon):
    hiz = max(0, min(hiz, 100))
    if yon == "ileri":
        IN1.on(); IN2.off()
        IN3.off(); IN4.on()
    elif yon == "geri":
        IN1.off(); IN2.on()
        IN3.on(); IN4.off()
    elif yon in ["sag", "saga_don"]:
        IN1.off(); IN2.on()
        IN3.off(); IN4.on()
    elif yon in ["sol", "sola_don"]:
        IN1.on(); IN2.off()
        IN3.on(); IN4.off()
    elif yon == "dur":
        IN1.off(); IN2.off()
        IN3.off(); IN4.off()

    ENA.value = hiz / 100.0
    ENB.value = hiz / 100.0
