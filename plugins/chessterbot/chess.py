#!/usr/bin/python

from Chesster import ChessBoard

crontable = []
outputs = []
client_hook =  None
accounts = []

cb = ChessBoard()

valid_actions = ["show", "give"]

def setup(hook2cl=None):
	if hook2cl is not None:
		global client_hook, accounts
		print "Hey, I'm Chesster !"
		client_hook = hook2cl
		print type(client_hook)
		nbOfUsers = len(hook2cl.server.users)
	#	print "Got a hook", hook2cl
	#	print hook2cl.server.domain
	#	print hook2cl.server.users

#def catch_all(data):
#	print "catch all:",data

def process_message(data):
	#Needed to modify global variables :
	#global accounts
	print "---------------------------"
#	print "message", data
	#print "user id:", data["user"]
	#print "user name:", client_hook.server.users
	#print accounts
	msg = data["text"]
	args = []

	print msg
	if msg == "display":
#		print cb.board
		#visualboard= "+---+---+---+---+---+---+---+---+---+\n|   | A | B | C | D | E | F | G | H |"
		# |   | A | B | C | D | E | F | G | H |
		# +---+---+---+---+---+---+---+---+---+
		# | 1 |   |   |   |   |   |   |   |   |
		# | 2 |   |   |   |   |   |   |   |   |
		# | 3 |   |   |   |   |   |   |   |   |
		# | 4 |   |   |   |   |   |   |   |   |
		# | 5 |   |   |   |   |   |   |   |   |
		# | 6 |   |   |   |   |   |   |   |   |
		# | 7 |   |   |   |   |   |   |   |   |
		# | 8 |   |   |   |   |   |   |   |   |
		# +---+---+---+---+---+---+---+---+---+

		#visualboard = '\n+---+----+\n'.join(['  |  '.join(l) for l in cb.board])
		#visualboard = '\n-----------------------------\n'.join(['  |  '.join(l) for l in cb.board])
		visualboard = '\n'.join(['|'.join(l) for l in cb.board])
		#print visualboard
		outputs.append([data['channel'], "{}".format(visualboard)])
		#outputs.append('C05640UU7', "{}".format(visualboard))
		#outputs.append(['C05640UU7', "{}".format("pouet")])

	#THIS PART IS TRICKY !

#        if msg[:6] == "_money":
#                args=msg[6:].split()
#		print "\033[31mGot the _money command with args :", args,"\033[00m(",len(args),")"
#		if len(args) > 0:
#			if args[0] in valid_actions:
#				print "Actionvalid"
#				if args[0] == "give":
#					if len(args) == 3:
#						give(data['user'], args[2], args[1])
#					else:
#						print "Wrong nb of args required 3"
#			else:
#				print "passing"
#				pass
#		else:
#			print "no args"
#	else:
#		pass
		#self.moneyCommand = True
#                     args=userMsg[6:].split()
#                     if args:
#                             if args[0] == "give":
#                                     if len(args) == 3:
#                                             lookFor=self.slack_client.server.users.find(args[1])
#                                             if lookFor == None:
#                                                     recipient = 'U08JAGFV0'
#                                             else:
#                                                     recipient=lookFor.id
#
#                                             #print args[2], self.accounts[userID]
#                                             try:
#                                                     amount = float(args[2])
#                                             except ValueError:
#                                                     amount = 0.0
#
#                                             if amount > self.accounts[userID]:
#                                                     self.moneyCmdResult = "Not enough Jollars, transaction aborted"
#                                             else:
#                                                     self.accounts[userID] -= abs(amount)
#                                                     if recipient is not None:
#                                                             self.accounts[recipient] += amount
#                                                     self.moneyCmdResult = self.slack_client.server.users.find(userID).name+" gave "+str(amount)+" J to "+self.slack_client.server.users.find(recipient).name
#                                             with open(self.accountFile, 'a') as of:
#                                                     of.write(str(self.accounts)+'\n')
#                             elif args[0] == "bot":
#                                     self.moneyCmdResult = "I have "+str(self.accounts['U08JAGFV0'])+" J"
#                             else:
#                                     self.moneyCommand = False
#                     else:
#                             self.moneyCmdResult = self.slack_client.server.users.find(userID).name+": "+str(self.accounts[userID])+" jollar(s)"
#

def process_presence_changed(data):
	print "message", data

#crontable.append([10, "periodic_annoyance"])
#crontable.append([10, "zob"])
# periodic job :
def periodic_annoyance():
	outputs.append(['C05640UU7', "{}".format("pouet")])

def zob():
	print "data zob"

#def process_user_typing(data):
#	# Sleep for a bit before replying; you'll seem more real this way
#	#time.sleep(random.randint(0,9) *.2)
#	#outputs.append([data['channel'], "{}".format(ellie.respond(data['text'])) ])
#	outputs.append([data['channel'], "{}".format("=") ])

#if "type" in data:
#         function_name = "process_" + data["type"]
#         #print data["type"]
#         dbg("got {}".format(function_name))
#         for plugin in self.bot_plugins:
#             plugin.register_jobs()
#             plugin.do(function_name, data)
#         if data['type'] == 'message' and ("text" in data) and ("user" in data):
#             userID=data['user']
#             userMsg=data['text']
#             print userID,":",userMsg
#             print self.slack_client.server.users.find(userID).name
#             if userMsg[:6] == "_money":
#                     self.moneyCommand = True
#                     args=userMsg[6:].split()
#                     if args:
#                             if args[0] == "give":
#                                     if len(args) == 3:
#                                             lookFor=self.slack_client.server.users.find(args[1])
#                                             if lookFor == None:
#                                                     recipient = 'U08JAGFV0'
#                                             else:
#                                                     recipient=lookFor.id
#
#                                             #print args[2], self.accounts[userID]
#                                             try:
#                                                     amount = float(args[2])
#                                             except ValueError:
#                                                     amount = 0.0
#
#                                             if amount > self.accounts[userID]:
#                                                     self.moneyCmdResult = "Not enough Jollars, transaction aborted"
#                                             else:
#                                                     self.accounts[userID] -= abs(amount)
#                                                     if recipient is not None:
#                                                             self.accounts[recipient] += amount
#                                                     self.moneyCmdResult = self.slack_client.server.users.find(userID).name+" gave "+str(amount)+" J to "+self.slack_client.server.users.find(recipient).name
#                                             with open(self.accountFile, 'a') as of:
#                                                     of.write(str(self.accounts)+'\n')
#                             elif args[0] == "bot":
#                                     self.moneyCmdResult = "I have "+str(self.accounts['U08JAGFV0'])+" J"
#                             else:
#                                     self.moneyCommand = False
#                     else:
#                             self.moneyCmdResult = self.slack_client.server.users.find(userID).name+": "+str(self.accounts[userID])+" jollar(s)"
#
