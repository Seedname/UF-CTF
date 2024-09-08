from PIL import Image
import numpy as np

def xor_images(image_path1, image_path2, output_path):
    # Open images
    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)

    # Convert images to RGB if they are in RGBA format
    if img1.mode == 'RGBA':
        img1 = img1.convert('RGB')
    if img2.mode == 'RGBA':
        img2 = img2.convert('RGB')

    # Ensure both images are in the same mode and size
    if img1.mode != img2.mode or img1.size != img2.size:
        raise ValueError("Both images must have the same size and mode.")

    # Convert images to numpy arrays
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    # Perform XOR operation
    xor_result = np.bitwise_and(arr1, arr2)

    # Convert result array back into an image
    xor_image = Image.fromarray(xor_result)

    # Save or show the resulting image
    xor_image.save(output_path)

# Example usage:
image1_path = 'secret.png'
image2_path = 'original.png'
output_image_path = 'result_image.png'

xor_images(image1_path, image2_path, output_image_path)
