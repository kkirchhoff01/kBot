import traceback
from plugins import Commands, link_reader
import time
import socket 

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
        if any(command_item in command_msg for command_item in Commands.get_command_list()):
            try:
                cmd = command_msg.split(' ')[0]
                msg = ''
                if len(cmd) < len(command_msg):
                    msg = command_msg[len(cmd)+1:]
                result = Commands.get_command(cmd,msg)
                if result:
                    self.ircsock.send("PRIVMSG " + self.channel + " :" +user_name + ": " + result + "\n")
                    return
            except ValueError:
                print traceback.print_stack()
            except Exception, err:
                print traceback.print_stack(), err
                self.ircsock.send("PRIVMSG " + self.channel + " :Something went wrong!\n")
        if link_reader.check_link(command_msg):
            link = link_reader.check_link(command_msg);
            self.ircsock.send("PRIVMSG " + self.channel + " :[URL] "+ link_reader.read_link(link) +"\n")
              
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
        if "PRIVMSG" in ircmsg:
            bot.log(ircmsg)#log_msg)
            command_msg = ircmsg.split(channel)
            user_name = command_msg[0][1:command_msg[0].index('!')]
            bot.command(command_msg[1][2:], user_name)

        if ircmsg.find(":Hello "+ botnick) != -1:
            bot.hello()
        
        if ircmsg.find("JOIN :") != -1:
            bot.assign(ircmsg[1:ircmsg.index("!")])

        if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
            bot.ping()
