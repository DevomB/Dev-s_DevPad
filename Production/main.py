import board
import time

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import Encoder
from kmk.modules.macros import Macros # Necessary for KC.MACRO_TAP

# --- Basic Setup ---
keyboard = KMKKeyboard()
keyboard.modules.append(Macros()) # Add Macros module to use KC.MACRO_TAP

# --- Pin Definitions ---
# Buttons:
# For KMK, we define the row and column pins that form our key matrix.
# Even with independent buttons, we can represent them as a single row with multiple columns,
# or multiple rows with a single dummy column.
# Here, we're treating each button's GPIO as a 'row' and using one unused GPIO as a 'column'.
# This allows KMK's matrix scanning to handle the buttons correctly with internal pull-ups.
keyboard.row_pins = (board.GP26, board.GP27, board.GP28) # Button 1, Button 2, Button 3
keyboard.col_pins = (board.GP0,) # Using an unused GPIO as a dummy column pin

# Rotary Encoder:
# Connect encoder phases A and B to these pins as per your PCB layout.
encoder_pins = (
    (board.GP6, board.GP7), # Encoder 1 (A phase pin, B phase pin)
)
# Add the Encoder module to the keyboard.
keyboard.modules.append(Encoder(
    encoder_pins=encoder_pins,
    # Define what key combinations to send for clockwise/counter-clockwise rotation.
    # KMK automatically handles the press/release for these modifier combinations.
    # (KC.MODIFIER(KC.KEY)) syntax creates a modifier+key combination.
    # For clockwise (CW), send Ctrl+Tab.
    # For counter-clockwise (CCW), send Ctrl+Shift+Tab.
    encoder_map=(
        ((KC.LCTRL(KC.TAB),), (KC.LCTRL(KC.LSHIFT(KC.TAB)),)), # Encoder 1: CW, CCW actions
    )
))

# --- Macro Definitions ---
# This macro handles the "Win+R, wt, Enter" sequence for opening the terminal.
# KC.MACRO_TAP sends a series of key presses/releases with optional delays.
# Each item in the sequence can be a single key, or a tuple of keys for simultaneous press.
# KC.WAIT(milliseconds) inserts a pause.
KC_TERMINAL_SEQUENCE = (
    (KC.LWIN, KC.R),     # 1. Press and release Win+R
    KC.WAIT(50),         # 2. Wait 50ms for the Run dialog to appear
    KC.W,                # 3. Type 'w'
    KC.T,                # 4. Type 't'
    KC.WAIT(50),         # 5. Wait 50ms before pressing Enter
    KC.ENTER,            # 6. Press and release Enter
)

# --- Keymap ---
# Define the keymap. This is a list of layers.
# We'll use a single base layer (layer 0) for your macropad.
# The `keymap` list maps the physical button positions to the desired keycodes or macros.
# The order here corresponds to your `row_pins` (GP26, GP27, GP28) and `col_pins` (GP0).
# So, the first element `[0][0]` maps to GP26, `[1][0]` to GP27, `[2][0]` to GP28.
keyboard.keymap = [
    [
        KC.MACRO_TAP(KC_TERMINAL_SEQUENCE),  # Button 1 (connected to GP26) -> Win+R, wt, Enter
        KC.LWIN(KC.LSHIFT(KC.S)),            # Button 2 (connected to GP27) -> Win+Shift+S (Screenshot)
        KC.LALT(KC.F4),                      # Button 3 (connected to GP28) -> Alt+F4 (Kill Window)
    ]
]

# --- Start the keyboard ---
if __name__ == '__main__':
    keyboard.go()