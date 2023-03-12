import codecs
import logging
import os

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from PIL.Image import Exif


class PhotoManager:

    def __init__(self) -> None:
        super().__init__()

    def sort_folder(self, folder_path):
        logging.info(folder_path)

        for root, dirs, files in os.walk(folder_path, topdown=True):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                logging.info(file_path)

                image: Image = Image.open(file_path)

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
                for tag_id, value in image._getexif().items():
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

                for key, value in info_dict.items():
                    logging.info(f'{key:30}: {value}')

                break

    @staticmethod
    def decode_bytes(value) -> str:
        return codecs.decode(value, 'UTF-8') if isinstance(value, bytes) else value

    @staticmethod
    def byte_string_to_numbers(value) -> [str]:
        return [str(ord(x)) for x in PhotoManager.decode_bytes(value)]
