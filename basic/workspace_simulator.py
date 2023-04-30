import matplotlib
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
 
class Workspace():
    inputPos = np.array([0., 0., 0.])
    inputRot = np.array([np.deg2rad(0.), np.deg2rad(0.), np.deg2rad(0.)])
    lastPos = np.zeros(3)
    lastRot = np.zeros(3)
    machineOffset = np.array([0., 0., 800.])
    toolOffset = ([0, 0, 0])

    basePos = np.zeros((6, 3))
    platformPos = np.zeros((6, 3))
    prisma = np.zeros(3)
    prismaLength = np.zeros(6)
    dataPrismaLength = np.zeros((2,6))

    static_posz = 350.

    trajectory = np.array([[inputPos[0]], [inputPos[1]], [inputPos[2]]])
    rotating_joint0 = np.array([[0.], [0.], [static_posz]])
    rotating_joint1 = np.array([[0.], [0.], [static_posz]])
    rotating_joint2 = np.array([[0.], [0.], [static_posz]])
    rotating_joint3 = np.array([[0.], [0.], [static_posz]])
    rotating_joint4 = np.array([[0.], [0.], [static_posz]])
    rotating_joint5 = np.array([[0.], [0.], [static_posz]])

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

    def draw(self, mode):
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

        # Define sphere parameters
        r = self.rPlatform
        pi = np.pi
        cos = np.cos
        sin = np.sin
        phi, theta = np.mgrid[0.0:pi:100j, 0.0:2 * pi:100j]

        # Define cartesian coordinates
        x = r*sin(phi)*cos(theta)
        y = r*sin(phi)*sin(theta)
        z = (r*cos(phi)) + self.static_posz

        # Plot sphere
        ax.plot_surface(x, y, z, color='gray', alpha=0.2)

        ax.set_box_aspect([1, 1, 1])

        # plot the scatter points
        cmap = matplotlib.colormaps['RdYlGn_r']
        # cmap = matplotlib.colormaps['gray']

        if(mode=="position"):
            tri = Triangulation(self.trajectory[0], self.trajectory[1])
            ax.scatter(self.trajectory[0], self.trajectory[1], self.trajectory[2], c=self.trajectory[2], cmap=cmap)

        elif(mode=="orientation"):
            ax.scatter(self.rotating_joint0[0], self.rotating_joint0[1], self.rotating_joint0[2], c=self.rotating_joint0[2], cmap=cmap)
            # ax.scatter(self.rotating_joint1[0], self.rotating_joint1[1], self.rotating_joint1[2], c=self.rotating_joint1[2], cmap=cmap)
            # ax.scatter(self.rotating_joint2[0], self.rotating_joint2[1], self.rotating_joint2[2], c=self.rotating_joint2[2], cmap=cmap)
            # ax.scatter(self.rotating_joint3[0], self.rotating_joint3[1], self.rotating_joint3[2], c=self.rotating_joint3[2], cmap=cmap)
            # ax.scatter(self.rotating_joint4[0], self.rotating_joint4[1], self.rotating_joint4[2], c=self.rotating_joint4[2], cmap=cmap)
            # ax.scatter(self.rotating_joint5[0], self.rotating_joint5[1], self.rotating_joint5[2], c=self.rotating_joint5[2], cmap=cmap)

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

            self.rotating_joint0 = np.append(self.rotating_joint0, [[self.platformPos[0,0]], [self.platformPos[0,1]], [self.platformPos[0,2]]], axis=1)
            self.rotating_joint1 = np.append(self.rotating_joint1, [[self.platformPos[1,0]], [self.platformPos[1,1]], [self.platformPos[1,2]]], axis=1)
            self.rotating_joint2 = np.append(self.rotating_joint2, [[self.platformPos[2,0]], [self.platformPos[2,1]], [self.platformPos[2,2]]], axis=1)
            self.rotating_joint3 = np.append(self.rotating_joint3, [[self.platformPos[3,0]], [self.platformPos[3,1]], [self.platformPos[3,2]]], axis=1)
            self.rotating_joint4 = np.append(self.rotating_joint4, [[self.platformPos[4,0]], [self.platformPos[4,1]], [self.platformPos[4,2]]], axis=1)
            self.rotating_joint5 = np.append(self.rotating_joint5, [[self.platformPos[5,0]], [self.platformPos[5,1]], [self.platformPos[5,2]]], axis=1)                                                

    def position(self):
        for z in range(0, 290, 20):
            for y in range(-350, 350, 20):
                for x in range(-370, 390, 20):
                    self.inputPos = np.array([x, y, z])
                    self.inputRot = np.array([np.deg2rad(0.), np.deg2rad(0.), np.deg2rad(0.)])
                    
                    self.ik_orientation()
                    self.ik_position()
                    self.dataPrismaLength[0,:] = self.ik_prismatic()
                    self.validator() 
                    print(x,y,z)
        self.draw("position")
        print("min x: ", np.min(self.trajectory[0]), ", max x: ", np.max(self.trajectory[0]))
        print("min y: ", np.min(self.trajectory[1]), ", max y: ", np.max(self.trajectory[1]))
        print("min z: ", np.min(self.trajectory[2]), ", max z: ", np.max(self.trajectory[2]))


    def orientation(self):
        roll = 0
        pitch = 0
        yaw = 0
        self.inputPos = np.array([0., 0., self.static_posz])
        self.inputRot = np.array([np.deg2rad(roll), np.deg2rad(pitch), np.deg2rad(yaw)])
        for yaw in range(-180, 180, 5):
            for roll in range(-180, 180, 5):
                self.inputRot = np.array([np.deg2rad(roll), np.deg2rad(pitch), np.deg2rad(yaw)])
                self.ik_orientation()
                self.ik_position()
                self.dataPrismaLength[0,:] = self.ik_prismatic()
                self.validator()
                print(roll,pitch,yaw)
        self.draw("orientation")

if __name__ == '__main__':
    ws = Workspace()
    ws.orientation()