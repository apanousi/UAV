#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from dronekit_sitl import SITL
from dronekit import Vehicle, VehicleMode, connect, LocationGlobalRelative
from flight_plotter import Location, CoordinateLogger, GraphPlotter
from ned_utilities import ned_controller
from generate_vc import generate_vc, check_crossingpoint
from collision_circle import flycircle
from get_dist import get_distance_meters
import matplotlib.pyplot as plt

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

# Starting coordinates
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

#########################################
#               Test 1                  #
#########################################

print("Test 1: Drones flying directly towards each other")
print("-------------------------------------------------")
time.sleep(5)

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
logA1 = CoordinateLogger()
logA1.add_data(startingLocationA.lat, startingLocationA.lon)
logB1 = CoordinateLogger()
logB1.add_data(startingLocationB.lat, startingLocationB.lon)



# ! this is where collision avoidance happens
print("Flying...")
currentLocationA = Location(droneA.location.global_relative_frame.lat, droneA.location.global_relative_frame.lon)
currentLocationB = Location(droneB.location.global_relative_frame.lat, droneB.location.global_relative_frame.lon)

willCollide = True
distCollide = 0

# get point of collision if they will collide
#if check_crossingpoint(startingLocationA, startingLocationB, targetLocationA, targetLocationB):
#    collision_point = generate_vc(startingLocationA, startingLocationB, targetLocationA, targetLocationB, droneA.location.global_relative_frame.alt)
if check_crossingpoint(coordinates[0], coordinates[1], coordinates[1], coordinates[0]):
    collision_point = generate_vc(coordinates[0], coordinates[1], coordinates[1], coordinates[0], droneA.location.global_relative_frame.alt)

else: #no collision
    collision_point = -1

#if collision_point == -1:    
    #willCollide = False    uncomment once other working

#TEMPORARY!!!!!
#print(collision_point)
#collision_point = Location(41.715171, -86.242484)
#print("It will collide? - %b\n", willCollide)


while (get_distance_meters(currentLocationA, targetLocationA) > .05) and (get_distance_meters(currentLocationB,targetLocationB ) > .05):
    currentLocationA = Location(droneA.location.global_relative_frame.lat, droneA.location.global_relative_frame.lon)
    currentLocationB = Location(droneB.location.global_relative_frame.lat, droneB.location.global_relative_frame.lon)
    distance_to_targetA = get_distance_meters(currentLocationA, targetLocationA)
    distance_to_targetB = get_distance_meters(currentLocationB, targetLocationB)
    
    #ned and check if about to collide 
    if(willCollide):
        distCollide = get_distance_meters(currentLocationA, collision_point)
        print("Collision Distance is %.6f\n" % distCollide)

    if(willCollide == False or distCollide > 10): #not collide yet or already collided 
        nedA = nedcontroller.setNed(currentLocationA, targetLocationA)
        nedB = nedcontroller.setNed(currentLocationB, targetLocationB)
        nedcontroller.send_ned_velocity(nedA.north, nedA.east, nedA.down, 1, droneA)
        nedcontroller.send_ned_velocity(nedB.north, nedB.east, nedB.down, 1, droneB)
    else: #Too close to intersection point
        print("Start avoiding collision")
        #Stop both - not necessary
        #nedcontroller.send_ned_velocity(0,0,0,1,droneA)
        #nedcontroller.send_ned_velocity(0,0,0,1,droneB)
        #nedcontroller.send_ned_stop(droneA)
        #nedcontroller.send_ned_stop(droneB)

        #Circle around
        flycircle(droneA, droneB, collision_point, currentLocationA, currentLocationB, nedA, nedB)

        # go north
        #newCoord = Location(currentLocationA.lat + .005, currentLocationA.lon)
        #nedA = nedcontroller.setNed(currentLocationA, newCoord)
        #nedcontroller.send_ned_velocity(nedA.north, nedA.east, nedA.down, 1, droneA);


        willCollide = False


    # add points to plot
    logA1.add_data(currentLocationA.lat, currentLocationA.lon)
    logB1.add_data(currentLocationB.lat, currentLocationB.lon)
    
    print('Drone A:\n\tDistance:  {0}  Ground speed:  {1}  Lat:  {2}  Lon:   {3}'.format(distance_to_targetA, droneA.groundspeed, currentLocationA.lat, currentLocationA.lon))
    print('Drone B:\n\tDistance:  {0}  Ground speed:  {1}  Lat:  {2}  Lon:   {3}'.format(distance_to_targetB, droneB.groundspeed, currentLocationB.lat, currentLocationB.lon))
    print("-----")

#########################################
#               Test 2                  #
#########################################

print("Test 2: Drones flying in parallel")
print("-------------------------------------------------")
time.sleep(5)

# start: different latitudes, same longitudes as each other
# target: same latitude, different longitudes as self

# drone A
startA = [droneA.location.global_relative_frame.lat, droneA.location.global_relative_frame.lon, 10]
startingLocationA = Location(droneA.location.global_relative_frame.lat, droneA.location.global_relative_frame.lon)

# send drone B to start position
startB = [startA[0], startA[1] + .00005, startA[2]]
startingLocationB = Location(droneB.location.global_relative_frame.lat, droneB.location.global_relative_frame.lon)
dist_start = get_distance_meters(droneB.location.global_relative_frame, LocationGlobalRelative(startB[0], startB[1], startB[2]))
print("Sending drone B to starting point...")
while dist_start > 1:
    droneB.simple_goto(LocationGlobalRelative(startB[0], startB[1], 10))
    dist_start = get_distance_meters(droneB.location.global_relative_frame, LocationGlobalRelative(startB[0], startB[1], startB[2]))
    print("Distance: %.2f" % dist_start)
    time.sleep(5)

targetLocationA = LocationGlobalRelative(startA[0] + .0005, startA[1], startA[2])
totalDistanceA = get_distance_meters(startingLocationA, targetLocationA)
print("Distance to travel for drone A: " + str(totalDistanceA))

# drone B
startingLocationB = Location(droneB.location.global_relative_frame.lat, droneB.location.global_relative_frame.lon)
targetLocationB = LocationGlobalRelative(startB[0] + .0005, startB[1], startB[2])
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
logA2 = CoordinateLogger()
logA2.add_data(startingLocationA.lat, startingLocationA.lon)
logB2 = CoordinateLogger()
logB2.add_data(startingLocationB.lat, startingLocationB.lon)

# ! this is where collision avoidance happens
print("Flying...")
currentLocationA = Location(droneA.location.global_relative_frame.lat, droneA.location.global_relative_frame.lon)
currentLocationB = Location(droneB.location.global_relative_frame.lat, droneB.location.global_relative_frame.lon)

willCollide = True
distCollide = 0

# get point of collision if they will collide
#if check_crossingpoint(startingLocationA, startingLocationB, targetLocationA, targetLocationB):
#    collision_point = generate_vc(startingLocationA, startingLocationB, targetLocationA, targetLocationB, droneA.location.global_relative_frame.alt)
if check_crossingpoint(coordinates[0], coordinates[1], coordinates[1], coordinates[0]):
    collision_point = generate_vc(coordinates[0], coordinates[1], coordinates[1], coordinates[0], droneA.location.global_relative_frame.alt)

else: #no collision
    collision_point = -1

#if collision_point == -1:    
    #willCollide = False    uncomment once other working

#TEMPORARY!!!!!
#print(collision_point)
#collision_point = Location(41.715171, -86.242484)
#print("It will collide? - %b\n", willCollide)


while (get_distance_meters(currentLocationA, targetLocationA) > 1) and (get_distance_meters(currentLocationB,targetLocationB ) > 1):
    currentLocationA = Location(droneA.location.global_relative_frame.lat, droneA.location.global_relative_frame.lon)
    currentLocationB = Location(droneB.location.global_relative_frame.lat, droneB.location.global_relative_frame.lon)
    distance_to_targetA = get_distance_meters(currentLocationA, targetLocationA)
    distance_to_targetB = get_distance_meters(currentLocationB, targetLocationB)
    
    #ned and check if about to collide 
    if(willCollide):
        distCollide = get_distance_meters(currentLocationA, collision_point)
        print("Collision Distance is %.6f\n" % distCollide)

    if(willCollide == False or distCollide > 10): #not collide yet or already collided 
        nedA = nedcontroller.setNed(currentLocationA, targetLocationA)
        nedB = nedcontroller.setNed(currentLocationB, targetLocationB)
        nedcontroller.send_ned_velocity(nedA.north, nedA.east, nedA.down, 1, droneA)
        nedcontroller.send_ned_velocity(nedB.north, nedB.east, nedB.down, 1, droneB)
    else: #Too close to intersection point
        print("Start avoiding collision")
        #Stop both - not necessary
        #nedcontroller.send_ned_velocity(0,0,0,1,droneA)
        #nedcontroller.send_ned_velocity(0,0,0,1,droneB)
        #nedcontroller.send_ned_stop(droneA)
        #nedcontroller.send_ned_stop(droneB)

        #Circle around
        flycircle(droneA, droneB, collision_point, currentLocationA, currentLocationB, nedA, nedB)

        # go north
        #newCoord = Location(currentLocationA.lat + .005, currentLocationA.lon)
        #nedA = nedcontroller.setNed(currentLocationA, newCoord)
        #nedcontroller.send_ned_velocity(nedA.north, nedA.east, nedA.down, 1, droneA);


        willCollide = False


    # add points to plot
    logA2.add_data(currentLocationA.lat, currentLocationA.lon)
    logB2.add_data(currentLocationB.lat, currentLocationB.lon)
    
    print('Drone A:\n\tDistance:  {0}  Ground speed:  {1}  Lat:  {2}  Lon:   {3}'.format(distance_to_targetA, droneA.groundspeed, currentLocationA.lat, currentLocationA.lon))
    print('Drone B:\n\tDistance:  {0}  Ground speed:  {1}  Lat:  {2}  Lon:   {3}'.format(distance_to_targetB, droneB.groundspeed, currentLocationB.lat, currentLocationB.lon))
    print("-----")


# Land them
land_drones()

# Close all vehicles
for c in copters:
  c.close()

# Shut down simulators
for s in sitls:
    s.stop()

# plot graph 1
f = plt.figure(1)
plotter1 = GraphPlotter(logA1.lat_array, logA1.lon_array, logB1.lat_array, logB1.lon_array)
plotter1.scatter_plot()

# plot graph 2
g = plt.figure(2)
plotter2 = GraphPlotter(logA2.lat_array, logA2.lon_array, logB2.lat_array, logB2.lon_array)
plotter2.scatter_plot()

plt.show()
