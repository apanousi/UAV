#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import math
from dronekit_sitl import SITL
from dronekit import Vehicle, VehicleMode, connect, LocationGlobalRelative

def reached_point(alt, copter):
    drone_alt = copter.location.global_relative_frame.alt

    distance = math.sqrt((alt - drone_alt)**2)
    #print("Distance to waypoint: %.2f m" % distance)
    if distance <= 1:
        return True
    else:
        return False

#Line pattern
def line(copters):
    #Overall pattern

    alts = []
    seconds = []
    count = 0
    seconds.append(count)
    indexes = [0, 1, 2, 3, 4]
    for i in indexes:
        alts.append([])
    
    print("inc line 1")
    up1 = move_up(copters[1], 1, 1)
    up2 = move_up(copters[2], 2, 2)
    up3 = move_up(copters[3], 3, 3)
    up4 = move_up(copters[4], 4, 4)
    while (up1 is False) or (up2 is False) or (up3 is False) or (up4 is False):
        up1 = move_up(copters[1], 1, 1)
        up2 = move_up(copters[2], 2, 2)
        up3 = move_up(copters[3], 3, 3)
        up4 = move_up(copters[4], 4, 4)
        
        #plotting
        for i in indexes:
            alts[i].append(copters[i].location.global_relative_frame.alt)
        time.sleep(3)
        count += 3
        seconds.append(count)
    
    print("return center 1")
    c = return_center_all(copters)
    while (c is False):
        c = return_center_all(copters)

        for i in indexes:
            alts[i].append(copters[i].location.global_relative_frame.alt)
        time.sleep(3)
        count += 3
        seconds.append(count)
    
    print("even up 1")
    up0 = move_up(copters[0], 5, 0)
    up2 = move_up(copters[2], 5, 2)
    up4 = move_up(copters[4], 5, 4)
    while (up0 is False) or (up2 is False) or (up4 is False):
        up0 = move_up(copters[0], 5, 0)
        up2 = move_up(copters[2], 5, 2)
        up4 = move_up(copters[4], 5, 4)

        for i in indexes:
            alts[i].append(copters[i].location.global_relative_frame.alt)
        time.sleep(3)
        count += 3
        seconds.append(count)

    print("inc line 2")
    up1 = move_up(copters[1], 1, 1)
    up2 = move_up(copters[2], 2, 2)
    up3 = move_up(copters[3], 3, 3)
    up4 = move_up(copters[4], 4, 4)
    while (up1 is False) or (up2 is False) or (up3 is False) or (up4 is False):
        up1 = move_up(copters[1], 1, 1)
        up2 = move_up(copters[2], 2, 2)
        up3 = move_up(copters[3], 3, 3)
        up4 = move_up(copters[4], 4, 4)

        for i in indexes:
            alts[i].append(copters[i].location.global_relative_frame.alt)
        time.sleep(3)
        count += 3
        seconds.append(count)
    
    print("even down 1")
    down0 = move_down(copters[0],5,0)
    down2 = move_down(copters[2],5,2)
    down4 = move_down(copters[4],5,4)
    while (down0 is False) or (down2 is False) or (down4 is False):
        down0 = move_down(copters[0],5,0)
        down2 = move_down(copters[2],5,2)
        down4 = move_down(copters[4],5,4)

        for i in indexes:
            alts[i].append(copters[i].location.global_relative_frame.alt)
        time.sleep(3)
        count += 3
        seconds.append(count)
    
    print("even up 2")
    up0 = move_up(copters[0], 5, 0)
    up2 = move_up(copters[2], 5, 2)
    up4 = move_up(copters[4], 5, 4)
    while (up0 is False) or (up2 is False) or (up4 is False):
        up0 = move_up(copters[0], 5, 0)
        up2 = move_up(copters[2], 5, 2)
        up4 = move_up(copters[4], 5, 4)

        for i in indexes:
            alts[i].append(copters[i].location.global_relative_frame.alt)
        time.sleep(3)
        count += 3
        seconds.append(count)

    print("return center 2")
    c = return_center_all(copters)
    while (c is False):
        c = return_center_all(copters)

        for i in indexes:
            alts[i].append(copters[i].location.global_relative_frame.alt)
        time.sleep(3)
        count += 3
        seconds.append(count)
    
    print("random")
    down3 = move_down(copters[3], 2, 3)
    up0 = move_up(copters[0], 10, 0)
    up4 = move_up(copters[4], 10, 4)
    while (down3 is False) or (up0 is False) or (up4 is False):
        down3 = move_down(copters[3], 2, 3)
        up0 = move_up(copters[0], 10, 0)
        up4 = move_up(copters[4], 10, 4)
        for i in indexes:
            alts[i].append(copters[i].location.global_relative_frame.alt)
        time.sleep(3)
        count += 3
        seconds.append(count)

    print("last inc line")
    up1 = move_up(copters[1], 1, 1)
    up2 = move_up(copters[2], 2, 2)
    up3 = move_up(copters[3], 3, 3)
    up4 = move_up(copters[4], 4, 4)
    while (up1 is False) or (up2 is False) or (up3 is False) or (up4 is False):
        up1 = move_up(copters[1], 1, 1)
        up2 = move_up(copters[2], 2, 2)
        up3 = move_up(copters[3], 3, 3)
        up4 = move_up(copters[4], 4, 4)
        
        #plotting
        for i in indexes:
            alts[i].append(copters[i].location.global_relative_frame.alt)
        time.sleep(3)
        count += 3
        seconds.append(count)
    
    print("final return c")
    c = return_center_all(copters)
    while (c is False):
        c = return_center_all(copters)

        for i in indexes:
            alts[i].append(copters[i].location.global_relative_frame.alt)
        time.sleep(3)
        count += 3
        seconds.append(count)

    # print("inc line 1")
    # form_increasing_line(copters)
    # print("return center")
    # return_center_all(copters)

    # print("even up 1")
    # even_up(copters)
    # print("inc line 2")
    # form_increasing_line(copters)
    # print("even down 1")
    # even_down(copters)
    # print("even up 2")
    # even_up(copters)

    # return_center_all(copters)

    # move_down(copters[3], 2, 3)
    # move_up(copters[0], 10, 0)
    # move_up(copters[4], 10, 4)
    # form_increasing_line(copters)

    # return_center_all(copters)
    
    return (0, alts, seconds)

def form_increasing_line(copters):
    up1 = move_up(copters[1], 1, 1)
    up2 = move_up(copters[2], 2, 2)
    up3 = move_up(copters[3], 3, 3)
    up4 = move_up(copters[4], 4, 4)
    while (up1 is False) or (up2 is False) or (up3 is False) or (up4 is False):
        up1 = move_up(copters[1], 1, 1)
        up2 = move_up(copters[2], 2, 2)
        up3 = move_up(copters[3], 3, 3)
        up4 = move_up(copters[4], 4, 4)
    

def even_up(copters):
    up0 = move_up(copters[0], 5, 0)
    up2 = move_up(copters[2], 5, 2)
    up4 = move_up(copters[4], 5, 4)
    while (up0 is False) or (up2 is False) or (up4 is False):
        up0 = move_up(copters[0], 5, 0)
        up2 = move_up(copters[2], 5, 2)
        up4 = move_up(copters[4], 5, 4)

def even_down(copters):
    down0 = move_down(copters[0],5,0)
    down2 = move_down(copters[2],5,2)
    down4 = move_down(copters[4],5,4)
    while (down0 is False) or (down2 is False) or (down4 is False):
        down0 = move_down(copters[0],5,0)
        down2 = move_down(copters[2],5,2)
        down4 = move_down(copters[4],5,4)

def return_center(copter, index):
    lat = copter.location.global_relative_frame.lat
    lon = copter.location.global_relative_frame.lon
    alt = 10
    point = LocationGlobalRelative(lat, lon, alt)
    copter.simple_goto(point)
    print_point(point, index)
    reached = reached_point(alt, copter)
    if reached is True:
        return True
    else:
        return False
    #time.sleep(6)

def return_center_all(copters):
    i = 0
    reached = []
    for c in copters:
        reached.append(return_center(c, i))
        i=i+1
    if (reached[0] is True) and (reached[1] is True) and (reached[2] is True) and (reached[3] is True) and (reached[4] is True):
        return True
    else:
        return False 

def move_up(copter, change, index):
    lat = copter.location.global_relative_frame.lat
    lon = copter.location.global_relative_frame.lon
    alt = copter.location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt + change)
    print_point(point, index)
    copter.simple_goto(point)
    reached = reached_point(alt + change, copter)
    if reached is True:
        return True
    else:
        return False
    # time.sleep(1*change)

def move_down(copter, change, index):
    lat = copter.location.global_relative_frame.lat
    lon = copter.location.global_relative_frame.lon
    alt = copter.location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt - change)
    print_point(point, index)
    copter.simple_goto(point)
    reached = reached_point(alt - change, copter)
    if reached is True:
        return True
    else:
        return False
    #time.sleep(1*change)

def print_point(point, index):
    print("Copter " + str(index) + " is at:")
    print(point)
