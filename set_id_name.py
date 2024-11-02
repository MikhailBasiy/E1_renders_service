import shutil
import os
import pandas as pd
import re

from icecream import ic


def process(outer_id_file: str = "table.xlsx") -> None:
        # unmatched_items: list[str] = []
        # source_dir_abspath = os.path.join(os.getcwd(), "renders")
        filenames_lst = os.listdir(source_dir_abspath)
        output_dir_abspath = os.path.join(os.getcwd(), "output")
        if not (os.path.exists(output_dir_abspath) and os.path.isdir):
                os.makedirs(output_dir_abspath, mode=0o777, exist_ok=False)
        table = pd.read_excel("table.xlsx")

        for tpl in table.itertuples():
                ### e.g. Прайм 2-х дверный (ЛДСП, Стекло хаки) окутанный (Белый снег 1200х2300х570 Прайм 2х Черный профиль)'
                rgx_pattern = re.compile(
                        "^(\w*) (\d-[хx ]{0,2}дверный) \(([\w\s,]*)\) [^\(]*\(([А-Яа-я ]*) [\w\s]* ([А-Яа-я]+ профиль)\)", ### redo: series via search([locker|||]), 
                        re.IGNORECASE
                )
                series, wardrobe_type, front_name, clr, profile_clr = re.search(
                        rgx_pattern,
                        tpl.Название
                ).groups()
                filename_pattern = f"{series} {wardrobe_type} ({front_name}) {clr} {profile_clr}"
                for filename in filenames_lst:
                        if filename_pattern in filename:
                                outer_code = tpl.Внешний_код
                                shutil.copy(os.path.join(source_dir_abspath, filename), os.path.join(output_dir_abspath, outer_code + ".jpg"))


