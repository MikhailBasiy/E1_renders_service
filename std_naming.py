from pathlib import Path
import re
import shutil

from functions_lib import get_dir_ready
from parsing_settings import series_pattern, wardrobe_type_pattern, \
                             case_color_pattern, profile_clr_pattern, \
                             color_matchings, wardrobe_type_matchings, \
                             front_materials_pattern, front_materials_matchings, \
                             skip_words
from imgs_settings import acceptable_exts

from icecream import ic


def search_property(
    obj,
    filename: str,
    search_pattern: str,
    correct_matches: dict[str: str],
    err_dir: Path,
) -> str | None:
    try:
        property_value = re.search(
            search_pattern, filename, re.I
        ).group(1)
        property_value = correct_matches[property_value]
    except AttributeError as e:             ### In case there's no finding
        ic(e, filename)
        ic(search_pattern)
        shutil.copy(obj, err_dir)
        return
    except KeyError as e:                   ### In case there's no correct match
        ic(e, filename)
        ic(property_value)
        # ic(obj, filename, search_pattern, correct_matches, err_dir)
        shutil.copy(obj, err_dir)
        return
    return property_value


def normalize_filename(
        imgs_lst: list[Path],
        dest_path: str,
        err_path: str,
        **default_values: dict[str: str],
) -> None:
    # '''
    # renames files with correct string appropriate to subsequent processing
    # pattern: "Прайм 2-х дверный (Белое стекло) Бетон Черный профиль"
    # '''
    ic(default_values)
    dest_dir: Path = get_dir_ready(dest_path)
    err_dir: Path = get_dir_ready(err_path)

    for obj in imgs_lst:
        filename = re.sub("[-_(),]", " ", obj.stem).replace("  ", " ").lower()
        if any(word in filename for word in skip_words):
            continue
        file_ext = obj.suffix
        ### Серия                       TODO: check that
        if default_series:  
            series = default_series
        else:
            series = re.search(
                series_pattern, filename, re.I
            ).group(1).capitalize()
        ### Тип шкафа                   TODO: check that
        if default_wardrobe_type:
            wardrobe_type = default_wardrobe_type 
        else:
            try:
                wardrobe_type = re.search(
                    wardrobe_type_pattern, filename, re.I
                ).group(1)
                wardrobe_type = wardrobe_type_matchings[wardrobe_type]
            except AttributeError as e:
                ic()
                ic(e, filename, front_type)
                return
            except KeyError as e:
                ic()
                ic(e, filename, front_type)
                return
        ### Цвет корпуса
        case_clr = default_values.get("case_clr", None)
        if not case_clr:
            case_clr = search_property(
                obj,
                filename,
                case_color_pattern,
                color_matchings,
                err_dir
            )
        ### Цвет профиля                TODO: fix that
        if default_profile_clr:
            profile_clr = default_profile_clr
        else:
            profile_clr = re.search(
                profile_clr_pattern,
                filename,
                re.I
                ).group(1)
            
        filename = re.sub(f"{profile_clr}", "", filename)

        filename = re.sub(" +", " ", filename).strip()
        ### Тип фасада (1 секция, БМММБ и пр.)
        front_type = default_values.get("front_type", None)
        if not front_type:
            front_type = search_property(
                obj,
                filename,
                front_type_pattern,
                front_type_matchings,
                err_dir
            )

        ### Материалы фасада (ЛДСП, Зеркало, Волны, Матовое стекло и пр.)
        front_materials = default_values.get("front_materials", None)
        if not front_materials:
            front_materials = search_property(
                obj,
                filename,
                front_materials_pattern,
                front_materials_matchings,
                err_dir
            )
        ### Сохранение картинки с новым названием
        if all([series, wardrobe_type, front_type, case_clr, profile_clr]):
            new_filename = f"{series} {wardrobe_type} {front_type} "\
                f"({front_materials}) {case_clr} {profile_clr}{file_ext}"
            shutil.copy(obj, dest_dir/new_filename)
    return
    
    
if __name__ == "__main__":
    default_series = "Оптим"
    default_wardrobe_type = ""
    default_front_type = "1 секция"
    default_front_materials = ""
    default_case_clr = ""
    default_profile_clr = "Серебро профиль"

    default_values = {
        "series": default_series,
        "wardrobe_type": default_wardrobe_type,
        "front_type": default_front_type,
        "front_materials": default_front_materials,
        "case_clr": default_case_clr,
        "profile_clr": default_profile_clr
    }

    ic(default_values)

    DEST_DIR = "images/Картинки_стандарт_имена"
    ERROR_DIR = "images/Картинки_нераспозн_имена"

    src_dir = Path("images/Исходные_картинки")
    imgs_lst = []
    for obj in src_dir.rglob("*"):
        if obj.is_file() and obj.suffix in acceptable_exts:
            imgs_lst.append(obj)

    ic(imgs_lst)

    normalize_filename(
        imgs_lst,
        DEST_DIR,
        ERROR_DIR,
        **default_values,
    )