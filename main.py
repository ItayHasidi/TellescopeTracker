import cv2 as cv
import time
import Telcontrol

# telescope
telescope = Telcontrol.Telcontrol()

time.sleep(2)
dif = 20

# name of the window
cv.namedWindow("tracking")
# camera input
camera = cv.VideoCapture(0)
# reading from the camera
ok, image = camera.read()
# checking validity of the camera
if not ok:
    print('Failed to read video')
    exit()

bbox = cv.selectROI("tracking", image)
# tracker settings
tracker = cv.TrackerMIL_create()
# init of vars
init_once = False
flag = False
cur_image = []
prev_image = cur_image

# main while
while camera.isOpened():
    ok, image = camera.read()
    if not ok:
        print('no image to read')
        break

    if not init_once:
        ok = tracker.init(image, bbox)
        init_once = True
    prev_image = cur_image
    ok, temp_image = tracker.update(image)
    if ok:
        cur_image = temp_image
    print(ok, cur_image, prev_image)

    # painting the rectangle
    if ok:
        p1 = (int(cur_image[0]), int(cur_image[1]))
        p2 = (int(cur_image[0] + cur_image[2]), int(cur_image[1] + cur_image[3]))
        cv.rectangle(image, p1, p2, (200, 0, 0))

    cv.imshow("tracking", image)
    k = cv.waitKey(1) & 0xff
    # esc pressed
    if k == 27:
        telescope.stop_y()
        telescope.stop_x()
        break
    # calculating the movement of the telescope
    # in the first iteration skip this
    if flag:
        difX = cur_image[0] - prev_image[0]
        difY = cur_image[1] - prev_image[1]
        if difX > dif:
            # moving right
            telescope.manualRight(6)
        elif difX < -1 * dif:
            # moving left
            telescope.manualLeft(6)
        if difY > dif:
            # moving up
            telescope.manualUp(6)
        elif difY < -1 * dif:
            # moving down
            telescope.manualDown(6)

    flag = True

    # sleep to minimize the number of the inputs per second
    time.sleep(0.2)
