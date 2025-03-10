import pathlib
from PIL import Image

from functions_lib import get_dir_ready
from imgs_settings import acceptable_exts
 
from icecream import ic


def get_cropped_img(
        src_path: str,
        dest_path: str
) -> None:
    '''
    '''
    src_dir = pathlib.Path(src_path)
    dest_dir = get_dir_ready(dest_path)

    output_extension = ".webp"

    for num, obj in enumerate(src_dir.glob("*")):
        if obj.suffix in acceptable_exts:        ### Test all extensions!
            filename = obj.name
            new_filename = obj.stem + output_extension
            img = Image.open(obj)
            if img.mode in ("RGBA", "P"): 
                img = img.convert("RGB")
            width, height = img.size
            if width == height:
                processed_img = img.resize((1000, 1000), resample=1)
                processed_img.save(dest_dir/new_filename, quality=85)
            elif height == 3000 and width == 4000:
                processed_img = img.crop((610, 105, 3390, 2885))
                processed_img = processed_img.resize((1000, 1000), resample=1)
                processed_img.save(dest_dir/new_filename, quality=60) 
    return


if __name__ == "__main__":
    get_cropped_img(
        src_path = "images/Картинки_стандарт_имена",
        dest_path = "images/Картинки для выгрузки"
    )