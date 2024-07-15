from datetime import datetime
import pytz
import argparse
import matplotlib.pyplot as plt

import graphs

class Logger:
    def __init__(self, logFile="log.dat", logLevelConsole: int=4, timeZone :str="Europe/Paris") -> None:
        self.f = open(logFile, 'a+')
        self.logLevelConsole = logLevelConsole
        self.tz = pytz.timezone(timeZone)

    def log(self, message : str, level: int=5):
        messageToWrite = "[{}][{}] {}".format(datetime.now(self.tz).strftime("%d%m%Y %H:%M:%S"), level, message)
        self.f.write(messageToWrite + "\n")
        if level >= self.logLevelConsole:
            print(messageToWrite)

class CLI:
    def __init__(self, logger) -> None:
        self.logger = logger
        self.logger.log("Successfully created CommandLineInterface")

        self.S_iTGraph = graphs.S_iTGraph()
        self.T_FTGraph = graphs.T_FTGraph()

        self.S_iTGraph.link_T_FTGraph(self.T_FTGraph)

        plt.ion()
        plt.show()

    def graph(self, name, *args):
        graphFunction = getattr(self.S_iTGraph, name)
        
        if args:
            graphFunction(args)
        else:
            graphFunction()

        self.S_iTGraph.refresh()
        self.T_FTGraph.refresh()

    def show(self, name):
        self.S_iTGraph.set_visibility(name, True)
        self.T_FTGraph.set_visibility(name, True)

    def hide(self, name):
        self.S_iTGraph.set_visibility(name, False)
        self.T_FTGraph.set_visibility(name, False)


