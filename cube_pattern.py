import time
from dronekit_sitl import SITL
from dronekit import Vehicle, VehicleMode, connect, LocationGlobalRelative
#from multiple_drones3 import copters
#CUBE pattern
def cube_pattern(copters):

    #initializing the starting point
    print("initializing the starting point")
    middle(copters, 0)
    top_left(copters,1)
    top_right(copters, 2)
    bottem_left(copters, 4)
    bottom_right(copters, 3)
    time.sleep(3)
    # 1     2
    #    0
    # 4     3

    # spinning clockwise based on drone[0]
    print("begin rotation")
    first_rotation(copters)
    second_rotation(copters)
    third_rotation(copters)
    fourth_rotation(copters)

    return 0





def middle(copters, index):
    lat = copters[0].location.global_relative_frame.lat
    lon = copters[0].location.global_relative_frame.lon
    alt = copters[0].location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt)
    copters[index].simple_goto(point)
    print("copter %d is at lat:%f lon:%f alt:%f" %(index,lat,lon,alt))
    time.sleep(10)



def top_left(copters, index):
    lat = copters[0].location.global_relative_frame.lat - 0.00005
    lon = copters[0].location.global_relative_frame.lon + 0.00005
    alt = copters[0].location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt)
    copters[index].simple_goto(point)
    print("copter %d is at lat:%f lon:%f alt:%f" %(index,lat,lon,alt))
    time.sleep(10)


def top_right(copters, index):
    lat = copters[0].location.global_relative_frame.lat + 0.00005
    lon = copters[0].location.global_relative_frame.lon + 0.00005
    alt = copters[0].location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt)
    copters[index].simple_goto(point)
    print("copter %d is at lat:%f lon:%f alt:%f" %(index,lat,lon,alt))
    time.sleep(10)


def bottem_left(copters, index):
    lat = copters[0].location.global_relative_frame.lat - 0.00005
    lon = copters[0].location.global_relative_frame.lon - 0.00005
    alt = copters[0].location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt)
    copters[index].simple_goto(point)
    print("copter %d is at lat:%f lon:%f alt:%f" %(index,lat,lon,alt))    
    time.sleep(10)


def bottom_right(copters, index):
    lat = copters[0].location.global_relative_frame.lat + 0.00005
    lon = copters[0].location.global_relative_frame.lon - 0.00005
    alt = copters[0].location.global_relative_frame.alt
    point = LocationGlobalRelative(lat, lon, alt)
    copters[index].simple_goto(point)
    print("copter %d is at lat:%f lon:%f alt:%f" %(index,lat,lon,alt))
    time.sleep(10)


def first_rotation(copters):
    #spin first quarter (clockwise)
    print("begin first rotation")
    top_right(copters, 1)
    bottom_right(copters, 2)
    bottem_left(copters, 3)
    top_left(copters, 4)
    time.sleep(3)
    # 4     1
    #    0
    # 3     2

def second_rotation(copters):
    #spin second quarter (clockwise)
    print("begin second rotation")
    top_right(copters, 4)
    bottom_right(copters, 1)
    bottem_left(copters, 2)
    top_left(copters, 3)
    time.sleep(3)
    # 3     4
    #    0
    # 2     1

def third_rotation(copters):
    #spin third quarter (clockwise)
    print("begin third rotation")
    top_right(copters, 3)
    bottom_right(copters, 4)
    bottem_left(copters, 1)
    top_left(copters, 2)
    time.sleep(3)
    # 2     3
    #    0
    # 1     4

def fourth_rotation(copters):
    #spin fourth quarter (clockwise)
    print("begin fourth rotation")
    top_left(copters, 1)
    top_right(copters, 2)
    bottem_left(copters, 4)
    bottom_right(copters, 3)
    time.sleep(3)
    # 1     2
    #    0
    # 4     3


