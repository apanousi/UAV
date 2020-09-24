#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from dronekit_sitl import SITL
from dronekit import Vehicle, VehicleMode, connect, LocationGlobalRelative

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

    print("line pattern start")
    points = form_increasing_line(copters)
    for i in indexes:
        alts[i].append(points[i])
    count += 10
    seconds.append(count)

    return_center_all(copters)
    for i in indexes:
        alts[i].append(10)
    count += 6*5
    seconds.append(count)

    print("first pattern")
    points = even_up(copters)
    for i in indexes:
        alts[i].append(points[i])
    count += 15
    seconds.append(count)

    points = form_increasing_line(copters)
    for i in indexes:
        alts[i].append(points[i])
    count += 10
    seconds.append(count)

    points = even_down(copters)
    for i in indexes:
        alts[i].append(points[i])
    count += 15
    seconds.append(count)

    points = even_up(copters)
    for i in indexes:
        alts[i].append(points[i])
    count += 15
    seconds.append(count)

    return_center_all(copters)
    for i in indexes:
        alts[i].append(10)
    count += 6
    seconds.append(count)

    print("last pattern")
    alts[1].append(10)
    alts[2].append(10)
    alts[3].append(move_down(copters[3], 2, 3))
    alts[0].append(move_up(copters[0], 10, 0))
    alts[4].append(move_up(copters[4], 10, 4))
    count += 22
    seconds.append(count)
    points = form_increasing_line(copters)
    for i in indexes:
        alts[i].append(points[i])
    count += 10
    seconds.append(count)

    return_center_all(copters)
    for i in indexes:
        alts[i].append(10)
    count += 6*5
    seconds.append(count)

    print("line pattern done")
    
    return (0, alts, seconds)

def form_increasing_line(copters):
    points = []
    
    points.append(copters[0].location.global_relative_frame.alt)
    points.append(move_up(copters[1], 1, 1))
    points.append(move_up(copters[2], 2, 2))
    points.append(move_up(copters[3], 3, 3))
    points.append(move_up(copters[4], 4, 4))
    return points

def even_up(copters):
    points = []
    points.append(move_up(copters[0], 5, 0))
    points.append(copters[1].location.global_relative_frame.alt)
    points.append(move_up(copters[2], 5, 2))
    points.append(copters[3].location.global_relative_frame.alt)
    points.append(move_up(copters[4], 5, 4))
    return points

def even_down(copters):
    points = []
    points.append(move_down(copters[0],5,0))
    points.append(copters[1].location.global_relative_frame.alt)
    points.append(move_down(copters[2],5,2))
    points.append(copters[3].location.global_relative_frame.alt)
    points.append(move_down(copters[4],5,4))
    return points

def return_center(copter, index):
    lat = copter.location.global_relative_frame.lat
    lon = copter.location.global_relative_frame.lon
    alt = 10
    point = LocationGlobalRelative(lat, lon, alt)
    copter.simple_goto(point)
    print_point(point, index)
    time.sleep(6)

def return_center_all(copters):
    i = 0
    for c in copters:
        return_center(c, i)
        i=i+1

def move_up(copter, change, index):
    lat = copter.location.global_relative_frame.lat
    lon = copter.location.global_relative_frame.lon
    alt = copter.location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt + change)
    print_point(point, index)
    copter.simple_goto(point)
    time.sleep(1*change)
    return alt+change

def move_down(copter, change, index):
    lat = copter.location.global_relative_frame.lat
    lon = copter.location.global_relative_frame.lon
    alt = copter.location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt - change)
    print_point(point, index)
    copter.simple_goto(point)
    time.sleep(1*change)
    return alt-change

def print_point(point, index):
    print("Copter " + str(index) + " is at:")
    print(point)
