# Stylus-Snake-Game

## A Briefing

This Stylus Snake game project is an OpenCV and Pygame Python implementation. The main processes involved in the implementation are:
1. Detecting the HSV values of the Stylus
2. Stylus Detection and Tracking the Dynamic Stylus motion
3. Playing the game

## 1. Detecting HSV values of the Stylus

Firstly the program detects the HSV values of the color of the stylus used by the user. This is done in the following steps:
* The user has to align the center of the stlyus to the red dot in the square region and capture by pressing 'Q'.
* On capturing, a small 10x10 region around the center is captured.
* The HSV values of each pixel is taken and the average of all the HSV values is taken. 

Now with the HSV values of the Stylus taken, the gameplay starts.

## 2. Stylus Detection and Tracking the Dynamic Stylus motion

Using the HSV values found, we use it to detect the stylus therefore tracking the motion of the center of the stylus. This is done in the following steps:
* Noise removal from the frame.
* HSV thresholding using an upper and lower bound of the HSV values to create a mask and detect the stylus.
* Finding the contours of the mask.
* Using the contours to find the centroid.

## 3. Playing the Game

The game is made using pygame. Using the centroid, we can now track the dynamic motion of the stylus and thus of the snake.

There are eight hurdle design and the game randomly chooses anyone of them each time it runs.

The snake has to move through the hurdles and eat the fruit which spawns at random locations. Doing so increases the length of the snake. After every 50 points, the speed of the snake increases slightly

If the snake collides with either the wall, or the edge of the window or with its ownself, the game ends and pressing the 'quit' button closes the window.

---
🔗LINK TO THE VIDEO

---
