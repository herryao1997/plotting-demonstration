from PIL import Image, ImageDraw

# Create a GIF with 80 frames, displaying time from 0.0 to 40.0 seconds
# Each frame will display a progressive time with an increment

# Define parameters for the GIF
num_frames = 80
total_time = 40.0
increment = total_time / num_frames
img_size = (150, 50)
bg_color = "white"
text_color = "black"
font_size = 24  # Adjusting font size for better visibility

# Create a list to hold all the frames
frames = []

for i in range(num_frames):
    # Calculate the time for the current frame
    time = increment * i

    # Create a new image with white background
    img = Image.new("RGB", img_size, bg_color)

    # Get a drawing context
    d = ImageDraw.Draw(img)

    # Define the font size (no specific font type, using default PIL font)
    # Draw the time text onto the image centered
    time_text = f"Time = {time:.2f} s"
    text_width, text_height = d.textsize(time_text)
    x_pos = (img_size[0] - text_width) // 2
    y_pos = (img_size[1] - text_height) // 2

    # Draw the time text onto the image
    d.text((x_pos, y_pos), time_text, fill=text_color)

    # Append the frame to the list of frames
    frames.append(img)

# Save the frames as a GIF
output_file_path = "output_with_default_font.gif"
frames[0].save(output_file_path, save_all=True, append_images=frames[1:], optimize=False, duration=500, loop=0)
