import traceback
from plugins import Commands, link_reader
import time
import socket


class Bot:
    # Some basic variables used to configure the bot
    def __init__(self):
        self.server = "irc.freenode.net"
        self.channels = ["#icecube"]  # Channel
        self.botnick = "kBot9000"
        self.last_msg = {}
        self.users = []
        self.log_file = open('IRC.log', 'a')
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ircsock.connect((self.server, 6667))
        self.ircsock.send("USER " + self.botnick + " " + self.botnick + " " +
                          self.botnick + " :This bot is Kevin's\n")
        self.ircsock.send("NICK " + self.botnick + "\n")

    @property
    def server(self):
        return self.server

    @property
    def channels(self):
        return self.channels

    @property
    def botnick(self):
        return self.botnick

    def get_data(self):
        return self.ircsock.recv(2048)

    def sendmsg(self, chan, msg):  # Sends messages to the channel.
        self.ircsock.send("PRIVMSG " + chan + " :" + msg + "\n")

    def ping(self):  # Responds to server Pings.
        self.ircsock.send("PONG :pingis\n")

    def joinchan(self, chan):  # This function is used to join channels.
        self.ircsock.send("JOIN " + chan + "\n")

    # A friendly "Hello!"
    def hello(self, chan):
        self.ircsock.send("PRIVMSG " + chan + " :Hello!\n")

    # Check for command
    def command(self, command_msg, user_name, chan):
        # Check for command in command list
        if any(command_item in command_msg for
                command_item in Commands.get_command_list()):
            try:
                command_list = command_msg.split(' ')
                cmd = command_list[0]
                msg = ''
                if len(command_list) > 1:
                    msg = ' '.join(command_list[1:])
                result = Commands.get_command(cmd, msg)
                if result:
                    self.ircsock.send("PRIVMSG " + chan + " :" +
                                      user_name + ": " + result + "\n")
                    return
            except ValueError:
                print traceback.print_stack()
            except Exception, err:
                print traceback.print_stack(), err
                self.ircsock.send("PRIVMSG " + chan +
                                  " :Something went wrong!\n")

        # Sub string command
        elif(len(command_msg.split('/')) == 3 and
                command_msg.split('/')[0] == 's'):
            try:
                new_msg = self.last_msg[user_name].replace(
                        command_msg.split('/')[1], command_msg.split('/')[2])
                if new_msg != self.last_msg[user_name]:
                    self.ircsock.send("PRIVMSG " + chan + " :" + user_name +
                                      " meant to say: " + new_msg + "\n")
            except KeyError:
                pass

        # Respond to .bots
        elif command_msg == '.bots':
            self.ircsock.send("PRIVMSG " + chan + " :Reporting in! [Python]\n")

        # Reads link from text
        if link_reader.check_link(command_msg):
            link = link_reader.check_link(command_msg)
            result = link_reader.read_link(link)
            if result:
                self.ircsock.send("PRIVMSG " + chan +
                                  " :[URL] " + result + "\n")

    # Logger
    def log(self, name, message):
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        with open(self.log_file, 'a') as log:
            log.write("%s %s: %s \n" % (str(timestamp), name, str(message)))

    # Assigns op status to anyone in op list and gives them a friendly welcome
    def assign(self, name, chan):
        with open('operators.list', 'r') as o:
            if name in o.read().strip("\n"):
                self.ircsock.send("MODE " + chan + " +o " + name + "\n")
                self.ircsock.send("PRIVMSG " + chan + " :Hey!\n")

if __name__ == "__main__":
    bot = Bot()
    server = bot.server
    channels = bot.channels
    botnick = bot.botnick
    for channel in channels:
        bot.joinchan(channel)
        while "JOIN " + channel not in bot.get_data():
            time.sleep(0.1)
        bot.hello(channel)

    # Main loop
    while 1:
        ircmsg = bot.get_data()  # receive data from the server
        print ircmsg
        ircmsg = ircmsg.strip('\n\r')  # removing any unnecessary linebreaks.
        msg_channel = ''
        for channel in channels:
            if channel in ircmsg:
                msg_channel = channel
                break
        if "PRIVMSG" in ircmsg:
            command_msg = ircmsg.split(msg_channel)
            user_name = command_msg[0][1:command_msg[0].index('!')]
            bot.command(command_msg[1][2:], user_name, msg_channel)
            bot.log(user_name, command_msg[1][2:])
            bot.last_msg[user_name] = command_msg[1][2:]

        # Fun response
        if ircmsg.find(":Hello " + botnick) != -1:
            bot.hello()

        # Checks for ops when someone joins
        if ircmsg.find("JOIN :") != -1:
            bot.assign(ircmsg[1:ircmsg.index("!")], msg_channel)

        # Ping response
        if ircmsg.find("PING :") != -1:  # Respond to ping
            bot.ping()
