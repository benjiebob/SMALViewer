import numpy as np

def rand_to_cart(u1, u2, r):
    theta = np.arccos(2 * u1 - 1) # 0 <= theta <= pi
    phi = 2 * np.pi * u2 # 0 <= phi <= 2 * pi

    return sphere_to_cart(theta, phi, r)
    
def sphere_to_cart(theta, phi, r):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    return np.array([x, y, z])

def main():
    num_samples = 1000
    u1s = np.random.rand(num_samples)
    u2s = np.random.rand(num_samples)
    rs = np.random.rand(num_samples) * np.pi / 6

    for u1, u2, r in zip(u1s, u2s, rs):
        print (rand_to_cart(u1, u2, r))

if __name__ == '__main__':
    main()