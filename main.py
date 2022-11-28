import math
import random

import cv2
import numpy as np

img = cv2.imread('document3.png')

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


canny = cv2.Canny(img_gray, 100, 200)

lines = cv2.HoughLines(canny, 1, np.pi / 180, 120)

rhos = []
thetas = []

if lines is not None:
    for i in range(0, len(lines)):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        if theta == 0.0:
            continue
        rhos.append(rho)
        thetas.append(theta)

correct_rhos = []
correct_thetas = []

for line in lines:
    rho = line[0][0]
    theta = line[0][1]

    rhos_copy = rhos.copy()
    thetas_copy = thetas.copy()

    try:
        rho_idx = rhos.index(rho)
    except:
        continue

    closest_rho = np.isclose(rho, rhos_copy, atol=20.0)
    closest_theta = np.isclose(theta, thetas_copy, atol=np.pi / 36.0)

    for idx, (rho_val, theta_val) in enumerate(zip(closest_rho, closest_theta)):
        if rho_val == True and rho_val == theta_val:
            if rhos[idx] == rho:
                continue
            thetas[idx] = -1
            rhos[idx] = -1

rhos = list(filter(lambda x: x != -1, rhos))
thetas = list(filter(lambda x: x != -1, thetas))

for rho, theta in zip(rhos, thetas):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    a = math.cos(theta)
    b = math.sin(theta)
    x0 = a * rho
    y0 = b * rho
    pt1 = (int(x0 + 3000 * (-b)), int(y0 + 3000 * a))
    pt2 = (int(x0 - 3000 * (-b)), int(y0 - 3000 * a))
    cv2.line(img, pt1, pt2, color, 3, cv2.LINE_AA)

cv2.imshow('img orig', img)
cv2.imwrite('houghline_after_nms2.jpg', img)
cv2.waitKey(0)
