import shutil
import os
import pathlib
import pandas as pd
import re

from functions import get_dir_ready

from icecream import ic        


def parse_item_names(items_filename: str) -> pd.DataFrame:


    def parse_name(item_name: str) -> tuple[str]:
        pattern = "^([А-Яа-я\s]+) ((?:2х |2-|2-х |3х |3-х |3-)дверный) \(([\w\s,/]+)\)"
        try:
            series, wardrobe_type, front_type = re.search(pattern, item_name).groups()
        except AttributeError as e:
            ic(e, item_name)
        else:
            return series, wardrobe_type, front_type  
        
             
    items_ids = pd.read_excel(items_filename)
    items_ids.rename(columns={
        "Внешний код": "Внешний_код",
        "Цвет корпуса": "Цвет_корпуса",
        "Цвет профиля": "Цвет_профиля"
        },
        inplace=True
    )
    items_ids["Серия"], items_ids["Тип_шкафа"], items_ids["Тип_фасада"] = \
        zip(*items_ids["Название"].apply(parse_name))
    return items_ids


def parse_img_names(src_dir: pathlib.Path) -> pd.DataFrame:
    parsed_data: list[str] = []
    for object in src_dir.rglob("*"):
        if object.is_file() and object.suffix in (".jpg", ".jpeg", ".webp"):
            pattern = "^(Локер|Оптим|Широкий Прайм|Прайм|Экспресс|Эста) " \
                      "(\d-х дверный) \(([\w\s,]*)\) ([\w\s ]+) " \
                      "([А-Яа-я]+ профиль)$"
            series, wardrobe_type, front_type, case_clr, profile_clr = (
                re.search(pattern, object.stem, re.I)
            ).groups()
            parsed_data.append(
                [series, wardrobe_type, front_type, case_clr, profile_clr, object.stem, object.suffix]
            )
    result = pd.DataFrame(
        parsed_data,
        columns=[
            "Серия",
            "Тип_шкафа",
            "Тип_фасада",
            "Цвет_корпуса",
            "Цвет_профиля",
            "Название_рендера",
            "Расширение"],
    )
    return result


def rename(
        products_ids_filename: str,
        src_path: str,
        dest_path: str,
        err_path: str
) -> None:
    
    src_dir = pathlib.Path(src_path)
    dest_dir = get_dir_ready(dest_path)
    err_dir = get_dir_ready(err_path)

    parsed_img_names: pd.DataFrame = parse_img_names(src_dir)
    parsed_product_names: pd.DataFrame = parse_item_names(products_ids_filename)

    merged_df = parsed_product_names.merge(
        parsed_img_names,
        how="left",
        on=["Серия", "Тип_шкафа", "Тип_фасада", "Цвет_корпуса", "Цвет_профиля"]
    )

    for row in merged_df.dropna(how="any").itertuples():
        filename = row.Название_рендера + row.Расширение
        new_filename = row.Внешний_код + row.Расширение
        shutil.copy(src_dir/filename, dest_dir/new_filename)

    ### TODO: add check for unrenamed files.


if __name__ == "__main__":
    SOURCE_DIR = "checked_files"
    DEST_DIR = "processed_files"
    ERROR_DIR = "unprocessed_files"

    filename = "outer_ids.xlsx"

    rename(
        products_ids_filename = filename,
        src_path = SOURCE_DIR,
        dest_path = DEST_DIR,
        err_path = ERROR_DIR
    )


