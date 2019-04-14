import os
import typing as T
from collections import defaultdict

import PIL.Image
import PIL.ImageFilter
import d3dshot
import numpy as np
from PIL.Image import Image

screen_snapper = d3dshot.create()
width, height = 154, 44
debug = False

gun_edge_templates: T.Dict[str, Image] = {}
guns: T.List[str] = []


def grab_and_detect(region: T.Tuple[int, int, int, int]) -> str:
    image = screen_snapper.screenshot(region=region)
    gun = detect_gun(image.convert('L'))
    return gun



def grab_and_save(label: str, ts_nano: int, region: T.Tuple[int, int, int, int]) -> None:
    image = screen_snapper.screenshot(region=region)
    gun = detect_gun(image.convert('L'))
    directory = f'images/uncategorized/{gun}/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    image.save(f'{directory}{label}_{ts_nano}.png')


def average_template(images: T.List[Image]) -> Image:
    arr = np.zeros((height, width), np.float)
    for image in images:
        arr += np.array(image, dtype=np.float)
    arr /= len(images)
    arr = np.array(np.round(arr), dtype=np.uint8)
    return PIL.Image.fromarray(arr, mode='L')


def edge_detect(image: Image) -> Image:
    edge = image.filter(PIL.ImageFilter.FIND_EDGES)
    arr = np.array(edge, dtype=np.uint8)
    arr[0, :] = 0
    arr[:, 0] = 0
    arr[-1, :] = 0
    arr[:, -1] = 0
    if np.all(arr == 0):
        return image
    threshold = np.mean(arr[arr > 0])
    arr[arr <= int(threshold)] = 0
    if np.all(arr == 0):
        return image
    threshold = np.mean(arr[arr > 0])
    arr[arr < int(threshold)] = 0
    arr[arr >= int(threshold)] = 255
    edge = PIL.Image.fromarray(arr, mode='L')
    arr = np.array(edge, dtype=np.float)
    edge = PIL.Image.fromarray(np.array(arr, dtype=np.uint8), mode='L')
    return edge


def diff(a: Image, b: Image) -> Image:
    a = np.array(a, dtype=np.float)
    b = np.array(b, dtype=np.float)
    return PIL.Image.fromarray(np.array(np.abs(a-b), dtype=np.uint8), mode='L')


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    len_a = np.linalg.norm(a)
    len_b = np.linalg.norm(b)
    if len_a == 0 or len_b == 0:
        return 0
    return np.dot(a, b) / (len_a * len_b)


def similarity(edge: Image, edge_template: Image) -> float:
    edge = np.array(edge, dtype=np.float).flatten()
    edge_template = np.array(edge_template, dtype=np.float).flatten()
    return cosine_similarity(edge, edge_template)


def detect_gun(image: Image) -> str:
    edge = edge_detect(image)
    gun_similarities = {}
    for gun, edge_template in gun_edge_templates.items():
        gun_similarities[gun] = similarity(edge, edge_template)
    gun = max(gun_similarities.items(), key=lambda x: x[1])[0]
    return gun


def init():
    global gun_edge_templates, guns
    guns = sorted(set(os.listdir('images/')) - {'uncategorized'})
    gun_images: T.DefaultDict[str, T.List[Image]] = defaultdict(list)

    for gun in guns:
        image_files = os.listdir(f'images/{gun}/')
        for image_file in image_files:
            if image_file[0] == '_':
                continue
            image: Image = PIL.Image.open(f'images/{gun}/{image_file}').convert('L')  # grayscale
            assert image.size == (width, height)
            gun_images[gun].append(image)

    gun_edge_templates = {}
    for gun in guns:
        avg_img = average_template(gun_images[gun])
        edge_img = edge_detect(avg_img)

        gun_edge_templates[gun] = edge_img

        avg_img.save(f'images/{gun}/_average_template.png')
        edge_img.save(f'images/{gun}/_edge_template.png')


def test():
    correct_count = 0
    count = 0
    for gun in guns:
        image_files = sorted(os.listdir(f'images/{gun}/'))
        for image_file in image_files:
            if image_file[0] == '_':
                continue
            image: Image = PIL.Image.open(f'images/{gun}/{image_file}').convert('L')  # grayscale
            assert image.size == (width, height)
            detected_gun = detect_gun(image)
            count += 1
            if gun == detected_gun:
                correct_count += 1
            if debug and gun != detected_gun:
                edge = edge_detect(image)
                expected = gun_edge_templates[gun]
                found = gun_edge_templates[detected_gun]

                edge.show(title='edges')
                # expected.show(title=f'template for {gun}')
                # found.show(title=f'template for {detected_gun}')
                input(f'Actual: {gun}, detected: {detected_gun}. File: {image_file}')
                # diff(edge, expected).show(title=f'edges vs {gun}')
                # diff(edge, found).show(title=f'edges vs {detected_gun}')
                # input()
                # input()
                # input()
                # input()
    print(f'Got {correct_count} correct out of {count}. ({100 * correct_count / count:.2f}%)')


if __name__ == '__main__':
    os.chdir('../')

init()

if __name__ == '__main__':
    test()

