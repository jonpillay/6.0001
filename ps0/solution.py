"""Returns the x to the power of Y and log(x)

Takes x and Y as user input.
"""

import numpy as np

x = int(input("Enter x: "))
Y = int(input("Enter Y: "))

print("X**y = " + str(x**Y))
print("log(x) = " + str(np.log2(x)))