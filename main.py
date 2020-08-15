from telnetlib import Telnet

#Commands



class Robot():
	#Standard Command Set, not exhaustive
	ATTACH = "attach"
	BASE = "base"
	EXIT = "exit"
	HOME = "home"
	HOMEALL = "homeAll"
	HP = "hp"
	MODE = "mode"
	MSPEED = "mspeed"
	NOP = "nop"
	PC = "pc"
	PD = "pd"
	LOC = "loc"
	WHERE = "where"
	DESTC = "DestC"
	DESTJ = "DestJ"
	MOVE = "Move"
	HALT = "halt"
	ZEROTORQUE = "zeroTorque"

	#PARobot Command Set, not exhaustive
	CHANGECONFIG = "ChangeConfig"
	CHANGECONFIG2 = "ChangeConfig2"
	FREEMODE = "FreeMode"
	GRASPDATA = "GraspData"
	GRIPCLOSEPOS = "GripClosePos"
	GRIPOPENPOS =  "GripOpenPos"
	GRIPPER = "Gripper"
	MOVERAIL = "MoveRail"
	MOVE2SAFE = "movetosafe"
	PALLETINDEX =  "PalletIndex"
	PALLETORIGIN = "PalletOrigin"
	PALLETX = "PalletX"
	PALLETY = "PalletY"
	PALLETZ = "PalletZ"
	PICKPLATE = "PickPlate"
	PLACEPLATE = "PlacePlate"
	RAIL = "Rail"
	TEACHPLATE = "TeachPlate"

	def __init__(self,HOST="192.168.0.1",PORT=10000,timeout=1): #change timeout to 10
		try:
			print("Trying to connect...")
			self.tn = Telnet(HOST,PORT,timeout=timeout) 
		except Exception:
			print("Can't Connect!")
			self.tn = Telnet() #remove this when testing on a real robot
			return None
		print("Successfully connected!")

		self.HOST = HOST
		self.PORT = PORT
		self.timeout = timeout

		self.first_status_connect()

		self.saved_positions = {}

	def first_status_connect(self):
		with Telnet(self.HOST, 10000, timeout=self.timeout) as tn:
			print(tn.read_all()) #see what first status message is

	def send_command(self,command=NOP,args=[]):
		msg = command
		for arg in args:
			msg+= " "+arg #create the command message by concatenating into one string, split by spaces
		msg+= " \n"

		print(msg) #debug helpful

		self.tn.write(msg)

	def read_reply(self):
		msg = self.tn.read_until(b"\r\n",timeout=self.timeout)
		reply = []
		for m in msg.strip().split("\\s+"): #remove any trailing whitespaces, split replycode and data by spaces
			reply.append(m)
		err = reply[0]
		return reply,err

	def attach(self):
		self.send_command(self.ATTACH,["1"])

	def release(self):
		self.send_command(self.ATTACH,["0"])

	def set_gripper_close_pos(self,pos):
		self.send_command(self.GRIPCLOSEPOS,[pos])

	def set_gripper_open_pos(self,pos):
		self.send_command(self.GRIPOPENPOS,[pos])

	def get_attach_state(self):
		self.send_command(self.ATTACH)
		reply,err = self.read_reply()
		if err:
			print("Error Code: ", err)
			return None
		else:
			return reply

	def get_station_loc(self,station_index):
		self.send_command(self.LOC,[str(station_index)])
		reply,err = self.read_reply()
		if err:
			print("Error Code: ", err)
			return None
		else:
			return reply

	def get_current_position(self):
		self.send_command(self.WHERE)
		reply,err = self.read_reply()
		if err:
			print("Error Code: ", err)
			return None
		else:
			return reply

	def get_goal_position(self):
		self.send_command(self.DESTC)
		reply,err = self.read_reply()
		if err:
			print("Error Code: ", err)
			return None
		else:
			return reply

	def limp(self,axes=b"0"):
		self.send_command(self.ZEROTORQUE,["0"])
		#need to re-write this for logic on if you want to set only a few axes limp, instead of all of them.

	def move(self,loc_ind,prof_ind):
		self.send_command(self.MOVE,[str(loc_ind),str(prof_ind)])

	def close_gripper(self):
		self.send_command(self.GRIPPER,["2"])

	def open_gripper(self):
		self.send_command(self.GRIPPER,["1"])

	def move_rail(self,station_index,mode=0,destination=" "):
		self.send_command(self.MOVERAIL,[str(station_index),str(mode),str(destination)])

	def teach_position(self,pos_label):
		self.limp() #stop all torque
		self.release() #don't need to send any motion commands
		input("Start moving the robot! Press enter when at desired position.")
		position = self.get_current_position()
		if position is not None:
			self.saved_positions[pos_label] = position[1:]
		print("Saved %s at %s"%(pos_label,position))

	def teach_profile():
		try:
			while True:
				self.get_current_position()
		except KeyboardInterrupt:
			pass

	def move_to_station(self,station_index):
		self.attach() #attach robot to be able to use motion commands
		loc = self.get_station_loc(station_index)

	def load_position():
		pass

	def transfer_pallet(self,pallet,station_destination):
		pass


if __name__ == '__main__':
	HOST = "192.168.0.1" # IP Address of Controller
	PORT = 10000 # First Status Connection
	PORT1 = 10100 # Robot 1

	#testing functions here, they will throw errors without a Telnet connection
	robot = Robot(HOST,PORT)
	#robot.get_station_loc("1")
	robot.teach_position("1")
