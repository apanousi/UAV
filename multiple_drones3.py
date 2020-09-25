#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)
Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.
Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

import time
from dronekit_sitl import SITL
from dronekit import Vehicle, VehicleMode, connect, LocationGlobalRelative
from line_pattern import line
from cube_pattern import cube_pattern 
import matplotlib.pyplot as plt
import numpy as np

copters = []
sitls = []

def connect_virtual_vehicle(instance, home):
    sitl = SITL()
    sitl.download('copter', '3.3', verbose=True)
    instance_arg = '-I%s' %(str(instance))
    print("Drone instance is: %s" % instance_arg)
    home_arg = '--home=%s, %s,%s,180' % (str(home[0]), str(home[1]), str(home[2]))
    sitl_args = [instance_arg, '--model', 'quad', home_arg]
    sitl.launch(sitl_args, await_ready=True)
    tcp, ip, port = sitl.connection_string().split(':')
    port = str(int(port) + instance * 10)
    conn_string = ':'.join([tcp, ip, port])
    print('Connecting to vehicle on: %s' % conn_string)

    vehicle = connect(conn_string)
    vehicle.wait_ready(timeout=120)

    # Collections
    copters.append(vehicle)
    sitls.append(sitl)

def copters_armable():
    unarmed = False
    for c in copters:
        print ("Trying one")
        if (not c.is_armable):
             unarmed = True
        else:
            print ("Copter armed")
    time.sleep(3)
    return not unarmed

def copters_at_altitude(aTargetAltitude):
    while True:
        at_altitude = True
        ctr=1
        for c in copters:
            print ('Copter ID: {} at altitude {} '.format(ctr,str(c.location.global_relative_frame.alt))) 
            ctr = ctr + 1
            if (not c.location.global_relative_frame.alt >= aTargetAltitude * 0.95):
                at_altitude = False
        time.sleep(3)

        if at_altitude == True:
            print("All drones have reached their target altitudes")
            break     

def copters_arm():
    for c in copters:
        c.mode = VehicleMode("GUIDED")
        c.armed = True

    for c in copters:
        while not (c.armed):
            time.sleep(1)

def land_drones():
    for c in copters:
        c.mode = VehicleMode("LAND")
    print ("LANDING....")
    time.sleep(30)

def copters_armable():
 
    while True:
        unarmable = False
        for c in copters:
            if (not c.is_armable):
                unarmable = True
        time.sleep(3)

        if unarmable == False:
            break     


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    copters_armable()
 
    print("Arming motors")
    copters_arm()
  
    print("Vehicle armed!")

    print("All drones are now Taking off!")
    aTargetAltitude = 10
    for c in copters:
        c.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    print("Waiting for copters to ascend")
    copters_at_altitude(aTargetAltitude)

def travel_north(point1):
    for c in copters:
        c.simple_goto(point1) 
    time.sleep(20)

# Starting coordinates
coordinates = [41.714621, -86.241484,0]

# Copter list
for n in range(5):
    coordinates = [coordinates[0],coordinates[1]-(0.00005*n),coordinates[2]]
    connect_virtual_vehicle(n,coordinates)



# Arm and takeoff to 10 meters
arm_and_takeoff(10) 

# Fly North for 20 sec
#print("Going north for 20 seconds ...")
#point1 = LocationGlobalRelative(50, -86.241484,0)
#travel_north(point1)

# CONNECT TO PATTERNS
print("Starting Line Dancing Pattern")
return_line = line(copters)
if return_line[0] < 0:
    print("Error with line pattern")
    exit(1)
print("Finished Line Dancing Pattern")

# print("Starting Cube Pattern")
# return_cube = cube_pattern(copters)
# if return_cube[0] < 0:
#     print("Error with cube pattern")
#     exit(1)
# print("Finished Cube Pattern")

# Land them
land_drones()

# Close all vehicles
for c in copters:
  c.close()

# Shut down simulators
for s in sitls:
    s.stop()

indexes = [0, 1, 2, 3, 4]

# line plot
# f = plt.figure(1)

print(len(return_line[2]))
print(len(return_line[1]))
for i in indexes:
    plt.plot(return_line[2][i], return_line[1][i], label="Drone %d"%(i+1))
plt.xlabel("time in seconds")
plt.ylabel("altitude")

# cube plot
#g = plt.figure(2)
# for i in indexes:
#     plt.plot(return_cube[2][i], return_cube[1][i], label="Drone %d"%(i+1))
# plt.xlabel("longitude")
# plt.ylabel("latitude")

plt.show()
