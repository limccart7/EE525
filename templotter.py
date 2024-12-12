import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.signal import welch
import csv

# I used com7 use whatever you need
ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2) 

temperatures = []
timestamps = []

#collect data for 4 min for now
collect_duration = 4*60
start_time = time.time()


# Collect data for 60 seconds
while time.time() - start_time < collect_duration:
    data = ser.readline().decode('ascii').strip()  #serial data parse
    if "Temperature:" in data:
        temp_value = data.split(":")[1].strip()  
        
        try:
            temp = float(temp_value)  #string to float
            current_time = time.time() - start_time  #time for graph

            #add data
            temperatures.append(temp)
            timestamps.append(current_time)

            #print so im not going insane for a minute
            print(f"Time: {current_time:.2f}s, Temperature: {temp:.2f}°C")
        
        except ValueError:
            pass  #invalid data

ser.close()

with open('temperature_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time (s)', 'Temperature (°C)'])
    writer.writerows(zip(timestamps, temperatures))

if temperatures:
    #temp vs time to see temp change
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, temperatures, label='Temperature (°C)', color='b', marker='o')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature vs. Time')
    plt.grid(True)
    plt.legend()
    plt.show()

    #noise analysis
    temperatures = np.array(temperatures)
    noise = temperatures - np.mean(temperatures)  #0 mean

    #gaussian histogram to verify
    plt.figure(figsize=(10, 6))
    plt.hist(noise, bins=30, density=True, alpha=0.6, color='g')
    mu, std = norm.fit(noise)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    plt.title('Noise Histogram with Gaussian Fit')
    plt.xlabel('Noise (°C)')
    plt.ylabel('Density')
    plt.show()

    #PSD
    fs = 1 / np.mean(np.diff(timestamps))  # Sampling frequency
    frequencies, psd = welch(noise, fs=fs)

    plt.figure(figsize=(10, 6))
    plt.semilogy(frequencies, psd)
    plt.title('Power Spectral Density (PSD)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power Spectral Density (°C^2/Hz)')
    plt.grid(True)
    plt.show()

else:
    print("No data collected.")
