import cv2
import numpy as np
import os


def translate_image_to_focus_point(focus_points):
    # Ensure the output directory exists
    output_dir = 'translated'
    os.makedirs(output_dir, exist_ok=True)

    # Load the 4 extracted images
    images = [cv2.imread(f'splitted/image_{i + 1}.jpg') for i in range(4)]
    original_images = [img.copy() for img in images]  # Keep a copy of the original images

    # Define the target focus point (use the first focus point)
    target_focus_point = focus_points[0]

    # Function to translate the image
    def translate_image(img, focus_point, target_point):
        tx = target_point[0] - focus_point[0]
        ty = target_point[1] - focus_point[1]
        translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
        # Translate the image
        translated_img = cv2.warpAffine(img, translation_matrix, (img.shape[1], img.shape[0]),
                                        borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
        return translated_img

    # First, calculate the size of the largest translated image
    translated_images = []
    for idx in range(len(images)):
        img = original_images[idx]
        focus_point = focus_points[idx]

        # Translate the image so the focus point aligns with the target focus point
        translated_img = translate_image(img, focus_point, target_focus_point)

        # Store the translated image
        translated_images.append(translated_img)

    def pad_image(img, max_width, max_height):
        height, width = img.shape[:2]
        top = bottom = left = right = 0

        # Calculate padding
        if width < max_width:
            right = max_width - width
        if height < max_height:
            bottom = max_height - height

        # Pad the image
        padded_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        return padded_img

    # Set the target size to the largest dimensions found
    max_width = max(img.shape[1] for img in translated_images)
    max_height = max(img.shape[0] for img in translated_images)

    # Save the padded translated images
    for idx, img in enumerate(translated_images):
        padded_frame = pad_image(img, max_width, max_height)
        # padded_frame = img
        cv2.imwrite(os.path.join(output_dir, f'translated_image_{idx + 1}.jpg'), padded_frame)

    print(f'Translated and padded images saved to "{output_dir}"')


if __name__ == '__main__':
    focus_points = [(1265, 1025), (1290, 1030), (1300, 1015), (1340, 1025)]
    translate_image_to_focus_point(focus_points)