import cv2
import time
import numpy as np
from datetime import datetime
import pandas

# NB values of contour area, threshold trial & error, depending on location &c


def timepair(timelist):
    """generator for converting a list of start-finish times into a list of pairs"""
    for start, finish in zip(timelist[::2], timelist[1::2]):        # nothing for the 1st argument, or 2nd, jump by 2
        yield start, finish
    # https://stackoverflow.com/a/50798932
    # https://stackoverflow.com/a/3453103


np.set_printoptions(threshold=np.inf)       # print out all of numpy array

first_frame = None
motion_status_list = [None, None]           # initialise status list so that first negative index checks will work
motion_times_list = []
df = pandas.DataFrame(columns=['Start', 'End'])

video = cv2.VideoCapture(0)

frame_count = 0

while True:
    frame_count = frame_count + 1
    check, frame = video.read()
    motion_status = 0              # status of zero d'indicate no motion
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey = cv2.GaussianBlur(grey, (21, 21), 0)     # Gaussian blur using 21x21 kernel, stdev 0

    if first_frame is None:
        first_frame = grey
        continue                    # on 1st iteration, continue *back to beginning of loop* don't do rest

    delta_frame = cv2.absdiff(first_frame, grey)          # difference of current & first frames (blurred)

    _, threshold_delta_frame = cv2.threshold(delta_frame, 102, 255, cv2.THRESH_BINARY)
    # threshold greyscale to black & white
    # binary threshold - set to 255 if above (say, 30)
    # _, thresh = xyz to unpack tuple, or thresh = xyz[1]


    threshold_delta_frame = cv2.dilate(threshold_delta_frame, None, iterations=2)     # no kernel passed in,
    # dilate to consolidate contours

    # (_, contours, _) = cv2.findContours(threshold_delta_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    (contours, _) = cv2.findContours(threshold_delta_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # enumerate the contours in greyscaled thresholded frame
    # retrieve external
    # tuple returned -

    for contour in contours:
        if cv2.contourArea(contour) < 2e3:      # if bigger than a certain number of pixels e.g. 1e3
            continue                    # continue back to the beginning of the loop - go no further in this loop
        motion_status = 1
        (x, y, width, height) = cv2.boundingRect(contour)      # else
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0))
        # from top left on original frame, draw 3-pixel BGR green rectangle

    motion_status_list.append(motion_status)
    if motion_status_list[-1] == 1 and motion_status_list[-2] == 0:
        motion_times_list.append(datetime.now())
    if motion_status_list[-1] == 1 and motion_status_list[-2] == 1:
        motion_times_list.append(datetime.now())
    cv2.imshow('Capturing Grey', grey)
    cv2.imshow('Delta frame', delta_frame)
    cv2.imshow('Threshold frame', threshold_delta_frame)
    cv2.imshow('Colour result frame', frame)



    key = cv2.waitKey(1)
    # print(grey)
    # print(delta_frame)      # delta_frame/difference values higher if motion
    print(threshold_delta_frame)
    print('Motion status: ' + str(motion_status))

    if key == ord('q'):
        if motion_status == 1:
            motion_times_list.append(datetime.now())
        break

print('Frame count: ' + str(frame_count))
print('Motion status list: ' + str(motion_status_list))
print('Motion times list: ' + str(motion_times_list))

start_finish_list = timepair(motion_times_list)             # generate list of pairs of start/finish times - PNJ

for timestamp_pair in start_finish_list:                    # write pairs of start/finish times to csv
    df = df.append({'Start': timestamp_pair[0], 'End': timestamp_pair[1]}, ignore_index=True)

df.to_csv('Times.csv')

video.release()
cv2.destroyAllWindows()

