from PIL import Image
import os


def merge_images(image_files, prefixes, output_filename):
    images = []
    for image, prefix in zip(image_files, prefixes):
        img = Image.open(image)
        width, height = img.size
        img = img.crop((0, 0, width - width // 5, height))  # 裁剪图片宽度的1/5
        images.append(img)

    # 获取单个图片的宽度和高度
    widths, heights = zip(*(i.size for i in images))

    # 新图片的总宽度和高度
    total_width = sum(widths)
    max_height = max(heights)

    # 创建一个新的空白图片
    new_img = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in images:
        new_img.paste(img, (x_offset, 0))
        x_offset += img.size[0]

    # 保存新图片
    new_img.save(output_filename)

    # 关闭所有打开的图像
    for img in images:
        img.close()


# 定义文件夹名称和对应的文件名前缀
folders_and_prefixes = {
    'floor_view': 'floor-view_',
    'outlet_view': 'outlet-view_',
    'top_view': 'top-view_'
}

output_folder = 'merged'
os.makedirs(output_folder, exist_ok=True)

# 假设每个文件夹中的图片数量相同
num_images = len(os.listdir('floor_view'))  # 用'center'文件夹作为参考

# 合并图片
for i in range(num_images):
    # 创建文件路径和前缀列表
    image_files = [os.path.join(folder, f"{prefix}{i:04d}.png") for folder, prefix in folders_and_prefixes.items()]
    prefixes = [prefix for prefix in folders_and_prefixes.values()]
    output_filename = os.path.join(output_folder, f"merged_{i:04d}.png")
    merge_images(image_files, prefixes, output_filename)

print("图片合并完成！")
