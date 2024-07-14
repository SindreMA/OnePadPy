import pyvjoy
import time

# Initialize vJoy device
j = pyvjoy.VJoyDevice(1)

# Function to set axis value
def set_axis(axis, value):
    j.set_axis(axis, value)

# Cycle through axis values
def cycle_axis():
    axis_values = range(0, 32768, 1000)  # vJoy uses values between 0 and 32768
    while True:
        for value in axis_values:
            set_axis(pyvjoy.HID_USAGE_X, value)  # X-axis
            set_axis(pyvjoy.HID_USAGE_Y, value)  # Y-axis
            set_axis(pyvjoy.HID_USAGE_Z, value)  # Z-axis
            set_axis(pyvjoy.HID_USAGE_RX, value)  # Rx-axis
            set_axis(pyvjoy.HID_USAGE_RY, value)  # Ry-axis
            set_axis(pyvjoy.HID_USAGE_RZ, value)  # Rz-axis
            time.sleep(0.01)  # Adjust the sleep time for smoother or faster cycling

if __name__ == "__main__":
    cycle_axis()
