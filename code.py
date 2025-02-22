# Libraries
import time
import board
import digitalio
import usb_hid
import json
import storage
import busio
import adafruit_ssd1306
import adafruit_dht
import pwmio
import analogio
import keymap  

# === HID Initizalization ===
from adafruit_hid.keyboard import Keyboard                  # Keyboard
from adafruit_hid.consumer_control import ConsumerControl   # Consumer Control

# === OLED DISPLAY CONFIGURATION ===
i2c = busio.I2C(scl=board.IO9, sda=board.IO8)                   # I2C Bus for OLED Display)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)    # OLED Display initialization

# === BUZZER (Audio Feedback) ===   
buzzer = pwmio.PWMOut(board.IO17, duty_cycle=0, frequency=880)  # Buzzer initialization

# === BEEP FUNCTION ===
# Play a beep sound for a given time
def beep(t):
    buzzer.duty_cycle = 440
    time.sleep(t)
    buzzer.duty_cycle = 0

# === DTH11 Initialization ===
dht = adafruit_dht.DHT11(board.IO15)    

# === RGB LED initialization ===
led_red = pwmio.PWMOut(board.IO14, frequency=5000, duty_cycle=0)    # Red LED
led_green = pwmio.PWMOut(board.IO13, frequency=5000, duty_cycle=0)  # Green LED
led_blue = pwmio.PWMOut(board.IO12, frequency=5000, duty_cycle=0)   # Blue LED

# === RGB LED CONTROL ===
# Set the color of the RGB LED using values from 0 to 255
def set_rgb(r, g, b):    
    led_red.duty_cycle = int((r / 255) * 65535)
    led_green.duty_cycle = int((g / 255) * 65535)
    led_blue.duty_cycle = int((b / 255) * 65535)

# === RGB ANIMATION ===
# Play an animation on the RGB LED
def rgb_animation():
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    for color in colors:
        set_rgb(*color)
        time.sleep(0.2)
    set_rgb(0, 0, 0)

# === LDR (Light Sensor) init ===
ldr = analogio.AnalogIn(board.IO1)

# === Check if the environment is dark based on the LDR value ===
def is_dark():
    return ldr.value < 20000  # Adjust this value according to your environment

# === NIGHT MODE ===
# Enable night mode if the environment is dark
def apply_night_mode():
    if is_dark():
        oled.contrast(10)    # Low contrast for OLED
        set_rgb(50, 50, 50)  # Low brightness for RGB LED
    else:
        oled.contrast(255)    # High contrast for OLED
        set_rgb(255, 0, 255)  # High brightness for RGB LED // Pink

# === Keyboard and consumer control objects ===
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# === MACROPAD Button ===
keys = [
    digitalio.DigitalInOut(board.IO7),  # BT1 
    digitalio.DigitalInOut(board.IO6),  # BT2
    digitalio.DigitalInOut(board.IO5),  # BT3
    digitalio.DigitalInOut(board.IO4),  # BT4
    digitalio.DigitalInOut(board.IO3),  # BT5
    digitalio.DigitalInOut(board.IO2)   # BT6
]

# === Set the direction and pull for each key ===
for key in keys:
    key.direction = digitalio.Direction.INPUT
    key.pull = digitalio.Pull.UP

# === Profile file path ===
PROFILE_FILE = "/profiles.json"

# === Load profiles from a JSON file and convert to Keycodes ===
def load_profiles():
    try:
        with open(PROFILE_FILE, "r") as f:
            profiles_raw = json.load(f)
        
        profiles_converted = {}
        for profile_name, key_list in profiles_raw.items():
            profiles_converted[profile_name] = [keymap.convert_keys(keys) for keys in key_list]

        return profiles_converted
    except Exception as e:
        print(f"Error to load profiles: {e}")
        return {"Default": [[]] * 6}  


# === Load profiles and get the profile names ===
profiles = load_profiles()              # Load profiles from JSON file
profile_names = list(profiles.keys())   # Get the profile names
current_profile_index = 0               # Start with the first profile


# === PROFILE SWITCHING ===
# Switch the active profile by pressing the first button for 2 seconds
def switch_profile():
    global current_profile_index
    start_time = time.monotonic()
    
    while not keys[0].value:                                                            # While the button is pressed
        if time.monotonic() - start_time > 2:                                           # if the button is pressed for 2 seconds
            current_profile_index = (current_profile_index + 1) % len(profile_names)    # Switch to the next profile
            oled_display()                                                              # Update the OLED display                                             
            beep(0.1)                                                                   # Play a beep sound to indicate the profile change                        
            while not keys[0].value:                                                    # Wait until the button is released    
                pass
            return True                                                                 # return True if the button was pressed for 2 seconds
    return False                                                                        # if the button was not pressed for 2 seconds

# === Debounce and repeat variables ===
last_key_states = [True] * len(keys)    # button last state
key_press_times = [0] * len(keys)       # button press time
repeat_delay = 0.1                      # Initial delay before repeating (seconds)
repeat_rate = 0.005                     # Rate of repeating (seconds)

# === EXECUTE MACRO ===
# Execute the command configured for the pressed key, applying debounce and repetition
def execute_macro(key_index):
    global last_key_states, key_press_times

    current_state = keys[key_index].value   # Read the current state of the key
    now = time.monotonic()                  # Read the current time

    if current_state == False:                  # if the button is pressed
        if last_key_states[key_index]:          # if the button was not pressed before
            last_key_states[key_index] = False  # Set the button state to pressed
            key_press_times[key_index] = now    # Set the press time
            
            if key_index == 0:                  # If the first button is pressed
                if switch_profile():            # Switch the profile
                    return                      # If the button was pressed for 2 seconds, return
                                                # Otherwise, continue to process the key press
            profile = profile_names[current_profile_index]  # Get the active profile
            actions = profiles[profile][key_index]          # Get the actions for the pressed key

            beep(0.01) # Play a beep sound to indicate the key press
            print(f"Key {key_index + 1} pressed on profile {profile}: {actions}") # Print the key press for debugging

            if isinstance(actions, list) and len(actions) > 0:  # If there are actions to execute
                if all(action in keymap.CONSUMER_CONTROL_MAP.values() for action in actions):   # If all actions are ConsumerControlCode
                    print(f"🎵 ConsumerControlCode: {actions[0]}")     # Print for debuggind
                    cc.send(actions[0])                                # Send the ConsumerControlCode
                else:
                    print(f"⌨ Keycode: {actions}")                  # Print for debugging
                    kbd.send(*actions)                               # Send the Keycodes

        elif now - key_press_times[key_index] > repeat_delay:  # if the button was pressed before and the delay has passed
            if (now - key_press_times[key_index]) % repeat_rate < 0.01:  # if the time is a multiple of the repeat rate
                profile = profile_names[current_profile_index]          # Get the active profile
                actions = profiles[profile][key_index]                  # Get the actions for the pressed key

                print(f"🔄 Repeating command: {actions}")         # Print for debugging      
                beep(0.01)                                         # Play a beep sound to indicate the key press            
                if isinstance(actions, list) and len(actions) > 0:  # If there are actions to execute
                    if all(action in keymap.CONSUMER_CONTROL_MAP.values() for action in actions):   # If all actions are ConsumerControlCode
                        cc.send(actions[0])
                    else:
                        kbd.send(*actions)

    else:  # if the button is released
        if not last_key_states[key_index]:       # if the button was pressed before
            last_key_states[key_index] = True   # Set the button state to released
            print(f"⬆ Key {key_index + 1} released") # Print for debugging
            kbd.release_all()

# === OLED DISPLAY ===
# Display the active profile, temperature, and humidity on the OLED
def oled_display():
    oled.fill(0)    # Clear the OLED display
    oled.text(f"Profile: {profile_names[current_profile_index]}", 0, 0, 1)

    try:
        temp = dht.temperature
        humidity = dht.humidity
        if temp is not None and humidity is not None:
            oled.text(f"T: {temp:.1f} C", 0, 20, 1)
            oled.text(f"H: {humidity:.1f} %", 0, 30, 1)
    except RuntimeError:
        oled.text("Erro DHT", 0, 20, 1)

    oled.show() # Update the OLED display

rgb_animation() # Initial animation
oled_display()  # update OLED display

# === MAIN LOOP ===
while True:
    apply_night_mode()                  # verify if night mode should be enabled

    for i, key in enumerate(keys):      # Loop through all keys
        execute_macro(i)                # Process each key in the loop

    oled_display()                      # Update the OLED display
    time.sleep(0.01)                    # Polling interval
