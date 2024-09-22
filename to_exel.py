import xlwt

import filter
import count_list

# Вместо использования сторонних библиотек возьем по простому из списка.
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

# Составим словарь для записи домов для счетчика.
count_dict = {i: 0 for i in count_list.count_lst}
print(f"count_dict {count_dict}")


def save_to_exel(table, date, to="AllTO"):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(f"Подключения")
    n = 2  # Стартовый номер строки для екселя

    for i in table:
        # print(f"i {i}")
        # Проверим совпадение по районам для ТО.
        if to == "TONorth":
            if i[7] not in filter.district_north:
                continue

        elif to == "TOSouth":
            if i[7] not in filter.district_south:
                continue
            if i[7] == "Московский":
                if i[3] in filter.west_in_moscow:
                    continue
            if i[7] == "Кировский":
                if i[3] in filter.west_in_kirov:
                    continue
            if i[7] == "Фрунзенский":
                if i[3] in filter.west_in_frunze:
                    continue

        elif to == "TOWest":
            if i[7] not in filter.district_west:
                continue
            if i[7] == "Московский":
                if i[3] not in filter.west_in_moscow:
                    continue
            if i[7] == "Кировский":
                if i[3] not in filter.west_in_kirov:
                    continue
            if i[7] == "Фрунзенский":
                if i[3] not in filter.west_in_frunze:
                    continue

        elif to == "TOEast":
            if i[7] not in filter.district_east:
                continue

        elif to == "AllTO":
            srch = f"{i[3]} {i[4]}"
            # print(f"srch {srch}")
            if srch in count_list.count_lst:
                count_dict[srch] += 1
                print(f"Найдено совпадения для счетчика домов: {srch}")

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

    wb.save(f'{to}/{to}_{date}.xls')

    if to == "AllTO":
        print(count_dict)
        return count_dict