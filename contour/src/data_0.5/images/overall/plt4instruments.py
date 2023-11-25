from PIL import Image
import os


def merge_images(image_files, prefixes, output_filename):
    # We will collect the images and then resize the 'trace_' images to match the height of the first image
    images = []
    first_image_height = None  # We'll store the height of the first image here

    for image, prefix in zip(image_files, prefixes):
        img = Image.open(image)
        width, height = img.size

        # Save the height of the first image
        if first_image_height is None:
            first_image_height = height

        if prefix == 'blocking_':
            img = img.crop((0, 0, width - width // 5, height))  # Crop width of 'blocking_' images
        elif prefix == 'overall_':
            img = img.crop((width // 4, 0, width - width // 5, height))  # Crop width of 'overall_' images
        elif prefix == 'trace_':
            if first_image_height is not None:  # If the height of the first image is known, resize proportionally
                aspect_ratio = width / height
                new_height = first_image_height
                new_width = int(aspect_ratio * new_height)
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
                img = img.crop((new_width // 4, 0, new_width - new_width // 5, new_height))

        images.append(img)

    # Combine the images horizontally
    total_width = sum(img.size[0] for img in images)
    max_height = max(img.size[1] for img in images)  # The maximum height is now the first image's height
    new_img = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in images:
        y_offset = (max_height - img.size[1]) // 2  # Center the image vertically
        new_img.paste(img, (x_offset, y_offset))
        x_offset += img.size[0]
        img.close()  # Close the image after pasting

    # Save the combined image
    new_img.save(output_filename)


# Define folder names and corresponding file prefixes
folders_and_prefixes = {
    'blocking': 'blocking_',
    'contamination_overall': 'overall_',
    'trace': 'trace_'
}

# Create the output folder
output_folder = 'merged'
os.makedirs(output_folder, exist_ok=True)

# Assume each folder contains the same number of images
num_images = len(os.listdir('blocking'))  # Use the 'blocking' folder as a reference

# Merge the images
for i in range(num_images):
    # Create file paths and prefix lists
    image_files = [os.path.join(folder, f"{prefix}{i:04d}.png") for folder, prefix in folders_and_prefixes.items()]
    prefixes = list(folders_and_prefixes.values())
    output_filename = os.path.join(output_folder, f"merged_{i:04d}.png")
    merge_images(image_files, prefixes, output_filename)

print("Image merging complete!")
