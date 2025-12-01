import time, math, odrive
from odrive.utils import dump_errors

#Config

print("Connecting...")
odrv0 = odrive.find_any(timeout=15)
axis0 = odrv0.axis0
axis1 = odrv0.axis1

for axis in [axis0, axis1]:
    motor = axis.motor
    enc   = axis.encoder
    ctl   = axis.controller

    print(f"vbus = {odrv0.vbus_voltage:.2f} V")

    #Motor Params 

    motor.config.pole_pairs = 15
    motor.config.motor_type = 0          # 0 = HIGH_CURRENT
    motor.config.current_lim = 10.0
    motor.config.calibration_current = 10.0

    enc.config.mode = 1                  # 1 = HALL
    enc.config.cpr  = 6 * motor.config.pole_pairs
    enc.config.bandwidth = 100.0

    #Position Control Params 

    ctl.config.control_mode = 3          # 3 = POSITION_CONTROL
    ctl.config.input_mode   = 1          # 1 = PASSTHROUGH (we'll stream input_pos)
    ctl.config.pos_gain     = 20.0       # Tune as needed
    ctl.config.vel_gain     = 0.02       # Tune as needed
    ctl.config.vel_integrator_gain = 0.1 # Tune as needed

    axis.motor.config.pre_calibrated = False
    axis.encoder.config.pre_calibrated = False

#Save config and reboot 

odrv0.save_configuration()
print("Saved configuration. Rebooting...")
try:
    odrv0.reboot()
except Exception:
    pass
time.sleep(5)

print("Reconnecting...")
odrv0 = odrive.find_any(timeout=15)
axis0 = odrv0.axis0
axis1 = odrv0.axis1

#Cal
print("Calibrating...")
axis0.requested_state = 3   # FULL_CALIBRATION_SEQUENCE
axis1.requested_state = 3
time.sleep(25) #Make sure this is enough to complete the calibration 

axis0.requested_state = 1  # IDLE
axis1.requested_state = 1  # IDLE
dump_errors(odrv0)
print("Done.")


