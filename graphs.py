import matplotlib.pyplot as plt
import matplotlib.text
from labellines import labelLines
import numpy as np
from numpy._core.function_base import linspace as linspace

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

    def plot(self, x, y, name, label="", color='b', lw=1, labelLine=True, align=True, xvals=None):
        self.lines[name], = self.ax.plot(x, y, label=label, color=color, lw=lw)
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

    def S_i1(self):
        S_in = [parametrization.S_w2S_i_P0(T, 1) for T in self.Tn]
        self.plot(self.Tn, S_in, name="S_w1", label="$S_w = 1$", color="blue")

        if self.T_FTGraphLinked:
            T_Fn = self.T_FTGraph.S_in2T_Fn(self.Tn, S_in)
            self.T_FTGraph.plot(self.Tn, T_Fn, name="S_w1", label="$S_w = 1$", color="blue")

    def iso_S_w(self, S_wn = np.linspace(0,0.9, 10)):
        for S_w in S_wn:
            S_in = [parametrization.S_w2S_i_P0(T, S_w) for T in self.Tn]
            self.plot(self.Tn, S_in, name="S_w{:0.1f}".format(S_w), label="{:0.1f}".format(S_w), color="lightgrey", xvals=270)

            if not S_w == 0.0:
                T_Fn = self.T_FTGraph.S_in2T_Fn(self.Tn, S_in)
                self.T_FTGraph.plot(self.Tn, T_Fn, name="S_w{:0.1f}".format(S_w), label="{:0.1f}".format(S_w), color="lightgrey", xvals=270)
            else:
                self.T_FTGraph.plot([], [], name="S_w0")     
        
class T_FTGraph(Graph):

    def __init__(self, title="$T_F = f(T)$", x_label="$T (K)$", y_label="$T_F(T)$", Tn=np.linspace(235, 273, 100)):
        super().__init__(title, x_label, y_label, Tn)

    def S_in2T_Fn(self, Tn, S_in):
        TnLen = np.array(Tn).size
        ln_p = np.log(S_in) + parametrization.ln_p_i_P0(Tn)

        return parametrization.T_F_MurphyKoop2002(ln_p)