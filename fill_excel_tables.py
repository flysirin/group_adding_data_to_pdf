# pip install pandas
# pip install Faker
# pip install openpyxl   <- If it complains about the absence of this library
# pip install reportlab
# pip install PyPDF2
# pip install tqdm==4.66.1

import pandas as pd
from faker import Faker
from random import randint
from pathlib import Path
from add_text_to_pdf import GenerateFromTemplate
from multiprocessing import Pool
from time import time
from tqdm import tqdm


excel_file_11k: str = 'C:/path_to exel/.../file.xlsx'
_pdf_folder: str = 'C:/../Path_to_folder'


# Create DataFrame (table)
def crate_fake_tabel(count: int = 1000, table_name: str = 'table_name') -> None:
    faker = Faker('ru_RU')
    data = {'Name': [faker.name() for _ in range(count)],
            'Age': [randint(25, 70) for _ in range(count)],
            'City': [faker.city() for _ in range(count)],
            'Phone': [faker.phone_number() for _ in range(count)]}
    df = pd.DataFrame(data)
    excel_file = f'{table_name}.xlsx'
    df.to_excel(excel_file, index=False)


def add_pdf_ticket_to_user(excel_file_path: str, pdf_folder_path: str) -> list:
    df = pd.read_excel(excel_file_path)
    pdf_folder = Path(pdf_folder_path)
    next_pdf_file = iter(pdf_folder.glob(pattern='*.pdf'))

    pdf_user_data: list = []
    for index, row in df.iterrows():
        if row['Phone']:
            pdf_file_path = next(next_pdf_file)
            user_name = row['Name']
            phone = row['Phone']
            text = user_name + "\n" + phone
            df.at[index, 'pdf ticket'] = pdf_file_path.name
            pdf_user_data.append((str(pdf_file_path), text))
    df.to_excel('excel_test.xlsx', index=False)
    return pdf_user_data


def add_name_phone_into_pdf_file(args: tuple[str, str]) -> None:
    pdf_file_path, text = args
    pdf_add_name_phone = GenerateFromTemplate(str(pdf_file_path))
    pdf_add_name_phone.add_text(text=text, point=(49, 800))
    pdf_add_name_phone.merge()
    pdf_add_name_phone.generate(str(pdf_file_path))


# crate_fake_tabel(count=11000, table_name='example_name')


if __name__ == '__main__':
    start_time = time()
    user_data: list[tuple[str, str]] = add_pdf_ticket_to_user(excel_file_path=excel_file_11k,
                                                              pdf_folder_path=_pdf_folder)
    pool = Pool(processes=9)
    for _ in tqdm(pool.imap_unordered(func=add_name_phone_into_pdf_file,
                                      iterable=user_data), total=len(user_data)):
        pass
    pool.close()
    pool.join()
    delta_time = time() - start_time
    print(delta_time)

# 11 000 files - 9 processes, 430.568 sec startmap()
# 11 000 files - 9 processes, 419.553 sec imap_unordered()
