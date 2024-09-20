import cv2
import numpy as np
import os
import config

def check_difference(points):
    max_limit = config.MAX_DIFFERENCE_LIMIT
    points = np.array(points)
    x_diff = np.abs(points[:, None, 0] - points[None, :, 0])
    y_diff = np.abs(points[:, None, 1] - points[None, :, 1])

    over_limit = (x_diff > max_limit) | (y_diff > max_limit)
    return np.any(over_limit)

def find_points(show_results=False, debug=False):
    # Load the 4 extracted images
    input_dir = config.SPLIT_DIR
    output_dir = config.SPOTTED_DIR
    images = [cv2.imread(f'{input_dir}/image_{i + 1}.png') for i in range(4)]
    original_images = [img.copy() for img in images]  # Keep a copy of the original images

    # Get dimensions of the first image
    h, w, _ = images[0].shape

    # Scale factor for display (0.2 as per your setup)
    scale_factor = config.SCALE_FACTOR_SINGLE

    # Resize images for display
    resized_images = [cv2.resize(img, (int(w * scale_factor), int(h * scale_factor))) for img in images]

    # Parameters for ROI
    roi_size = config.ROI_SIZE  # Size of the square ROI (e.g., 200px)
    scaled_roi_size = int(roi_size * scale_factor)  # Scaled ROI size for display

    # Mouse callback to capture the clicked point
    selected_point = None

    # Create directory to save result images if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    def select_point(event, x, y, flags, param):
        nonlocal selected_point
        if event == cv2.EVENT_LBUTTONDOWN:
            # Scale the selected point back to the original image coordinates
            orig_x = int(x / scale_factor)
            orig_y = int(y / scale_factor)
            selected_point = (orig_x, orig_y)

            # Draw a red dot on the selected point and a rectangle around the ROI in the resized image
            cv2.circle(resized_images[0], (x, y), 2, (0, 0, 255), -1)
            cv2.rectangle(resized_images[0], (x - scaled_roi_size // 2, y - scaled_roi_size // 2),
                          (x + scaled_roi_size // 2, y + scaled_roi_size // 2), (0, 255, 0), 2)
            cv2.imshow('Image 1', resized_images[0])

    # Display the first resized image and select a point
    print("Select the focus point and press any key")
    cv2.imshow('Image 1', resized_images[0])
    cv2.setMouseCallback('Image 1', select_point)
    cv2.waitKey(0)

    # Write to spotted for debugging
    cv2.imwrite(f'{output_dir}/result_image_1.png', resized_images[0])

    if selected_point is None:
        raise Exception("No point selected")

    # Use the selected point for ROI in the first image
    x, y = selected_point
    x_start, x_end = max(0, x - roi_size // 2), min(w, x + roi_size // 2)
    y_start, y_end = max(0, y - roi_size // 2), min(h, y + roi_size // 2)
    roi = images[0][y_start:y_end, x_start:x_end]

    # cv2.imshow('ROI', roi)
    # cv2.waitKey(0)

    if debug:
        cv2.circle(original_images[0], (x, y), 5, (0, 0, 255), -1)
        cv2.rectangle(original_images[0], (x - roi_size // 2, y - roi_size // 2),
                      (x + roi_size // 2, y + roi_size // 2), (0, 255, 0), 10)
        # Write over the splitted image with the ROI
        cv2.imwrite(f'{input_dir}/image_1.png', original_images[0])

    # Initialize list to store match results
    match_results = []

    # Template matching to find the best match in other images
    for i in range(1, 4):
        # Perform template matching on the original image
        result = cv2.matchTemplate(images[i], roi, cv2.TM_CCOEFF_NORMED)

        # Find the location with the highest match value
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        match_point = max_loc
        match_results.append((i, match_point))

    # Draw results on original images and store focus points
    focus_points = [selected_point]  # Include the manually selected focus point
    for i, match_point in match_results:
        # Draw a rectangle around the best match and a dot on the best match point
        top_left = match_point
        bottom_right = (top_left[0] + roi_size, top_left[1] + roi_size)
        cv2.rectangle(original_images[i], top_left, bottom_right, (0, 255, 0), 10)
        cv2.circle(original_images[i], (top_left[0] + roi_size // 2, top_left[1] + roi_size // 2), 5, (0, 0, 255), -1)

        # Add the focus point to the list
        focus_points.append((top_left[0] + roi_size // 2, top_left[1] + roi_size // 2))

        # Resize the result image for display
        result_image = cv2.resize(original_images[i], (int(w * scale_factor), int(h * scale_factor)))
        if show_results:
            cv2.imshow(f'Result Image {i + 1}', result_image)

        # Save the result image to 'spotted/' directory
        cv2.imwrite(f'{output_dir}/result_image_{i + 1}.png', original_images[i])
        if debug:
            cv2.imwrite(f'{input_dir}/image_{i + 1}.png', original_images[i])

    if show_results:
        cv2.waitKey(0)

    # Print all focus points in the required list format
    print(f"Focus points for all images: {focus_points}")

    cv2.destroyAllWindows()

    return focus_points

if __name__ == '__main__':
    find_points()
