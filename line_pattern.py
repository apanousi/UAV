#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from dronekit_sitl import SITL
from dronekit import Vehicle, VehicleMode, connect, LocationGlobalRelative

#Line pattern
def line(copters):
    #Overall pattern

    

    form_increasing_line(copters)
    return_center_all(copters)

    even_up(copters)
    form_increasing_line(copters)
    even_down(copters)
    even_up(copters)
    return_center_all(copters)

    move_down(copters[3], 2, 3)
    move_up(copters[0], 10, 0)
    move_up(copters[4], 10, 4)
    form_increasing_line(copters)

    return_center_all(copters)
    
    return 0;

def form_increasing_line(copters):
    move_up(copters[1], 1, 1)
    move_up(copters[2], 2, 2)
    move_up(copters[3], 3, 3)
    move_up(copters[4], 4, 4)

def even_up(copters):
    move_up(copters[0], 5, 0)
    move_up(copters[2], 5, 2)
    move_up(copters[4], 5, 4)

def even_down(copters):
    move_down(copters[0],5,0)
    move_down(copters[2],5,2)
    move_down(copters[4],5,4)

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

def move_down(copter, change, index):
    lat = copter.location.global_relative_frame.lat
    lon = copter.location.global_relative_frame.lon
    alt = copter.location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt - change)
    print_point(point, index)
    copter.simple_goto(point)
    time.sleep(1*change)

def print_point(point, index):
    print("Copter " + str(index) + " is at:")
    print(point)
