import cv2
import numpy as np
import os


def translate_image_to_focus_point(focus_points):
    # Ensure the output directory exists
    output_dir = 'translated'
    os.makedirs(output_dir, exist_ok=True)

    # Load the 4 extracted images
    images = [cv2.imread(f'splitted/image_{i + 1}.png') for i in range(4)]
    original_images = [img.copy() for img in images]  # Keep a copy of the original images

    # Define the target focus point (use the first focus point)
    target_focus_point = focus_points[0]

    # Calculate translation offsets and determine maximum padding required
    min_tx = min_ty = 0
    max_tx = max_ty = 0
    translations = []

    for focus_point in focus_points:
        # Calculate translation offsets
        tx = target_focus_point[0] - focus_point[0]
        ty = target_focus_point[1] - focus_point[1]
        translations.append((tx, ty))

        # Update min and max translation values
        min_tx = min(min_tx, tx)
        max_tx = max(max_tx, tx)
        min_ty = min(min_ty, ty)
        max_ty = max(max_ty, ty)

    # Define the padding values based on the max shifts calculated
    padding_left = -min_tx
    padding_right = max_tx
    padding_top = -min_ty
    padding_bottom = max_ty

    # Function to pad and translate an image to ensure focus points are aligned correctly
    def pad_and_translate_image(img, tx, ty):
        # Pad the image with the calculated padding
        padded_img = cv2.copyMakeBorder(
            img,
            padding_top,
            padding_bottom,
            padding_left,
            padding_right,
            cv2.BORDER_CONSTANT,
            value=(0, 0, 0)
        )

        # Create the translation matrix
        translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])

        # Translate the padded image within its new dimensions
        translated_img = cv2.warpAffine(
            padded_img,
            translation_matrix,
            (padded_img.shape[1], padded_img.shape[0]),
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0)
        )

        return translated_img

    # Process and translate each image with the required padding
    translated_images = []
    for idx, (img, (tx, ty)) in enumerate(zip(original_images, translations)):
        padded_translated_img = pad_and_translate_image(img, tx, ty)
        translated_images.append(padded_translated_img)

    # Ensure all images are the same size by padding them to the maximum width and height
    pad_images_to_same_size(translated_images, output_dir)


def pad_images_to_same_size(images, output_dir):
    # Find the maximum width and height among all images
    max_width = max(image.shape[1] for image in images)
    max_height = max(image.shape[0] for image in images)

    # Function to pad an image to the target size by adding padding only to the right and bottom
    def pad_to_size(img, target_width, target_height):
        height, width = img.shape[:2]
        pad_bottom = target_height - height
        pad_right = target_width - width

        # Pad the image only to the right and bottom
        padded_img = cv2.copyMakeBorder(
            img,
            0,            # top padding
            pad_bottom,   # bottom padding
            0,            # left padding
            pad_right,    # right padding
            cv2.BORDER_CONSTANT,
            value=(0, 0, 0)
        )

        return padded_img

    # Pad each image to the maximum width and height and save them
    for idx, img in enumerate(images):
        padded_img = pad_to_size(img, max_width, max_height)
        cv2.imwrite(os.path.join(output_dir, f'translated_image_{idx + 1}.png'), padded_img)

    print(f'Final padded images saved to \"{output_dir}\"')


if __name__ == '__main__':
    focus_points = [(2025, 1060), (2036, 1054), (2070, 1033), (2087, 1025)]
    translate_image_to_focus_point(focus_points)
