import cv2, time, numpy as np

np.set_printoptions(threshold=np.inf)       # print out all of numpy array

first_frame = None

video = cv2.VideoCapture(0)

frame_count = 0

while True:
    frame_count = frame_count + 1
    check, frame = video.read()

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey = cv2.GaussianBlur(grey, (21, 21), 0)     # Gaussian blur using 21x21 kernel, stdev 0

    if first_frame is None:
        first_frame = grey
        continue                    # on 1st iteration, continue *back to beginning of loop* don't do rest

    delta_frame = cv2.absdiff(first_frame, grey)          # difference of current & first frames (blurred)

    _, threshold_delta_frame = cv2.threshold(delta_frame, 100, 255, cv2.THRESH_BINARY)
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
        if cv2.contourArea(contour) < 1000:
            continue                    # continue back to the beginning of the loop - go no further in this loop
        (x, y, width, height) = cv2.boundingRect(contour)      # else
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0) )
        # from top left on original frame, draw 3-pixel BGR green rectangle


    cv2.imshow('Capturing Grey', grey)
    cv2.imshow('Delta frame', delta_frame)
    cv2.imshow('Threshold frame', threshold_delta_frame)
    cv2.imshow('Colour result frame', frame)



    key = cv2.waitKey(1)
    # print(grey)
    # print(delta_frame)      # delta_frame/difference values higher if motion
    print(threshold_delta_frame)

    if key == ord('q'):
        break
print('Frame count: ' + str(frame_count))
video.release()
cv2.destroyAllWindows()

