from pprint import pprint

import requests
from bs4 import BeautifulSoup
import lxml

import json
import config
import address_filter
import to_exel

session = requests.Session()

url_login_get = "https://us.gblnet.net/"
url_login = "https://us.gblnet.net/body/login"

HEADERS = {
    "main": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"
}

data_users = {
    "_csrf": '',
    "return_page": "",
    "username": config.loginUS,
    "password": config.pswUS
}
# Создание сессии, получение токена и авторизация

session_users = requests.Session()

req = session_users.get(url_login_get)

soup = BeautifulSoup(req.content, 'html.parser')
scripts = soup.find_all('script')
csrf_token = None
for script in scripts:
    if script.string is not None:
        script_lst = script.string.split(" ")
        for num, val in enumerate(script_lst):
            if val == "_csrf:":
                csrf = script_lst[num + 1]
                csrf_token = csrf[1:-3]


def create_users_sessions():
    while True:
        try:
            data_users["_csrf"] = csrf_token
            # print(f"data_users {data_users}")
            response_users2 = session_users.post(url_login, data=data_users, headers=HEADERS).text
            # print("Сессия Юзера создана 2")
            # print(f"response_users2 {response_users2}")
            return response_users2
        except ConnectionError:
            print("Ошибка создания сессии")
            # TODO функция отправки тут отсутствует
            # send_telegram("Ошибка создания сессии UserSide, повтор запроса через 5 минут")
            # time.sleep(300)


response_users = create_users_sessions()


def get_html(date):
    url_task = "https://us.gblnet.net/task/"
    link = (f"https://us.gblnet.net/oper/?core_section=customer_list&filter_selector0=billing&"
            f"billing0_value=1&filter_selector1=agreement_date&agreement_date1_value={date}&"
            f"filter_selector2=customer_type&customer_type2_value=1&filter_selector3=tariff&"
            f"tariff3_value2=2&tariff3_value=-501&filter_selector4=tariff&tariff4_value2=2&"
            f"tariff4_value=-500&filter_selector5=tariff&tariff5_value2=2&tariff5_value=1083&"
            f"filter_selector6=customer_mark&customer_mark6_value=66&filter_selector7=tariff&"
            f"tariff7_value2=2&tariff7_value=1088&filter_selector8=tariff&tariff8_value2=2&"
            f"tariff8_value=5788&filter_selector9=tariff&tariff9_value2=2&tariff9_value=12676&"
            f"filter_group_by=")

    # try:
    # Сразу подставим заголовок с токеном
    HEADERS["_csrf"] = csrf_token
    html = session_users.get(link, headers=HEADERS)
    answer = []
    brand = "ЕТ"
    if html.status_code == 200:
        # print("Код ответа 200")
        soup = BeautifulSoup(html.text, 'lxml')
        # print(f"soup {soup}")
        table = soup.find_all('tr', class_="cursor_pointer")
        print(f"Количество карточек: {len(table)}")
        for i in table:
            amd = i.find_all('td', class_="")
            # TODO добавить обработку IndexError для отсутсвующих значений

            # print(amd[1].text)  # Адрес. Необходимо пропустить через модуль редактирования.
            # print(amd[2].text)  # Мастер. Необходимо оставить только фамилию.
            # print(amd[3].text)  # Номер договора. Для ЕТ без изменений.
            print("############################")
            address = address_filter.calc_address(amd[1].text)
            print(f"address {address}")

            # Выделим фамилию мастера
            soname = amd[2].text.split(" ")
            soname = soname[0]

            one = [brand, date, amd[3].text, address[1], address[2], address[3], soname, address[0]]
            answer.append(one)
            # break
    # Передадим для записи в файл
    # Аргументы: 1 - дата для сохранения файла. 2 - список заявок.
    to_exel.save_to_exel(date, answer)

    # except:
    #     print("Ошибка в целом блоке функции get_html")
    #     return False




















































