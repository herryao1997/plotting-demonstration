from PIL import Image

def merge_gifs_vertically(gif1_path, gif2_path, output_path):
    # Open the first GIF file
    gif1 = Image.open(gif1_path)

    # Open the second GIF file
    gif2 = Image.open(gif2_path)

    # Get the number of frames in both GIFs
    frames1 = gif1.n_frames
    frames2 = gif2.n_frames

    # Get the longer duration between the two GIFs
    longer_duration = max(gif1.info.get('duration', 100) * frames1, gif2.info.get('duration', 100) * frames2)

    # Calculate the total number of frames after merging
    total_frames = max(frames1, frames2)

    # Create a new list of images to store the merged frames
    merged_frames = []

    # Loop to concatenate the frames from both GIFs
    for i in range(total_frames):
        # Calculate the current frame index in both GIFs
        gif1_index = i % frames1
        gif2_index = i % frames2

        # Extract the image of the current frame
        gif1.seek(gif1_index)
        frame1 = gif1.copy().convert('RGBA')
        gif2.seek(gif2_index)
        frame2 = gif2.copy().convert('RGBA')

        # Adjust the size of both frames to fit the concatenation
        width = max(frame1.width, frame2.width)
        height = frame1.height + frame2.height

        # Create a new image to store the merged frame (set the image mode to RGB
        # Extract the image of the current frame
        gif1.seek(gif1_index)
        frame1 = gif1.copy().convert('RGBA')
        gif2.seek(gif2_index)
        frame2 = gif2.copy().convert('RGBA')

        # Adjust the size of both frames to fit the concatenation
        width = max(frame1.width, frame2.width)
        height = frame1.height + frame2.height
        merged_frame = Image.new('RGBA', (width, height), (255, 255, 255, 0))

        # Calculate the horizontal offset for centering the images
        offset_x1 = (width - frame1.width) // 2
        offset_x2 = (width - frame2.width) // 2

        # Copy the first image to the merged image
        merged_frame.paste(frame1, (offset_x1, 0), mask=frame1)

        # Copy the second image to the merged image
        merged_frame.paste(frame2, (offset_x2, frame1.height), mask=frame2)

        # Set the delay time for the current frame
        merged_frame.info['duration'] = max(frame1.info.get('duration', 100), frame2.info.get('duration', 100))

        # Add the current frame to the list of merged frames
        merged_frames.append(merged_frame)

    # Save the merged GIF file
    merged_frames[0].save(output_path, save_all=True, append_images=merged_frames[1:], optimize=False, loop=0)

    print("GIF file has been merged!")


# usagesize
gif2_path = 'output.gif'  # Path to the first GIF file
gif1_path = 'velocity_massfraction_animation.gif'  # Path to the second GIF file
output_path = 'merged.gif'  # Path for the merged GIF file

merge_gifs_vertically(gif1_path, gif2_path, output_path)
