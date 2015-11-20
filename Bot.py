import traceback
import Commands
import time
import socket 
import time

class Bot:
	# Some basic variables used to configure the bot        
	def __init__(self):
		self.server = "irc.freenode.net" 
		self.channel = "#icecube" # Channel
		self.botnick = "kBot9000"
		self.users = []
		self.log_file = open('IRC.log', 'a')
		self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ircsock.connect((self.server, 6667))
		self.ircsock.send("USER "+ self.botnick +" "+ self.botnick +" "+ self.botnick +" :This bot is Kevin's\n")
		self.ircsock.send("NICK "+ self.botnick +"\n")
		#self.joinchan(self.channel)

	def get_server(self):
		return self.server
	
	def get_channel(self):
		return self.channel

	def get_nick(self):
		return self.botnick

	def get_data(self):
		return self.ircsock.recv(2048)
	
	def ping(self): # This is our first function! It will respond to server Pings.
		self.ircsock.send("PONG :pingis\n")  

	def sendmsg(self, chan , msg): # This is the send message function, it simply sends messages to the channel.
		self.ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

	def joinchan(self, chan): # This function is used to join channels.
		self.ircsock.send("JOIN "+ chan +"\n")

	def hello(self):
		self.ircsock.send("PRIVMSG "+ self.channel +" :Hello!\n")

	def command(self, command_msg, user_name):
		#command_msg = command_msg.split(":")
		#command_msg = command_msg[1]
		#print command_msg[0:command_msg.index(' ')]
		#command_item = c if command_msg.index(c) == 0 for c in commands.get_command_list()
		if any(command_item in command_msg for command_item in Commands.get_command_list()):
			try:
				cmd = command_msg.split(' ')[0]
				msg = ''
				if len(cmd) < len(command_msg):
					msg = command_msg[len(cmd)+1:]
				result = Commands.get_command(cmd,msg)
				self.ircsock.send("PRIVMSG " + self.channel + " :" +user_name + ": " + result + "\n")
			except ValueError:
				print traceback.print_stack()
			except Exception, err:
				print traceback.print_stack()
				self.ircsock.send("PRIVMSG " + self.channel + " :Something went wrong!\n")
			
			  
	def log(self, message):
		timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
		self.log_file.write(str(timestamp) + str(message) + '\n')

	def assign(self, name):
		with open('operators.list', 'r') as o:
			if name in o.read().strip("\n"):
				self.ircsock.send("MODE " + self.channel + " +o " + name + "\n")

if __name__ == "__main__":
	bot = Bot()
	server = bot.get_server()
	channel = bot.get_channel()
	botnick = bot.get_nick()
	bot.joinchan(channel)
	while "JOIN " + channel not in bot.get_data():
		time.sleep(0.1)

	while 1:
		ircmsg = bot.get_data()# receive data from the server
		ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
		#print('Message: ' + ircmsg)
		#log.write(ircmsg + '\n')
		if "PRIVMSG" in ircmsg:
			#log_msg = ircmsg.split(channel+" :")
			#name = log_msg[0].split('!')[0].strip(':')
			#log_msg = name + ': ' + log_msg[1]
			bot.log(ircmsg)#log_msg)
			command_msg = ircmsg.split(channel)
			user_name = command_msg[0][1:command_msg[0].index('!')]
			#print command_msg[1][2:]
			bot.command(command_msg[1][2:], user_name)

		if ircmsg.find(":Hello "+ botnick) != -1:
			bot.hello()
		
		if ircmsg.find("JOIN :") != -1:
			bot.assign(ircmsg[1:ircmsg.index("!")])

		if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
			bot.ping()