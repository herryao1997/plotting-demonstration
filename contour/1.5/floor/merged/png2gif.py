from PIL import Image
import os

# create the figure list
frames = []

# reading 68 png figures as one period
for i in range(80):
    filename = f"merged_{i:04}.png"
    if os.path.isfile(filename):
        image = Image.open(filename)
        frames.append(image)

# save as GIF
frames[0].save("output.gif", save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0)

print("GIF file is generated ！")
