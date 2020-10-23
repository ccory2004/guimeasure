#Developed by Cory Chang
#For the Keithley 2400 instrument, used for longer term LED cycle testing
import tkinter as tk
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.adapters import VISAAdapter
import csv
import numpy as np
from time import sleep
from datetime import datetime
import matplotlib.pyplot as plt
#On Click Start
def start():
    #Connect and configure the instrument
    adapter = VISAAdapter("ASRL"+comentry.get()+"::INSTR")
    sm = Keithley2400(adapter)
    sm.reset()
    noteline.insert(0,"")
    noteline.insert(0, sm.id)
    sm.use_front_terminals()
    sm.write("system:rsense ON")
    sm.write("sens:curr:nplc 0.01")
    sm.measure_voltage()
    sleep(0.1)

    #Set Input Params based upon user input
    sm.apply_current()
    cycles = float(cyclesentry.get())
    standardcurrent = float(currententry.get())
    curtime = int(curtimeentry.get())
    mincurrent = float(mincurentry.get())
    mintime = float(mintimeentry.get())
    filename = csventry.get()
    sm.source_current_range = float(srcrngentry.get())
    sm.compliance_voltage = float(cmplentry.get())
    sm.source_current = 0
    sm.enable_source()

    # Create CSV file
    with open(filename, "w") as lol:
        pass

    # Begin testing sequence
    for i in range(int(cycles)):
        data = []
        mindata = []
        sm.ramp_to_current(standardcurrent, steps=3, pause=0.01)
        for j in range(curtime):
            data.append(sm.voltage)
            sleep(1)
        sm.ramp_to_current(mincurrent, steps=3, pause=0.01)
        mindata.append(sm.voltage)
        sleep(mintime)
        noteline.insert(0, "Cycle "+str(i+1)+" completed")
        with open(filename, "a", newline="") as dataset:
            writer = csv.writer(dataset, delimiter=",")
            writer.writerow(data)
        sm.reset_buffer()
    with open(filename, "a", newline="") as dataset:
        writer = csv.writer(dataset, delimiter=",")
        writer.writerow(mindata)
    sm.shutdown()
    noteline.insert(0, "Test Complete! Data located in the file "+filename)

# Graphs of dataset
def standardchart():
    filename = csventry.get()
    csvdata = np.genfromtxt(filename, delimiter=',')
    numcols = np.size(csvdata, 1)
    csvdata = np.delete(csvdata, numcols-1, axis=1)
    csvdata = csvdata.flatten().tolist()
    print(csvdata)
    xvalue = []
    for i in range(len(csvdata)):
        xvalue.append(i)
    plt.scatter(xvalue, csvdata)
    plt.show()

def minchart():
    filename = csventry.get()
    csvdata = np.genfromtxt(filename, delimiter=',')
    csvdata = csvdata[:,2]
    csvdata = csvdata.flatten().tolist()
    print(csvdata)
    xvalue = []
    for i in range(len(csvdata)):
        xvalue.append(i)
    plt.scatter(xvalue, csvdata)
    plt.show()

# On Click graph
def graph():
    graphWindow = tk.Toplevel(window)
    standardchartbtn = tk.Button(graphWindow, text="Standard Current Graph", command=standardchart)
    standardchartbtn.pack()
    minchartbtn = tk.Button(graphWindow, text="Minimum Current Graph", command=minchart)
    minchartbtn.pack()
#On Click Help
def help():
    helpWindow = tk.Toplevel(window)
    tk.Message(helpWindow, text="Ignore the Not Responding warning for the application. It is still measuring in the background. \n\nThe data is stored in a dataset.csv file located in the same directory. Each cycle is a new row, first 30 columns are standard current measurements, 31st column is minimum current measurement.\n\nUsing this application requires 4 modules outside of a standard Python installation: matplotlib, PyMeasure, PyVISA, and NI VISA(ni.com)\n\nThis application communicates to the Keithley 2400 through RS-232\n\nOne cycle is approximately 30 seconds. \n\nDeveloped by Cory Chang 2020").pack()

#GUI Interface
window = tk.Tk()
window.title("Keithley 2400")
window.geometry("500x300")
tk.Label(window, text="Cycle Testing").grid(column=0, row=0, columnspan=4)
tk.Label(window, text="COM Port: ").grid(column=0, row=1)
comentry = tk.Entry(window, width=15)
comentry.insert(0, "3")
comentry.grid(column=1, row=1)
tk.Label(window, text="Number of Cycles: ").grid(column=0, row=2)
cyclesentry = tk.Entry(window, width=15)
cyclesentry.insert(0, "2")
cyclesentry.grid(column=1, row=2)
tk.Label(window, text="Standard Current(meas. in A): ").grid(column=0, row=3)
currententry = tk.Entry(window, width=15)
currententry.insert(0, "0.350")
currententry.grid(column=1, row=3)
tk.Label(window, text="cycle time: ").grid(column=2, row=3)
curtimeentry = tk.Entry(window, width=15)
curtimeentry.insert(0, "30")
curtimeentry.grid(column=3, row=3)
tk.Label(window, text="Minimum Current(meas. in A): ").grid(column=0, row=4)
mincurentry = tk.Entry(window, width=15)
mincurentry.insert(0, "0.001")
mincurentry.grid(column=1, row=4)
tk.Label(window, text="cycle time: ").grid(column=2, row=4)
mintimeentry = tk.Entry(window, width=15)
mintimeentry.insert(0, "0.1")
mintimeentry.grid(column=3, row=4)
tk.Label(window, text="Source I Range(meas. in A): ").grid(column=0, row=5)
srcrngentry = tk.Entry(window, width=15)
srcrngentry.insert(0, "1")
srcrngentry.grid(column=1, row=5)
tk.Label(window, text="Compliance V Range(meas. in V): ", padx=15).grid(column=0, row=6)
cmplentry = tk.Entry(window, width=15)
cmplentry.insert(0, "21")
cmplentry.grid(column=1, row=6)
tk.Label(window, text="CSV filename: ", padx=15).grid(column=0, row=7)
csventry = tk.Entry(window, width=26)
csventry.insert(0, "dataset_"+datetime.now().strftime("%Y%m%d%H%M")+".csv")
csventry.grid(column=1, row=7, columnspan=2)
tk.Label(window).grid(row=8)
start = tk.Button(window, text="Start", height=1, width = 5, command=start)
start.grid(column=0, row=9)
graph = tk.Button(window, text="Graph", height=1, width = 5, command=graph)
graph.grid(column=1, row=9)
help = tk.Button(window, text="Help", height=1, width = 5, command=help)
help.grid(column=3, row=9)
tk.Label().grid(row=10)
noteline = tk.Entry(relief="groove", width=70)
noteline.insert(0, "Hit Start to begin testing")
noteline.grid(column=0, row=11, columnspan=4)
window.mainloop()
