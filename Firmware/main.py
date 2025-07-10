import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import keypad.encoder

# --- Configuration ---

# Define the pins for your buttons
# Note: These pins match the GPIO numbers from your schematic
BUTTON_PINS = {
    "terminal": board.GPIO26,
    "screenshot": board.GPIO27,
    "kill_window": board.GPIO28,
}

# Define the pins for your rotary encoder
ENCODER_A_PIN = board.GPIO6
ENCODER_B_PIN = board.GPIO7

# --- HID Setup ---

# Initialize Keyboard and ConsumerControl objects
# Keyboard sends standard key presses
keyboard = Keyboard(usb_hid.devices)
# ConsumerControl sends multimedia and special keys (e.g., volume, browser functions)
# Not strictly needed for current functions, but good to have for future expansion.
# cc = ConsumerControl(usb_hid.devices)

# --- Button Setup ---

# Create DigitalInOut objects for each button
# Use pull=digitalio.Pull.UP because the buttons connect to GND when pressed
buttons = {}
for name, pin in BUTTON_PINS.items():
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons[name] = btn

# Store the last state of buttons for debouncing
button_states = {name: True for name in BUTTON_PINS.keys()} # True means not pressed (pull-up)

# --- Rotary Encoder Setup ---

# Initialize the rotary encoder
# The IncrementalEncoder automatically handles the A/B phase logic
encoder = keypad.encoder.IncrementalEncoder(ENCODER_A_PIN, ENCODER_B_PIN)
last_position = encoder.position

# --- Main Loop ---

print("Macropad ready!") # This will print to the serial console

while True:
    # --- Read Buttons ---
    for name, btn in buttons.items():
        current_state = btn.value # True if not pressed, False if pressed

        # Check for a transition from HIGH (not pressed) to LOW (pressed)
        if not current_state and button_states[name]: # Button just pressed
            print(f"{name} button pressed!") # Debugging output

            if name == "terminal":
                # Win + R
                keyboard.press(Keycode.GUI, Keycode.R)
                keyboard.release_all()
                time.sleep(0.05) # Small delay for the OS to react
                # Type "wt" (Windows Terminal)
                keyboard.send(Keycode.W, Keycode.T)
                time.sleep(0.05)
                # Press Enter
                keyboard.send(Keycode.ENTER)

            elif name == "screenshot":
                # Win + Shift + S
                keyboard.press(Keycode.GUI, Keycode.LEFT_SHIFT, Keycode.S)
                keyboard.release_all()

            elif name == "kill_window":
                # Alt + F4
                keyboard.press(Keycode.ALT, Keycode.F4)
                keyboard.release_all()

            # Debounce delay: important for physical buttons
            time.sleep(0.2) # Adjust this value if you experience multiple presses from one click

        # Update the button state
        button_states[name] = current_state

    # --- Read Rotary Encoder ---
    current_position = encoder.position
    if current_position != last_position:
        delta = current_position - last_position
        print(f"Encoder moved: {delta}") # Debugging output

        if delta > 0: # Clockwise rotation
            # Ctrl + Tab (next browser tab)
            keyboard.press(Keycode.CONTROL, Keycode.TAB)
            keyboard.release_all()
        elif delta < 0: # Counter-clockwise rotation
            # Ctrl + Shift + Tab (previous browser tab)
            keyboard.press(Keycode.CONTROL, Keycode.LEFT_SHIFT, Keycode.TAB)
            keyboard.release_all()

        last_position = current_position
        time.sleep(0.05) # Small delay after encoder turn

    time.sleep(0.01) # Short delay to prevent busy-waiting and save power