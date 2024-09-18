import cv2

def play_video(video_path, scale_factor, frame_ms):
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
            if cv2.waitKey(frame_ms) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

        # Release the video capture object to replay the video
        cap.release()

if __name__ == '__main__':
    play_video("output_video.avi", scale_factor=0.2, frame_ms=30)
