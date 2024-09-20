import cv2

import config


# frame_ms is a lie, and depends on hardware
def play_video(video_path):
    scale_factor = config.SCALE_FACTOR_PLAYBACK
    frame_ms = config.PLAYBACK_FRAME_MS_PSEUDO
    print(f"Playing video {video_path}. Press 'q' to quit.")
    while True:
        # Open the video file
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Error: Could not open video.")
            return

        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            if not ret:
                break

            # Resize the frame
            frame = cv2.resize(frame, (0, 0), fx=scale_factor, fy=scale_factor)

            # Display the frame
            cv2.imshow('Video', frame)

            # Exit if the user presses the 'q' key
            key = cv2.waitKey(frame_ms) & 0xFF
            if key == ord("q") or key == ord("y") or key == ord("n"):
                cap.release()
                cv2.destroyAllWindows()

                # return yes/no
                return key == ord("q") or key == ord("y")

        # Release the video capture object to replay the video
        cap.release()
