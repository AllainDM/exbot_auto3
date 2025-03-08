import imaplib
import email
import time
import os

import xlrd3

import config
import for_api
import address_filter
import filter

# Настройка imaplib
mail_pass = config.password
username = config.address
imap_server = "imap.mail.ru"
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, mail_pass)

# imap.select("INBOX")
imap.select('user')
# p = imap.search(None, 'ALL')
# r = imap.uid('search', "UNSEEN", "ALL")
time.sleep(1)
typ, data = imap.uid('search', "UNSEEN", "ALL")


def start_module():
    global imap
    global typ
    global data
    # Настройка imaplib
    # mail_pass = config.password
    # username = config.address
    # imap_server = "imap.mail.ru"
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, mail_pass)

    # imap.select("INBOX")
    imap.select('user')
    # p = imap.search(None, 'ALL')
    # r = imap.uid('search', "UNSEEN", "ALL")
    time.sleep(1)
    typ, data = imap.uid('search', "UNSEEN", "ALL")
    time.sleep(2)

start_module()


# Проверим почту и сохраним файлы в папку для дальнейшей обработки.
def check_mail():
    n = 1  # Дополнение к названию файла, т.к. приходят с одинаковым названием с разных брендов.
    for num in data[0].split():
        time.sleep(1)
        res, msg = imap.uid('fetch', num, '(RFC822)')
        mail = email.message_from_bytes(msg[0][1])

        # Является ли письмо многокомпонентным (multipart)
        if mail.is_multipart():
            time.sleep(1)
            for part in mail.walk():
                # content_type = part.get_content_type()
                filename = part.get_filename()
                # Найдем файлы с названием(строка)
                # if type(filename) == str and filename[16] == 'c':  # Первый вариант для userside
                if type(filename) == str:
                    print(filename)
                    print(type(filename))
                    # list_filenames.append(filename)
                    # Создадим папку для месяца если ее не существует.
                    if not os.path.exists(f"files_mail/{filename[:7]}"):
                        os.makedirs(f"files_mail/{filename[:7]}")
                    with open(f'files_mail/{filename[:7]}/{filename[:-5]}{n}.xlsx', 'wb') as new_file:
                        new_file.write(part.get_payload(decode=True))
                    n += 1

def start(date):
    # Преобразуем дату формата "14.09.2024" к названию папки формата "2024-09"
    print(date)
    date_lst = date.split(".")
    print(date_lst)
    year_month = f"{date_lst[2]}-{date_lst[1]}"
    print(year_month)
    # И для формата с днем, для поиска файла.
    year_month_day = f"{date_lst[2]}-{date_lst[1]}-{date_lst[0]}"
    answer = []

    if os.path.exists(f'files_mail/{year_month}'):
        files = os.listdir(f'files_mail/{year_month}')
        print(f"Папка найдена: {year_month}")
        print(f"files {files}")
        # Переберем весь список файлов для нахождения совпадения в названии.
        for i in files:
            if i[:16] == f"{year_month_day}-new_c":
                wb = xlrd3.open_workbook(f'files_mail/{year_month}/{i}')
                sheet = wb.sheet_by_index(0)
                # Старт со второй строчки
                for row in range(1, sheet.nrows):
                    list_one = []

                    # 1 Бренд, получим с помощью API
                    try: list_one.append(for_api.search_brand(int(sheet.cell_value(row, 6))))
                    except ValueError: list_one.append(" ")

                    # 2 Дата
                    list_one.append(date)  # В файле дата в неподходящем формате + там время.

                    # 3 Лицевой счет
                    try: list_one.append(int(sheet.cell_value(row, 6)))
                    except ValueError: list_one.append(sheet.cell_value(row, 6))

                    # 4 Улица
                    street = address_filter.cut_street(sheet.cell_value(row, 3))
                    list_one.append(street)

                    # 5 Дом
                    try: list_one.append(int(sheet.cell_value(row, 4)))
                    except ValueError: list_one.append(sheet.cell_value(row, 4))

                    # 6 Квартира
                    try: list_one.append(int(sheet.cell_value(row, 5)))
                    except ValueError: list_one.append(sheet.cell_value(row, 5))

                    # 7 Мастер
                    master = sheet.cell_value(row, 8)
                    # Фильтр фамилий мастеров подрядчиков.
                    try:
                        if master.lower() in filter.filter_master_no_to:
                            continue
                        else:
                            master = master.split(" ")
                            master = master[0]
                            list_one.append(master)  # Возьмем только фамилию
                    except AttributeError:
                        # ...
                        master = "Неизвестно"

                    # 8 Район
                    list_one.append(sheet.cell_value(row, 2))

                    # 9 Месяц
                    list_one.append(int(date_lst[1]))

                    # 10 Метраж
                    try: list_one.append(int(sheet.cell_value(row, 9)))
                    except ValueError: list_one.append(0)

                    answer.append(list_one)
                print(f"answer {answer}")
                return answer
    print(f"Папка НЕ найдена: {year_month}")
    return answer

