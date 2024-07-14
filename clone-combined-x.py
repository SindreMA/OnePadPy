import pygame
import pyvjoy
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# Initialize Pygame and the joystick module
pygame.init()
pygame.joystick.init()

# Check if a joystick is connected
if pygame.joystick.get_count() == 0:
    logger.error("No joystick connected!")
    exit()

# Initialize the joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()
logger.info("Joystick initialized: %s", joystick.get_name())

# Initialize vJoy
vjoy_device_id = 1

def acquire_vjoy_device(device_id):
    from pyvjoy.exceptions import vJoyFailedToAcquireException
    try:
        vjoy_device = pyvjoy.VJoyDevice(device_id)
        logger.info("vJoy device %d acquired", device_id)
        return vjoy_device
    except vJoyFailedToAcquireException as e:
        logger.error("Failed to acquire vJoy device %d: %s", device_id, e)
        exit()

vjoy_device = acquire_vjoy_device(vjoy_device_id)

# Define a function to map the axis values from pygame to vJoy
def map_axis(value):
    # Pygame axis value ranges from -1 to 1, vJoy expects 0 to 32767
    return int((value + 1) * 0x4000)

# Initialize previous state for logging changes
prev_axes = [0, 0, 0, 0]
prev_buttons = [0] * joystick.get_numbuttons()
prev_hat = (0, 0)

try:
    while True:
        # Process Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Read axis values
        # Setting left stick
        left_x_axis = joystick.get_axis(0)
        left_y_axis = joystick.get_axis(1)

        # Setting right stick
        right_x_axis = joystick.get_axis(2)
        right_y_axis = joystick.get_axis(3)

        # Setting triggers
        left_trigger_axis = joystick.get_axis(4)
        right_trigger_axis = joystick.get_axis(5)


        axes = [left_x_axis, left_y_axis, right_x_axis, right_y_axis, left_trigger_axis, right_trigger_axis]

        # Log axis values only if they change
        if axes != prev_axes:
            logger.info("Axes: %s", axes)
            prev_axes = axes

        # Map the values to vJoy range and update vJoy

        # Left stick
        vjoy_device.data.wAxisX = map_axis(left_x_axis + right_x_axis)
        vjoy_device.data.wAxisY = map_axis(left_y_axis)

        # Right stick
        vjoy_device.data.wAxisXRot = map_axis(right_x_axis)
        vjoy_device.data.wAxisYRot = map_axis(right_y_axis)

        # Triggers
        vjoy_device.data.wAxisZ = map_axis(left_trigger_axis)
        vjoy_device.data.wAxisZRot = map_axis(right_trigger_axis)

        vjoy_device.update()

        # Read button values
        buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]

        # Log button values only if they change
        if buttons != prev_buttons:
            for i, button_value in enumerate(buttons):
                if button_value != prev_buttons[i]:
                    logger.info("Button %d: %d", i + 1, button_value)
            prev_buttons = buttons

        # Update vJoy buttons
        for i, button_value in enumerate(buttons):
            vjoy_device.set_button(i + 1, button_value)

        # Read hat switch values (d-pad)
        hat_value = joystick.get_hat(0)

        # Log hat switch values only if they change
        if hat_value != prev_hat:
            logger.info("D-Pad: %s", hat_value)
            prev_hat = hat_value

 # Update vJoy buttons for d-pad directions
        # Here, we map the d-pad directions to buttons 13-16
        # Adjust the button numbers as needed for your configuration
        vjoy_device.set_button(13, int(hat_value == (0, 1)))  # Up
        vjoy_device.set_button(14, int(hat_value == (1, 0)))  # Right
        vjoy_device.set_button(15, int(hat_value == (0, -1)))  # Down
        vjoy_device.set_button(16, int(hat_value == (-1, 0)))  # Left

        # Sleep for a short duration to avoid high CPU usage
        pygame.time.wait(10)

except KeyboardInterrupt:
    pygame.quit()
    exit()
