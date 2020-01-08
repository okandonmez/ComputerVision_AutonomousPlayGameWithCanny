import cv2
import pyautogui
import time
import numpy as np
import copy
from scipy import ndimage, signal
from scipy import linalg as la
import matplotlib.image as mpimg

def cannyEdgeDetection(image):
    removed_noise = cv2.GaussianBlur(image, (5, 5), 0)

    edges = np.uint8(removed_noise)  # Otherwise Canny detector gives depth error
    canny_edge_detected = cv2.Canny(edges, 100, 100)

    return canny_edge_detected, removed_noise

def minEigenValueDetection(gray_image, src_color):
    eigenValues = cv2.cornerEigenValsAndVecs(gray_image, 3, 3)

    corners = []

    corners_inserted_image = np.empty(gray_image.shape, dtype=np.float32)
    corners_inserted_image.fill(0)

    for i in range(gray_image.shape[0]):
        for j in range(gray_image.shape[1]):

            lambda_1 = eigenValues[i, j, 0]
            lambda_2 = eigenValues[i, j, 1]

            if lambda_1 > 0 and lambda_2 > 0:
                if lambda_2 > 0.09:
                    corners_inserted_image[i, j] = 255
                    corners.append((j, i))
                    src_color = cv2.circle(src_color, (j, i), 2, (0,255,0))

    return corners_inserted_image, src_color, corners

def sobel_filter(image):

    image = image.astype(np.float)

    kX = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float)
    kY = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=np.float)

    gx = signal.convolve2d(image, kX, mode='same', boundary='symm', fillvalue=0)
    gy = signal.convolve2d(image, kY, mode='same', boundary='symm', fillvalue=0)

    g = np.sqrt(gx * gx + gy * gy)
    g *= 255.0 / np.max(g)

    return g

def isFullScreenCheck(image):
    firstPixelValue = image[0, 0]

    if firstPixelValue[0] == 114 and firstPixelValue[1] == 111 and firstPixelValue[2] == 255:
        return True

    return False

def takeScreenshot(fileName, durationOfSleep = 5):                #takes shot of screen after invoking that function in 5 seconds
    time.sleep(durationOfSleep)

    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(fileName)

def giveTheGameArea(image, destinationSize):         # if the game is not full screen call that method for getting game area from screenshot
    horizontalFrameConstant = 0.664
    verticalFrameConstant = 0.664

    image = cv2.resize(image, destinationSize)

    height = int(image.shape[0])
    width = int(image.shape[1])

    tempX = 0
    tempY = 0
    firstSquareIsFindFlag = False

    for i in range(height):
        if firstSquareIsFindFlag:
            break
        for j in range(width):
            pixel = image[i, j]
            if pixel[0] == 114 and pixel[1] == 111 and pixel[2] == 255:
                tempX = j
                tempY = i
                firstSquareIsFindFlag = True
                break

    firstSquarePixCoordinate = (tempX, tempY)
    print(firstSquarePixCoordinate)

    horizontalLength = int(width*horizontalFrameConstant)
    verticalLenght = int(height*horizontalFrameConstant)

    crop_img = image[firstSquarePixCoordinate[1]:firstSquarePixCoordinate[1]+verticalLenght, firstSquarePixCoordinate[0]:firstSquarePixCoordinate[0]+horizontalLength]
    return crop_img

if __name__ == "__main__":

#region PREPARATIONS

    destFileName = "screenshot.png"
    destSize     = (600, 400)

    takeScreenshot(destFileName, 3)

    image        = cv2.imread(destFileName)
    isFullScreen = isFullScreenCheck(image)

    if isFullScreen:
        image = cv2.resize(image, destSize)
    else:
        image = giveTheGameArea(image, destSize)
        image = cv2.resize(image, destSize)

    gray_scale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#endregion

#region PART1 - SOBEL FILTER

    sobel_filtered_image = sobel_filter(gray_scale_image)

#endregion

#region PART2 - CANNY EDGE DETECTOR
    canny_edge_detected, removed_noise = cannyEdgeDetection(sobel_filtered_image)

#endregion

#region PART3 - MIN EIGENVALUE CORNER DETECTOR
    _, corner_detected, _ = minEigenValueDetection(canny_edge_detected, image)
#endregion

    cv2.imshow("1- Captured Image", image)
    cv2.imshow("2- Gray Scale Image", gray_scale_image)
    cv2.imshow("3- Sobel Filtered Image", sobel_filtered_image)
    cv2.imshow("4- Gaussian Smoothed Image", removed_noise)
    cv2.imshow("5- Canny Detected Image", canny_edge_detected)
    cv2.imshow("6- Corner Detected Image", corner_detected)

    cv2.waitKey()



