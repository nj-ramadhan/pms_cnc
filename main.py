import numpy as np
import kivy
import sys
import os
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.animation import Animation
from kivymd.theming import ThemableBehavior
from kivy.clock import Clock
from kivy.config import Config
from kivy.metrics import dp
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.ticker import AutoMinorLocator
from datetime import datetime

plt.style.use('bmh')

colors = {
    "Red": {
        "200": "#EE2222",
        "500": "#EE2222",
        "700": "#EE2222",
    },

    "Blue": {
        "200": "#2222EE",
        "500": "#2222EE",
        "700": "#2222EE",
    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "#202020",
        "Background": "#EEEEEE",
        "CardsDialogs": "#FFFFFF",
        "FlatButtonDown": "#CCCCCC",
    },
}

from kivy.properties import ObjectProperty
import time

STEPS = 51
MAX_POINT = 500
ELECTRODES_NUM = 48

flag_run = False

class ScreenSplash(BoxLayout):
# class ScreenSplash(Screen):
    screen_manager = ObjectProperty(None)
    screen_setting = ObjectProperty(None)
    app_window = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(ScreenSplash, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_progress_bar, .01)

    def update_progress_bar(self, *args):
        if (self.ids.progress_bar.value + 1) < 100:
            raw_value = self.ids.progress_bar_label.text.split('[')[-1]
            value = raw_value[:-2]
            value = eval(value.strip())
            new_value = value + 1
            self.ids.progress_bar.value = new_value
            self.ids.progress_bar_label.text = 'Loading.. [{:} %]'.format(new_value)
        else:
            self.ids.progress_bar.value = 100
            self.ids.progress_bar_label.text = 'Loading.. [{:} %]'.format(100)
            time.sleep(0.5)
            self.screen_manager.current = 'screen_home'
            return False

class ScreenHome(BoxLayout):
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ScreenHome, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init)
        Clock.schedule_interval(self.regular_check, 1)

    def regular_check(self, dt):
        x = datetime.now()
        text_waktu = x.strftime("%H:%M:%S\n%Y-%m-%d")
        self.ids.text_jam.text = text_waktu
        global flag_run

    def delayed_init(self, dt):
        self.fig, self.ax = plt.subplots()
        self.fig.set_facecolor("#eeeeee")
        self.fig.tight_layout(pad=3.0)

    def illustrate(self):
        global dt_mode
        global dt_config

    def measure(self):
        global flag_run
        if(flag_run):
            flag_run = False
        else:
            flag_run = True

    def screen_home(self):
        self.screen_manager.current = 'screen_home'
    
    def screen_setting(self):
        self.screen_manager.current = 'screen_setting'

    def screen_data(self):
        self.screen_manager.current = 'screen_data'

    def screen_graph(self):
        self.screen_manager.current = 'screen_graph'

class ScreenSetting(BoxLayout):
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ScreenSetting, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init)
        Clock.schedule_interval(self.regular_check, 1)

    def regular_check(self, dt):
        x = datetime.now()
        text_waktu = x.strftime("%H:%M:%S\n%Y-%m-%d")
        self.ids.text_jam.text = text_waktu
        global flag_run

    def delayed_init(self, dt):
        self.fig, self.ax = plt.subplots()
        self.fig.set_facecolor("#eeeeee")
        self.fig.tight_layout(pad=3.0)

    def illustrate(self):
        global dt_mode
        global dt_config

    def measure(self):
        global flag_run
        if(flag_run):
            flag_run = False
        else:
            flag_run = True

    def screen_setting(self):
        self.screen_manager.current = 'screen_setting'

    def screen_data(self):
        self.screen_manager.current = 'screen_data'

    def screen_graph(self):
        self.screen_manager.current = 'screen_graph'

class ScreenData(BoxLayout):
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ScreenData, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init)
        Clock.schedule_interval(self.regular_check, 0.1)

    def regular_check(self, dt):
        global flag_run

    def delayed_init(self, dt):
        print("enter delayed init")
        layout = self.ids.layout_tables
        
        self.data_tables = MDDataTable(
            use_pagination=True,
            column_data=[
                ("No.", dp(30)),
                ("Voltage", dp(30)),
                ("Current", dp(30)),
                ("Resistivity", dp(30)),
                ("Std Dev Voltage", dp(30)),
                ("Std Dev Current", dp(30)),
            ],
            row_data=[(f"{i + 1}", "1", "2", "3", "4", "5") for i in range(5)]
        )
        layout.add_widget(self.data_tables)

    def save_data(self):
        self.data_tables.row_data=[(f"{i + 1}", "1", "2", "3", "4", "5") for i in range(5)]

    def measure(self):
        global flag_run
        if(flag_run):
            flag_run = False
        else:
            flag_run = True

    def screen_setting(self):
        self.screen_manager.current = 'screen_setting'

    def screen_data(self):
        self.screen_manager.current = 'screen_data'

    def screen_graph(self):
        self.screen_manager.current = 'screen_graph'

class ScreenGraph(BoxLayout):
    screen_manager = ObjectProperty(None)
    global flag_run

    def __init__(self, **kwargs):
        super(ScreenGraph, self).__init__(**kwargs)
        Clock.schedule_once(self.delayed_init)
        Clock.schedule_interval(self.regular_check, 0.1)

    def regular_check(self, dt):
        global flag_run

    def delayed_init(self, dt):
        print("enter delayed init")
        
        self.fig, self.ax = plt.subplots()
        self.fig.set_facecolor("#eeeeee")
        self.fig.tight_layout(pad=3.0)

        self.data_colormap = np.zeros((10, 100))

        clrmesh = self.ax.pcolor(self.data_colormap, cmap='seismic', vmin=-0.1, vmax=0.1)
        self.fig.colorbar(clrmesh, ax=self.ax, format='%f')

        self.ids.layout_graph.add_widget(FigureCanvasKivyAgg(self.fig))

    def measure(self):
        global flag_run
        if(flag_run):
            flag_run = False
        else:
            flag_run = True

    def save_graph(self):
        pass

    def screen_setting(self):
        self.screen_manager.current = 'screen_setting'

    def screen_data(self):
        self.screen_manager.current = 'screen_data'

    def screen_graph(self):
        self.screen_manager.current = 'screen_graph'

class PMS_CNCApp(MDApp):
    def build(self):
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Blue"
        # Window.fullscreen = 'auto'
        # Window.borderless = True
        # Window.size = (1280, 1024)
        # Window.size = (1280, 786)
        Window.size = (1024, 600)
        Window.allow_screensaver = True
        self.icon = 'asset/logo.ico'

        screen = Builder.load_file('main.kv')

        return screen


if __name__ == '__main__':
    PMS_CNCApp().run()