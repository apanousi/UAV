from dronekit import Vehicle, LocationGlobalRelative
from ned_utilities import ned_controller
from flight_plotter import Location
import math

from get_dist import get_distance_meters

def point_on_circle(radius, angle_indegrees, latitude, longitude):
    # Convert from degrees to radians
    lon = (radius * math.cos(angle_indegrees * math.pi / 180)) + longitude
    lat = (radius * math.sin(angle_indegrees * math.pi / 180)) + latitude
    return Location(lat,lon)

def fly_to(vehicle, targetLocation, groundspeed):
    print("Flying from: " + str(vehicle.location.global_frame.lat) + "," + str(
        vehicle.location.global_frame.lon) + " to " + str(targetLocation.lat) + "," + str(targetLocation.lon))
    vehicle.groundspeed = groundspeed
    currentTargetLocation = targetLocation
    vehicle.simple_goto(currentTargetLocation)
    remainingDistance = get_distance_meters(currentTargetLocation, vehicle.location.global_frame)

    while vehicle.mode.name == "GUIDED":
        remainingDistance = get_distance_meters(currentTargetLocation, vehicle.location.global_frame)
        if remainingDistance < 1:
            print("Reached target")
            break
        time.sleep(1)


def flycircle(vehicleA, vehicleB, collision_pt, LocationA, LocationB):
    print("CIRCLING.....");
    # Get current location of vehicle and establish a conceptual circle around it for flying
    center = collision_pt #!!!!! COLLISON POINT 
    radius = get_distance_meters(LocationA, collision_pt) # !!!! SET TO DISTANCE

    # Get start angle for A & B
    [azA, elev, sR] = ned2aer(LocationA.north, LocationA.east, LocationA.down)
    print("azA is %d\n", azA)
    start_angleA = azA
    angleA = start_angleA

    [azB, elev, sR] = ned2aer(LocationB.north, LocationB.east, LocationB.down)
    print("azB is %d\n", azB)
    start_angleB = azB
    angleB = start_angleB


    # Fly to starting position using waypoint
    currentLocation = center
    #startingPos = point_on_circle(radius*.95, angle+1, center.lat, center.lon)  # Close to first position on circle perimeter
    startingPosA = LocationA
    startingPosB = LocationB
    #firstTargetPosition = LocationGlobalRelative(startingPos.lat, startingPos.lon, 10)
    #fly_to(vehicle, firstTargetPosition, 10)

    # Establish an instance of CoordinateLogger
    #log1 = CoordinateLogger()

    # Create a NedController
    #nedcontroller = ned_controller()
    waypoint_goto = False

    # Fly from one point on the circumference to the next
    while (angleA - start_angleA <= 180) and (angleB - start_angleB <=180): # !!! 180 compared to starting angle

        # For NED flying compute the NED Velocity vector for drone a and b
        print("\nA's New target " + str(angleA))
        nextTargetA = (point_on_circle(radius, angleA, center.lat, center.lon))
        currentLocationA = Location(vehicleA.location.global_relative_frame.lat, vehicleA.location.global_relative_frame.lon)
        distance_to_targetA = get_distance_meters(currentLocationA, nextTargetA)
        closestDistanceA = distance_to_targetA
        nedA = nedcontroller.setNed(currentLocationA, nextTargetA)

        print("\nB's New target " + str(angleB))
        nextTargetB = (point_on_circle(radius, angleB, center.lat, center.lon))
        currentLocationB = Location(vehicleB.location.global_relative_frame.lat, vehicleB.location.global_relative_frame.lon)
        distance_to_targetB = get_distance_meters(currentLocationB, nextTargetB)
        closestDistanceB = distance_to_targetB
        nedB = nedcontroller.setNed(currentLocationB, nextTargetB)


        # Keep going until target is reached
        while distance_to_targetA > 1 and distance_to_targetB > 1:
            currentLocationA = Location(vehicleA.location.global_relative_frame.lat,
                                       vehicleA.location.global_relative_frame.lon)
            currentLocationB = Location(vehicleB.location.global_relative_frame.lat,
                                       vehicleB.location.global_relative_frame.lon)

            distance_to_targetA = get_distance_meters(currentLocationA, nextTargetA)
            distance_to_targetB = get_distance_meters(currentLocationB, nextTargetB)
            print ('Current Pos of A: (' + str(currentLocationA.lat) + "," + str(currentLocationA.lon) +
                   ') Target Pos of A: ' + str(nextTargetA.lat) + ' Target  lon: ' + str(nextTargetA.lon) + ' Distance: ' + str(
                        distance_to_targetA) + " NED: " + str(nedA.north) + " " + str(nedA.east))

            print ('Current Pos of B: (' + str(currentLocationB.lat) + "," + str(currentLocationB.lon) +
                   ') Target Pos of B: ' + str(nextTargetB.lat) + ' Target  lon: ' + str(nextTargetB.lon) + ' Distance: ' + str(
                        distance_to_targetB) + " NED: " + str(nedB.north) + " " + str(nedB.east))

            if distance_to_targetA > closestDistanceA: #Prevent unwanted fly-by
                break
            else:
                closestDistanceA = distance_to_targetA

            if distance_to_targetB > closestDistanceB: #Prevent unwanted fly-by
                break
            else:
                closestDistanceB = distance_to_targetB

            # Needed if the ned vectors don't take you to the final target i.e.,
            # You'll need to create another NED.  You could reuse the previous one
            # but recomputing it can mitigate small errors which otherwise build up.

#Testing
LocationA = Location(41, -86.2)
LocationB = Location(41.0010, -86.2010)
collision = LocationGlobalRelative(41.0005, -88.2005)
#ans = flycircle(collision, LocationA, LocationB)
#print(ans)
