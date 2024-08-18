import os
import csv


class PriceMachine:

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
                        reader = csv.DictReader(csvfile, delimiter=';')
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

        # Пример использования

        price_machine = PriceMachine()
        price_machine.load_prices(file_path='C:/PyCharmProject/Attitstation work')  # Замените на ваш путь