import pathlib
from PIL import Image

from functions import get_dir_ready
 
from icecream import ic


def get_cropped_img(
        src_path: str,
        dest_path: str
) -> None:
    '''
    '''
    src_dir = pathlib.Path(src_path)
    dest_dir = get_dir_ready(dest_path)

    for num, obj in enumerate(src_dir.glob("*")):
        if obj.suffix in (".jpg", ".jpeg", ".webp"):        ### Test all extensions!
            filename = obj.name
            ic(obj.name)
            img = Image.open(obj)
            width, height = img.size
            if height == 3000 and width == 4000:
                processed_img = img.crop((610, 105, 3390, 2885))
                processed_img = processed_img.resize((1000, 1000), resample=1)
                processed_img.save(dest_dir/filename, quality=60)
    return


if __name__ == "__main__":
    get_cropped_img(
        src_path = "processed_files",
        dest_path = "resized_imgs"
    )