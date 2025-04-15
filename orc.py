import os
import numpy as np
import torch
import torchvision.transforms as T
from PIL import Image
from torchvision.transforms.functional import InterpolationMode
from transformers import AutoModel, AutoTokenizer

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

def build_transform(input_size):
    MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
    transform = T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=MEAN, std=STD)
    ])
    return transform

def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio

def dynamic_preprocess(image, min_num=1, max_num=12, image_size=448, use_thumbnail=False):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    # calculate the existing image aspect ratio
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    # find the closest aspect ratio to the target
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)

    # calculate the target width and height
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    # resize the image
    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        # split the image
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images

def load_image(image_file, input_size=448, max_num=12):
    image = Image.open(image_file).convert('RGB')
    transform = build_transform(input_size=input_size)
    images = dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values

model = AutoModel.from_pretrained(
    "5CD-AI/Vintern-1B-v2",
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    trust_remote_code=True,
).eval().cuda()
tokenizer = AutoTokenizer.from_pretrained("5CD-AI/Vintern-1B-v2",
                                          trust_remote_code=True,
                                          use_fast=False)

generation_config = dict(max_new_tokens= 1024,
                         do_sample=False,
                         num_beams = 3,
                         repetition_penalty=2.5)

question = '<image>\nTrích xuất thông tin từ ảnh, bao gồm cả các tiêu đề (theo cách định dạng markdown)'

pages_dir = 'data/154_ngu-van-10-tap-2/pages'
orc_dir = pages_dir.replace('pages', 'text')
accepted_img_extensions = ['jpg', 'jpeg', 'png']

for img_name in os.listdir(pages_dir):
    if img_name.split('.')[-1] in accepted_img_extensions:
        print('Processing image:', img_name)
        image_path = os.path.join(pages_dir, img_name)
        pixel_values = load_image(image_path, max_num=12).to(torch.bfloat16).cuda()
        response = model.chat(tokenizer,
                              pixel_values,
                              question,
                              generation_config,
                              history=None,
                              return_history=False)
        print(f'User: {question}\nAssistant: {response}')

        # Save the response to a text file
        text_file_path = os.path.join(orc_dir,
                                      img_name.replace(img_name.split('.')[-1], 'txt'))
        os.makedirs(os.path.dirname(text_file_path), exist_ok=True)
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(response)