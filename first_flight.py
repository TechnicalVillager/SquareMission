#...........................................................................
# Author: Saiffullah Sabir Mohamed
# Email:  saif25596@gmail.com
# Github: https://github.com/TechnicalVillager
#...........................................................................

#!/usr/bin/env python
import math
import time
import sys
from flyt_python import api

# Initialize Vehicle
drone = api.navigation()

def destination_location(homeLatitude, homeLongitude, distance, bearing, alt):
    #...........................................................................
    # Purpose: This function returns the latitude and longitude of unknown
    #          position with known distance and bearing from current position.
    #
    # Format:  destination_location(18.5308934, 73.8545103, 50, 102, 25)
    #
    # Inputs:
    #           homeLatitude     -->     Latitude of home location
    #           homeLongitude    -->     Longitude of home location
    #           distance         -->     distance in meters
    #           bearing          -->     Bearing angle
    #
    # Outputs:
    #           [rlat, rlon, alt] --> Latitude, Longitude, Altitude
    #
    # Source: https://github.com/TechnicalVillager/distance-bearing-calculation
    #...........................................................................

    R = 6371e3 #Radius of earth in metres
    rlat1 = homeLatitude * (math.pi/180)
    rlon1 = homeLongitude * (math.pi/180)
    d = distance
    bearing = bearing * (math.pi/180) #Converting bearing to radians
    rlat2 = math.asin((math.sin(rlat1) * math.cos(d/R)) + (math.cos(rlat1) * math.sin(d/R) * math.cos(bearing)))
    rlon2 = rlon1 + math.atan2((math.sin(bearing) * math.sin(d/R) * math.cos(rlat1)) , (math.cos(d/R) - (math.sin(rlat1) * math.sin(rlat2))))
    rlat2 = rlat2 * (180/math.pi) #Converting to degrees
    rlon2 = rlon2 * (180/math.pi) #converting to degrees
    location = [rlat2, rlon2, alt]
    return location

def generate_waypoints(wp_list):
    #............................................................................
    # Purpose: This function generate waypoint in required format mentioned in
    #          the API Documentation.
    #
    # Format: generate_waypoints([wp1], [wp2],..., [wpn])
    #
    # Inputs:
    #              wp_list     -->     List of waypoints in lat, lon, alt format
    #
    # Outputs:
    #              wp_dict = { 'frame'        : 0,
    #                          'command'      : command,
    #                          'is_current'   : True,
    #                           'autocontinue' : True,
    #                          'param1'       : 1,
    #                          'param2'       : 0.25,
    #                          'param3'       : 0.25,
    #                          'param4'       : 0,
    #                          'x_lat'        : wp_list[wp-1][0],
    #                          'y_long'       : wp_list[wp-1][1],
    #                          'z_alt'        : wp_list[wp-1][2]
    #                        }
    # Note:
    #      1. In APM | SITL, two WP will be added additionally
    #      2. Please refer API Documentation for more details about this parameters
    #............................................................................

    final_wp = []
    for wp in range(1,len(wp_list)+1):
        command = 16
        if wp == 5:
            command = 21

        # Waypoint Format
        wp_dict = { 'frame'        : 3,
                    'command'      : command,
                    'is_current'   : True,
                    'autocontinue' : True,
                    'param1'       : 0,
                    'param2'       : 0,
                    'param3'       : 0,
                    'param4'       : 0,
                    'x_lat'        : wp_list[wp-1][0],
                    'y_long'       : wp_list[wp-1][1],
                    'z_alt'        : wp_list[wp-1][2]
                   }

        if wp == 1:
            command = [16, 22]
            for cmnd in command:
                if cmnd == 16:
                    frame, alt = 0, 100.0
                else:
                    frame, alt = 3, 1.0
                wp_dict2 = { 'frame'        : frame,
                             'command'      : cmnd,
                             'is_current'   : True,
                             'autocontinue' : True,
                             'param1'       : 0,
                             'param2'       : 0,
                             'param3'       : 0,
                             'param4'       : 0,
                             'x_lat'        : wp_list[wp-1][0],
                             'y_long'       : wp_list[wp-1][1],
                             'z_alt'        : alt
                            }
                final_wp.append(wp_dict2)
            final_wp.append(wp_dict)
        else:
            final_wp.append(wp_dict)
    return final_wp

def square_mission(alt = 0, side_length = 0):
    #............................................................................
    # Purpose: This function generate a square mission of required side length.
    #
    # Format:  square_mission(alt = 10, side_length = 7.5)
    #
    # Inputs:
    #              alt             -->     Altitude
    #              side_length     -->     Side length of square mission
    #............................................................................

    gpos = drone.get_global_position()
    origin = [gpos.lat, gpos.lon, alt]
    position1 = destination_location(homeLatitude = origin[0], homeLongitude = origin[1], distance = side_length, bearing = -90, alt=alt)
    position2 = destination_location(homeLatitude = position1[0], homeLongitude = position1[1], distance = side_length, bearing = 0, alt=alt)
    position3 = destination_location(homeLatitude = position2[0], homeLongitude = position2[1], distance = side_length, bearing = 90, alt=alt)
    position4 = origin
    waypoints = generate_waypoints([origin, position1, position2, position3, position4])
    drone.waypoint_set(waypoints)

def simple_mission(altitude = 5, side_length = 6.5):
    #............................................................................
    # Purpose: This is main function. As per the Assignment, to make the drone
    #          takeoff at 5m, move in asquare trajectory of side length 6.5m at
    #          height 5m and land once the entire mission is over.
    #
    # Details: Once after this function is executed it will generate the square
    #          mission by setting waypoints in the order of
    #                   WP 1        -->     TAKEOFF
    #                   WP 2,3,4    -->     waypoints of square mission
    #                   WP 5        -->     LAND
    #
    # Format: simple_mission(altitude = 10, side_length = 7.5)
    #
    # Inputs:
    #              altitude        -->     Altitude
    #              side_length     -->     Side length of square mission
    #............................................................................

    # wait for interface to initialize
    time.sleep(3.0)

    # Arm the Vehicle
    drone.arm()

    # Ensure Vehicle is armed
    if drone.is_armed() != False:
        print("ARMED")

    # set waypoints for square mission
    square_mission(alt = altitude, side_length = side_length)

    # get list of current waypoints
    waypoints = drone.waypoint_get()

    # Ensure waypoints are inserted properly
    if waypoints.get('wp_received') == 7:
        # In APM | SITL, two WP will be added additionally
        print('SUCCESS: WAYPOINTS INSERTED PROPERLY')

        # Execute the flight plan after inserting all the waypoints
        drone.waypoint_execute()
    mission_completed = False
    while mission_completed != True:
        print("WAITING: TO COMPLETE THE MISSION")
        if drone.get_vehicle_mode() == 'API|WAYPOINT':
            if drone.is_armed() != True:
                mission_completed = True

    if mission_completed != False:
        print("SUCCESS: MISSION COMPLETED")

        # shutdown the instance
        drone.disconnect()

# Executing main function
simple_mission(altitude = float(sys.argv[1]), side_length = float(sys.argv[2]))
