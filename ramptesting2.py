#Developed by Cory Chang
#For the Keithley 2400 instrument, used for longer term LED cycle testing
import pyvisa
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.adapters import VISAAdapter
import csv
import numpy as np
from time import sleep
from datetime import datetime

#Define variables for startup
print("Ramp Testing Version 2")
comPort = input("Enter the COM Port of the device: ")
stepCurr = []
stepVolt = []
srcCurrRng = float(input("Define the Source Current Range: "))
cmplVolt = float(input("Define the Compliance Voltage: "))
stepsNum = int(input("Enter the number of steps: "))
for i in range(stepsNum):
    stepCurr.append(float(input("Enter the current for step #"+str(i)+": ")))

#Instantiate the device
adapter = VISAAdapter("ASRL"+comPort+"::INSTR")
sm = Keithley2400(adapter)
sm.reset()
print(sm.id)
sm.use_front_terminals()
sm.write("system:rsense ON")
sm.write("sens:curr:nplc 0.01")
sm.measure_voltage()
sleep(0.1)

sm.apply_current()
standardcurrent = float(currententry.get())
filename = "dataset_"+datetime.now().strftime("%Y%m%d%H%M")+".csv"
sm.source_current_range = srcCurrRng
sm.compliance_voltage = cmplVolt
sm.source_current = 0
sm.enable_source()

# Create CSV file
with open(filename, "w") as lol:
    pass

#Begin the testing
for i in range(stepsNum):
    sm.ramp_to_current(stepCurr[i], steps=3, pause=0.01)
    stepVolt.append(sm.voltage)
with open(filename, "a", newline="") as dataset:
    writer = csv.writer(dataset, delimiter=",")
    writer.writerow(data)
sm.shutdown()
print("Testing complete! Data located in the file "+filename)
