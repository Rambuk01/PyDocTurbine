import PIL
from PIL import Image, ImageDraw, ImageFont
import os
from tkinter import Tk
from tkinter import filedialog
import json

IMAGE_INFO_ORDER = ['date', 'site', 'turbine_number', 'blade_number', 'blade_type', 'section', 'element', 'task'];
def load_section_data():
    # Load the JSON data from a file
    with open('report_script/sections.json', 'r') as file:
        data = json.load(file)
    return data


def load_images(path):
    dir_items = os.listdir(path)
    images = [file for file in dir_items if file.lower().endswith(('.jpg', '.jpeg')) and file != 'd.jpg']

    
    return images

# Takes the image name, and splits by _. Adds the values to the IMAGE_INFO_ORDER by order. Returns the dict.
def get_image_info(image: str, id: int, path):
    image_info = {}

    # Add id first
    image_info['id'] = id

    # Add full image name:
    image_info['path'] = f"{path}/{image}"

    # Split on _ , and add each value to the dict.
    values = image.split('_')
    for n, key in enumerate(IMAGE_INFO_ORDER):
        image_info[key] = values[n].replace('.jpg', '')

    # We can also check for values, not in image_info. Perhaps we want to add more infomation to each image?

    return image_info;

# Get the image info, for each image. Add it to a list and return it
def get_image_info_list(images: list, path: str):
    image_info_list = []
    
    # We would probably want to sort the images, by 'date', 'site', 'turbine_number', 'blade_number', 'blade_type', 'section', 'element', 'task'
    images.sort()

    for n, image in enumerate(images):
        image_info = get_image_info(image, n, path)
        image_info_list.append(image_info)

    return image_info_list

def select_folder(initial_folder=None):
    # Hide the main tkinter window
    root = Tk()
    root.withdraw()  # Prevents the Tk window from appearing

    # Open a file dialog to select the folder
    folder_path = filedialog.askdirectory(title="Select a folder", initialdir=initial_folder)
    
    return folder_path


def process_images(image_list: list, path):
    # Create output folder if it doesn't exist
    output_folder = f"{path}/new"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through the list of dictionaries
    for data in image_list:
        input_image_path = data['path']
        output_image_path = os.path.join(output_folder, f"{data['id']}_{os.path.basename(data['path'])}")
        
        # Add text to the image and save it
        new_img = add_text_to_image(input_image_path, output_image_path, data)
        print(f"Saved: {output_image_path}")

        # Add new key-values to the original data dictionary
        data['new_path'] = new_img
    
    return image_list


def add_text_to_image(image_path, output_path, text_data):
    # Open the image
    img = Image.open(image_path).convert("RGBA")  # Ensure the image is in RGBA mode for transparency
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))  # Create a transparent overlay
    
    draw = ImageDraw.Draw(overlay)
    
    # Load a custom font with a larger size (change the path to a valid .ttf font if needed)
    #font_path = "/path/to/your/font.ttf"  # You can replace this with a custom font path
    font = ImageFont.load_default(36)  # Using truetype to specify size

    # Prepare the text from the dictionary
    lines = [
        f"Date: {text_data['date']}",
        f"Site: {text_data['site']}",
        f"Turbine: {text_data['turbine_number']}",
        f"Blade: {text_data['blade_number']}",
        f"Blade Type: {text_data['blade_type']}",
        f"Section: {text_data['section']}",
        f"Element: {text_data['element']}",
        f"Task: {text_data['task']}"
    ]

    # Combine the lines into one block of text
    text_block = "\n".join(lines)

    # Get the bounding box of the text to calculate its width and height
    text_bbox = draw.textbbox((0, 0), text_block, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Position the text at the bottom right
    padding = 20
    x = img.width - text_width - padding
    y = img.height - text_height - padding

    # Add a semi-transparent background rectangle behind the text
    background_color = (0, 0, 0, 128)  # Black with 50% opacity
    rectangle_x1 = x - padding
    rectangle_y1 = y - padding
    rectangle_x2 = img.width
    rectangle_y2 = img.height
    draw.rectangle([(rectangle_x1, rectangle_y1), (rectangle_x2, rectangle_y2)], fill=background_color)

    # Write the text over the rectangle
    draw.multiline_text((x, y), text_block, font=font, fill=(255, 255, 255, 255))  # White text with full opacity

    # Combine the overlay with the original image
    img_with_overlay = Image.alpha_composite(img, overlay)

    # Convert back to RGB mode for saving as JPEG (optional)
    img_with_overlay = img_with_overlay.convert("RGB")
    
    # Save the edited image
    img_with_overlay.save(output_path)
    return output_path