from PIL import Image, ImageDraw

def cut_image(input_image_path, output_cropped_image_path, output_removed_part_path):
    """
    Cut a part of an image and save it as a new image.

    Parameters:
    input_image_path (str): The path to the input image file.
    output_cropped_image_path (str): The path to save the cropped image.
    output_removed_part_path (str): The path to save the removed part of the image.
    """
    original_image = Image.open(input_image_path)

    left = 0
    top = 0
    right = original_image.width
    bottom = original_image.height - 50  # Remove 20 pixels from the bottom

    # Crop the specified region from the original image
    cropped_image = original_image.crop((left, top, right, bottom))

    # Save the cropped image
    cropped_image.save(output_cropped_image_path)

    # Create a blank image to save the removed part
    removed_part_image = Image.new("RGBA", (original_image.width, 50), (255, 255, 255, 0))

    # Paste the removed part onto the blank image
    removed_part_image.paste(original_image.crop((left, bottom, right, original_image.height)), (left, 0))

    # Save the removed part image
    removed_part_image.save(output_removed_part_path)


def cut_circle(input_image_path, output_image_path, center, radius):
    """
    Cut a circular region from an image and save it as a new image.

    Parameters:
    input_image_path (str): The path to the input image file.
    output_image_path (str): The path to save the circular region as a new image.
    center (tuple): The center coordinates (x, y) of the circular region.
    radius (int): The radius of the circular region.
    """
    # Open the original image
    original_image = Image.open(input_image_path)

    # Create a new image with an alpha channel
    mask = Image.new("L", original_image.size, 0)

    # Create a drawing context for the mask
    draw = ImageDraw.Draw(mask)

    # Draw a white circle on the mask
    draw.ellipse((center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius), fill=255)

    # Create a copy of the original image
    result_image = original_image.copy()

    # Apply the mask to the image
    result_image.putalpha(mask)

    # Save the resulting image with the circular region cut out
    result_image.save(output_image_path)



# Example usage:
input_image_path = "plus_button_resized.png"
output_cropped_image_path = "cropped_image.png"
output_removed_part_path = "removed_part.png"

cut_image(input_image_path, output_cropped_image_path, output_removed_part_path)

# Example usage:
input_image_path = "removed_part.png"
output_image_path = "output_image_with_circle_cut.png"

# Center coordinates of the circular region
center = (75, 50    )

# Radius of the circular region
radius = 30

cut_circle(input_image_path, output_image_path, center, radius)
