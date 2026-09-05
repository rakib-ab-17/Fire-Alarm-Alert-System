import machine
import onewire
import ds18x20
import time

# ---------------- Pin setup ----------------
FLAME_PIN = 2
DS_PIN = 3
BUZZER_PIN = 4
RED_LED_PIN = 5
GREEN_LED_PIN = 6

TEMP_THRESHOLD = 40.0  # Celsius

flame_sensor = machine.Pin(FLAME_PIN, machine.Pin.IN)
red_led = machine.Pin(RED_LED_PIN, machine.Pin.OUT)
green_led = machine.Pin(GREEN_LED_PIN, machine.Pin.OUT)

buzzer = machine.PWM(machine.Pin(BUZZER_PIN))
buzzer.duty_u16(0)

ds_sensor = ds18x20.DS18X20(onewire.OneWire(machine.Pin(DS_PIN)))


def set_alarm(active):
    if active:
        red_led.value(1)
        green_led.value(0)
        buzzer.freq(1000)
        buzzer.duty_u16(30000)
    else:
        red_led.value(0)
        green_led.value(1)
        buzzer.duty_u16(0)


print("Fire alarm (debug mode - no button) starting...")
green_led.value(1)  # start in normal state clearly

while True:
    roms = ds_sensor.scan()
    flame_raw = flame_sensor.value()
    flame_detected = (flame_raw == 0)

    temp_c = None
    if roms:
        ds_sensor.convert_temp()
        time.sleep_ms(750)
        temp_c = ds_sensor.read_temp(roms[0])

    alarm_active = flame_detected and (temp_c is not None) and (temp_c > TEMP_THRESHOLD)

    print("flame_pin_raw={}  flame_detected={}  temp={}  ALARM={}".format(
        flame_raw, flame_detected,
        ("{:.1f}".format(temp_c) if temp_c is not None else "None"),
        alarm_active
    ))

    set_alarm(alarm_active)
    time.sleep(1)