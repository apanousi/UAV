
def flycircle(collision_pt, LocationA, LocationB):

    # Get current location of vehicle and establish a conceptual circle around it for flying
    center = Location(collision_pt) #!!!!! COLLISON POINT 
    radius = get_distance_meters(LocationA, collision_pt) # !!!! SET TO DISTANCE

    # Fly to starting position using waypoint
    currentLocation = center
    startingPos = point_on_circle(radius*.95, angle+1, center.lat, center.lon)  # Close to first position on circle perimeter
    firstTargetPosition = LocationGlobalRelative(startingPos.lat, startingPos.lon, 10)
    fly_to(vehicle, firstTargetPosition, 10)

    # Establish a starting angle to compute next position on circle
    start_angle = 0 # !!! Starting point on circle
    angle = start_angle

    # Establish an instance of CoordinateLogger
    log1 = CoordinateLogger()

    # Create a NedController
    nedcontroller = ned_controller()
    waypoint_goto = False

    # Fly from one point on the circumference to the next
    while angle - start_angle <= 180: # !!! 180 compared to starting angle

        # For NED flying compute the NED Velocity vector
        print("\nNew target " + str(angle))
        nextTarget = (point_on_circle(radius, angle, center.lat, center.lon))
        currentLocation = Location(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon)
        distance_to_target = get_distance_meters(currentLocation, nextTarget)
        closestDistance=distance_to_target
        ned = nedcontroller.setNed(currentLocation, nextTarget)

        # Keep going until target is reached
        while distance_to_target > 1:
            currentLocation = Location(vehicle.location.global_relative_frame.lat,
                                       vehicle.location.global_relative_frame.lon)
            distance_to_target = get_distance_meters(currentLocation, nextTarget)
            print ('Current Pos: (' + str(currentLocation.lat) + "," + str(currentLocation.lon) +
                   ') Target Pos: ' + str(nextTarget.lat) + ' Target  lon: ' + str(nextTarget.lon) + ' Distance: ' + str(
                        distance_to_target) + " NED: " + str(ned.north) + " " + str(ned.east))

            if distance_to_target > closestDistance: #Prevent unwanted fly-by
                break
            else:
                closestDistance = distance_to_target

            # Needed if the ned vectors don't take you to the final target i.e.,
            # You'll need to create another NED.  You could reuse the previous one
            # but recomputing it can mitigate small errors which otherwise build up.
