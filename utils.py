from datetime import datetime
import pytz
import argparse
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
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

        #cursor = Cursor(self.S_iTGraph.fig, useblit=True, color='black', linewidth=1)

        plt.ion()
        plt.show()

    def graph(self, args):
        if args[0] == "-h":
            nameChoices = [func for func in dir(self.S_iTGraph) if callable(getattr(self.S_iTGraph, func)) and not func.startswith("__") and not func in dir(graphs.Graph)] # choices are not-default class methods, and not inherited methods

            self.logger.log("usage: graph [-h] {}".format(nameChoices)) 
            self.logger.log("Plot predefined graphs (see graph list)")
            return

        graphFunction = getattr(self.S_iTGraph, args[0])
        graphFunction(args[1:])

        self.S_iTGraph.refresh()

    def delete(self, args):
        parser = argparse.ArgumentParser(prog="delete", exit_on_error=False, description="Delete lines from the graph. RegularExpressions can be used")
        parser.add_argument("expression", action="store", type=str, help="RegularExpression to math the lines to delete")

        parsedArgs = parser.parse_args(args)

        parsedArgs = parser.parse_args(args)

        if parsedArgs.expression == "*":
            lineNames = list(self.S_iTGraph.lines.keys())

            for lineName in lineNames:
                self.S_iTGraph.delete(lineName)

        else:
            pattern = re.compile(parsedArgs.expression)

            lineNames = list(self.S_iTGraph.lines.keys())

            for lineName in lineNames:
                if bool(pattern.match(lineName)):
                    self.S_iTGraph.delete(lineName)

    def show(self, args):
        parser = argparse.ArgumentParser(prog="show", exit_on_error=False, description="Show hidden lines on the graph. RegularExpressions can be used")
        parser.add_argument("expression", action="store", type=str)

        parsedArgs = parser.parse_args(args)

        parsedArgs = parser.parse_args(args)
        if parsedArgs.expression == "*":
            for lineName in self.S_iTGraph.lines.keys():
                self.S_iTGraph.set_visibility(lineName, True)
        else:
            pattern = re.compile(parsedArgs.expression)
            for lineName in self.S_iTGraph.lines.keys():
                if bool(pattern.match(lineName)):
                    self.S_iTGraph.set_visibility(lineName, True)

    def hide(self, args):
        parser = argparse.ArgumentParser(prog="hide", exit_on_error=False, description="Hide lines on the graph. RegularExpressions can be used")
        parser.add_argument("expression", action="store", type=str)

        parsedArgs = parser.parse_args(args)
        if parsedArgs.expression == "*":
            for lineName in self.S_iTGraph.lines.keys():
                self.S_iTGraph.set_visibility(lineName, False)

        else:
            pattern = re.compile(parsedArgs.expression)
            for lineName in self.S_iTGraph.lines.keys():
                if bool(pattern.match(lineName)):
                    self.S_iTGraph.set_visibility(lineName, False)

    def list(self, args):
        parser = argparse.ArgumentParser(prog="list", exit_on_error=False)
        parser.add_argument("option", default="all", type=str, action="store", choices=["all", "hidden", "visible"], nargs='?')

        try: # prevents parser from exiting main program after displaying help
            parsedArgs = parser.parse_args(args)
        except SystemExit:
            return

        message = ""
        if parsedArgs.option == "visible":
            message += ("S_i T Diagram :")
            for name, line in self.S_iTGraph.lines.items():
                if line.get_visible():
                    message += ("\n\t{}".format(name))

        elif parsedArgs.option == "hidden":
            message += ("\n\nS_i T Diagram :")
            for name, line in self.S_iTGraph.lines.items():
                if not line.get_visible():
                    message += ("\n\t{}".format(name))

        elif parsedArgs.option == "all":
            message += ("\n\nS_i T Diagram :")
            for name, line in self.S_iTGraph.lines.items():
                message += ("\n\t[{}] {}".format("V" if line.get_visible() else " ", name))

        self.logger.log(message)

    def c2k(self, args):
        parser = argparse.ArgumentParser(prog="c2k", description="Converts Celcius to Kelvin", exit_on_error=False)
        parser.add_argument("celcius", type=float, help="Celcius temperature to convert")

        try: # prevents parser from exiting main program after displaying help
            parsedArgs = parser.parse_args(args)
        except SystemExit:
            return

        self.logger.log(str(parsedArgs.celcius + 273.15))

    def k2c(self, args):
        parser = argparse.ArgumentParser(prog="k2c", description="Converts Kelvin to Celcius", exit_on_error=False)
        parser.add_argument("kelvin", type=float, help="Kelvin temperature to convert")

        try: # prevents parser from exiting main program after displaying help
            parsedArgs = parser.parse_args(args)
        except SystemExit:
            return

        self.logger.log(str(parsedArgs.kelvin - 273.15))


