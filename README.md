# DIY Macropad with CircuitPython and Franzininho WiFi LAB01

## **Introduction**

A **shortcut keyboard**, also known as a **macropad**, is an input device with a set of **programmable keys** designed to execute specific functions or shortcuts. These keys can be configured to open programs, run macros, insert text, control volume, adjust brightness, and perform various other computer functions.

These devices are extremely useful for **video, audio, and image editors, as well as gamers**, as they allow **frequent tasks to be executed quickly**, without the need to access menus or use complex shortcuts. Additionally, they can be used to **automate repetitive tasks and increase productivity**.

Today, with access to **maker boards** such as **Arduino** and **Franzininho WiFi**, it is possible to **create a functional and fully customizable macropad**. It can also be **adapted for individuals with motor limitations**, using larger, spaced-out keys or alternative activation methods.

This project presents a **programmable macropad using Franzininho WiFi LAB01** and **CircuitPython**. The macropad **automates keyboard shortcuts and multimedia commands**, making it an excellent tool for **developers, video editors, designers, and gamers**.

Additionally, the **OLED display shows the active profile, temperature, and humidity**, adding extra functionality to the project.

## **Circuit**

To facilitate the development and daily use of the macropad, I used the **Franzininho WiFi LAB01**, which already includes **all the necessary resources (and more)** for the project.



## **Main Features**

- **6 programmable buttons** for customizable shortcuts.
- **Dynamic profile switching** without the need to restart.
- **Support for multimedia commands**, such as volume, brightness, and media control.
- **OLED display showing** the **active profile, temperature, and humidity**.
- **Audible feedback with a buzzer** to indicate actions.
- **Animated RGB LED** for dynamic visual effects.
- **Night mode based on LDR sensor**, adjusting OLED brightness automatically.
- **Support for combined keys**, such as `ALT + TAB`, `CTRL + C`, and others.


## **Required Libraries**

For the code to work correctly on **CircuitPython**, some **libraries** need to be installed in the **`lib/`** folder on **Franzininho WiFi LAB01**.

**Download the CircuitPython Libraries Bundle:**  
Download Libraries

### **Files required in the `lib/` folder**

1. **HID Libraries (Keyboard and Media Controls):**
    
    - `adafruit_hid/` (full folder)
2. **OLED Display Library (SSD1306 via I2C):**
    
    - `adafruit_ssd1306.mpy`
    - `fonts/font5x8.bin` (**Required for text display on OLED**)
3. **Temperature and Humidity Sensor Library (DHT11):**
    
    - `adafruit_dht.mpy`
4. **PWM Control Library (RGB LED and Buzzer):**
    
    - **Already included in CircuitPython by default.**
5. **Analog Input Handling Library (LDR Sensor):**
    
    - **Already included in CircuitPython by default.**

**Installation Steps:**

1. **Download the compatible library bundle for your CircuitPython version.**
2. **Extract the listed files.**
3. **Copy them to the `lib/` folder on the Franzininho WiFi LAB01.**
4. **Restart the board and run the code.**

## **Source Code**

This project is **open-source** and was developed using **CircuitPython**.

The code is divided into:

- `code.py` – Main code, responsible for button logic, profiles, OLED display, and visual/audio feedback.
- `keymap.py` – Key mapping and multimedia commands.
- `profiles.json` – Configuration file for customized key profiles.

## **How to Set Up and Use**

### **1. Set Up CircuitPython**

1. **Download and install CircuitPython** on **Franzininho WiFi LAB01**.
2. **Copy the complete project to the board** (including the libraries).

### **2. Create Custom Profiles**

Edit the **`profiles.json`** file to configure **new shortcuts**.

### **3. Switch Profiles**

- **Press and hold button 1 for 2 seconds** to switch between configured profiles.
- The **OLED display will show the active profile, temperature, and humidity**.

### **4. Test the Shortcuts**

- Press the buttons and see the shortcuts working on your computer.
- To test the commands, use an **online keyboard tester**, such as [Keyboard Event Viewer](https://keyboardchecker.com/).

