import pathlib
import re
import shutil

from functions import get_dir_ready

import logging
from datetime import datetime

logging.basicConfig(
    level="DEBUG", 
    filename=f"logs/card_conf_{datetime.now().strftime('%m-%d_%H-%M')}.log", 
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
    encoding='utf-8')

from icecream import ic

correct_colorname = {
    "анкор": "Ясень Анкор светлый",
    "белый снег": "Белый снег",
    "бетон": "Бетон",
    "венге": "Венге",
    "диамант": "Серый диамант",
    "крафт": "Крафт табачный",
    "сонома": "Сонома",
    "снег": "Белый снег",
    "кашемир": "Кашемир",
    "ясень анкор": "Ясень Анкор светлый"
}
front_types = {
    "б стекло х3": "Белое стекло",
    "б стекло зеркало б стекло": "Белое стекло, Зеркало",
    "б стекло лдсп б стекло": "Белое стекло, ЛДСП",
    "б стекло ч стекло б стекло": "Белое стекло, Черное стекло",
    "белое стекло белое стекло": "Белое стекло",
    "белое стекло зеркало": "Белое стекло, Зеркало",
    "белое стекло лдсп": "Белое стекло, ЛДСП",
    "белое стекло черное стекло": "Белое стекло, Черное стекло",
    "зеркало 3х": "Зеркало",
    "зеркало х3": "Зеркало",
    "зеркало б стекло зеркало": "Зеркало, Белое стекло",
    "зеркало белое стекло": "Зеркало, Белое стекло",
    "зеркало зеркало": "Зеркало",
    "зеркало лдсп": "Зеркало, ЛДСП",
    "зеркало лдсп зеркало": "Зеркало, ЛДСП",
    "зеркало стекло белое": "Зеркало, Белое стекло",
    "зеркало ч стекло зеркало": "Зеркало, Черное стекло",
    "зеркало черное стекло": "Зеркало, Черное стекло",
    "стекло белое белое стекло": "Белое стекло",
    "лдсп х3": "ЛДСП",
    "лдспх3": "ЛДСП",
    "лдсп б стекло лдсп": "ЛДСП, Белое стекло",
    "лдсп белое стекло": "ЛДСП, Белое стекло",
    "лдсп зеркало": "ЛДСП, Зеркало",
    "лдсп зеркало лдсп": "ЛДСП, Зеркало",
    "лдсп лдсп": "ЛДСП",
    "лдсп стекло белое": "ЛДСП, Белое стекло",
    "лдсп ч стекло лдсп": "ЛДСП, Черное стекло",
    "лдсп черное стекло": "ЛДСП, Черное стекло",
    "ч стеклох3": "Черное стекло",
    "ч стекло х3": "Черное стекло",
    "ч стекло б стекло чстекло": "Черное стекло, Белое стекло",
    "ч стекло б стекло ч стекло": "Черное стекло, Белое стекло",
    "ч стекло зеркало ч стекло": "Черное стекло, Зеркало",
    "ч стекло лдсп ч стекло": "Черное стекло, ЛДСП",
    "черное стекло зеркало": "Черное стекло, Зеркало",
    "черное стекло белое стекло": "Черное стекло, Белое стекло",
    "черное стекло лдсп": "Черное стекло, ЛДСП",
    "черное стекло черное стекло": "Черное стекло",
}

SOURCE_DIR = "source_files"
DEST_DIR = "checked_files"
ERROR_DIR = "error_files"


def rename(
        default_series: str,
        default_wardrobe_type: str,
        default_front_type: str,
        default_case_clr: str,
        default_profile_clr: str,
        src_path: str = SOURCE_DIR,
        dest_path: str = DEST_DIR,
        err_path: str = ERROR_DIR
) -> None:
    '''
    renames files with correct string appropriate to subsequent processing
    pattern: "Прайм 2-х дверный (Белое стекло) Бетон Черный профиль"
    '''
    src_dir = pathlib.Path(src_path)
    dest_dir = get_dir_ready(dest_path)
    err_dir = get_dir_ready(err_path)

    for object in src_dir.rglob('*'):
        if object.is_file() and object.suffix in (".jpg", ".jpeg", ".webp"):
            filename = re.sub("[-_\(\),]", " ", object.stem)
            file_ext = object.suffix
            try:
                ### Серия
                if default_series:  
                    series = default_series
                else:
                    series = re.search(
                        "(Локер|Оптим|Широкий Прайм|Прайм|Экспресс|Эста)",
                        filename,
                        re.I
                        ).group(1)
                    filename = re.sub(f"{series}", "", filename)
                ### Тип
                if default_wardrobe_type:                                   ### TODO: добавить замену найденного вхождения на допустимый вариант
                    wardrobe_type = default_wardrobe_type 
                else:
                    wardrobe_type = re.search(
                        "(2-х дверный|2-дверный|3-х дверный|3-дверный)",
                        filename,
                        re.I
                        ).group(1)
                    filename = re.sub(f"{wardrobe_type}", "", filename)
                ### Цвет корпуса
                if default_case_clr:
                    case_clr = default_case_clr
                else:
                    case_clr = re.search(
                        "(белый снег|снег|бетон|венге|серый диамант|диамант|крафт табачный|крафт|дуб табачный|дуб сонома|сонома|ясень анкор светлый|ясень анкор|анкор|ясень шимо светлый|ясень шимо|шимо)",
                        filename,
                        re.I
                        ).group()
                    filename = re.sub(f"{case_clr}", "", filename)
                    case_clr = correct_colorname[case_clr]
                ### Цвет профиля
                if default_profile_clr:
                    profile_clr = default_profile_clr
                else:
                    profile_clr = re.search(
                        "(серебро|черный профиль|чёрный матовый|белый профиль|бронза профиль)",
                        filename,
                        re.I
                        ).group(1)
                    
                filename = re.sub(f"{profile_clr}", "", filename)

                filename = re.sub(" +", " ", filename).strip()
                ### Тип фасада
                if default_front_type:
                    front_type = default_front_type
                else:
                    front_type = front_types[filename]

                new_filename = f"{series} {wardrobe_type} "\
                    f"({front_type}) {case_clr} {profile_clr}{file_ext}"
                
                shutil.copy(object, dest_dir/new_filename)
                # ic(f"{filename} успешно скопирован с именем {new_filename}")
            except Exception as e:
                ic(e)
                ic(front_type)
                logging.exception(
                    f"Ошибка при парсинге характеристик изделия: " \
                    f"{object.absolute()}")
                shutil.copy(object, err_dir)
    return
    
    
if __name__ == "__main__":
    default_series = "Прайм"
    default_wardrobe_type = "3-х дверный"
    default_front_type = ""
    default_case_clr = ""
    default_profile_clr = "Черный профиль"

    rename(
        default_series,
        default_wardrobe_type,
        default_front_type,
        default_case_clr,
        default_profile_clr
    )