import codecs
import logging
import os
import pathlib
import shutil
from datetime import datetime

import ffmpeg
from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS, GPSTAGS
from PIL.Image import Exif


class PhotoManager:

    def __init__(self) -> None:
        super().__init__()

    def sort_folder(self, folder_path, output_folder):
        logging.info(folder_path)

        for root, dirs, files in os.walk(folder_path, topdown=True):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                original_datetime = None
                if PhotoManager.size_stat(file_path) == 0:
                    logging.warning(f'SIZE 0 -> {file_path}')
                    continue

                if file_path.endswith('.jpg'):
                    try:
                        info_dict = PhotoManager.extract_metadata(file_path)
                        logging.info(file_path)

                        if info_dict.get('DateTimeOriginal'):
                            original_datetime = datetime.strptime(info_dict.get('DateTimeOriginal'),
                                                                  '%Y:%m:%d %H:%M:%S')
                        else:
                            original_datetime = PhotoManager.time_stat(file_path)
                    except UnidentifiedImageError:
                        logging.error(file_path)
                        continue
                elif file_path.endswith('.mp4'):
                    logging.info(file_path)
                    streams = ffmpeg.probe(file_path)["streams"]
                    for stream in streams:
                        if stream['codec_type'] == 'video':
                            if stream.get('tags', {}).get('creation_time'):
                                original_datetime = datetime.strptime(stream.get('tags', {}).get('creation_time'),
                                                                      '%Y-%m-%dT%H:%M:%S.%fZ')
                            else:
                                original_datetime = PhotoManager.time_stat(file_path)
                            break
                else:
                    continue

                dest_sub_folder = root.replace(os.path.dirname(output_folder), '').replace('/', '_')
                dest_folder = os.path.join(output_folder, dest_sub_folder, str(original_datetime.year),
                                           str(original_datetime.month))
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(file_path,
                            os.path.join(dest_folder, os.path.basename(file_path)))

                logging.info(original_datetime)

    @staticmethod
    def extract_metadata(image_path, verbose=False) -> dict:
        image: Image = Image.open(image_path)

        info_dict = {
            "Filename": image.filename,
            "ImageSize": image.size,
            "ImageHeight": image.height,
            "ImageWidth": image.width,
            "ImageFormat": image.format,
            "ImageMode": image.mode,
            "IsAnimated": getattr(image, "is_animated", False),
            "NFrames": getattr(image, "n_frames", 1)
        }

        exif_data: Exif = image.getexif()
        for tag_id, value in image._getexif().items() if image._getexif() else {}:
            decoded_tag = TAGS.get(tag_id, tag_id)

            if decoded_tag == "GPSInfo":
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)

                    if sub_decoded == 'GPSVersionID':
                        sub_value = PhotoManager.byte_string_to_numbers(value[t])
                        sub_value = '.'.join(sub_value)
                    else:
                        sub_value = PhotoManager.decode_bytes(value[t])

                    info_dict[sub_decoded] = sub_value
            elif decoded_tag != 'MakerNote':
                value = PhotoManager.decode_bytes(value)
                info_dict[decoded_tag] = value

        if verbose:
            for key, value in info_dict.items():
                logging.info(f'{key:30}: {value}')

        return info_dict

    @staticmethod
    def decode_bytes(value) -> str:
        return codecs.decode(value, 'UTF-8') if isinstance(value, bytes) else value

    @staticmethod
    def byte_string_to_numbers(value) -> [str]:
        return [str(ord(x)) for x in PhotoManager.decode_bytes(value)]

    @staticmethod
    def time_stat(file_path):
        return datetime.fromtimestamp(os.path.getmtime(file_path))

    @staticmethod
    def size_stat(file_path):
        return os.path.getsize(file_path)