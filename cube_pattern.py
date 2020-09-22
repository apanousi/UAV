import time
from dronekit_sitl import SITL
from dronekit import Vehicle, VehicleMode, connect, LocationGlobalRelative

#CUBE pattern
def square(copters):
    middle(coptercopter[0])
    top_left(coptercopter[1])
    top_right(coptercopter[2])
    bottem_left(coptercopter[3])
    bottom_right((coptercopter[4]))

def middle(copter):
    lat = copter.location.global_relative_frame.lat
    lon = copter.location.global_relative_frame.lon
    alt = 10
    point = LocationGlobalRelative(lat, lon, alt)
    copter.simple_goto(point)
    timesleep(10)


def top_left(copter):
    lat = copter.location.global_relative_frame.lat - 0.00005
    lon = copter.location.global_relative_frame.lon + 0.00005
    alt = copter.location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt)
    copter.simple_goto(point)
    timesleep(10)


def top_right(copter):
    lat = copter.location.global_relative_frame.lat + 0.00005
    lon = copter.location.global_relative_frame.lon + 0.00005
    alt = copter.location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt)
    copter.simple_goto(point)
    timesleep(10)


def bottem_left(copter):
    lat = copter.location.global_relative_frame.lat - 0.00005
    lon = copter.location.global_relative_frame.lon - 0.00005
    alt = copter.location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt)
    copter.simple_goto(point)
    timesleep(10)


def bottom_right(copter):
    lat = copter.location.global_relative_frame.lat + 0.00005
    lon = copter.location.global_relative_frame.lon - 0.00005
    alt = copter.location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt)
    copter.simple_goto(point)
    timesleep(10)