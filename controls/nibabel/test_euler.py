import eulerangles as ea
import numpy as np

z_rot = ea.euler2angle_axis(np.pi * 2, 0, 0)
z2_rot = ea.euler2angle_axis(np.pi, 0, 0)
y_rot = ea.euler2angle_axis(0, 1, 0)
x_rot = ea.euler2angle_axis(0, 0, 1)

print z_rot

print z2_rot

# print y_rot

# print x_rot

