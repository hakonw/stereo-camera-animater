import cv2
import numpy as np

def find_points():
    # Load the 4 extracted images
    images = [cv2.imread(f'splitted/image_{i + 1}.jpg') for i in range(4)]
    original_images = [img.copy() for img in images]  # Keep a copy of the original images

    # Get dimensions of the first image
    h, w, _ = images[0].shape

    # Scale factor for display (0.2 as per your setup)
    scale_factor = 0.2

    # Resize images for display
    resized_images = [cv2.resize(img, (int(w * scale_factor), int(h * scale_factor))) for img in images]

    # Parameters for ROI
    roi_size = 200  # Size of the square ROI (e.g., 200px)
    scaled_roi_size = int(roi_size * scale_factor)  # Scaled ROI size for display

    # Mouse callback to capture the clicked point
    selected_point = None


    def select_point(event, x, y, flags, param):
        nonlocal selected_point
        if event == cv2.EVENT_LBUTTONDOWN:
            # Scale the selected point back to the original image coordinates
            orig_x = int(x / scale_factor)
            orig_y = int(y / scale_factor)
            selected_point = (orig_x, orig_y)

            # Draw a red dot on the selected point and a rectangle around the ROI in the resized image
            cv2.circle(resized_images[0], (x, y), 5, (0, 0, 255), -1)
            cv2.rectangle(resized_images[0], (x - scaled_roi_size // 2, y - scaled_roi_size // 2),
                          (x + scaled_roi_size // 2, y + scaled_roi_size // 2), (0, 255, 0), 2)
            cv2.imshow('Image 1', resized_images[0])

    # Display the first resized image and select a point
    cv2.imshow('Image 1', resized_images[0])
    cv2.setMouseCallback('Image 1', select_point)
    cv2.waitKey(0)

    if selected_point is None:
        raise Exception("No point selected")

    # Use the selected point for ROI in the first image
    x, y = selected_point
    x_start, x_end = max(0, x - roi_size // 2), min(w, x + roi_size // 2)
    y_start, y_end = max(0, y - roi_size // 2), min(h, y + roi_size // 2)
    roi = images[0][y_start:y_end, x_start:x_end]

    # Resize ROI for consistency with the original images
    roi_resized = cv2.resize(roi, (scaled_roi_size, scaled_roi_size))

    # Initialize list to store match results
    match_results = []

    # Template matching to find the best match in other images
    for i in range(1, 4):
        # Resize the image for consistency
        resized_image = cv2.resize(images[i], (int(w * scale_factor), int(h * scale_factor)))

        # Perform template matching
        result = cv2.matchTemplate(resized_image, roi_resized, cv2.TM_CCOEFF_NORMED)

        # Find the location with the highest match value
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        match_point = max_loc
        match_results.append((i, match_point))

    # Draw results on original images and store focus points
    focus_points = [selected_point]  # Include the manually selected focus point
    for i, match_point in match_results:
        # Draw a rectangle around the best match and a dot on the best match point
        top_left = (int(match_point[0] / scale_factor), int(match_point[1] / scale_factor))
        bottom_right = (top_left[0] + roi_size, top_left[1] + roi_size)
        cv2.rectangle(original_images[i], top_left, bottom_right, (0, 255, 0), 10)
        cv2.circle(original_images[i], (top_left[0] + roi_size // 2, top_left[1] + roi_size // 2), 5, (0, 0, 255), -1)

        # Add the focus point to the list
        focus_points.append((top_left[0] + roi_size // 2, top_left[1] + roi_size // 2))

        # Resize the result image for display
        result_image = cv2.resize(original_images[i], (int(w * scale_factor), int(h * scale_factor)))
        cv2.imshow(f'Result Image {i + 1}', result_image)
        cv2.waitKey(0)

    # Print all focus points in the required list format
    print("Focus points for all images:")
    print(focus_points)

    cv2.destroyAllWindows()

    return focus_points

if __name__ == '__main__':
    find_points()