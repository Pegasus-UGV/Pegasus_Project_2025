import time, odrive
from odrive.utils import dump_errors

#ASSUMES YOU HAVE RUN CALIBRATION FILE PREVIOUSLY 

def revolve(axis, pos=0, hz=50, timeout=5):
    axis.controller.input_pos = pos
    
    dt = 1.0 / hz
    t0 = time.time()
    while True:
        pos = axis.encoder.pos_estimate
        print(f"pos={pos: .4f} turns ({pos*360: .1f}°)")
        if time.time() - t0 > timeout:
            print("Stop Reading.")
            break
        time.sleep(dt)

print("Connecting...")
odrv0 = odrive.find_any(timeout=15)
axis = odrv0.axis0
ctl  = axis.controller

print(f"vbus = {odrv0.vbus_voltage:.2f} V")

# --- Confirm pre-calibration flags are still true ---
print(f"Motor pre-calibrated: {axis.motor.config.pre_calibrated}")
print(f"Encoder pre-calibrated: {axis.encoder.config.pre_calibrated}")

ctl = axis.controller
ctl.config.control_mode = 3          # POSITION_CONTROL
ctl.config.input_mode   = 1          # PASSTHROUGH

# PID controller limits/gains 
axis.controller.config.vel_limit          = 10.0
ctl.config.pos_gain                       = 20.0
ctl.config.vel_gain                       = 0.02
ctl.config.vel_integrator_gain            = 0.1

axis.requested_state = 8   # CLOSED_LOOP_CONTROL
time.sleep(0.3)

revolve(axis, 0)

axis.requested_state = 1  # IDLE
dump_errors(odrv0)
print("Done.")


