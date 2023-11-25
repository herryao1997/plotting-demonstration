from PIL import Image
import os


def merge_images(image_files, prefixes, output_filename):
    images = []
    for image, prefix in zip(image_files, prefixes):
        img = Image.open(image)

        # Crop based on the prefix
        width, height = img.size
        if prefix == 'bottom-view_':
            img = img.crop((0, height//5, width - width // 3, height - height//15))  # Keep 2/3 from left
        elif prefix == 'side-view_':
            img = img.crop((0, height//5, width - width // 4, height - height//15))  # Keep 3/4 from left
        else:
            # Customize the crop to remove unwanted whitespace without affecting color bars
            # This is a placeholder; you'll need to adjust the crop area based on your images
            img = img.crop((left_margin, 0, width - right_margin, height))

        images.append(img)

    # Combine images horizontally
    total_width = sum(img.size[0] for img in images)
    max_height = max(img.size[1] for img in images)
    new_img = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in images:
        new_img.paste(img, (x_offset, 0))
        x_offset += img.size[0]
        img.close()  # Close the image after pasting

    new_img.save(output_filename)


# Define folders and prefixes
folders_and_prefixes = {
    'bottom_view': 'bottom-view_',
    'side_view': 'side-view_'
}

# Create output folder
output_folder = 'merged'
os.makedirs(output_folder, exist_ok=True)

# Assume all folders contain the same number of images
num_images = len(os.listdir('bottom_view')) # Example reference

# Process images
for i in range(num_images):
    image_files = [os.path.join(folder, f"{prefix}{i:04d}.png") for folder, prefix in folders_and_prefixes.items()]
    prefixes = list(folders_and_prefixes.values())
    output_filename = os.path.join(output_folder, f"merged_{i:04d}.png")
    merge_images(image_files, prefixes, output_filename)

print("Image merging complete!")
