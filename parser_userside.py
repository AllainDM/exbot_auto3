from datetime import datetime

import requests
from bs4 import BeautifulSoup
import lxml


import config
import address_filter

import logging
# Настройка логирования
logging.basicConfig(level=logging.INFO)

logging.debug("Это отладочное сообщение")
logging.info("Это информационное сообщение")
logging.warning("Это предупреждение")
logging.error("Это ошибка")
logging.critical("Это критическая ошибка")

logger = logging.getLogger(__name__)


# session = requests.Session()

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

# session_users = requests.Session()
#
# req = session_users.get(url_login_get)
#
# csrf = None
#
# def get_token():
#     global csrf
#     soup = BeautifulSoup(req.content, 'html.parser')
#     # logger.debug(soup)
#     logger.debug("###################")
#     scripts = soup.find_all('script')
#
#     for script in scripts:
#         if script.string is not None:
#             # logger.debug(script.string)
#             script_lst = script.string.split(" ")
#             # logger.debug(script_lst)
#             for num, val in enumerate(script_lst):
#                 if val == "_csrf:":
#                     csrf = script_lst[num+1]
#     logger.debug(f"csrf {csrf}")
#
# get_token()
#
#
# def create_users_sessions():
#     while True:
#         try:
#             data_users["_csrf"] = csrf[1:-3]
#             # logger.debug(f"data_users {data_users}")
#             response_users2 = session_users.post(url_login, data=data_users, headers=HEADERS).text
#             # logger.debug("Сессия Юзера создана 2")
#             # logger.debug(f"response_users2 {response_users2}")
#             return response_users2
#         except ConnectionError:
#             logger.debug("Ошибка создания сессии")
#             # TODO функция отправки тут отсутствует
#             # send_telegram("Ошибка создания сессии UserSide, повтор запроса через 5 минут")
#             # time.sleep(300)
#
#
# response_users = create_users_sessions()

# Новый способ получения токена и авторизации.
def get_token(session_users):
    req = session_users.get(url_login_get)
    soup = BeautifulSoup(req.content, 'html.parser')
    # logger.debug(soup)
    # logger.debug("###################")
    scripts = soup.find_all('script')

    csrf = None
    for script in scripts:
        if script.string is not None:
            script_lst = script.string.split(" ")
            for num, val in enumerate(script_lst):
                if val == "_csrf:":
                    csrf = script_lst[num+1]
                    break
        if csrf:
            break
    logger.debug(f"csrf {csrf}")
    return csrf[1:-3] if csrf else None

def create_users_sessions():
    session_users = requests.Session()
    csrf = get_token(session_users)
    if not csrf:
        raise Exception("CSRF token not found")

    data_users["_csrf"] = csrf
    response_users2 = session_users.post(url_login, data=data_users, headers=HEADERS)
    if response_users2.status_code != 200:
        raise Exception("Failed to create user session")
    return session_users


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
    logger.info(link)

    # Новый способ получения токена и авторизации.
    session_users = create_users_sessions()

    # try:
    # Сразу подставим заголовок с токеном
    # HEADERS["_csrf"] = csrf[1:-3]

    # Новый способ получения токена и авторизации.
    HEADERS["_csrf"] = data_users["_csrf"]

    html = session_users.get(link, headers=HEADERS)
    answer = []
    brand = "ЕТ"
    if html.status_code == 200:
        # logger.debug("Код ответа 200")
        soup = BeautifulSoup(html.text, 'lxml')
        # logger.debug(f"soup {soup}")
        table = soup.find_all('tr', class_="cursor_pointer")
        logger.debug(f"Количество карточек: {len(table)}")

        # Доп поля: месяц(цифра) и метраж
        mnth = datetime.now().month
        logger.debug(f"mnth {mnth}")
        metr = 50  # Данных в выгрузке нет, берем среднее.


        for i in table:
            amd = i.find_all('td', class_="")
            # logger.debug(f"amd[1] {amd[1]}")
            # logger.debug(f"amd[1].text {amd[1].text}")
            # TODO добавить обработку IndexError для отсутсвующих значений
            try:
                logger.info(f"amd[1] {amd[1]}")
                logger.info(f"amd[1].text {amd[1].text}")
                # logger.debug(amd[1].text)  # Адрес. Необходимо пропустить через модуль редактирования.
                # logger.debug(amd[2].text)  # Мастер. Необходимо оставить только фамилию.
                # logger.debug(amd[0].text)  # Номер договора. Убрать пробелы и перенос строки(!).
                # logger.debug("############################")
                address = address_filter.calc_address(amd[1].text)
                # logger.debug(f"address {address}")

                # Выделим фамилию мастера
                soname = amd[2].text.split(" ")
                soname = soname[0]

                # ЛС. Убрать пробелы и перенос строки(!).
                ls = amd[0].text.split("\n")
                ls = ls[0]

                one = [brand, date, ls, address[1], address[2], address[3], soname, address[0], mnth, metr]
                answer.append(one)
            except IndexError:
                one = [brand, date, "я", "хз", "что", "тут", "за", "адрес", mnth, metr]
                answer.append(one)
            # break
    # Вернем в основную функцию, для обьединения отчетов разных брендов.
    return answer





















































