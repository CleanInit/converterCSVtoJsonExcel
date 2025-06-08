import pandas as pd
import os
import logging
import json

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="converter.log",
                    filemode="a",
                    )

logs = logging.getLogger(__name__)

def _path_currently_csv():
    path_currently_csv = input("Путь/Название файла формата *.csv (example.csv): ")
    if path_currently_csv.startswith("~"):
        path_currently_csv = os.path.abspath(os.path.expanduser(path_currently_csv))

    if os.path.exists(path_currently_csv) and path_currently_csv.endswith(".csv"):
        logs.debug(f"Путь к *.csv файлу: {path_currently_csv}")
        return path_currently_csv
    logs.error(f"Файл не найден или расширение не .csv, путь: {path_currently_csv}")
    exit(1)

def _convert_csv_to_xlsx(path_csv: str):
    df = pd.read_csv(path_csv)
    base_name = os.path.splitext(os.path.basename(path_csv))[0]
    _path_output_excel = os.path.join("outputs", f"{base_name}.xlsx")
    df.to_excel(_path_output_excel, index=False, sheet_name=base_name) # Так-как мы не можем достать название листа в .csv, то делаем имя листа ввиде названия файлаю.
    logs.info(f"Файл конвентирован по пути: {_path_output_excel}")
    return _path_output_excel

def _convert_xlsx_to_json(path_excel: str):

    all_data = {}

    xlsx = pd.ExcelFile(path_excel)
    sheet_names = xlsx.sheet_names
    for sheet in sheet_names:
        df = pd.read_excel(path_excel, sheet_name=sheet)
        sheet_data = {}
        for col in df.columns:
            col_data = df[col].dropna().tolist()
            logs.debug(f'Колонка "{col}" содержит {len(col_data)} непустых значений')
            sheet_data[col] = col_data
        all_data[sheet] = sheet_data
        logs.info(f'Лист "{sheet}" обработан')

    base_name = os.path.splitext(os.path.basename(path_excel))[0]
    path_currently_json = os.path.join("outputs",f"{base_name}.json")

    with open(path_currently_json, 'w+') as file:
        json.dump(all_data, file, indent=4)

def main():
    path_csv = _path_currently_csv()
    os.makedirs("outputs", exist_ok=True)
    path_excel = _convert_csv_to_xlsx(path_csv=path_csv)
    _convert_xlsx_to_json(path_excel=path_excel)

if __name__ == "__main__":
    main()
