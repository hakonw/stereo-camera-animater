import cv2
import os

# Parameters
def make_vid():
    image_folder = 'translated'
    output_video = 'output_video.avi'
    frame_duration = 3  # Number of frames to display each image
    loop_count = 5      # Number of times to loop the sequence
    fps = 24            # Frames per second for the video
    frame_sequence = [0, 1, 2, 3, 2, 1]  # Image indices for the sequence (0-based)

    # Load images
    image_files = [os.path.join(image_folder, f'translated_image_{i + 1}.jpg') for i in range(4)]
    images = [cv2.imread(img_file) for img_file in image_files]

    # Check if images are loaded correctly
    if any(img is None for img in images):
        raise ValueError("One or more images could not be loaded. Please check the file paths.")

    # Get dimensions of the first image
    h, w, _ = images[0].shape

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .avi file
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (w, h))  # Use fps variable

    # Add frames to the video
    for _ in range(loop_count):
        for idx in frame_sequence:
            image = images[idx]
            # Add the image to the video 'frame_duration' times
            for _ in range(frame_duration):
                video_writer.write(image)

    # Release the VideoWriter
    video_writer.release()

    print(f'Video saved as {output_video}')

if __name__ == '__main__':
    make_vid()