#!/usr/bin/python3

##############################
# Skeleton of how to use IRC protocol with Python to make a bot
# Discord proves to be both easier to program and more accessible to players
##############################

import socket

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net"
port = 6667
max_username_char_length = 16
channel = "##resistance-bot"
botnick = "ResistanceBot"
adminname = "wugs"
exitcode = "!kill " + botnick

ircsock.connect((server, port)) # passed as a tuple
ircsock.send(bytes("USER {0} {0} {0} {0}\n".format(botnick), "UTF-8"))
ircsock.send(bytes("NICK {0}\n".format(botnick), "UTF-8")) # assign the nick

def joinchan(chan): # join channel(s).
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

def ping(): # respond to server Pings.
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

def sendmsg(msg, target=channel): # sends messages to the target.
    ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))

def main():
    joinchan(channel)
    while 1:
        ircmsg = ircsock.recv(2048).decode("UTF-8") # up to 2048 bytes
        ircmsg = ircmsg.strip('\n\r') # control characters from server
        print(ircmsg) # print to terminal

    if ircmsg.find("PRIVMSG") != -1:
        # Messages come in from from IRC in the format of
        # :[Nick]!~[hostname]@[IP Address] PRIVMSG [channel] :[message]
        name = ircmsg.split('!',1)[0][1:]
        message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]

        if len(name) <= max_username_char_length:
            if message.find('Hi ' + botnick) != -1:
                sendmsg("Hello " + name + "!")

            if message[:5].find('.tell') != -1 and message.find(' ') != -1:
                target = message.split(' ', 1)[1] # split at first space
                if target.find(' ') != -1:
                    message = target.split(' ', 1)[1]
                    target = target.split(' ')[0] # cut off message
                else: # incorrect format
                    target = name # the person who tried to use the command
                    message = "Could not parse. The message should be in the format of '.tell [target] [message]' to work properly."
                sendmsg(message, target)

            if name.lower() == adminname.lower() and message.rstrip() == exitcode:
                sendmsg("brutal.")
                ircsock.send(bytes("QUIT \n", "UTF-8"))
                return

    else:
        if ircmsg.find("PING :") != -1:
            ping()

if __name__ == '__main__':
    main()
