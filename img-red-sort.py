import cv2
from cv2.typing import MatLike
import numpy as np
import os
import argparse
from dataclasses import dataclass


@dataclass
class Options:
    red_treshold = 0.2
    img_dir = "."
    downscale_factor = 0.3


def load_names(dir_name : str) -> list[str]:
    imgnames = []
    dir = os.fsencode(dir_name)
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        if filename.endswith((".png", ".jpg")):
            imgnames.append(filename)

    return imgnames


def load_images(dir : str, names : list[str]) -> dict[str,MatLike]:
    images = {}
    for name in names:
        path = os.path.join(dir, name)
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        images[name] = image
        if image is None:
            print(f'Failed to load image: {name}')

    return images


def downscale(image : MatLike, factor : float):
    height = int(image.shape[0] * factor)
    width = int(image.shape[1] * factor)
    dim = (height, width)
    return cv2.resize(image, dim)


def redness(image : MatLike) -> float:
    y_shape = image.shape[0]
    x_shape = image.shape[1]
    image = image.astype(np.int64)
    mask = ((image[:, :, 0] <= 10) | (image[:, :, 0] >= 170)) & (image[:, :, 1] > 150) & (image[:, :, 2] > 75)
    return sum(mask.flatten()) / (y_shape * x_shape)


def main(options : Options):
    image_to_redness : dict[str, float] = {}
    image_names = load_names(options.img_dir)
    print(f'LOADED {len(image_names)} images')
    if len(image_names) == 0: 
        print("Check image dir path, use -h for help")
        return

    images = load_images(options.img_dir, image_names)

    for image_name in images:
        images[image_name] = downscale(
            images[image_name],
            options.downscale_factor
        )

    for image_name, image in images.items():
        image_to_redness[image_name] = redness(image)

    image_names.sort(
        key=lambda k: image_to_redness[k],
        reverse=True
    )

    red_images = filter(
        lambda name: image_to_redness[name] >= options.red_treshold,
        image_names
    )

    print("name --- redness")
    for name in red_images:
        print(f'{name} --- {image_to_redness[name]}')


def parse_args() -> Options:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--image-dir', '-d',
        help='specify directory with images', dest='imgdir',
        default='.'
    )
    parser.add_argument(
        '--red-treshold', '-t',
        help="images with lower proportion of red won't be recognized as red",
        dest='red_tr', default='0.2'
    )
    parser.add_argument(
        '--downscale', '-s',
        help='images will be scaled by this number before analyzing',
        default='0.3'
    )

    options = Options()

    args = parser.parse_args()
    options.img_dir = args.imgdir
    options.red_treshold = float(args.red_tr)
    options.downscale_factor = float(args.downscale)

    return options


if __name__ == '__main__':
    main(parse_args())

