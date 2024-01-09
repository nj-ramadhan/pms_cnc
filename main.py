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

#     def __init__(self, parent):
#         Frame.__init__(self, parent)
#         self.parent = parent
#         self.initConfig()
#         self.initUI()

#     def initConfig(self):
#         self.run = False
#         self.patternText = np.array(["G","X","Y","Z","A","B","C"])
#         self.lastText = np.array(["0","0.00","0.00","0.00","0.00","0.00","0.00"])      
        
#         self.inputPos = np.array([0., 0., 300.])
#         self.inputRot = np.array([np.deg2rad(0.), np.deg2rad(0.), np.deg2rad(0.)])
#         self.trajectory = np.array([[self.inputPos[0]], [self.inputPos[1]], [self.inputPos[2]]])
#         self.lastPos = np.zeros(3)
#         self.lastRot = np.zeros(3)
#         self.machineOffset = np.array([0., 0., 800.])
#         self.toolOffset = ([0, 0, 90])

#         self.basePos = np.zeros((6, 3))
#         self.platformPos = np.zeros((6, 3))
#         self.prisma = np.zeros(3)
#         self.prismaLength = np.zeros(6)
#         self.dataPrismaLength = np.zeros((2,6))
#         self.travel = np.zeros(3)
#         self.travelLength = 0
#         self.travelVel = 0
#         self.travelTime = 0
#         self.timeSystem = 0
        
#         self.rPlatform = 170.  # in mm
#         self.rBase = 350.     # in mm

#         self.minLength = 490.     # in mm
#         self.maxLength = 740.     # in mm
#         self.maxSpeed = 28.    # in mm/s

#         self.thetaPlatform = np.array([np.deg2rad(45),
#                                        np.deg2rad(75),
#                                        np.deg2rad(165),
#                                        np.deg2rad(-165),
#                                        np.deg2rad(-75),
#                                        np.deg2rad(-45)])

#         self.thetaBase = np.array([np.deg2rad(10),
#                                    np.deg2rad(110),
#                                    np.deg2rad(130),
#                                    np.deg2rad(-130),
#                                    np.deg2rad(-110),
#                                    np.deg2rad(-10)])        

#     def initUI(self):
#         self.parent.title("5 AXIS STEWART CNC G-CODE READER")
#         self.pack(fill=BOTH, expand=1)
#         self.line = 1.0
#         self.maxLine = 1.0
#         self.lineNC = 1.0

#         menubar = Menu(self.parent)
#         self.parent.config(menu=menubar)

#         fileMenu = Menu(menubar)
#         fileMenu.add_command(label="Open", command=self.onOpen)
#         fileMenu.add_command(label="Clear", command=self.onClear)
#         fileMenu.add_command(label="Save", command=self.onSave)
#         fileMenu.add_command(label="Export", command=self.onExport)
#         fileMenu.add_command(label="Exit", command=self.onExit)
#         menubar.add_cascade(label="File", menu=fileMenu)

#         runMenu = Menu(menubar)
#         runMenu.add_command(label="Initialize", command=self.onInit)
#         runMenu.add_command(label="Run/Pause", command=self.onRun)
#         runMenu.add_command(label="Stop", command=self.onStop)
#         menubar.add_cascade(label="Run", menu=runMenu)

#         self.execButton = Button(self, text="Execute", command=self.onExec)
#         self.execButton.place(x=650, y=20)

#         self.prevButton = Button(self, text="Prev", command=self.onPrev)
#         self.prevButton.place(x=780, y=20)

#         self.nextButton = Button(self, text="Next", command=self.onNext)
#         self.nextButton.place(x=840, y=20)

#         self.notif = "Application Started"

#         self.lblGCode = Label(self, text="G-CODE")
#         self.lblGCode.place(x=10, y=0)

#         self.lblNC = Label(self, text="NC")
#         self.lblNC.place(x=10, y=360)
        
#         self.lblNotif = Label(self, text="Application Started")
#         self.lblNotif.config(font=("Calibri", 20))
#         self.lblNotif.place(x=1020, y=100)

#         self.lblG = Label(self, text="G :")
#         self.lblG.place(x=520, y=60)
#         self.lblX = Label(self, text="X :")
#         self.lblX.place(x=520, y=120)
#         self.lblY = Label(self, text="Y :")
#         self.lblY.place(x=520, y=150)
#         self.lblZ = Label(self, text="Z :")
#         self.lblZ.place(x=520, y=180)
#         self.lblA = Label(self, text="A :")
#         self.lblA.place(x=520, y=240)
#         self.lblB = Label(self, text="B :")
#         self.lblB.place(x=520, y=270)
#         self.lblF = Label(self, text="F :                                       Time")
#         self.lblF.place(x=520, y=330)

#         self.lblL = Label(self, text="Link Length      -      Link Length/sec")
#         self.lblL.place(x=680, y=80)
#         self.lblL1 = Label(self, text="1 :                         mm                                 mm/s")
#         self.lblL1.place(x=650, y=120)
#         self.lblL2 = Label(self, text="2 :                         mm                                 mm/s")
#         self.lblL2.place(x=650, y=150)
#         self.lblL3 = Label(self, text="3 :                         mm                                 mm/s")
#         self.lblL3.place(x=650, y=180)
#         self.lblL4 = Label(self, text="4 :                         mm                                 mm/s")
#         self.lblL4.place(x=650, y=210)
#         self.lblL5 = Label(self, text="5 :                         mm                                 mm/s")
#         self.lblL5.place(x=650, y=240)
#         self.lblL6 = Label(self, text="6 :                         mm                                 mm/s")
#         self.lblL6.place(x=650, y=270)

#         self.txtGCode = Text(self, width=47, height=17)
#         self.txtGCode.place(x=10, y=20)
#         self.txtGCode.tag_configure('highlightline', background="#a9e9e9")
#         self.txtGCode.config(font=("TkTextFont", 12))
#         self._highlight_current_line()

#         self.txtNC = Text(self, width=105, height=17)
#         self.txtNC.place(x=10, y=380)
#         self.txtNC.config(font=("TkTextFont", 10))
        
#         self.txtG = Text(self, width=8, height=1)
#         self.txtG.place(x=550, y=60)
#         self.txtX = Text(self, width=8, height=1)
#         self.txtX.place(x=550, y=120)
#         self.txtY = Text(self, width=8, height=1)
#         self.txtY.place(x=550, y=150)
#         self.txtZ = Text(self, width=8, height=1)
#         self.txtZ.place(x=550, y=180)
#         self.txtA = Text(self, width=8, height=1)
#         self.txtA.place(x=550, y=240)
#         self.txtB = Text(self, width=8, height=1)
#         self.txtB.place(x=550, y=270)
#         self.txtF = Text(self, width=8, height=1)
#         self.txtF.place(x=550, y=330)

#         self.txtL1 = Text(self, width=10, height=1)
#         self.txtL1.place(x=680, y=120)
#         self.txtL2 = Text(self, width=10, height=1)
#         self.txtL2.place(x=680, y=150)
#         self.txtL3 = Text(self, width=10, height=1)
#         self.txtL3.place(x=680, y=180)
#         self.txtL4 = Text(self, width=10, height=1)
#         self.txtL4.place(x=680, y=210)
#         self.txtL5 = Text(self, width=10, height=1)
#         self.txtL5.place(x=680, y=240)
#         self.txtL6 = Text(self, width=10, height=1)
#         self.txtL6.place(x=680, y=270)

#         self.txtL1Dot = Text(self, width=10, height=1)
#         self.txtL1Dot.place(x=840, y=120)
#         self.txtL2Dot = Text(self, width=10, height=1)
#         self.txtL2Dot.place(x=840, y=150)
#         self.txtL3Dot = Text(self, width=10, height=1)
#         self.txtL3Dot.place(x=840, y=180)
#         self.txtL4Dot = Text(self, width=10, height=1)
#         self.txtL4Dot.place(x=840, y=210)
#         self.txtL5Dot = Text(self, width=10, height=1)
#         self.txtL5Dot.place(x=840, y=240)
#         self.txtL6Dot = Text(self, width=10, height=1)
#         self.txtL6Dot.place(x=840, y=270)
#         self.txtTime = Text(self, width=10, height=1)
#         self.txtTime.place(x=760, y=330)

#         self.f = Figure(figsize=(3.5, 3.5), dpi=100)
#         self.canvas = FigureCanvasTkAgg(self.f,self)
#         self.canvas.draw()

#         # self.ax = Axes3D(self.f)
#         self.ax = self.f.add_subplot(111, projection='3d')
#         self.ax.mouse_init()
#         self.set_ax()
        
#         self.canvas.get_tk_widget().place(x=890, y=320)


#     def _highlight_current_line(self, interval=100):
#         '''Updates the 'current line' highlighting every "interval" milliseconds'''
#         self.txtGCode.tag_remove('highlightline', 1.0, "end")
#         self.txtGCode.tag_add('highlightline', self.line, str(int(self.line)) +'.end+1c' )
#         self.after(interval, self._highlight_current_line)

#     def extractG(self):
#         try:
#             posG = self.txtGCode.search("G", self.line, str(int(self.line)) + '.end',2)
#             textG = self.txtGCode.get(posG + '+1c', posG + '+2c')
#             self.txtG.insert(1.0, textG)
#             self.lastText[0] = textG
#         except:
#             self.txtG.insert(1.0, self.lastText[0])
#         return (self.txtG.get(1.0, 'end'))

#     def extractX(self):
#         try:
#             posX = self.txtGCode.search("X", self.line, str(int(self.line)) + '.end',6)
#             textX = self.txtGCode.get(posX + '+1c', posX + '+6c')
#             self.txtX.insert(1.0, textX)
#             self.lastText[1] = textX
#         except:
#             self.txtX.insert(1.0, self.lastText[1])
#         return (self.txtX.get(1.0, 'end'))

#     def extractY(self):
#         try:
#             posY = self.txtGCode.search("Y", self.line, str(int(self.line)) + '.end',6)
#             textY = self.txtGCode.get(posY + '+1c', posY + '+6c')
#             self.txtY.insert(1.0, textY)
#             self.lastText[2] = textY
#         except:
#             self.txtY.insert(1.0, self.lastText[2])
#         return (self.txtY.get(1.0, 'end'))

#     def extractZ(self):
#         try:
#             posZ = self.txtGCode.search("Z", self.line, str(int(self.line)) + '.end',6)
#             textZ = self.txtGCode.get(posZ + '+1c', posZ + '+6c')
#             self.txtZ.insert(1.0, textZ)
#             self.lastText[3] = textZ
#         except:
#             self.txtZ.insert(1.0, self.lastText[3])
#         return (self.txtZ.get(1.0, 'end'))

#     def extractA(self):
#         try:
#             posA = self.txtGCode.search("A", self.line, str(int(self.line)) + '.end',6)
#             textA = self.txtGCode.get(posA + '+1c', posA + '+6c')
#             self.txtA.insert(1.0, textA)
#             self.lastText[4] = textA
#         except:
#             self.txtA.insert(1.0, self.lastText[4])
#         return (self.txtA.get(1.0, 'end'))

#     def extractB(self):
#         try:
#             posB = self.txtGCode.search("B", self.line, str(int(self.line)) + '.end',6)
#             textB = self.txtGCode.get(posB + '+1c', posB + '+6c')
#             self.txtB.insert(1.0, textB)
#             self.lastText[5] = textB
#         except:
#             self.txtB.insert(1.0, self.lastText[5])
#         return (self.txtB.get(1.0, 'end'))

#     def extractF(self):
#         try:
#             posF = self.txtGCode.search("F", self.line, str(int(self.line)) + '.end',6)
#             textF = self.txtGCode.get(posF + '+1c', posF + '+6c')
#             self.txtF.insert(1.0, textF)
#             self.lastText[6] = textF
#         except:
#             self.txtF.insert(1.0, self.lastText[6])
#         return (self.txtF.get(1.0, 'end'))
    
#     def draw(self):
#         basePlate = np.array([np.append(self.basePos[:, 0], self.basePos[0, 0]),
#                               np.append(self.basePos[:, 1], self.basePos[0, 1]),
#                               np.append(self.basePos[:, 2], self.basePos[0, 2])])
#         platformPlate = np.array([np.append(self.platformPos[:, 0], self.platformPos[0, 0]),
#                               np.append(self.platformPos[:, 1], self.platformPos[0, 1]),
#                               np.append(self.platformPos[:, 2], self.platformPos[0, 2])])

#         self.ax.plot_trisurf(basePlate[0], basePlate[1], basePlate[2], color='gray', alpha=0.5)
#         self.ax.plot_trisurf(platformPlate[0], platformPlate[1], platformPlate[2], color='gray', alpha=0.5)
#         self.ax.plot_surface(basePlate[0], basePlate[1], np.array([basePlate[2],basePlate[2] - 50]), color='gray')

#         for i in range(6):
#             self.ax.scatter(self.basePos[i, 0], self.basePos[i, 1], self.basePos[i, 2], color="g", s=25)
#             self.ax.scatter(self.platformPos[i, 0], self.platformPos[i, 1], self.platformPos[i, 2], color="g", s=25)
#             self.ax.plot3D([self.basePos[i, 0], self.platformPos[i, 0]], [self.basePos[i, 1], self.platformPos[i, 1]],
#                       [self.basePos[i, 2], self.platformPos[i, 2]])

#         self.ax.plot3D([-400,400], [0,0], [0,0], color="r")
#         self.ax.plot3D([0, 0], [-400, 400], [0, 0], color="r")
#         self.ax.plot3D([self.posMatrix[0], self.inputMatrix[0]], [self.posMatrix[1], self.inputMatrix[1]], [self.posMatrix[2], self.inputMatrix[2]])
#         self.ax.scatter(self.posMatrix[0], self.posMatrix[1], self.posMatrix[2], color="r", s=10)
#         self.ax.scatter(self.inputMatrix[0], self.inputMatrix[1], self.inputMatrix[2], color="b", s=10)
        
#         self.ax.plot3D(self.trajectory[0,:], self.trajectory[1,:], self.trajectory[2,:], color="g")
#         #self.ax.plot3D(self.trajectoryG1[0,:], self.trajectoryG1[1,:], self.trajectoryG1[2,:], color="g")

#     def writeNC(self):
#         self.txtL1.insert(1.0, "{:.3f}".format(self.prismaLength[0]))
#         self.txtL2.insert(1.0, "{:.3f}".format(self.prismaLength[1]))
#         self.txtL3.insert(1.0, "{:.3f}".format(self.prismaLength[2]))
#         self.txtL4.insert(1.0, "{:.3f}".format(self.prismaLength[3]))
#         self.txtL5.insert(1.0, "{:.3f}".format(self.prismaLength[4]))
#         self.txtL6.insert(1.0, "{:.3f}".format(self.prismaLength[5]))
            
#         self.txtL1Dot.insert(1.0, "{:.3f}".format(self.dL[0]))
#         self.txtL2Dot.insert(1.0, "{:.3f}".format(self.dL[1]))
#         self.txtL3Dot.insert(1.0, "{:.3f}".format(self.dL[2]))
#         self.txtL4Dot.insert(1.0, "{:.3f}".format(self.dL[3]))
#         self.txtL5Dot.insert(1.0, "{:.3f}".format(self.dL[4]))
#         self.txtL6Dot.insert(1.0, "{:.3f}".format(self.dL[5]))
        
#         self.txtTime.insert(1.0, "{:.3f}".format(self.travelTime))

#     def validator(self):
#         if (self.shortPrismatic >= self.minLength) and (self.longPrismatic <= self.maxLength) and (self.maxDL <= self.maxSpeed):  # check boundaries          
#             self.notif = "Executing Move Command"
#             self.lblNotif.configure(text=self.notif, foreground="green")
#             self.ax.cla()
#             self.set_ax()
#             self.draw()
#             self.canvas.draw()
			
# ##            self.ij_prismaVel()
# ##            print(self.prismaVel)
            
#         else:
#             self.notif = "Move Command Couldn't Be Executed"
#             self.lblNotif.configure(text=self.notif, foreground="red")
#             self.onStop()


#     def onExec(self):
#         self.resetData()
#         if int(self.extractG()) == 0:
#             self.travelVel = 20.0
#             self.txtF.insert(1.0, '20.0')            
#             self.inputPos = np.array([float(self.extractX()), float(self.extractY()), float(self.extractZ())])
#             self.inputRot = np.array([np.deg2rad(0.), np.deg2rad(float(self.extractB())), np.deg2rad(float(self.extractA()))])
            
#             self.trajectory = np.append(self.trajectory, [[self.inputPos[0]], [self.inputPos[1]], [self.inputPos[2]]], axis=1)
#             self.ik_orientation()
#             self.ik_position()
            
#             self.dataPrismaLength[0,:] = self.ik_prismatic()

#             if self.travelVel > 0:
#                 self.travelTime = self.travelLength / self.travelVel
#                 #print(self.travelTime)
			
#             else:
#                 self.travelTime = 0.1           
            
#             if self.travelTime > 0:
#                 self.dL = (self.dataPrismaLength[0,:] - self.dataPrismaLength[1,:]) / self.travelTime
#             else:
#                 self.dL = np.zeros(6)
            
#             self.timeSystem = self.timeSystem + self.travelTime
#             self.travel = self.inputPos - self.lastPos
#             self.travelLength = np.sqrt(np.dot(self.travel , self.travel.T))

#             self.maxDL = np.max(np.abs(self.dL))
                    
#             self.writeNC()
                        
#             lbl = ["A","B","C","D","E","F"]
#             text1 = text2 = ""
#             for i in range(0,6):
#                 text1 += "L" + lbl[i] + "{:.2f} ".format(self.prismaLength[i])

#             for i in range(0,6):
#                 text2 += "dL" + lbl[i] + "{:.2f} ".format(self.dL[i])

#             text = text1 + text2 + "T" + "{:.2f}".format(self.timeSystem) + "\n"

#             self.txtNC.insert(self.lineNC, text)
#             self.lineNC += 1

#             self.lblNotif.update()
#             self.lastPos = self.inputPos
#             self.lastRot = self.inputRot
#             self.dataPrismaLength[1,:] = self.dataPrismaLength[0,:]            
            
#             self.validator()        

            
#         else:
#             self.travelVel = float(self.extractF())
#             self.inputPos = np.array([float(self.extractX()), float(self.extractY()), float(self.extractZ())])
#             self.inputRot = np.array([np.deg2rad(0.), np.deg2rad(float(self.extractB())), np.deg2rad(float(self.extractA()))])
            
#             self.trajectory = np.append(self.trajectory, [[self.inputPos[0]], [self.inputPos[1]], [self.inputPos[2]]], axis=1)
#             self.ik_orientation()
#             self.ik_position()

#             self.dataPrismaLength[0,:] = self.ik_prismatic()

#             if self.travelVel > 0:
#                 self.travelTime = self.travelLength / self.travelVel
			
#             else:
#                 self.travelTime = 0.1           
            
#             if self.travelTime > 0:
#                 self.dL = (self.dataPrismaLength[0,:] - self.dataPrismaLength[1,:]) / self.travelTime
#             else:
#                 self.dL = np.zeros(6)
            
#             self.travel = self.inputPos - self.lastPos
#             self.travelLength = np.sqrt(np.dot(self.travel , self.travel.T))

#             self.maxDL = np.max(np.abs(self.dL))
            
#             n = int(self.travelTime / 1.0)  #constant time for interpolation
            
#             tempPosX = np.linspace(self.lastPos[0], self.inputPos[0], n)
#             tempPosY = np.linspace(self.lastPos[1], self.inputPos[1], n)
#             tempPosZ = np.linspace(self.lastPos[2], self.inputPos[2], n)
#             tempRotA = np.linspace(self.lastRot[0], self.inputRot[0], n)
#             tempRotB = np.linspace(self.lastRot[1], self.inputRot[1], n)
#             tempTime = np.linspace(0, self.travelTime, n)
            
#             for i in range (n):
#                 self.inputPos = np.array([tempPosX[i], tempPosY[i], tempPosZ[i]])
#                 self.inputRot = np.array([np.deg2rad(0.), tempRotB[i], tempRotA[i]])
#                 self.ik_orientation()
#                 self.ik_position()
                
#                 self.dataPrismaLength[0,:] = self.ik_prismatic()
#                 self.resetDataInterpolating()
#                 self.writeNC()
                
#                 lbl = ["A","B","C","D","E","F"]
#                 text1 = text2 = ""
#                 for j in range(0,6):
#                     text1 += "L" + lbl[j] + "{:.2f} ".format(self.prismaLength[j])
                    
#                 for k in range(0,6):
#                     text2 += "dL" + lbl[k] + "{:.2f} ".format(self.dL[k])

#                 text = text1 + text2 + "T" + "{:.2f}".format(self.timeSystem + tempTime[i]) + "\n"
#                 self.txtNC.insert(self.lineNC, text)
#                 self.lineNC += 1
        
#             self.lblNotif.update()
#             self.lastPos = self.inputPos
#             self.lastRot = self.inputRot
#             self.dataPrismaLength[1,:] = self.dataPrismaLength[0,:]
            
#             self.timeSystem = self.timeSystem + self.travelTime
#             self.validator()


#     def onPrev(self):
#         if self.line > 1.0:
#             self.line -= 1.0
#         else:
#             self.line = 1.0

#     def onNext(self):
#         if self.line < self.maxLine:
#             self.line += 1.0
        
#     def onSave(self):
#         name = filedialog.asksaveasfile(mode='w',defaultextension=".gcode")
#         text2save=str(self.txtGCode.get(0.0,END))
#         name.write(text2save)
#         name.close

#     def onExport(self):
#         name = filedialog.asksaveasfile(mode='w',defaultextension=".spnc")
#         text2save=str(self.txtNC.get(0.0,END))
#         name.write(text2save)
#         name.close

#     def onClear(self):
#         self.txtGCode.delete(1.0, 'end')
#         self.txtNC.delete(1.0, 'end')
#         self.trajectory = np.array([[self.inputPos[0]], [self.inputPos[1]], [self.inputPos[2]]])
#         #self.trajectoryG0 = np.array([[self.inputPos[0]], [self.inputPos[1]], [self.inputPos[2]]])
#         #self.trajectoryG1 = np.array([[self.inputPos[0]], [self.inputPos[1]], [self.inputPos[2]]])
#         self.draw()
#         self.canvas.draw()

#     def onOpen(self):
#         ftypes = [('G-code files', '*.gcode'), ('All files', '*')]
#         dlg = filedialog.Open(self, filetypes = ftypes)
#         fl = dlg.show()

#         if fl != '':
#             text = self.readFile(fl)
#             self.txtGCode.insert(1.0, text)
#             self.maxLine = math.floor(float(self.txtGCode.index('end-1c')))

#     def readFile(self, filename):
#         f = open(filename, "r")
#         text = f.read()
#         return text

#     def onInit(self):
#         self.inputPos = np.array([0., 0., 300.])
#         self.trajectory = np.array([[self.inputPos[0]], [self.inputPos[1]], [self.inputPos[2]]])
#         #self.trajectoryG1 = np.array([[self.inputPos[0]], [self.inputPos[1]], [self.inputPos[2]]])
#         self.line = 1.0
#         self.timeSystem = 0
#         self.onExec()

#     def onRun(self):
#         self.run = not self.run
#         if self.run:
#             print("Robot Started")
#             self.notif = "Robot Started"
#             self.lblNotif.configure(text=self.notif, foreground="blue")
            
#             self.trajectory = np.delete(self.trajectory, 0, 1)
#             #self.trajectoryG1 = np.delete(self.trajectoryG1, 0, 1)            
            
#             #time.sleep(5)
#             while self.line <= self.maxLine:
#                 self.onExec()
#                 t = 0.
#                 while t < self.travelTime:
#                     t+=0.1
#                     #time.sleep(0.1)

#                     # run control here
                    
#                 if self.line == self.maxLine:
#                     self.notif = "End of Process"
#                     self.lblNotif.configure(text=self.notif, foreground="red")
#                     self.onStop()

#                 if not self.run:
#                     break
                
#                 self.notif = "Move Command Executed"
#                 self.lblNotif.configure(text=self.notif, foreground="blue")
#                 #time.sleep(5)

#                 self.onNext()
                                
#         else:
#             print("Robot Paused")
#             self.notif = "Robot Paused"
#             self.lblNotif.configure(text=self.notif, foreground="red")

#     def onStop(self):
#         print("Robot Stopped")
#         self.run = False

#     def onExit(self):
#         self.quit()
#         # self.destroy()
        
#     def ik_prismatic(self):
#         for i in range(6):
#             self.basePos[i] = [self.rBase * np.cos(self.thetaBase[i]), self.rBase * np.sin(self.thetaBase[i]), 0] + self.machineOffset
#             self.platformPos[i] = [self.rPlatform * np.cos(self.thetaPlatform[i]), self.rPlatform * np.sin(self.thetaPlatform[i]), 0]

#         self.platformPos = np.dot(self.orientMatrix, self.platformPos.T)
#         self.platformPos = self.posMatrix + self.platformPos.T
#         self.prisma = self.platformPos - self.basePos

#         for i in range(6):
#             self.prismaLength[i] = np.sqrt(np.dot(self.prisma[i], self.prisma[i].T))

#         self.shortPrismatic = np.min(self.prismaLength)
#         self.longPrismatic = np.max(self.prismaLength)
        
#         return self.prismaLength

#     def ik_position(self):
#         self.inputMatrix = np.array([self.inputPos[0], self.inputPos[1], self.inputPos[2]])
#         self.posMatrix = self.inputMatrix + np.dot(self.orientMatrix, self.toolOffset)
#         return self.posMatrix

#     def ik_orientation(self):
#         self.orientMatrix = np.array([[np.cos(self.inputRot[0]) * np.cos(self.inputRot[1]),
#                                   (np.cos(self.inputRot[0]) * np.sin(self.inputRot[1]) * np.sin(self.inputRot[2])) - (np.sin(self.inputRot[0]) * np.cos(self.inputRot[2])),
#                                   (np.cos(self.inputRot[0]) * np.sin(self.inputRot[1]) * np.cos(self.inputRot[2])) + (np.sin(self.inputRot[0]) * np.sin(self.inputRot[2]))],
#                                  [np.sin(self.inputRot[0]) * np.cos(self.inputRot[1]),
#                                   (np.sin(self.inputRot[0]) * np.sin(self.inputRot[1]) * np.sin(self.inputRot[2])) + (np.cos(self.inputRot[0]) * np.cos(self.inputRot[2])),
#                                   (np.sin(self.inputRot[0]) * np.sin(self.inputRot[1]) * np.cos(self.inputRot[2])) - (np.cos(self.inputRot[0]) * np.sin(self.inputRot[2]))],
#                                  [-np.sin(self.inputRot[1]),
#                                   np.cos(self.inputRot[1]) * np.sin(self.inputRot[2]),
#                                   np.cos(self.inputRot[1]) * np.cos(self.inputRot[2])]])
#         return self.orientMatrix

#     def ij_constant(self):
#         for i in range(6):
#             self.basePos[i] = [self.rBase * np.cos(self.thetaBase[i]), self.rBase * np.sin(self.thetaBase[i]), 0] + self.machineOffset
#             self.platformPos[i] = [self.rPlatform * np.cos(self.thetaPlatform[i]), self.rPlatform * np.sin(self.thetaPlatform[i]), 0]

#         c1 = np.dot(self.orientMatrix, self.platformPos.T)
#         c1T = np.transpose(c1)
#         c2 = np.cross(c1 , self.prisma)
#         c2T = np.transpose(c2)
#         c3 = np.dot(c1T , c2T)
#         return c3

#     def ij_variable(self):
#         dLinear = self.inputPos - self.lastPos
#         dAngular = self.inputRot - self.lastRot
#         self.velocity = np.array([self.dLinear, self.dAngular])
#         return self.velocity

#     def ij_invDiagLength(self):
#         diag = np.diag(self.prismaLength)
#         invDiag = np.linalg.inv(diag)
#         return invDiag

#     def ij_prismaVel(self):
#         temp = np.dot(self.ij_constant() , self.ij_variable())
#         prismaVel = np.dot(self.ij_invDiagLength() , temp)
#         return prismaVel
    
#     def set_ax(self):#ax panel set up
#         self.ax.set_aspect("equal")
#         self.ax.set_xlim3d(-400, 400)
#         self.ax.set_ylim3d(-400, 400)
#         self.ax.set_zlim3d(0, 800)
#         self.ax.set_xlabel('X axis')
#         self.ax.set_ylabel('Y axis')
#         self.ax.set_zlabel('Z axis')
#         self.ax.set_axisbelow(True) #send grid lines to the background

#     def resetData(self):
#         self.txtG.delete(1.0, 'end')
#         self.txtA.delete(1.0, 'end')
#         self.txtB.delete(1.0, 'end')
#         self.txtX.delete(1.0, 'end')
#         self.txtY.delete(1.0, 'end')
#         self.txtZ.delete(1.0, 'end')
#         self.txtF.delete(1.0, 'end')
#         self.txtL1.delete(1.0, 'end')
#         self.txtL2.delete(1.0, 'end')
#         self.txtL3.delete(1.0, 'end')
#         self.txtL4.delete(1.0, 'end')
#         self.txtL5.delete(1.0, 'end')
#         self.txtL6.delete(1.0, 'end')
#         self.txtL1Dot.delete(1.0, 'end')
#         self.txtL2Dot.delete(1.0, 'end')
#         self.txtL3Dot.delete(1.0, 'end')
#         self.txtL4Dot.delete(1.0, 'end')
#         self.txtL5Dot.delete(1.0, 'end')
#         self.txtL6Dot.delete(1.0, 'end')
#         self.txtTime.delete(1.0, 'end')

#     def resetDataInterpolating(self):
#         self.txtL1.delete(1.0, 'end')
#         self.txtL2.delete(1.0, 'end')
#         self.txtL3.delete(1.0, 'end')
#         self.txtL4.delete(1.0, 'end')
#         self.txtL5.delete(1.0, 'end')
#         self.txtL6.delete(1.0, 'end')
#         self.txtL1Dot.delete(1.0, 'end')
#         self.txtL2Dot.delete(1.0, 'end')
#         self.txtL3Dot.delete(1.0, 'end')
#         self.txtL4Dot.delete(1.0, 'end')
#         self.txtL5Dot.delete(1.0, 'end')
#         self.txtL6Dot.delete(1.0, 'end')
#         self.txtTime.delete(1.0, 'end')

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