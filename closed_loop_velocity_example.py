import time, odrive
from odrive.utils import dump_errors

#ASSUMES YOU HAVE RUN CALIBRATION FILE PREVIOUSLY 

print("Connecting...")
odrv0 = odrive.find_any(timeout=15)
axis = odrv0.axis0
ctl  = axis.controller

print(f"vbus = {odrv0.vbus_voltage:.2f} V")

# --- Confirm pre-calibration flags are still true ---
print(f"Motor pre-calibrated: {axis.motor.config.pre_calibrated}")
print(f"Encoder pre-calibrated: {axis.encoder.config.pre_calibrated}")

# --- Go straight into closed-loop ---
axis.requested_state = 8  # CLOSED_LOOP_CONTROL
time.sleep(0.5)

# --- Velocity control setup ---
ctl.config.control_mode = 2   # VELOCITY_CONTROL
ctl.config.input_mode   = 2   # VEL_RAMP
ctl.config.vel_ramp_rate = 3.0

print("Spinning at +3 rps…")
ctl.input_vel = 3.0
time.sleep(3)

print("Reverse…")
ctl.input_vel = -3.0
time.sleep(3)

print("Stop")
ctl.input_vel = 0.0
time.sleep(1)

axis.requested_state = 1  # IDLE
dump_errors(odrv0)
print("Done.")
