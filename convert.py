import fire
import glob as glb
import os
import uuid
import sys
from PIL import Image


WHATSAPP_IMAGE_SIZE = 512, 512
WHATSAPP_IMAGE_SIZE_WITHOUT_MARGIN = WHATSAPP_IMAGE_SIZE[0] - 16 * 2, WHATSAPP_IMAGE_SIZE[1] - 16 * 2


def try_get_image(filename: str):
    try:
        return Image.open(filename)
    except IOError:
        return None


def convert_image(image):
    image = image.resize(WHATSAPP_IMAGE_SIZE_WITHOUT_MARGIN, Image.ANTIALIAS)
    new_image = Image.new('RGBA', WHATSAPP_IMAGE_SIZE, (255, 0, 0, 0))
    x_pos = int((WHATSAPP_IMAGE_SIZE_WITHOUT_MARGIN[0] - WHATSAPP_IMAGE_SIZE[0]) / 2)
    y_pos = int((WHATSAPP_IMAGE_SIZE_WITHOUT_MARGIN[1] - WHATSAPP_IMAGE_SIZE[1]) / 2)
    new_image.paste(image, (x_pos, y_pos))
    return new_image


def save_image_as_webp(image, file, out_dir, keep_original_name):
    file_name = os.path.basename(file) if keep_original_name else str(uuid.uuid4())
    file_path = os.path.join(out_dir, file_name) + '.webp'
    print(f'Saving file to {file_path}')
    image.save(file_path, 'WEBP')


def convert(dir, glob, out, use_original_file_name=False):
    """Converts the given files into WhatsApp compatible webp images with a resolution of 512x512 and a margin of 16px.

    Args:
        dir (str): The base directory to execute the glob in.
        glob (str): The glob to find the files.
        out (str): The output directory for the created webp files.
        use_original_file_name (bool): Whether to use the original file name or not.
    """
    if not os.path.isdir(out):
        print(f'ERR: Invalid dir {out}')
        return

    os.chdir(dir)
    files = list(glb.iglob(glob, recursive=True))
    for file in files:
        image = try_get_image(file)
        if not image:
            print(f'ERR: File {file} is not a valid image')
        else:
            try:
                print(f'Converting {file}...')
                image = convert_image(image)
                save_image_as_webp(image, file, out, use_original_file_name)
            except:
                print(f'Failed to convert image {file}!')


def main(_=None):
      fire.Fire(convert)

if __name__ == '__main__':
    main()