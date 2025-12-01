import time, odrive
from odrive.utils import dump_errors
import math
import sys, termios, threading

#Harrison Chung 

#ASSUMES YOU HAVE RUN CALIBRATION FILE PREVIOUSLY 

#Function Declarations 

#E-Stop Functions 

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty = termios.tcgetattr(fd)
        tty[3] = tty[3] & ~(termios.ICANON | termios.ECHO)
        termios.tcsetattr(fd, termios.TCSADRAIN, tty)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def estop_key_listener():
    while True:
        key = getch()
        print("\nSoftware E-STOP triggered.")
        e_stop()

def e_stop():
    axis_L.controller.input_vel = 0
    axis_R.controller.input_vel = 0
    axis_L.controller.input_pos = axis_L.encoder.pos_estimate
    axis_R.controller.input_pos = axis_R.encoder.pos_estimate
    axis_L.requested_state = 1
    axis_R.requested_state = 1
    dump_errors(odrv0)

def clear_axis_errors(axis):
    axis.error = 0
    axis.motor.error = 0
    axis.encoder.error = 0
    axis.controller.error = 0

#Movement Functions 

def revolve(axis, pos=0, hz=50, timeout=100, tol=0.1):
    axis.controller.input_pos = pos
    
    dt = 1.0 / hz
    t0 = time.time()
    while True:
        curr_pos = axis.encoder.pos_estimate
        err = abs(pos - curr_pos)
        print(f"pos={curr_pos: .4f} turns ({curr_pos*360: .1f}°)")

        if abs(err) < tol:
            print(f"\nReached target: |err| < {tol} turns")
            break

        if time.time() - t0 > timeout:
            break
        time.sleep(dt)

def move_forward(distance, timeout=100):
    turns = distance / WHEEL_CIRCUMFERENCE_M

    left_start  = axis_L.encoder.pos_estimate
    right_start = axis_R.encoder.pos_estimate

    left_target  = left_start  + turns
    right_target = right_start - turns  

    tL = threading.Thread(target=revolve,
                          args=(axis_L, left_target, timeout))
    tR = threading.Thread(target=revolve,
                          args=(axis_R, right_target, timeout))

    tL.start()
    tR.start()

    tL.join()
    tR.join()

def move_backward(distance, timeout=100):
    turns = distance / WHEEL_CIRCUMFERENCE_M

    left_start  = axis_L.encoder.pos_estimate
    right_start = axis_R.encoder.pos_estimate

    left_target  = left_start  - turns
    right_target = right_start + turns  

    tL = threading.Thread(target=revolve,
                          args=(axis_L, left_target, timeout))
    tR = threading.Thread(target=revolve,
                          args=(axis_R, right_target, timeout))

    tL.start()
    tR.start()

    tL.join()
    tR.join()

WHEEL_DIAMETER_M = 0.1524
WHEEL_CIRCUMFERENCE_M = math.pi * WHEEL_DIAMETER_M

threading.Thread(target=estop_key_listener, daemon=True).start() #E-Stop listener 

print("Connecting...")
odrv0 = odrive.find_any(timeout=15)

print(f"vbus = {odrv0.vbus_voltage:.2f} V")

axis_L = odrv0.axis0
axis_R = odrv0.axis1

for axis in [axis_L, axis_R]:
    clear_axis_errors(axis)

    axis.motor.config.pre_calibrated = True
    axis.encoder.config.pre_calibrated = True
    print(f"Motor pre-calibrated: {axis.motor.config.pre_calibrated}")
    print(f"Encoder pre-calibrated: {axis.encoder.config.pre_calibrated}")

    axis.controller.config.control_mode = 3        # POSITION_CONTROL
    axis.controller.config.input_mode = 1     #PASSTHROUGH 
    axis.controller.config.vel_limit = 2.0
    axis.controller.config.pos_gain = 5.0
    axis.controller.config.vel_gain = 0.07
    axis.controller.config.vel_integrator_gain = 0.005

axis_L.requested_state = 8
axis_R.requested_state = 8

time.sleep(0.3)

for i in range(5):
    move_forward(0.25)
    move_backward(0.25)

axis_L.requested_state = 1  # IDLE
axis_R.requested_state = 1

dump_errors(odrv0)
print("Done.")
