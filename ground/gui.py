import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import time

class GUI(): #this is a very crude version of this class, much to do
    def __init__(self):
        #didn't make root into its own config cause this is root's config, will change probs
        self.root = tk.Tk()
        self.root.title("Front-end is not rocket science")

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.left_frame = self.init_lf() 
        self.right_frame = self.init_rf() 
        self.fig3d = graph3d(self.left_frame, 0, 0)
        self.fig2d = graph2d(self.left_frame, 1, 0)


    def init_lf(self):
        left_frame = tk.Frame(self.root, bg='lightblue')
        left_frame.grid(row=0, column=0, sticky="nsew")
        #left frame config    
        left_frame.grid_rowconfigure(0, weight=3)
        left_frame.grid_rowconfigure(1, weight=2)
        left_frame.grid_columnconfigure(0, weight=1)
        return left_frame

    def init_rf(self):
        right_frame = tk.Frame(self.root, bg='lightgreen', borderwidth=2, relief='groove')
        #right frame config
        right_frame.grid(row=0, column=1, sticky="nsew")
        return right_frame

    def run(self):
        self.root.mainloop()

class graph3d:
    def __init__(self, parent_frame, row, column):
        self.frame = tk.Frame(parent_frame, bg='blue', borderwidth=2, relief='groove')
        self.frame.grid(row=row, column=column, sticky="nsew")
        self.line = None
        self.plt = None
        self.fig_3d = self.createPlot(self.frame.winfo_width(), self.frame.winfo_height())
        self.canvas_3d = FigureCanvasTkAgg(self.fig_3d, master=self.frame)
        self.canvas_3d.draw()
        self.canvas_3d.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def createPlot(self, w, h):
        fig_3d = Figure(figsize=(w/100, h/100), dpi=100)
        plot_3d = fig_3d.add_subplot(111, projection='3d')
        #example data
        x = [0, 100, 200]
        y = [0, 100, 200]
        z = [0, 100, 200]
        plot_3d.set_title(f'Trajectory')
        plot_3d.set_xlabel('X[m]')
        plot_3d.set_ylabel('Y[m]')
        plot_3d.set_zlabel('Z[m]')
        #plot_3d.zaxis._axinfo['label']['space_factor'] = 20.0
        #messing around with stuff
        plot_3d.axes.set_xlim([-200, 200])
        plot_3d.axes.set_ylim([-200,200]) 
        plot_3d.axes.set_zlim([0, 600])
        self.line, = plot_3d.plot(x, y, z)
        return fig_3d

    def update(x, y, z):
        #TO DO
        self.line.set_data_3d(x, y, z)
        self.canvas_3d.draw()
 
class graph2d:
    def __init__(self, parent_frame, row, column):
        self.frame = tk.Frame(parent_frame, bg='red', borderwidth=2, relief='groove')
        self.frame.grid(row=row, column=column, sticky="nsew")
        self.line = None
        self.plt = None
        self.fig_2d = self.createPlot(self.frame.winfo_width(), self.frame.winfo_height())
        self.canvas_2d = FigureCanvasTkAgg(self.fig_2d, master=self.frame)  
        self.canvas_2d.draw()
        self.canvas_2d.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def createPlot(self, w, h):
        fig_2d = Figure(figsize = (w/100,h/100), dpi =100)
        plt = fig_2d.add_subplot(1, 1, 1)
        x = [0, 10, 20]
        y = [0, -5, 5]
        self.line, = plt.plot(x, y)
        plt.set_title(f'Height vs time')
        plt.set_xlabel('Time[s]')
        plt.set_ylabel('Height[m]')
        plt.set_xlim([0, 50])
        plt.set_ylim([-10,10]) 
        return fig_2d

    def update(self, x, y):
        #TODO also resizing, clearing and sliding? (when too much time passes so that old data is forgotten or have rather some leeway? IDK
        self.line.set_data(x, y)
        self.canvas_2d.draw()

if __name__ == "__main__":
    mygui = GUI()
    mygui.run()
