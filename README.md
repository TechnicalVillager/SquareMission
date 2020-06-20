# SquareMission

    #...........................................................................
    # Author: Saiffullah Sabir Mohamed
    # Email:  saif25596@gmail.com
    # Github: https://github.com/TechnicalVillager
    #...........................................................................


USAGE: 

    $ ./square_mission.sh
    
How to Run:

    After executing the shell square_mission.sh script command in Terminal, user 
    needs to enter the altitude and side length required for the mission.

first_flight.py:           

    #............................................................................
    # Purpose: This is main function. As per the Assignment, to make the drone 
    #          takeoff at 5m, move in asquare trajectory of side length 6.5m at 
    #          height 5m and land once the entire mission is over.
    # 
    # Details: Once after this function is executed it will generate the square 
    #          mission by setting waypoints in the order of
    #              WP 1           -->     TAKEOFF
    #              WP 2,3,4       -->     waypoints of square mission
    #              WP 5           -->     LAND
    #
    # Format: simple_mission(altitude = 10, side_length = 7.5)
    #
    # Inputs: 
    #              altitude        -->     Altitude
    #              side_length     -->     Side length of square mission
    #.............................................................................
    
    
    USAGE: 
          python first_flight.py param1 param2

          where,
                param1 - Altitude
                param2 - Side Length
