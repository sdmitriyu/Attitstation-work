import os
import csv
import html


class PriceMachine():

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path=''):
        for filename in os.listdir(file_path):
            if 'price' in filename and filename.endswith('.csv'):
                file_path_full = os.path.join(file_path, filename)
                try:
                    with open(file_path_full, newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile, delimiter=',')
                        headers = reader.fieldnames

                        if headers:
                            # Выводим заголовки для отладки
                            print(f"Заголовки в файле {filename}: {headers}")

                            product_col = self._search_column(headers, ['товар', 'название', 'наименование', 'продукт'])
                            price_col = self._search_column(headers, ['цена', 'розница'])
                            weight_col = self._search_column(headers, ['фасовка', 'масса', 'вес'])

                            if product_col and price_col and weight_col:
                                for row in reader:
                                    product = row.get(product_col)
                                    price = row.get(price_col)
                                    weight = row.get(weight_col)
                                    if product and price and weight:
                                        try:
                                            price = float(price)
                                            weight = float(weight)
                                            price_per_kg = price / weight if weight > 0 else 0
                                            self.data.append({
                                                'название': product,
                                                'цена': price,
                                                'вес': weight,
                                                'файл': filename,
                                                'цена за кг.': price_per_kg
                                            })
                                            if len(product) > self.name_length:
                                                self.name_length = len(product)
                                        except ValueError as e:
                                            print(f"Ошибка преобразования данных в файле {filename}: {e}")
                            else:
                                print(f"Не найдены необходимые столбцы в файле {filename}")
                        else:
                            print(f"Файл {filename} не содержит заголовков")

                except FileNotFoundError as e:
                    print(f"Файл не найден: {e}")
                except Exception as e:
                    print(f"Произошла ошибка при обработке файла {filename}: {e}")

    def _search_column(self, headers, key_phrases):
        """
        Ищет столбец в headers, который соответствует одному из ключевых слов в key_phrases.
        Возвращает название столбца или None, если не найдено.
        """
        key_phrases_lower = [phrase.lower() for phrase in key_phrases]
        return next((col for col in headers if col.lower() in key_phrases_lower), None)

    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Позиции продуктов</title>
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                table, th, td {{
                    border: 1px solid black;

                        }}
                        th, td {{
                            padding: 8px;
                            text-align: left;
                        }}
                        th {{
                            background-color: #f2f2f2;
                        }}
                </style>
            </head>
            <body>
                <table>
                    <tr>
                        <th>Номер</th>
                        <th>Название</th>
                        <th>Цена</th>
                        <th>Фасовка</th>
                        <th>Файл</th>
                        <th>Цена за кг.</th>
                    </tr>
                '''
        for index, item in enumerate(self.data, start=1):
            result += f'''
                        <tr>
                            <td>{index}</td>
                            <td>{html.escape(item['название'])}</td>
                            <td>{item['цена']}</td>
                            <td>{item['вес']}</td>
                            <td>{html.escape(item['файл'])}</td>
                            <td>{item['цена за кг.']:.2f}</td>
                        </tr>
                    '''
        result += '''
                    </table>
                </body>
                </html>
                '''
        with open(fname, 'w', encoding='utf-8') as file:
            file.write(result)

    def find_text(self, text):
        results = [item for item in self.data if text.lower() in item['название'].lower()]
        results_sorted = sorted(results, key=lambda x: x['цена за кг.'])
        print(
            f"{'№':<5} {'Наименование':<{self.name_length + 2}} {'цена':<8} {'вес':<5} {'файл':<15} {'цена за кг.':<10}")
        for i, item in enumerate(results_sorted, 1):
            print(
                f"{i:<5} {item['название']:<{self.name_length + 2}} {item['цена']:<8} {item['вес']:<5} {item['файл']:<15} {item['цена за кг.']:<10.2f}")

if __name__ == "__main__":
    pm = PriceMachine()
    pm.load_prices(r'C:\PyCharmProject\Attitstation work\price_files_folder')

    while True:
        try:
            user_input = input("Введите текст для поиска (или 'exit' для выхода): ").strip()
            if user_input.lower() == 'exit':
                print("Работа завершена.")
                break
            pm.find_text(user_input)
        except KeyboardInterrupt:
            print('Программа завершила свою работу.')

    pm.export_to_html('output.html')
    print('Данные экспортированы в output.html')
