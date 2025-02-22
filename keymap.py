from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Keycode map for the keyboard
# This is a dictionary where the key is the string and the value is the Keycode
# This is used to convert the keys from the JSON file to Keycodes
# This helps you to use the string representation of the key in the JSON file
# instead of the Keycode value
KEYCODE_MAP = {
    "A": Keycode.A,
    "B": Keycode.B,
    "C": Keycode.C,
    "D": Keycode.D,
    "E": Keycode.E,
    "F": Keycode.F,
    "G": Keycode.G,
    "H": Keycode.H,
    "I": Keycode.I,
    "J": Keycode.J,
    "K": Keycode.K,
    "L": Keycode.L,
    "M": Keycode.M,
    "N": Keycode.N,
    "O": Keycode.O,
    "P": Keycode.P,
    "Q": Keycode.Q,
    "R": Keycode.R,
    "S": Keycode.S,
    "T": Keycode.T,
    "U": Keycode.U,
    "V": Keycode.V,
    "W": Keycode.W,
    "X": Keycode.X,
    "Y": Keycode.Y,
    "Z": Keycode.Z,
    "1": Keycode.ONE,
    "2": Keycode.TWO,
    "3": Keycode.THREE,
    "4": Keycode.FOUR,
    "5": Keycode.FIVE,
    "6": Keycode.SIX,
    "7": Keycode.SEVEN,
    "8": Keycode.EIGHT,
    "9": Keycode.NINE,
    "0": Keycode.ZERO,
    "CONTROL": Keycode.CONTROL,
    "ALT": Keycode.ALT,
    "SHIFT": Keycode.SHIFT,
    "TAB": Keycode.TAB,
    "ENTER": Keycode.ENTER,
    "ESCAPE": Keycode.ESCAPE,
    "SPACEBAR": Keycode.SPACEBAR,
    "BACKSPACE": Keycode.BACKSPACE,
    "DELETE": Keycode.DELETE,
    "UP_ARROW": Keycode.UP_ARROW,
    "DOWN_ARROW": Keycode.DOWN_ARROW,
    "LEFT_ARROW": Keycode.LEFT_ARROW,
    "RIGHT_ARROW": Keycode.RIGHT_ARROW,
    "F1": Keycode.F1,
    "F2": Keycode.F2,
    "F3": Keycode.F3,
    "F4": Keycode.F4,
    "F5": Keycode.F5,
    "F6": Keycode.F6,
    "F7": Keycode.F7,
    "F8": Keycode.F8,
    "F9": Keycode.F9,
    "F10": Keycode.F10,
    "F11": Keycode.F11,
    "F12": Keycode.F12
}

# Consumer Control Code map for the keyboard
CONSUMER_CONTROL_MAP = {
    "VOLUME_INCREMENT": ConsumerControlCode.VOLUME_INCREMENT,
    "VOLUME_DECREMENT": ConsumerControlCode.VOLUME_DECREMENT,
    "MUTE": ConsumerControlCode.MUTE,
    "PLAY_PAUSE": ConsumerControlCode.PLAY_PAUSE,
    "SCAN_NEXT_TRACK": ConsumerControlCode.SCAN_NEXT_TRACK,
    "SCAN_PREVIOUS_TRACK": ConsumerControlCode.SCAN_PREVIOUS_TRACK,
    "BRIGHTNESS_INCREMENT": ConsumerControlCode.BRIGHTNESS_INCREMENT,
    "BRIGHTNESS_DECREMENT": ConsumerControlCode.BRIGHTNESS_DECREMENT
}


# === Convert keys ===
# Convert the keys from the JSON file to Keycodes and ConsumerControlCodes
def convert_keys(json_keys):
    converted_keys = []
    for key in json_keys:

        if isinstance(key, int):
            print(f"⚠️ ERROR: Json File ({key}), something is wrong!") # Print an error message if the JSON still has numbers
        
        if key in KEYCODE_MAP:  
            converted_keys.append(KEYCODE_MAP[key])
        elif key in CONSUMER_CONTROL_MAP:
            converted_keys.append(CONSUMER_CONTROL_MAP[key])
        else:
            print(f"⚠️ ERROR: Key '{key}' not founded!")
    return converted_keys


# === Reverse lookup ===
# Convert the keycodes to the string representation
def reverse_lookup(value):
    for name, code in KEYCODE_MAP.items():
        if code == value:
            return name
    for name, code in CONSUMER_CONTROL_MAP.items():
        if code == value:
            return name
    return f"UNK({value})"
