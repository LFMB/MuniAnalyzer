import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np


class Window(tk.Tk):
    def __init__(self, title, view_model_dict, geo_models):
        tk.Tk.__init__(self)
        self.title(title)
        # self.geometry("680x450")
        self.views = {}
        self.geo_models = geo_models
        self.ui_controllers = {}
        self.view_container = ''
        self.ui_controller_container = ''
        self.ui_controller_columns_num = len(view_model_dict)

        self.__create_view_container()
        self.__create_views(view_model_dict)

        self.__create_ui_controller_container()

    def __create_view_container(self):
        view_container = ttk.Frame(self)
        view_container.pack(side="top", fill="both")

        view_container.grid_rowconfigure(0, weight=1)
        view_container.grid_columnconfigure(0, weight=1)
        self.view_container = view_container

    def __create_views(self, view_model_dict):
        parent_frame = self.view_container
        geo_data = self.geo_models
        # print(geo_data.keys())
        for view_model_item in view_model_dict.values():
            name = view_model_item['name']
            text = view_model_item['text']
            if name == 'default_view':
                view = BasicView(master=parent_frame, name=name, text=text)
            else:
                print('name: ', name)
                # using just parcels but need to combine geo sets somehow
                view = HeatMapDistributionContainer(master=parent_frame, name=name, map_model=geo_data)
            view.grid(row=0, column=0, sticky="nsew")
            self.views[name] = view
        # print('created views: ', self.views)

    def __create_ui_controller_container(self):
        controller_container = ttk.Frame(self)
        controller_container.pack(side="bottom", fill="both")
        controller_item_columns = self.ui_controller_columns_num

        controller_container.grid_rowconfigure(1, weight=1)
        controller_container.grid_columnconfigure(controller_item_columns, weight=1)
        self.ui_controller_container = controller_container

    # uses the buttons_model which is aka view_model_dict in __create_views
    def create_ui_controllers(self, ui_controller_model_dict, app_controller):
        parent_frame = self.view_container
        column_num = 0
        for ui_controller in ui_controller_model_dict.values():
            name = ui_controller['name']
            text = ui_controller['text']
            # print('name: ', name)
            button = ttk.Button(parent_frame, text=text, command=lambda: app_controller.show_view(name))
            # need to fix grid spacing
            button.grid(row=1, column=column_num, sticky='ew')
            # don't have a use for the ui_controllers dict yet
            self.ui_controllers[name] = button
            column_num += 1


class BasicView(ttk.Frame):
    def __init__(self, master=None, name="Main", text=""):
        super().__init__(master)
        self.name = name
        self.__create_view(text)

    def __create_view(self, text):
        header = ttk.Label(self, text=text)
        # view.pack(side="top")
        header.grid(row=1)


# need to figure out how to segment statistical and map data
class HeatMapDistributionContainer(ttk.Frame):
    def __init__(self, master=None, map_model=[], stats_model={}, name=""):
        super().__init__(master)
        self.master = master
        self.container = ttk.Frame()
        self.name = name
        self.heat_map_figure = ''
        self.heat_map = ''
        self.distribution_graph = ''
        self.__create_map(map_model, stats_model)
        self.__create_graph(stats_model)

    def __create_map(self, map_model, stats_model):
        fig = Figure(figsize=(5, 5), dpi=200)
        axes = fig.add_subplot()
        # todo: still testing how to pass the stats_model that will be highlighted in view
        map_model.plot(ax=axes, column='Total_Asse')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)

        # need to assign UI element to self.heat_map
        header = ttk.Label(self, text=("map UI ", self.name))
        header.grid(row=2, column=0)

    def __create_graph(self, stats_model):

        fig = Figure(figsize=(5, 5), dpi=200)
        # junk data for placeholder view
        t = np.arange(0, 3, .01)
        fig.add_subplot().scatter(t, 2 * np.sin(2 * np.pi * t))
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1)
        # this proves each view is separate
        header = ttk.Label(self, text=("distribution_graph ", self.name))
        header.grid(row=2, column=1)
        self.distribution_graph = header



