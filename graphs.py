import matplotlib.pyplot as plt
import matplotlib.text
import matplotlib.colors as mcolors
from labellines import labelLines
import numpy as np
from numpy._core.function_base import linspace as linspace
import argparse

import parametrization

class Graph:
    def __init__(self, title, x_label, y_label, Tn=np.linspace(235, 273, 100)):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title(title)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)

        self.Tn = Tn

        self.lines = {}
        self.scatters = {}
        self.txts = {}

    def delete(self, name):
        if name in self.lines.keys():
            self.lines[name].remove()
            del self.lines[name]
        if name in self.txts.keys():
            self.txts[name].remove()
            del self.txts[name]

    def plot(self, x, y, name, label="", color='b', lw=1, labelLine=True, align=True, xvals=None):
        self.delete(name)
        self.lines[name] = self.ax.plot(x, y, label=label, color=color, lw=lw)[0]

        if labelLine:
            if xvals:
                txts = labelLines([self.lines[name]], xvals=xvals, align=align)
                if txts:
                    self.txts[name] = txts[0]
                else:
                    self.txts[name] = matplotlib.text.Text()
            else:
                txts = labelLines([self.lines[name]], align=align)
                if txts:
                    self.txts[name] = txts[0]
                else:
                    self.txts[name] = matplotlib.text.Text()
    
    def scatter(self, x, y, name, label, marker="x", color="b"):
        self.scatters[name] = self.ax.scatter(x, y, label=label, marker=marker, color=color)

    def refresh(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def set_visibility(self, name, value):
        if name in self.lines.keys():
            self.lines[name].set_visible(value)
            self.txts[name].set_visible(value)
        elif name in self.scatters.keys():
            self.scatters[name].set_visible(value)
            self.txts[name].set_visible(value)
        else:
            raise NameError("Line or scatter not found for changing visibility")

    #def list_visible

class S_iTGraph(Graph):

    def __init__(self, title="$S_i = f(T)$", x_label="$T (K)$", y_label="$S_i$", Tn=np.linspace(235, 273, 100)):
        super().__init__(title, x_label, y_label, Tn)
        self.T_FTGraphLinked = False

    def link_T_FTGraph(self, T_FTGraph):
        self.T_FTGraph = T_FTGraph
        self.T_FTGraphLinked = True

    def S_w1(self, args):
        S_in = [parametrization.S_w2S_i_P0(T, 1) for T in self.Tn]
        self.plot(self.Tn, S_in, name="S_w1", label="$S_w = 1$", color="blue")

        if self.T_FTGraphLinked:
            T_Fn = self.T_FTGraph.S_in2T_Fn(self.Tn, S_in)
            self.T_FTGraph.plot(self.Tn, T_Fn, name="S_w1", label="$S_w = 1$", color="blue")

    def S_w(self, args): ### PAS FINI
        parser = argparse.ArgumentParser(prog="S_w", description="Draw a single S_w line", exit_on_error=False)
        parser.add_argument("S_w", type=float, help="S_w line to draw")
        parser.add_argument("-c", "--color", choices=dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS).keys(), dest="color", default="lightgrey", help="Color of the line (default: %(default)s)", metavar='matplotlibColor')
        parser.add_argument("-w", "--lw", dest="lw", type=float, default=1, help="Line width (default: %(default)s)")
        parser.add_argument("-u", "--unlabeled", dest="labeled", action="store_false", help="Unlabeled - when on, does not apply label to the line")
        parser.add_argument("-x", "--xvals", dest="xvals", type=float, default=270, help="xvals, decide where to put the label, alignment with respect to the x-axis (default: %(default)s)")

        try: # prevents parser from exiting main program after displaying help
            parsedArgs = parser.parse_args(args)
        except SystemExit:
            return
        
        S_in = [parametrization.S_w2S_i_P0(T, parsedArgs.S_w) for T in self.Tn]
        self.plot(self.Tn, S_in, labelLine=parsedArgs.labeled, name="S_w{:0.2f}".format(parsedArgs.S_w), label="$S_w$={:0.2f}".format(parsedArgs.S_w), color=parsedArgs.color, lw=parsedArgs.lw, xvals=parsedArgs.xvals)

        T_Fn = self.T_FTGraph.S_in2T_Fn(self.Tn, S_in)
        self.T_FTGraph.plot(self.Tn, T_Fn, labelLine=parsedArgs.labeled, name="S_w{:0.2f}".format(parsedArgs.S_w), label="$S_w$={:0.2f}".format(parsedArgs.S_w), color=parsedArgs.color, lw=parsedArgs.lw, xvals=parsedArgs.xvals)


    def S_i(self, args):
        parser = argparse.ArgumentParser(prog="S_i", description="Draw a single S_i line", exit_on_error=False)
        parser.add_argument("S_i", type=float, help="S_i line to draw")
        parser.add_argument("-c", "--color", choices=dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS).keys(), dest="color", default="blue", help="Color of the line (default: %(default)s)", metavar='matplotlibColor')
        parser.add_argument("-w", "--lw", dest="lw", type=float, default=1, help="Line width (default: %(default)s)")
        parser.add_argument("-u", "--unlabeled", dest="labeled", action="store_false", help="Unlabeled - when on, does not apply label to the line")
        parser.add_argument("-x", "--xvals", dest="xvals", type=float, default=270, help="xvals, decide where to put the label, alignment with respect to the x-axis (default: %(default)s)")

        try: # prevents parser from exiting main program after displaying help
            parsedArgs = parser.parse_args(args)
        except SystemExit:
            return
        
        S_in = [parsedArgs.S_i] * self.Tn.size
        self.plot(self.Tn, S_in, labelLine=parsedArgs.labeled, name="S_i{:0.2f}".format(parsedArgs.S_i), label="$S_i$={:0.2f}".format(parsedArgs.S_i), color=parsedArgs.color, lw=parsedArgs.lw, xvals=parsedArgs.xvals)

        T_Fn = self.T_FTGraph.S_in2T_Fn(self.Tn, S_in)
        self.T_FTGraph.plot(self.Tn, T_Fn, labelLine=parsedArgs.labeled, name="S_i{:0.2f}".format(parsedArgs.S_i), label="$S_i$={:0.2f}".format(parsedArgs.S_i), color=parsedArgs.color, lw=parsedArgs.lw, xvals=parsedArgs.xvals)

    def iso_S_w(self, args):
        parser = argparse.ArgumentParser(prog="iso_S_w", description="Draw multiple S_w lines", exit_on_error=False)
        parser.add_argument("-s", "--start", dest="start", type=float, default=0, help="Starting saturation ratio (default: %(default)s)")
        parser.add_argument("-e", "--end", dest="end", type=float, default=0.9, help="Ending saturation ratio (default: %(default)s)")
        parser.add_argument("-n", "--steps", dest="steps", type=int, default=10, help="Number of steps (default: %(default)s)")
        parser.add_argument("-c", "--color", choices=dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS).keys(), dest="color", default="lightgray", help="Color of the line (default: %(default)s)", metavar='matplotlibColor')
        parser.add_argument("-w", "--lw", dest="lw", type=float, default=1, help="Line width (default: %(default)s)")
        parser.add_argument("-u", "--unlabeled", dest="labeled", action="store_false", help="Unlabeled - when on, does not apply label to the line")
        parser.add_argument("-x", "--xvals", dest="xvals", type=float, default=270, help="xvals, decide where to put the label, alignment with respect to the x-axis (default: %(default)s)")

        try: # prevents parser from exiting main program after displaying help
            parsedArgs = parser.parse_args(args)
        except SystemExit:
            return

        S_wn = np.linspace(parsedArgs.start, parsedArgs.end, parsedArgs.steps)
        for S_w in S_wn:
            S_in = parametrization.S_w2S_i_P0(self.Tn, S_w)
            self.plot(self.Tn, S_in, labelLine=parsedArgs.labeled, name="S_w{:0.1f}".format(S_w), label="{:0.1f}".format(S_w), color=parsedArgs.color, xvals=parsedArgs.xvals, lw=parsedArgs.lw)

            if not S_w == 0.0:
                T_Fn = self.T_FTGraph.S_in2T_Fn(self.Tn, S_in)
                self.T_FTGraph.plot(self.Tn, T_Fn, labelLine=parsedArgs.labeled, name="S_w{:0.1f}".format(S_w), label="{:0.1f}".format(S_w), color=parsedArgs.color, xvals=parsedArgs.xvals, lw=parsedArgs.lw)

    def T_F(self, args):
        parser = argparse.ArgumentParser(prog="T_F", description="Draw a single T_F line", exit_on_error=False)
        parser.add_argument("T_F", type=float, help="Frostpoint temperature to draw")
        parser.add_argument("-c", "--color", choices=dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS).keys(), dest="color", default="green", help="Color of the line (default: %(default)s)", metavar='matplotlibColor')
        parser.add_argument("-w", "--lw", dest="lw", type=float, default=0.5, help="Line width (default: %(default)s)")
        parser.add_argument("-u", "--unlabeled", dest="labeled", action="store_false", help="Unlabeled - when on, does not apply label to the line")
        parser.add_argument("-x", "--xvals", dest="xvals", type=float, default=260, help="xvals, decide where to put the label, alignment with respect to the x-axis (default: %(default)s)")

        try: # prevents parser from exiting main program after displaying help
            parsedArgs = parser.parse_args(args)
        except SystemExit:
            return

        S_in = self.T_F2S_in(self.Tn, parsedArgs.T_F)
        self.plot(self.Tn, S_in, labelLine=parsedArgs.labeled, name="T_F{:0.2f}".format(parsedArgs.T_F), label="$T_F$={:0.2f}".format(parsedArgs.T_F), color=parsedArgs.color, lw=parsedArgs.lw, xvals=parsedArgs.xvals)

        T_FnReconverted = self.T_FTGraph.S_in2T_Fn(self.Tn, S_in)
        self.T_FTGraph.plot(self.Tn, T_FnReconverted, labelLine=parsedArgs.labeled, name="T_F{:0.2f}".format(parsedArgs.T_F), label="$T_F$={:0.2f}".format(parsedArgs.T_F), color=parsedArgs.color, lw=parsedArgs.lw, xvals=parsedArgs.xvals)


    def iso_T_F(self, args):
        parser = argparse.ArgumentParser(prog="iso_T_F", description="Draw multiple T_F lines", exit_on_error=False)
        parser.add_argument("-s", "--start", dest="start", type=float, default=238, help="Starting temperature (default: %(default)s)")
        parser.add_argument("-e", "--end", dest="end", type=float, default=258, help="Ending temperature (default: %(default)s)")
        parser.add_argument("-n", "--steps", dest="steps", type=int, default=11, help="Number of steps (default: %(default)s)")
        parser.add_argument("-c", "--color", choices=dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS).keys(), dest="color", default="green", help="Color of the line (default: %(default)s)", metavar='matplotlibColor')
        parser.add_argument("-w", "--lw", dest="lw", type=float, default=0.5, help="Line width (default: %(default)s)")
        parser.add_argument("-u", "--unlabeled", dest="labeled", action="store_false", help="Unlabeled - when on, does not apply label to the line")
        parser.add_argument("-x", "--xvals", dest="xvals", type=float, default=260, help="xvals, decide where to put the label, alignment with respect to the x-axis (default: %(default)s)")

        try: # prevents parser from exiting main program after displaying help
            parsedArgs = parser.parse_args(args)
        except SystemExit:
            return

        T_Fn = np.linspace(parsedArgs.start, parsedArgs.end, parsedArgs.steps)

        for T_F in T_Fn:
            S_in = self.T_F2S_in(self.Tn, T_F)
            self.plot(self.Tn, S_in, labelLine=parsedArgs.labeled, name="T_F{:0.2f}".format(T_F), label="$T_F$={:0.2f}".format(T_F), color=parsedArgs.color, lw=parsedArgs.lw, xvals=parsedArgs.xvals)

            T_FnReconverted = self.T_FTGraph.S_in2T_Fn(self.Tn, S_in)
            self.T_FTGraph.plot(self.Tn, T_FnReconverted, labelLine=parsedArgs.labeled, name="T_F{:0.2f}".format(T_F), label="$T_F$={:0.2f}".format(T_F), color=parsedArgs.color, lw=parsedArgs.lw, xvals=parsedArgs.xvals)


    def ambiant_S_w(self, ambiantT=296, S_wn = np.linspace(0,5,6)):
        for S_w in S_wn:
            S_in = np.array([parametrization.S_w2S_i_P0(self.Tn, parametrization.S_w_changeTemp(T, ambiantT, S_w)) for T in self.Tn])
            self.plot(self.Tn, S_in, name="S_w{:0.1f}".format(S_w), label="{:0.1f}".format(S_w), color="orange")

            if not S_w == 0.0:
                T_Fn = self.T_FTGraph.S_in2T_Fn(self.Tn, S_in)
                self.T_FTGraph.plot(self.Tn, T_Fn, name="S_w{:0.1f}".format(S_w), label="{:0.1f}".format(S_w), color="lightgrey", xvals=270)
            else:
                self.T_FTGraph.plot([], [], name="S_w0")

    def T_F2S_in(self, Tn, T_F):
        ln_p = parametrization.ln_p_MurphyKoop2005(T_F)
        S_i = np.exp(ln_p - parametrization.ln_p_i_P0(Tn))

        return S_i
        
class T_FTGraph(Graph):

    def __init__(self, title="$T_F = f(T)$", x_label="$T (K)$", y_label="$T_F(T)$", Tn=np.linspace(235, 273, 100)):
        super().__init__(title, x_label, y_label, Tn)

    def S_in2T_Fn(self, Tn, S_in):
        ln_p = np.log(S_in) + parametrization.ln_p_i_P0(Tn)

        return parametrization.T_F_MurphyKoop2005(ln_p)