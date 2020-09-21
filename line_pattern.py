#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from dronekit_sitl import SITL
from dronekit import Vehicle, VehicleMode, connect, LocationGlobalRelative

#Line pattern
def line(copters):
    #Overall pattern
    move_up(copters[1])
    move_down(copters[1])
    return 0;

def move_up(copter):

    lat = copter.location.global_relative_frame.lat
    lon = copter.location.global_relative_frame.lon
    alt = copter.location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt + 5)
    print("New point is ")
    print(point)
    copter.simple_goto(point)
    time.sleep(5)

def move_down(copter):
    lat = copter.location.global_relative_frame.lat
    lon = copter.location.global_relative_frame.lon
    alt = copter.location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt - 5)
    print("New point is ")
    print(point)
    copter.simple_goto(point)
    time.sleep(5)

