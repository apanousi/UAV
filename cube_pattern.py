import time
import math
from dronekit_sitl import SITL
from dronekit import Vehicle, VehicleMode, connect, LocationGlobalRelative
#from multiple_drones3 import copters

def reached_point(waypoint, copters, index):
    # radius of earth in km
    R = 6373.0

    drone_lat = math.radians(copters[index].location.global_relative_frame.lat)
    drone_lon = math.radians(copters[index].location.global_relative_frame.lon)

    lat = math.radians(waypoint[0])
    lon = math.radians(waypoint[1])

    dlat = lat - drone_lat
    dlon = lon - drone_lon

    a = math.sin(dlat / 2)**2 + math.cos(drone_lat) * math.cos(lat) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # distance between points in meters
    distance = (R * c) * 1000
    print("Distance to waypoint: %.2f m" % distance)
    if distance <= 1:
        return True
    else:
        return False

#CUBE pattern
def cube_pattern(copters):

    #initializing the starting point
    print("initializing the starting point")
    mid = middle(copters, 0)
    top_l = top_left(copters, 1)
    top_r = top_right(copters, 2)
    bottom_l = bottom_left(copters, 4)
    bottom_r = bottom_right(copters, 3)

    while (mid is False) or (top_l is False) or (top_r is False) or (bottom_l is False) or (bottom_r is False):
        mid = middle(copters, 0)
        top_l = top_left(copters, 1)
        top_r = top_right(copters, 2)
        bottom_l = bottom_left(copters, 4)
        bottom_r = bottom_right(copters, 3)
        print("-----")
        time.sleep(3)
    
    print("reached starting point")

    # middle(copters, 0)
    # top_left(copters,1)
    
    # time.sleep(3)
    # 1     2
    #    0
    # 4     3

    # spinning clockwise based on drone[0]
    # print("begin rotation")
    # first_rotation(copters)
    # second_rotation(copters)
    # third_rotation(copters)
    # fourth_rotation(copters)

    return 0

def middle(copters, index):
    lat = copters[0].location.global_relative_frame.lat
    lon = copters[0].location.global_relative_frame.lon
    #alt = copters[0].location.global_relative_frame.alt
    point = [lat, lon]
    
    reached = reached_point(point, copters, index)
    copters[index].simple_goto(LocationGlobalRelative(point[0], point[1], 10))
    print("copter %d is at lat:%f lon:%f alt:%f" %(index,copters[index].location.global_relative_frame.lat,copters[index].location.global_relative_frame.lon,copters[index].location.global_relative_frame.alt))
    if reached is True:
        return True
    else:
        return False



def top_left(copters, index):
    lat = copters[0].location.global_relative_frame.lat - 0.00005
    lon = copters[0].location.global_relative_frame.lon + 0.00005
    #alt = copters[0].location.global_relative_frame.alt
    point = [lat, lon]

    reached = reached_point(point, copters, index)
    copters[index].simple_goto(LocationGlobalRelative(point[0], point[1], 10))
    print("copter %d is at lat:%f lon:%f alt:%f" %(index,copters[index].location.global_relative_frame.lat,copters[index].location.global_relative_frame.lon,copters[index].location.global_relative_frame.alt))
    if reached is True:
        return True
    else:
        return False
    
    # point = LocationGlobalRelative(lat, lon, alt)
    # copters[index].simple_goto(point)
    # print("copter %d is at lat:%f lon:%f alt:%f" %(index,lat,lon,alt))
    # time.sleep(10)


def top_right(copters, index):
    lat = copters[0].location.global_relative_frame.lat + 0.00005
    lon = copters[0].location.global_relative_frame.lon + 0.00005
    point = [lat, lon]

    reached = reached_point(point, copters, index)
    copters[index].simple_goto(LocationGlobalRelative(point[0], point[1], 10))
    print("copter %d is at lat:%f lon:%f alt:%f" %(index,copters[index].location.global_relative_frame.lat,copters[index].location.global_relative_frame.lon,copters[index].location.global_relative_frame.alt))
    if reached is True:
        return True
    else:
        return False


def bottom_left(copters, index):
    lat = copters[0].location.global_relative_frame.lat - 0.00005
    lon = copters[0].location.global_relative_frame.lon - 0.00005
    point = [lat, lon]

    reached = reached_point(point, copters, index)
    copters[index].simple_goto(LocationGlobalRelative(point[0], point[1], 10))
    print("copter %d is at lat:%f lon:%f alt:%f" %(index,copters[index].location.global_relative_frame.lat,copters[index].location.global_relative_frame.lon,copters[index].location.global_relative_frame.alt))
    if reached is True:
        return True
    else:
        return False


def bottom_right(copters, index):
    lat = copters[0].location.global_relative_frame.lat + 0.00005
    lon = copters[0].location.global_relative_frame.lon - 0.00005
    point = [lat, lon]

    reached = reached_point(point, copters, index)
    copters[index].simple_goto(LocationGlobalRelative(point[0], point[1], 10))
    print("copter %d is at lat:%f lon:%f alt:%f" %(index,copters[index].location.global_relative_frame.lat,copters[index].location.global_relative_frame.lon,copters[index].location.global_relative_frame.alt))
    if reached is True:
        return True
    else:
        return False


def first_rotation(copters):
    #spin first quarter (clockwise)
    print("begin first rotation")
    top_right(copters, 1)
    bottom_right(copters, 2)
    bottom_left(copters, 3)
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
    bottom_left(copters, 2)
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
    bottom_left(copters, 1)
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
    bottom_left(copters, 4)
    bottom_right(copters, 3)
    time.sleep(3)
    # 1     2
    #    0
    # 4     3


