#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from dronekit_sitl import SITL
from dronekit import Vehicle, VehicleMode, connect, LocationGlobalRelative
from flight_plotter import Location, CoordinateLogger, GraphPlotter
from ned_utilities import ned_controller
from math import sin, cos, atan2, radians, sqrt

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

# def copters_armable():
#     unarmed = False
#     for c in copters:
#         print ("Trying one")
#         if (not c.is_armable):
#              unarmed = True
#         else:
#             print ("Copter armed")
#     time.sleep(3)
#     return not unarmed

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

# def copters_arm():
#     for c in copters:
#         c.mode = VehicleMode("GUIDED")
#         c.armed = True

#     for c in copters:
#         while not (c.armed):
#             time.sleep(1)

def land_drones():
    for c in copters:
        c.mode = VehicleMode("LAND")
    print ("LANDING....")
    time.sleep(30)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    for c in copters:
        while not c.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)
    
    #print("home: " + str(vehicle.location.global_relative_frame.lat))
 
    print("Arming motors")
    for c in copters:
        c.mode = VehicleMode("GUIDED")
        c.armed = True

    # Confirm vehicle armed before attempting to take off
    for c in copters:
        while not c.armed:
            print(" Waiting for arming...")
            time.sleep(1)
  
    print("Vehicle armed!")

    print("All drones are now Taking off!")
    aTargetAltitude = 10
    for c in copters:
        c.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    print("Waiting for copters to ascend")
    while True:
        if (copters[0].location.global_relative_frame.alt >= .95 * aTargetAltitude) and (copters[1].location.global_relative_frame.alt >= .95 * aTargetAltitude):
            print("Reached target altitude")
            break  
        time.sleep(1)

def get_distance_meters(locationA, locationB):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(locationA.lat)
    lon1 = radians(locationA.lon)
    lat2 = radians(locationB.lat)
    lon2 = radians(locationB.lon)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = (R * c) * 1000

    # print("Distance (meters):", distance)
    return distance

# Starting coordinates
# TODO: get coordinates from user
coordinates = [[41.714621, -86.241484,0], [41.715721, -86.243484, 0]]

# Copter list
for n in range(2):
    connect_virtual_vehicle(n,coordinates[n])

# assigning variables to make life easier
droneA = copters[0]
droneB = copters[1]
startA = coordinates[0]
startB = coordinates[1]

# Arm and takeoff to 10 meters
arm_and_takeoff(10) 

# ! stuff happens

# TODO: will change when coordinates come from user
# drone A
startingLocationA = Location(droneA.location.global_relative_frame.lat, droneA.location.global_relative_frame.lon)
targetLocationA = LocationGlobalRelative(startB[0], startB[1], startB[2])
totalDistanceA = get_distance_meters(startingLocationA, targetLocationA)
print("Distance to travel for drone A: " + str(totalDistanceA))

# drone B
startingLocationB = Location(droneB.location.global_relative_frame.lat, droneB.location.global_relative_frame.lon)
targetLocationB = LocationGlobalRelative(startA[0], startA[1], startA[2])
totalDistanceB = get_distance_meters(startingLocationB, targetLocationB)
print("Distance to travel for drone B: " + str(totalDistanceB))

# Establish an instance of ned_controller
nedcontroller = ned_controller()

# Get the NED velocity vector mavlink message
nedA = nedcontroller.setNed(startingLocationA, targetLocationA)
nedB = nedcontroller.setNed(startingLocationB, targetLocationB)
nedcontroller.send_ned_velocity(nedA.north, nedA.east, nedA.down, 1, droneA)
nedcontroller.send_ned_velocity(nedB.north, nedB.east, nedB.down, 1, droneB)

# initialize plotting
logA = CoordinateLogger()
logA.add_data(startingLocationA.lat, startingLocationB.lon)
logB = CoordinateLogger()
logB.add_data(startingLocationB.lat, startingLocationB.lon)



# ! this is where collision avoidance happens
print("Flying...")
currentLocationA = Location(droneA.location.global_relative_frame.lat, droneA.location.global_relative_frame.lon)
currentLocationB = Location(droneB.location.global_relative_frame.lat, droneB.location.global_relative_frame.lon)
while (get_distance_meters(currentLocationA, targetLocationA) > .05) and (get_distance_meters(currentLocationB, targetLocationB) > .05):
    currentLocationA = Location(droneA.location.global_relative_frame.lat, droneA.location.global_relative_frame.lon)
    currentLocationB = Location(droneB.location.global_relative_frame.lat, droneB.location.global_relative_frame.lon)
    distance_to_targetA = get_distance_meters(currentLocationA, targetLocationA)
    distance_to_targetB = get_distance_meters(currentLocationB, targetLocationB)
    
    # add points to plot
    logA.add_data(currentLocationA.lat, currentLocationA.lon)
    logB.add_data(currentLocationB.lat, currentLocationB.lon)
    
    print('Drone A:\n\tDistance:  {0}  Ground speed:  {1}'.format(distance_to_targetA, droneA.groundspeed))
    print('\nDrone B:\n\tDistance:  {0}  Ground speed:  {1}'.format(distance_to_targetB, droneB.groundspeed))
    print("-----")

# Land them
land_drones()

# Close all vehicles
for c in copters:
  c.close()

# Shut down simulators
for s in sitls:
    s.stop()

# plot graph
plotter = GraphPlotter(logA.lat_array, logA.lon_array, logB.lat_array, logB.lon_array)
plotter.scatter_plot()
