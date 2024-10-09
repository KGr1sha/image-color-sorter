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


class Image:
    def __init__(self, path : str, name : str) -> None:
        self.name = name
        self.path = path
        self.data : MatLike
        self.shape : tuple[int, int] = (0, 0)
        self.redness : float = 0

    def load(self) -> None:
        self.data = cv2.cvtColor(
            cv2.imread(self.path),
            cv2.COLOR_BGR2HSV
        )
        if self.data is None:
            print("Failed to load image, check the path")
        self.shape = self.data.shape[0], self.data.shape[1]

    def downscale(self, factor : float) -> None:
        height = int(self.shape[0] * factor)
        width = int(self.shape[1] * factor)
        dim = (height, width)
        self.data = cv2.resize(self.data, dim)
        self.shape = dim

    def calculate_redness(self) -> None:
        self.data = self.data.astype(np.int64)
        mask = ((self.data[:, :, 0] <= 10) | (self.data[:, :, 0] >= 170)) & (self.data[:, :, 1] > 150) & (self.data[:, :, 2] > 75)
        self.redness = sum(mask.flatten()) / (self.shape[0] * self.shape[1])


def load_names(dir_name : str) -> list[str]:
    imgnames = []
    dir = os.fsencode(dir_name)
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        if filename.endswith((".png", ".jpg")):
            imgnames.append(filename)

    return imgnames


def load_images(dir : str, names : list[str]) -> list[Image]:
    images = []
    for name in names:
        path = os.path.join(dir, name)
        image = Image(path, name)
        image.load()
        images.append(image)

    return images


def main(options : Options):
    image_names = load_names(options.img_dir)
    print(f'LOADED {len(image_names)} images')
    if len(image_names) == 0: 
        print("Check image dir path, use -h for help")
        return

    images = load_images(options.img_dir, image_names)

    for image in images:
        image.downscale(options.downscale_factor)
        image.calculate_redness()

    images.sort(
        key=lambda img: img.redness,
        reverse=True
    )

    red_images :list[Image]= []

    for image in images:
        if image.redness >= options.red_treshold:
            red_images.append(image)

    print("name --- redness")
    for image in red_images:
        print(f'{image.name} --- {image.redness}')


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

