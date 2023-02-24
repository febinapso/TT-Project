import cv2

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'HEVC')
framerate = 150.0
resolution = (1920, 1080)
quality = 100
bitrate = int((resolution[0] * resolution[1] * framerate * quality) / 1000)

out = cv2.VideoWriter('../output.mp4', fourcc, framerate, resolution, isColor=True)
out.set(cv2.CAP_PROP_BITRATE, bitrate)

# Start capturing video from webcam
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
cap.set(cv2.CAP_PROP_FPS, framerate)

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret==True:
        # Write the frame into the video file
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('frame',frame)

        # Press 'q' to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything when done
cap.release()
out.release()
cv2.destroyAllWindows()
