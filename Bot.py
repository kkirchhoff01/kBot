import traceback
from plugins import Commands, link_reader
import time
import socket
import re


class Bot:
    # Some basic variables used to configure the bot
    def __init__(self):
        self.server = "irc.rizon.net"
        self.channels = ["#kBot9000"]  # Channel
        self.botnick = "kBot"
        self.last_msg = {}
        self.log_file = 'IRC_Logs.log'
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cooldown = 30.0

    # Connect to server
    def connect(self):
        self.ircsock.connect((self.server, 6667))

    # Send user/nick info to server
    def send_info(self):
        self.ircsock.send("USER " + self.botnick + " " + self.botnick + " " +
                          self.botnick + " :This bot is Kevin's\n")
        self.ircsock.send("NICK " + self.botnick + "\n")

    # Get irc message
    def get_data(self):
        return self.ircsock.recv(2048)

    def sendmsg(self, chan, msg):  # Sends messages to the channel
        self.ircsock.send("PRIVMSG " + chan + " :" + msg + "\n")

    def ping(self):  # Responds to server Pings
        self.ircsock.send("PONG :pingis\n")

    def joinchan(self, chan):  # This function is used to join channels
        self.ircsock.send("JOIN " + chan + "\n")

    # A friendly "Hello!"
    def hello(self, chan):
        self.ircsock.send("PRIVMSG " + chan + " :Hello!\n")

    # Check for command
    def command(self, command_msg, user_name, chan):
        # Check for command message
        command_match = re.match(r"^(\.)(?P<command>[a-zA-Z]+)" +
                                 r"($|\s(?P<msg>.+$))" +
                                 r"|^(s/)(?P<word>.+)(/)(?P<sub_word>.+$)",
                                 command_msg)

        # Read link if no command found
        if(command_match is None and
           link_reader.check_link(command_msg)):
            link = link_reader.check_link(command_msg)  # Get matching link
            # Extract matching link
            links = [i for i in command_msg.split(' ') if link in i]
            result = link_reader.read_link(links[0])  # Get info from link
            if result:
                self.sendmsg(chan, result)
            return

        # Command found/organize input
        elif command_match is not None:
            command_match = command_match.groupdict()

        # No command or link found
        else:
            return

        # Do command
        if(command_match['command'] in Commands.get_command_list()):
            try:
                cmd = command_match['command']
                msg = command_match['msg']
                result = Commands.get_command(cmd, msg)

                # Send normal command
                if result and cmd not in ['quote', 'draw']:
                    self.sendmsg(chan, user_name + ": " + result)
                    return

                # Quote command found
                elif result and cmd == 'quote':
                    # Responds without directed username of command sender
                    self.sendmsg(chan, result)
                    return

                # Draw command found
                elif result and cmd == 'draw':
                    # Cooldown prevents spam
                    if (time.time() - self.cooldown) < 30.0:
                        self.sendmsg(chan,
                                     "Draw can only be used once every 30 seconds (%.2f seconds left)" %
                                          (30.0 - (time.time() - self.cooldown)))
                        return
                    else:
                        result = result.split('\n')
                        # Need to send multiple lines
                        for line in result:
                            self.sendmsg(chan, line)
                        self.cooldown = time.time()
                        return

            except ValueError:
                print result
            except Exception, err:
                print traceback.print_stack()
                print err
                self.ircsock.send(chan, "Something went wrong!")

        # Sub string
        elif(command_match['word'] is not None and
             command_match['sub_word'] is not None):
            try:
                # Message with subbed word
                new_msg = self.last_msg[user_name].replace(
                    command_match['word'], command_match['sub_word'])
                # Check to make sure there was a word subbed
                if new_msg != self.last_msg[user_name]:
                    self.sendmsg(chan, user_name + " meant to say: " + new_msg)
            except KeyError:
                pass
            return

        # Resond to .bots
        elif command_match['command'] == 'bots' and command_match['msg'] is None:
            self.sendmsg(chan, "Reporting in! [Python]")
            return

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
                self.sendmsg(chan, "Hey!")

if __name__ == "__main__":
    import sys

    bot = Bot()
    bot.connect()
    bot.send_info()
    server = bot.server
    channels = bot.channels
    botnick = bot.botnick
    for channel in channels:
        bot.joinchan(channel)

    # Main loop
    while 1:
        ircmsg = bot.get_data()  # receive data from the server
        if not ircmsg:  # Check for disconnect
            # Attempt to reconnect
            try:
                bot.connect()
                bot.send_info()
            except:
                sys.exit(1)  # Exit if failed

        ircmsg = ircmsg.strip('\n\r')  # removing any unnecessary linebreaks.

        msg_channel = ircmsg.split(' ')
        if len(msg_channel) > 2:
            msg_channel = msg_channel[2]
        else:
            msg_channel = ''

        if "PRIVMSG" in ircmsg and msg_channel in channels:
            command_msg = ircmsg.split(msg_channel)
            user_name = command_msg[0][1:command_msg[0].index('!')]
            bot.command(command_msg[1][2:], user_name, msg_channel)
            bot.log(user_name, command_msg[1][2:])
            bot.last_msg[user_name] = command_msg[1][2:]

        # Fun response
        if ircmsg.find(":Hello " + botnick) != -1:
            bot.hello(msg_channel)

        # Checks for ops when someone joins
        if ircmsg.find("JOIN :") != -1:
            bot.assign(ircmsg[1:ircmsg.index("!")], msg_channel)

        # Ping response
        if ircmsg.find("PING :") != -1:
            bot.ping()
