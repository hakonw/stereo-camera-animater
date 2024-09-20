import os

import cv2
import numpy as np

import config


def split_image(image_name="bilde.jpg", auto=True, visualize=True):
    # Load the image (grayscale)
    print(f"Splitting image: {image_name}")
    output_dir = config.SPLIT_DIR
    scale_factor = config.SCALE_FACTOR

    image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
    original_image = cv2.imread(image_name)

    # Get original dimensions
    h, w = image.shape

    # Scale factor for display
    os.makedirs(output_dir, exist_ok=True)

    # Initialize variables
    grow_step = config.GROW_STEP
    seed_points = []  # list to store clicked points
    max_boxes = 4  # hardcoded for now

    # Threshold for stopping expansion (adjustable)
    darkness_threshold = config.DARKNESS_THRESHOLD  # This threshold defines how much pixel intensity change is needed to keep growing

    # Resize the image for display
    image_display = cv2.resize(image, (int(w * scale_factor), int(h * scale_factor)))

    # Box size limit
    box_size_limit = config.BOX_SIZE_UPPER_LIMIT_RATIO * w

    # Function to calculate darkness (sum of pixel intensities)
    def calculate_darkness(box):
        return np.sum(box)

    if auto:
        seed_points.append((int(w * (1 / 8)), int(h / 2)))
        seed_points.append((int(w * (3 / 8)), int(h / 2)))
        seed_points.append((int(w * (5 / 8)), int(h / 2)))
        seed_points.append((int(w * (7 / 8)), int(h / 2)))

    else:
        # Mouse callback to capture click points
        def select_seed(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN and len(seed_points) < max_boxes:
                # Scale the clicked coordinates back to the original image
                orig_x = int(x / scale_factor)
                orig_y = int(y / scale_factor)
                seed_points.append((orig_x, orig_y))
                print(f"Seed point {len(seed_points)}: ({orig_x}, {orig_y})")

        # Display the scaled image and let the user select seed points
        cv2.imshow('Image', image_display)
        cv2.setMouseCallback('Image', select_seed)

        # Wait for the user to select the 4 points
        while len(seed_points) < max_boxes:
            cv2.waitKey(1)

        cv2.destroyAllWindows()

    # Now process the 4 seed points on the original image
    boxes = []

    for (x_seed, y_seed) in seed_points:
        box_size = 50  # initial box size

        # Initialize box edges
        left, right = x_seed, x_seed + box_size
        top, bottom = y_seed, y_seed + box_size

        step_count = 0  # Step counter for visualization frequency

        # Grow each side iteratively until borders are found
        growing = True
        while growing:
            growing = False
            step_count += 1

            # Test growing the right side
            if right + grow_step < w:
                new_right = right + grow_step
                new_box = image[top:bottom, right:new_right]  # Check the area to the right
                darkness_diff = calculate_darkness(new_box)
                if darkness_diff > darkness_threshold:  # If difference is significant, keep growing
                    right = new_right
                    growing = True

            # Test growing the bottom side
            if bottom + grow_step < h:
                new_bottom = bottom + grow_step
                new_box = image[bottom:new_bottom, left:right]  # Check the area below
                darkness_diff = calculate_darkness(new_box)
                if darkness_diff > darkness_threshold:
                    bottom = new_bottom
                    growing = True

            # Test growing the left side
            if left - grow_step >= 0:
                new_left = left - grow_step
                new_box = image[top:bottom, new_left:left]  # Check the area to the left
                darkness_diff = calculate_darkness(new_box)
                if darkness_diff > darkness_threshold:
                    left = new_left
                    growing = True

            # Test growing the top side
            if top - grow_step >= 0:
                new_top = top - grow_step
                new_box = image[new_top:top, left:right]  # Check the area above
                darkness_diff = calculate_darkness(new_box)
                if darkness_diff > darkness_threshold:
                    top = new_top
                    growing = True

            # Check if the box exceeds the 30% size limit
            box_width = right - left
            if box_width > box_size_limit:
                raise ValueError(f"Error: Box width {box_width} exceeds 30% of the total image width!")

            # Visualization: only update every 5th step
            if visualize and step_count % 10 == 0:
                temp_image = image.copy()
                cv2.rectangle(temp_image, (left, top), (right, bottom), (255, 0, 0), 10)  # Thicker blue rectangle

                # Resize the temporary image for display
                temp_image_display = cv2.resize(temp_image, (int(w * scale_factor), int(h * scale_factor)))
                cv2.imshow('Finding Boxes', temp_image_display)
                cv2.waitKey(25)  # Add small delay for visualization

        # Save the best box found
        best_box = (left, top, right - left, bottom - top)
        if best_box[2] < config.BOX_SIZE_LOWER_LIMIT_RATIO * w or best_box[3] < config.BOX_SIZE_LOWER_LIMIT_RATIO * h:
            raise ValueError(f"Error: Box  undershoots {config.BOX_SIZE_LOWER_LIMIT_RATIO} of the total image width!")

        boxes.append(best_box)

    cv2.destroyAllWindows()

    # Save or display the results from the original image (do not mask white anymore)
    for idx, (x_start, y_start, box_w, box_h) in enumerate(boxes):
        extracted_img = original_image[y_start:y_start + box_h, x_start:x_start + box_w]
        cv2.imwrite(os.path.join(output_dir, f'image_{idx + 1}.png'), extracted_img)
    print(f"Saved {len(boxes)} boxes to {output_dir}")
