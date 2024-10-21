import os
import glob
import time
import datetime
import csv
import argparse
import serial
import RPi.GPIO as GPIO
from threading import Thread
from heartrate_monitor import HeartRateMonitor

# Setup GPIO for the buzzer
buzzer_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Normal ranges
normal_heart_rate_range = (60, 100)  # Example normal heart rate range
normal_temp_range = (36.1, 37.2)     # Example normal temperature range in Celsius


# Temperature sensor class
class DS18B20:
    def __init__(self):
        self.base_dir = r'/sys/bus/w1/devices/28*'
        self.sensor_path = []
        self.sensor_name = []
        self.temps = []
        self.rows = []

    def find_sensors(self):
        self.sensor_path = glob.glob(self.base_dir)
        self.sensor_name = [path.split('/')[-1] for path in self.sensor_path]

    def strip_string(self, temp_str):
        i = temp_str.index('t=')
        if i != -1:
            t = temp_str[i + 2:]
            temp_c = float(t) / 1000.0
            temp_f = temp_c * (9.0 / 5.0) + 32.0
        return temp_c, temp_f

    def read_temp(self):
        tstamp = datetime.datetime.now()
        for sensor, path in zip(self.sensor_name, self.sensor_path):
            with open(path + '/w1_slave', 'r') as f:
                valid, temp = f.readlines()
            if 'YES' in valid:
                self.rows.append((tstamp, sensor) + self.strip_string(temp))
                time.sleep(2)
            else:
                time.sleep(0.2)

    def print_temps(self):
        print('-' * 90)
        for t, n, c, f in self.rows:
            print(f'Sensor: {n}  C={c:,.3f}  F={f:,.3f}  DateTime: {t}')

    def log_csv(self):
        with open('log.csv', 'a+') as log:
            writer = csv.writer(log)
            writer.writerows(self.rows)

    def clear_rows(self):
        self.rows.clear()

# Function to sound the buzzer
def sound_buzzer(duration):
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(buzzer_pin, GPIO.LOW)

# Function to read heart rate with buzzer functionality
def heart_rate_monitor(args):
    print('Heart Rate Sensor starting...')
    hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))
    last_heart_rate = None
    hrm.start_sensor()
    
    try:
        while True:
            current_heart_rate = hrm.get_current_heart_rate()  # Assuming this function exists
            
            # Print current heart rate for debugging
            print(f'Current Heart Rate: {current_heart_rate}')

            # Check if we have a valid heart rate
            if current_heart_rate is not None:
                if current_heart_rate != last_heart_rate:
                    sound_buzzer(0.5)  # Beep for 0.5 seconds on change
                    last_heart_rate = current_heart_rate

                if current_heart_rate < normal_heart_rate_range[0] or current_heart_rate > normal_heart_rate_range[1]:
                    sound_buzzer(2)  # Continuous beep for 2 seconds if out of range
                    time.sleep(2)  # To prevent multiple beeps
            time.sleep(1)  # Adjust as needed

    except KeyboardInterrupt:
        print('Heart Rate monitor interrupted.')

# Function to monitor temperature and beep accordingly
def temperature_monitor():
    s = DS18B20()
    s.find_sensors()
    
    normal_buzzer_interval = 2  # Interval for normal beeping (2 seconds)
    last_buzzer_time = time.time()
    
    while True:
        s.read_temp()
        s.print_temps()
        s.log_csv()
        
        # Get current time
        current_time = time.time()
        
        # Check for temperature out of range and beep accordingly
        for t, n, c, f in s.rows:
            # Print current temperature for debugging
            print(f'Current Temperature: {c}')
            
            if c > normal_temp_range[1]:
                print("Temperature exceeds normal range! Long beep initiated.")
                sound_buzzer(10)  # Long beep for 10 seconds
                time.sleep(10)    # Prevent multiple long beeps immediately
            else:
                # Normal operation: beep every 2 seconds
                if current_time - last_buzzer_time >= normal_buzzer_interval:
                    print("Normal temperature range, short beep.")
                    sound_buzzer(0.5)  # Short beep
                    last_buzzer_time = current_time
        
        s.clear_rows()
        time.sleep(1)  # Adjust as needed to avoid too frequent readings

# Function to read ECG values from Arduino
def read_ecg_values():
    ser = serial.Serial('/dev/ttyS0', 9600)
    while True:
        if ser.in_waiting > 0:
            ecg_value = ser.readline().decode('utf-8').rstrip()
            print(f'ECG Value: {ecg_value}')


if __name__ == "__main__":
    # Set up argument parser and start threads
    parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
    parser.add_argument("-r", "--raw", action="store_true",
                        help="print raw data instead of calculation result")
    parser.add_argument("-t", "--time", type=int, default=30,
                        help="duration in seconds to read from sensor, default 30")
    args = parser.parse_args()

    # Start heart rate monitor in a thread
    hr_thread = Thread(target=heart_rate_monitor, args=(args,))
    temp_thread = Thread(target=temperature_monitor)
    ecg_thread = Thread(target=read_ecg_values)  # Start ECG reading thread

    hr_thread.start()
    temp_thread.start()
    ecg_thread.start()  # Start the ECG reading thread

    hr_thread.join()  # Wait for heart rate thread to finish
    temp_thread.join()  # This runs indefinitely, so you'll need to stop it manually
    ecg_thread.join()  # This runs indefinitely, so you'll need to stop it manually

# Cleanup GPIO on exit
try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()
