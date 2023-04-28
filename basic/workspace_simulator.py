# import matplotlib as mpl
# mpl.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# from matplotlib import style
# import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# # generate some random data
# x = np.random.rand(100)
# y = np.random.rand(100)
# z = np.random.rand(100)

# # create a 3D figure
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # plot the scatter points
# ax.scatter(x, y, z, c='r', marker='o')

# # set the axis labels
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')

# # show the plot
# plt.show()
   
class Run():
    inputPos = np.array([0., 0., 0.])
    inputRot = np.array([np.deg2rad(0.), np.deg2rad(0.), np.deg2rad(0.)])
    trajectory = np.array([[inputPos[0]], [inputPos[1]], [inputPos[2]]])
    lastPos = np.zeros(3)
    lastRot = np.zeros(3)
    machineOffset = np.array([0., 0., 800.])
    toolOffset = ([0, 0, 90])

    basePos = np.zeros((6, 3))
    platformPos = np.zeros((6, 3))
    prisma = np.zeros(3)
    prismaLength = np.zeros(6)
    dataPrismaLength = np.zeros((2,6))
    travel = np.zeros(3)
    travelLength = 0
    travelVel = 0
    travelTime = 0
    timeSystem = 0
    
    rPlatform = 170.  # in mm
    rBase = 350.     # in mm

    minLength = 490.     # in mm
    maxLength = 740.     # in mm
    maxSpeed = 28.    # in mm/s

    thetaPlatform = np.array([np.deg2rad(45),
                                    np.deg2rad(75),
                                    np.deg2rad(165),
                                    np.deg2rad(-165),
                                    np.deg2rad(-75),
                                    np.deg2rad(-45)])

    thetaBase = np.array([np.deg2rad(10),
                                np.deg2rad(110),
                                np.deg2rad(130),
                                np.deg2rad(-130),
                                np.deg2rad(-110),
                                np.deg2rad(-10)])        

    def draw(self):
        # create a 3D figure
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # # show robot
        # basePlate = np.array([np.append(self.basePos[:, 0], self.basePos[0, 0]),
        #                       np.append(self.basePos[:, 1], self.basePos[0, 1]),
        #                       np.append(self.basePos[:, 2], self.basePos[0, 2])])
        # platformPlate = np.array([np.append(self.platformPos[:, 0], self.platformPos[0, 0]),
        #                       np.append(self.platformPos[:, 1], self.platformPos[0, 1]),
        #                       np.append(self.platformPos[:, 2], self.platformPos[0, 2])])

        # ax.plot_trisurf(basePlate[0], basePlate[1], basePlate[2], color='gray', alpha=0.5)
        # ax.plot_trisurf(platformPlate[0], platformPlate[1], platformPlate[2], color='gray', alpha=0.5)
        # ax.plot_surface(basePlate[0], basePlate[1], np.array([basePlate[2],basePlate[2] - 50]), color='gray')

        # for i in range(6):
        #     ax.scatter(self.basePos[i, 0], self.basePos[i, 1], self.basePos[i, 2], color="g", s=25)
        #     ax.scatter(self.platformPos[i, 0], self.platformPos[i, 1], self.platformPos[i, 2], color="g", s=25)
        #     ax.plot3D([self.basePos[i, 0], self.platformPos[i, 0]], [self.basePos[i, 1], self.platformPos[i, 1]],
        #               [self.basePos[i, 2], self.platformPos[i, 2]])

        # ax.plot3D([-400,400], [0,0], [0,0], color="r")
        # ax.plot3D([0, 0], [-400, 400], [0, 0], color="r")
        # ax.plot3D([self.posMatrix[0], self.inputMatrix[0]], [self.posMatrix[1], self.inputMatrix[1]], [self.posMatrix[2], self.inputMatrix[2]])
       
        tri = Triangulation(self.trajectory[0], self.trajectory[1])

        # plot the scatter points
        cmap = matplotlib.colormaps['RdYlGn_r'] 
        # cmap = plt.cm.get_cmap('RdYlGn_r')
        # ax.scatter(self.trajectory[0], self.trajectory[1], self.trajectory[2], c=self.trajectory[2], cmap=cmap, s=5, alpha=0.5)
        ax.plot_trisurf(self.trajectory[0], self.trajectory[1], self.trajectory[2], triangles=tri.triangles, cmap=cmap)
        # cbar = plt.colorbar()
        # cbar.set_label('Z values')
        # set the axis labels
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        # show the plot
        plt.show()

    def ik_prismatic(self):
        for i in range(6):
            self.basePos[i] = [self.rBase * np.cos(self.thetaBase[i]), self.rBase * np.sin(self.thetaBase[i]), 0] + self.machineOffset
            self.platformPos[i] = [self.rPlatform * np.cos(self.thetaPlatform[i]), self.rPlatform * np.sin(self.thetaPlatform[i]), 0]

        self.platformPos = np.dot(self.orientMatrix, self.platformPos.T)
        self.platformPos = self.posMatrix + self.platformPos.T
        self.prisma = self.platformPos - self.basePos

        for i in range(6):
            self.prismaLength[i] = np.sqrt(np.dot(self.prisma[i], self.prisma[i].T))

        self.shortPrismatic = np.min(self.prismaLength)
        self.longPrismatic = np.max(self.prismaLength)
        
        return self.prismaLength

    def ik_position(self):
        self.inputMatrix = np.array([self.inputPos[0], self.inputPos[1], self.inputPos[2]])
        self.posMatrix = self.inputMatrix + np.dot(self.orientMatrix, self.toolOffset)
        return self.posMatrix

    def ik_orientation(self):
        self.orientMatrix = np.array([[np.cos(self.inputRot[0]) * np.cos(self.inputRot[1]),
                                  (np.cos(self.inputRot[0]) * np.sin(self.inputRot[1]) * np.sin(self.inputRot[2])) - (np.sin(self.inputRot[0]) * np.cos(self.inputRot[2])),
                                  (np.cos(self.inputRot[0]) * np.sin(self.inputRot[1]) * np.cos(self.inputRot[2])) + (np.sin(self.inputRot[0]) * np.sin(self.inputRot[2]))],
                                 [np.sin(self.inputRot[0]) * np.cos(self.inputRot[1]),
                                  (np.sin(self.inputRot[0]) * np.sin(self.inputRot[1]) * np.sin(self.inputRot[2])) + (np.cos(self.inputRot[0]) * np.cos(self.inputRot[2])),
                                  (np.sin(self.inputRot[0]) * np.sin(self.inputRot[1]) * np.cos(self.inputRot[2])) - (np.cos(self.inputRot[0]) * np.sin(self.inputRot[2]))],
                                 [-np.sin(self.inputRot[1]),
                                  np.cos(self.inputRot[1]) * np.sin(self.inputRot[2]),
                                  np.cos(self.inputRot[1]) * np.cos(self.inputRot[2])]])
        return self.orientMatrix

    def ij_constant(self):
        for i in range(6):
            self.basePos[i] = [self.rBase * np.cos(self.thetaBase[i]), self.rBase * np.sin(self.thetaBase[i]), 0] + self.machineOffset
            self.platformPos[i] = [self.rPlatform * np.cos(self.thetaPlatform[i]), self.rPlatform * np.sin(self.thetaPlatform[i]), 0]

        c1 = np.dot(self.orientMatrix, self.platformPos.T)
        c1T = np.transpose(c1)
        c2 = np.cross(c1 , self.prisma)
        c2T = np.transpose(c2)
        c3 = np.dot(c1T , c2T)
        return c3

    def ij_variable(self):
        dLinear = self.inputPos - self.lastPos
        dAngular = self.inputRot - self.lastRot
        self.velocity = np.array([self.dLinear, self.dAngular])
        return self.velocity

    def ij_invDiagLength(self):
        diag = np.diag(self.prismaLength)
        invDiag = np.linalg.inv(diag)
        return invDiag

    def ij_prismaVel(self):
        temp = np.dot(self.ij_constant() , self.ij_variable())
        prismaVel = np.dot(self.ij_invDiagLength() , temp)
        return prismaVel

    def validator(self):
        if (self.shortPrismatic >= self.minLength) and (self.longPrismatic <= self.maxLength): 
            self.trajectory = np.append(self.trajectory, [[self.inputPos[0]], [self.inputPos[1]], [self.inputPos[2]]], axis=1)

    def main(self):
        for z in range(0, 300, 20):
            for y in range(-400, 400, 50):
                for x in range(-400, 400, 50):
                    self.inputPos = np.array([x, y, z])
                    self.inputRot = np.array([np.deg2rad(0.), np.deg2rad(0.), np.deg2rad(0.)])
                    
                    self.ik_orientation()
                    self.ik_position()
                    self.dataPrismaLength[0,:] = self.ik_prismatic()
                    self.validator() 
                    print(x,y,z)
        self.draw()


if __name__ == '__main__':
    run = Run()
    run.main()