# PARobot TCS Driver

Python3 based driver functions for TCP Command Server interface over TCP/IP Ethernet. For use with Precise Automation PreciseFlex robot arms with grippers and rails. 

## Import
	from PARobot_TCS import robot
	robot1 = robot.Robot()

## Examples
	robot1.close_gripper() # this will send a command to close the gripper
	robot1.teach_position("Station 1 Stage Pose") # this will start a routine to allow user to position the robot in a saved pose 

## To Do

* Save positions and profiles in external file (.csv?)
* Load positions and profiles from external files to execute save motions
* Definition of pallets and functions for motion profiles to pick and place pallets
* Lots more


