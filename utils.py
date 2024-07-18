from datetime import datetime
import pytz
import argparse
import matplotlib.pyplot as plt
import re

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
            print(message)

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

    def show(self, args):
        parser = argparse.ArgumentParser(prog="show", exit_on_error=False)
        parser.add_argument("expression", action="store", type=str)

        parsedArgs = parser.parse_args(args)

        parsedArgs = parser.parse_args(args)
        if parsedArgs.expression == "*":
            for lineName in self.S_iTGraph.lines.keys():
                self.S_iTGraph.set_visibility(lineName, True)

            for lineName in self.T_FTGraph.lines.keys():
                self.T_FTGraph.set_visibility(lineName, True)

        else:
            pattern = re.compile(parsedArgs.expression)
            for lineName in self.S_iTGraph.lines.keys():
                if bool(pattern.match(lineName)):
                    self.S_iTGraph.set_visibility(lineName, True)

            for lineName in self.T_FTGraph.lines.keys():
                if bool(pattern.match(lineName)):
                    self.T_FTGraph.set_visibility(lineName, True)

    def hide(self, args):
        parser = argparse.ArgumentParser(prog="hide", exit_on_error=False)
        parser.add_argument("expression", action="store", type=str)

        parsedArgs = parser.parse_args(args)
        if parsedArgs.expression == "*":
            for lineName in self.S_iTGraph.lines.keys():
                self.S_iTGraph.set_visibility(lineName, False)

            for lineName in self.T_FTGraph.lines.keys():
                self.T_FTGraph.set_visibility(lineName, False)

        else:
            pattern = re.compile(parsedArgs.expression)
            for lineName in self.S_iTGraph.lines.keys():
                if bool(pattern.match(lineName)):
                    self.S_iTGraph.set_visibility(lineName, False)

            for lineName in self.T_FTGraph.lines.keys():
                if bool(pattern.match(lineName)):
                    self.T_FTGraph.set_visibility(lineName, False)

    def list(self, args):
        parser = argparse.ArgumentParser(prog="list", exit_on_error=False)
        parser.add_argument("option", default="all", type=str, action="store", choices=["all", "hidden", "visible"], nargs='?')

        parsedArgs = parser.parse_args(args)

        message = ""
        if parsedArgs.option == "visible":
            message += ("\n\nS_i T Diagram :")
            for name, line in self.S_iTGraph.lines.items():
                if line.get_visible():
                    message += ("\n\t{}".format(name))

            message += ("\n\nT_F T Diagram :")
            for name, line in self.T_FTGraph.lines.items():
                if line.get_visible():
                    message += ("\n\t{}".format(name))

        elif parsedArgs.option == "hidden":
            message += ("\n\nS_i T Diagram :")
            for name, line in self.S_iTGraph.lines.items():
                if not line.get_visible():
                    message += ("\n\t{}".format(name))

            message += ("\n\nT_F T Diagram :")
            for name, line in self.T_FTGraph.lines.items():
                if not line.get_visible():
                    message += ("\n\t{}".format(name))

        elif parsedArgs.option == "all":
            message += ("\n\nS_i T Diagram :")
            for name, line in self.S_iTGraph.lines.items():
                message += ("\n\t[{}] {}".format("V" if line.get_visible() else " ", name))

            message += ("\n\nT_F T Diagram :")
            for name, line in self.T_FTGraph.lines.items():
                message += ("\n\t[{}] {}".format("V" if line.get_visible() else " ", name))

        self.logger.log(message)


