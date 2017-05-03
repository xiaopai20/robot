import sys, getopt, datetime
import cv2


def main(argv):
    print argv
    mode = argv[1]
    interval = int(argv[2])

    #capture from camera at location 0
    cap = cv2.VideoCapture(0)
    i = 0
    while True:
        ret, img = cap.read()
        cv2.imshow("input", img)
        imgPath = "C:\\Users\\Hannah\\Desktop\\xiaopai\\images\\";
        if mode == "record":
            imgPath += datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + ".jpg"
            i += 1
        else:
            imgPath += "current\\img.jpg"
        cv2.imwrite(imgPath,img)
        print "save image to " + imgPath

        key = cv2.waitKey(interval)
        if key == 27:
            break

    cv2.destroyAllWindows()
    cv2.VideoCapture(0).release()


#   0  CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
#   1  CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
#   2  CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
#   3  CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
#   4  CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
#   5  CV_CAP_PROP_FPS Frame rate.
#   6  CV_CAP_PROP_FOURCC 4-character code of codec.
#   7  CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
#   8  CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
#   9 CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
#   10 CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
#   11 CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
#   12 CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
#   13 CV_CAP_PROP_HUE Hue of the image (only for cameras).
#   14 CV_CAP_PROP_GAIN Gain of the image (only for cameras).
#   15 CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
#   16 CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
#   17 CV_CAP_PROP_WHITE_BALANCE Currently unsupported
#   18 CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)

if __name__ == '__main__':
    main(sys.argv)