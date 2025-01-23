import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_image_from_text(text, output_path):
    # Define image size and font
    width, height = 800, 600
    background_color = "white"
    text_color = "black"
    border_size = 10
    font = ImageFont.load_default()

    # Create a new image with white background
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Wrap the text to fit within the image width
    wrapped_text = textwrap.fill(text, width=70)

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Draw the text on the image
    draw.text((text_x, text_y), wrapped_text, font=font, fill=text_color)

    # Add a border to the image
    image_with_border = Image.new("RGB", (width + 2 * border_size, height + 2 * border_size), background_color)
    image_with_border.paste(image, (border_size, border_size))

    # Save the image as JPEG and PNG
    image_with_border.save(output_path + ".jpg", "JPEG")
    image_with_border.save(output_path + ".png", "PNG")

def process_files(directory, output_directory):
    for root, _, files in os.walk(directory):
        subdir_name = os.path.basename(root)
        image_counter = 1

        for file in files:
            if file.endswith((".md", ".txt", ".py", ".rb")):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                    text = f.read()

                output_path = os.path.join(output_directory, f"{subdir_name}_{image_counter}")
                create_image_from_text(text, output_path)
                print(f"Created images: {output_path}.jpg and {output_path}.png")
                image_counter += 1

if __name__ == "__main__":
    output_directory = "malicious-images"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created directory: {output_directory}")

    process_files(".", output_directory)
    print("Image generation completed.")
