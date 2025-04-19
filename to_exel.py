import xlwt

import filter
import count_list

import logging
# Настройка логирования
logging.basicConfig(level=logging.INFO)

logging.debug("Это отладочное сообщение")
logging.info("Это информационное сообщение")
logging.warning("Это предупреждение")
logging.error("Это ошибка")
logging.critical("Это критическая ошибка")

logger = logging.getLogger(__name__)

# Вместо использования сторонних библиотек просто возьем из списка.
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]


def save_to_exel(table, date, to="AllTO"):
    # Составим словарь для записи домов для счетчика.
    # Больше неактуально. == Запускаю по просьбе Игоря
    count_dict = {i: 0 for i in count_list.count_lst}
    logger.debug(f"count_dict {count_dict}")

    wb = xlwt.Workbook()
    ws = wb.add_sheet(f"Подключения")
    n = 2  # Стартовый номер строки для екселя

    for i in table:
        # logger.debug(f"i {i}")
        # Проверим совпадение по районам для ТО.
        if to == "TONorth":
            if i[7] not in filter.district_north:
                continue
            if i[7] == "Красногвардейский":
                if i[3] not in filter.north_in_redarmy:
                    continue
            if i[7] == "Всеволожский":
                if i[3] in filter.east_in_vsevol:
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
            if i[7] == "Красногвардейский":
                if i[3] in filter.north_in_redarmy:
                    continue
            if i[7] == "Всеволожский":
                if i[3] not in filter.east_in_vsevol:
                    continue

        elif to == "AllTO":
            srch = f"{i[3]} {i[4]}"
            logger.debug(f"srch {srch}")
            if srch in count_list.count_lst:
                count_dict[srch] += 1
                logger.debug(f"Найдено совпадения для счетчика домов: {srch}")

        try:
            ws.write(n, 0, i[0])  # Бренд
            ws.write(n, 1, i[1])  # Дата
            ws.write(n, 2, i[2])  # Номер договора
            ws.write(n, 3, i[3])  # Улица
            ws.write(n, 4, i[4])  # Дом
            ws.write(n, 5, i[5])  # Квартира
            ws.write(n, 6, i[6])  # Мастер
            ws.write(n, 7, i[7])  # Район
            # ws.write(n, 11, months[i[8]-1])  # Месяц
            try:
                ws.write(n, 12, i[9])  # Метраж
            except IndexError:
                ws.write(n, 12, 45)  # Метраж
        except IndexError:
            ws.write(n, 0, "Ошибка с получением данных.")  # Ошибка

        n += 1

    wb.save(f'{to}/{to}_{date}.xls')

    if to == "AllTO":
        logger.debug(count_dict)
        return count_dict