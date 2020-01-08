import part_1_2_3 as prev_part
import cv2
import pyautogui
import time

if __name__ == "__main__":

#region PREPARATIONS
    destFileName = "screenshot.png"
    destSize = (600, 400)

    initial_ss_sec = 5
    prev_part.takeScreenshot(destFileName, initial_ss_sec)

    image = cv2.imread(destFileName)
    isFullScreen = prev_part.isFullScreenCheck(image)

    characterPos      = (300, 180)
    characterRotation = 0    # 0 -> North, 1 -> East

#endregion

#region PART4 - PLAYING GAME

    isGameContinue = True

    while isGameContinue:
        prev_part.takeScreenshot(destFileName, 1)

        image = cv2.imread(destFileName)

        if isFullScreen:
            image = cv2.resize(image, destSize)
        else:
            image = prev_part.giveTheGameArea(image, destSize)
            image = cv2.resize(image, destSize)

        gray_scale_image             = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobel_filtered_image         = prev_part.sobel_filter(gray_scale_image)
        canny_edge_detected, _       = prev_part.cannyEdgeDetection(sobel_filtered_image)
        corner_detected, _ , corners = prev_part.minEigenValueDetection(canny_edge_detected, image)

        goForward  = False
        goRight    = False

        #forward corner control
        for i in range(len(corners)):
            if corners[i][0] < characterPos[0] and corners[i][1] < characterPos[1]:
                if (abs(corners[i][1] - characterPos[1])) > 50:
                    goForward = True

        if(goForward == False):
            for i in range(len(corners)):
                if corners[i][0] > characterPos[0] and corners[i][1] < characterPos[1]:
                    if (abs(corners[i][0] - characterPos[0])) > 50:
                        goRight = True


        if goForward:
            pyautogui.keyDown("w")
            time.sleep(1)
            pyautogui.keyUp("w")

        if goRight:
            pyautogui.keyDown("d")
            time.sleep(1)
            pyautogui.keyUp("d")

        if not goForward and not goRight:
            isGameContinue = False

#endregion

    print("Reached end of the parkour")

