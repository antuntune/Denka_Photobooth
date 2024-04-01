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


def create_blank_image(width, height):
    """
    Create a blank image with the specified dimensions.

    Parameters:
    width (int): The width of the blank image.
    height (int): The height of the blank image.

    Returns:
    Image: A blank image object.
    """
    return Image.new("RGBA", (width, height), (255, 255, 255, 0))

def paste_image_final(original_image_path, output_image_path):
    """
    Paste an image onto a blank image and save the final image.

    Parameters:
    original_image_path (str): The path to the original image file.
    output_image_path (str): The path to save the final image.
    """
    original_image = Image.open(original_image_path)

    blank_image = create_blank_image(150, 165)

    # Calculate the y-coordinate to align the bottom lines of the two images
    y_coordinate = blank_image.height - original_image.height

    # Paste the original image onto the blank image at coordinates (0, y_coordinate)
    blank_image.paste(original_image, (0, y_coordinate))

    # Save the final image
    blank_image.save(output_image_path)

def add_shadow(input_image_path, output_image_path, shadow_color=(0, 0, 0), shadow_opacity=55, blur_radius=10):
    """
    Add a shadow effect to an image and save it as a new image.

    Parameters:
    input_image_path (str): The path to the input image file.
    output_image_path (str): The path to save the image with the shadow effect.
    shadow_color (tuple): The color of the shadow in RGB format. Default is black.
    shadow_opacity (int): The opacity of the shadow. Default is 128.
    blur_radius (int): The radius of the shadow blur effect. Default is 10.
    """
    # Open the original image
    original_image = Image.open(input_image_path)

    # Create a new blank image with the same size as the original image
    shadow_image = Image.new("RGBA", original_image.size, (0, 0, 0, 0))

    # Create a drawing context for the shadow image
    draw = ImageDraw.Draw(shadow_image)

    # Draw a shadow rectangle covering the entire image area
    draw.rectangle((0, 0, original_image.width, original_image.height), fill=shadow_color + (shadow_opacity,))

    # Apply a Gaussian blur filter to the shadow image
    shadow_image_blurred = shadow_image.filter(ImageFilter.GaussianBlur(blur_radius))

    # Composite the original image and the shadow image with alpha blending
    result_image = Image.alpha_composite(original_image.convert("RGBA"), shadow_image_blurred)

    # Save the resulting image with the shadow effect
    result_image.save(output_image_path)



def crop_circle(input_image_path, output_image_path, radius):
    """
    Remove a circular region from the center of an image and save the result as a new image.

    Parameters:
    input_image_path (str): The path to the input image file.
    output_image_path (str): The path to save the result without the circular region.
    radius (int): The radius of the circular region to be removed.
    """
    # Open the original image
    original_image = Image.open(input_image_path)

    # Create a mask with the same size as the original image
    mask = Image.new("L", original_image.size, 255)

    # Create a drawing context for the mask
    draw = ImageDraw.Draw(mask)

    # Calculate the center coordinates
    width, height = original_image.size
    center_x = width // 2
    center_y = height // 2

    # Draw a black circle on the mask to represent the circular region to be removed
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=0)

    # Apply the mask to the original image using bitwise operations
    result_image = original_image.copy()
    result_image.putalpha(mask)

    # Save the result image without the circular region
    result_image.save(output_image_path)


# Example usage:
input_image_path = "minus_button.png"
output_image_path = "minus_button_resized.png"
new_size = (150, 150)  # New size (width, height) in pixels
resize_image(input_image_path, output_image_path, new_size)

paste_image_final("minus_button_resized.png", "bg.png")

paste_image_final("minus_button_resized.png", "minus_buttonPressed.png")

add_shadow("minus_buttonPressed.png", "minus_buttonPressed.png")

add_shadow("bg.png", "bg_.png")

# Radius of the circular region (you may adjust this value)
radius = 50

crop_circle("bg_.png", "output_cropped_circle.png", radius)



