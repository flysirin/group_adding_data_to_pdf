from pathlib import Path
import shutil
from string import ascii_lowercase, digits
from random import randint


SYMBOLS: str = ascii_lowercase + digits
LEN_SYMBOLS = len(SYMBOLS)


def create_filenames(count_files: int, len_words: int = 8) -> set:
    set_filenames: set = set()
    for i in range(count_files):
        file_name: str = ''.join([SYMBOLS[randint(0, LEN_SYMBOLS - 1)] for _ in range(len_words)])
        set_filenames.add(file_name)
    while len(set_filenames) != count_files:
        file_name: str = ''.join([SYMBOLS[randint(0, LEN_SYMBOLS - 1)] for _ in range(len_words)])
        set_filenames.add(file_name)
    return set_filenames


def rename_files(path_folder: str) -> None:
    folder_path = Path(path_folder)

    count_files = len(list(folder_path.glob(f"*.pdf")))
    set_filenames = create_filenames(count_files, len_words=8)
    for file in folder_path.glob(pattern="*.pdf"):
        file_name = set_filenames.pop()
        try:
            file.rename(target=f"{path_folder}/{file_name}.pdf")
        except BaseException as e:
            print(f"{e}")


def create_duplicate_files(file_path: str, destination_path: str, count_copy: int) -> None:
    set_filenames = create_filenames(count_copy, len_words=8)
    for file_name in set_filenames:
        shutil.copy(file_path, dst=f"{destination_path}/{file_name}.pdf")


cur_path = "C:/path_to folder/file.pdf"
source_file_path = "C:/.../file.pdf"


# create_duplicate_files(source_file_path, cur_path, 11000)

# rename_files(cur_path)

