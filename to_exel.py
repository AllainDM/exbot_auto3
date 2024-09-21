import xlwt


def save_to_exel(date, table):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(f"Подключения")
    n = 2  # Стартовый номер строки для екселя
    for i in table:
        ws.write(n, 0, i[0])  # Бренд
        ws.write(n, 1, i[1])  # Дата
        ws.write(n, 2, i[2])  # Номер договора
        ws.write(n, 3, i[3])  # Улица
        ws.write(n, 4, i[4])  # Дом
        ws.write(n, 5, i[5])  # Квартира
        ws.write(n, 6, i[6])  # Мастер
        ws.write(n, 7, i[7])  # Район
        # ws.write(n, 10, i[8])  # Метраж
        n += 1

    wb.save(f'AllTO/{date}.xls')