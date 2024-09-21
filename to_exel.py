
import xlwt

import filter

# Вместо использования сторонних библиотек возьем по простому из списка.
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]


def save_to_exel(table, date, to="no"):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(f"Подключения")
    n = 2  # Стартовый номер строки для екселя

    for i in table:
        print(f"i {i}")
        # Проверим совпадение по районам для ТО.
        # if to == "TONorth":
        #     if i[7] in filter.district_north:
        #         ...
        try:
            ws.write(n, 0, i[0])  # Бренд
            ws.write(n, 1, i[1])  # Дата
            ws.write(n, 2, i[2])  # Номер договора
            ws.write(n, 3, i[3])  # Улица
            ws.write(n, 4, i[4])  # Дом
            ws.write(n, 5, i[5])  # Квартира
            ws.write(n, 6, i[6])  # Мастер
            ws.write(n, 7, i[7])  # Район
            ws.write(n, 11, months[i[8]-1])  # Месяц
            try:
                ws.write(n, 12, i[9])  # Метраж
            except IndexError:
                ws.write(n, 12, 45)  # Метраж
        except IndexError:
            ws.write(n, 0, "Ошибка с получением данных.")  # Ошибка

        n += 1

    wb.save(f'AllTO/{date}.xls')