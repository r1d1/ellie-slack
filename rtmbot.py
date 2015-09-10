#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True

import glob
import yaml
import json
import os
import sys
import time
import logging

from slackclient import SlackClient
# Erwan addition :
import numpy as np
from textProcessing import TextProcessing
from neuralNet import NeuralNet
import datetime

# Ugly global definition of wordLength
wordLength = 20

def dbg(debug_string):
    if debug:
        logging.info(debug_string)

class RtmBot(object):
    def __init__(self, token):
        self.token = token
        self.bot_plugins = []
        self.slack_client = None
	self.textProc = TextProcessing()
	self.layerLength = self.textProc.maxChar-self.textProc.minChar
	externalSize = self.layerLength*wordLength
	self.neuralnet = NeuralNet(externalSize, externalSize, externalSize / 2 )
	self.wordLengths = []
	self.errorEvolution=[]
	now = datetime.datetime.now()
	self.wordLengthsFile = "log_wordLengths"+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+".txt"
	print self.wordLengthsFile

    def connect(self):
        """Convenience method that creates Server instance"""
        self.slack_client = SlackClient(self.token)
        self.slack_client.rtm_connect()
    def start(self):
        self.connect()
        self.load_plugins()
        while True:
            for reply in self.slack_client.rtm_read():
                self.input(reply)
            self.crons()
            self.output()
            time.sleep(.1)
    def input(self, data):
    	#print "Read something :",data
        if "type" in data:
            function_name = "process_" + data["type"]
            dbg("got {}".format(function_name))
            for plugin in self.bot_plugins:
                plugin.register_jobs()
                plugin.do(function_name, data)
	    if data['type'] == 'message' and ("text" in data) and ("user" in data):
	    	print data['user'],":",data['text']
		# Process input for NN
		# For now, just printing the active inputs :
		for char in data['text']:
			print self.textProc.char2val(char),
		print ""
		for word in data['text'].split():
			# Build array input
			inputvec = [0.0 for i in range(len(self.neuralnet.inputLayer))]
			counter = 0
			for letter in word:
				try:
					inputvec[counter*self.layerLength + self.textProc.char2val(letter)] = 1.0
				except IndexError:
					print "Didn't get "+letter
				counter += 1
			self.wordLengths.append(len(word))
			with open(self.wordLengthsFile, 'a') as of:
			    of.write(str(len(word))+'\n')
			# Send to network :
			print word
			#print inputvec, word
			self.neuralnet.inputData(inputvec)
			self.neuralnet.computeOutput()
			self.errorEvolution.append(abs(self.neuralnet.endError))
			print self.errorEvolution[-1]
			answer=""
			for letter in range(wordLength):
				answer += self.textProc.vec2char(self.neuralnet.outputLayer_f[letter*wordLength:(letter+1)*wordLength].tolist())
			# Generate answer (which is way more tricky)
			print answer

    def output(self):
        for plugin in self.bot_plugins:
            limiter = False
            for output in plugin.do_output():
                channel = self.slack_client.server.channels.find(output[0])
                if channel != None and output[1] != None:
                    if limiter == True:
                        time.sleep(1)
                        limiter = False
                    message = output[1].encode('ascii','ignore')
		    # Erwan : Probabilistic output :
		    probOfSpeech=np.random.rand()
		    if probOfSpeech < 0.01:
		    	print probOfSpeech
		    	channel.send_message("{}".format(message))
                    limiter = True
    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()
    def load_plugins(self):
        for plugin in glob.glob(directory+'/plugins/*'):
            sys.path.insert(0, plugin)
            sys.path.insert(0, directory+'/plugins/')
        for plugin in glob.glob(directory+'/plugins/*.py') + glob.glob(directory+'/plugins/*/*.py'):
            logging.info(plugin)
            name = plugin.split('/')[-1][:-3]
	    print "Plugin loaded:",name
#            try:
            self.bot_plugins.append(Plugin(name))
#            except:
#                print "error loading plugin %s" % name

class Plugin(object):
    def __init__(self, name, plugin_config={}):
        self.name = name
        self.jobs = []
        self.module = __import__(name)
        self.register_jobs()
        self.outputs = []
        if name in config:
            logging.info("config found for: " + name)
            self.module.config = config[name]
        if 'setup' in dir(self.module):
            self.module.setup()
    def register_jobs(self):
        if 'crontable' in dir(self.module):
            for interval, function in self.module.crontable:
                self.jobs.append(Job(interval, eval("self.module."+function)))
            logging.info(self.module.crontable)
            self.module.crontable = []
        else:
            self.module.crontable = []
    def do(self, function_name, data):
        if function_name in dir(self.module):
            #this makes the plugin fail with stack trace in debug mode
            if not debug:
                try:
                    eval("self.module."+function_name)(data)
                except:
                    dbg("problem in module {} {}".format(function_name, data))
            else:
                eval("self.module."+function_name)(data)
        if "catch_all" in dir(self.module):
            try:
                self.module.catch_all(data)
            except:
                dbg("problem in catch all")
    def do_jobs(self):
        for job in self.jobs:
            job.check()
    def do_output(self):
        output = []
        while True:
            if 'outputs' in dir(self.module):
                if len(self.module.outputs) > 0:
                    logging.info("output from {}".format(self.module))
                    output.append(self.module.outputs.pop(0))
                else:
                    break
            else:
                self.module.outputs = []
        return output

class Job(object):
    def __init__(self, interval, function):
        self.function = function
        self.interval = interval
        self.lastrun = 0
    def __str__(self):
        return "{} {} {}".format(self.function, self.interval, self.lastrun)
    def __repr__(self):
        return self.__str__()
    def check(self):
        if self.lastrun + self.interval < time.time():
            if not debug:
                try:
                    self.function()
                except:
                    dbg("problem")
            else:
                self.function()
            self.lastrun = time.time()
            pass

class UnknownChannel(Exception):
    pass


def main_loop():
    if "LOGFILE" in config:
        logging.basicConfig(filename=config["LOGFILE"], level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info(directory)
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        logging.exception('OOPS')

if __name__ == "__main__":
    directory = os.path.dirname(sys.argv[0])
    if not directory.startswith('/'):
        directory = os.path.abspath("{}/{}".format(os.getcwd(),
                                directory
                                ))

    config = yaml.load(file('rtmbot.conf', 'r'))
    debug = config["DEBUG"]
    bot = RtmBot(config["SLACK_TOKEN"])
    site_plugins = []
    files_currently_downloading = []
    job_hash = {}

    if config.has_key("DAEMON"):
        if config["DAEMON"]:
            import daemon
            with daemon.DaemonContext():
                main_loop()
    main_loop()

