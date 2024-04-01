from PIL import Image, ImageDraw, ImageFilter

def resize_image(input_image_path, output_image_path, size):
    """
    Resize an image using PIL.

    Parameters:
    input_image_path (str): The path to the input image file.
    output_image_path (str): The path to save the resized image.
    size (tuple): A tuple containing the width and height of the resized image.
    """
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)

    # Example usage:
input_image_path = "eight_.png"
output_image_path = "eight.png"
new_size = (115, 150)  # New size (width, height) in pixels
resize_image(input_image_path, output_image_path, new_size)

input_image_path = "six_.png"
output_image_path = "six.png"
new_size = (115, 150)  # New size (width, height) in pixels
resize_image(input_image_path, output_image_path, new_size)

input_image_path = "four_.png"
output_image_path = "four.png"
new_size = (115, 150)  # New size (width, height) in pixels
resize_image(input_image_path, output_image_path, new_size)

input_image_path = "two_.png"
output_image_path = "two.png"
new_size = (115, 150)  # New size (width, height) in pixels
resize_image(input_image_path, output_image_path, new_size)