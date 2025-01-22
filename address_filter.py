import re

# Списки поселений и районов, для обработки исключений

list_villages = ["Парголово", "Шушары", "Новое Девяткино дер.", "пос. Шушары",
                 "Кудрово", "Мурино", "Бугры пос.", "Репино", "Сестрорецк",
                 "Янино-1", "Песочный", "Лисий", "Горелово", "Коммунар",
                 "Колпино", "Горская", "Понтонный", "Тельмана пос.",
                 "пос. Стрельна", "Новогорелово", "Пушкин", "Ломоносов"]

list_district = ["Колпинский р-н", "Ломоносовский р-н", "Всеволожский р-н"]

def calc_address(adrs):
    """
    Функция разделения адреса, на район, улицу, номер дома, номер квартиры.
    1. Делим полученную строку с адресом на список.
    2. Выделяем район.
    3. Выделяем улицу.
    """
    # new_address = []


    # 1. Делим полученную строку с адресом на список.
    # Разделим по "," для получения списка.
    address = adrs.split(",")


    # 2. Выделяем район.
    # Выделим район, убрав "р-н".
    # Исключения для области.
    # if district == "Кол":
    #     district = "Колпино"
    # elif district == "Пу":
    #     district = "Пушкин"
    # elif district == "Ломон":
    #     district = "Ломоносов"
    #


    # 3. Выделяем улицу.
    # Улица должна быть четвертым[3] элементом.
    # Но на этом месте может быть название поселка, поэтому ищев в исключениях.
    address_street = address[3].strip()

    if address_street in list_villages:
        street = address[4]
        district = address[2][1:-4].strip()
    elif address_street in list_district:
        street = address[4]
        district = address[3].strip()
    else:
        street = address[3]
        district = address[2][1:-4].strip()

    # # Отдельно для Кудрово у ЕТ пропишем район как Кудрово
    if address[3] == " Кудрово":
        district = "Кудрово"

    # Исключения для области.
    if district == "Кол":
        district = "Колпино"
    elif district == "Пу":
        district = "Пушкин"
    elif district == "Ломон":
        district = "Ломоносов"

    # Дальше отфильтруем улицу на лишние слова общим фильтром
    # street = street.strip()
    street = cut_street(street)

    # Ищем номер дома, при двойном адресе берем номер дома перед "вторым" адресом
    # Для счетчика при поиске домов с двойным адресом(там 2 раза упоминается страна).
    russia = adrs.replace(",", " ")
    russia = russia.split(" ")
    russia_count = russia.count("Россия")
    # print(f"russia_count {russia_count}")

    address_dom = ""
    if russia_count > 1:
        count_r = 0
        for num, el in enumerate(russia):
            # print(f"el: {el}")
            if el == "Россия" and count_r == 1:
                # print(f"Найдено второе совпадение, номер элемента: {num}")
                address_dom = russia[num - 2]
                break
            elif el == "Россия":
                count_r += 1
    else:
        address_dom = address[-1].split()
        # print(f"address_dom {address_dom}")
        address_dom = address_dom[0]
        # print(f"address_dom {address_dom}")

    # Отдельно надо разделить номер дома и квартиру
    if address_dom[-1].isdigit():
        address_dom = address_dom.replace("/", "к")
    else:
        address_dom = address_dom.replace("/", "")

    # Появилась подпись sms, она идет как -1
    # Под -2 идет телефон впритык с квартирой, наподобие 562+79516572283
    # address_kv = address_kv.split("+")
    # address_kv = address_kv[0]

    # Вариант через регулярки. Недоработан.
    # address_str = " ".join(address)
    # pattern_kv = r'кв\.?\s*(\d+)'
    # address_kv = re.search(pattern_kv, address_str)

    # address_kv = address[-1].split()
    address_kv = address[-1].replace("+", " + ")
    print(f"address_kv1 {address_kv}")
    address_kv = " ".join(address_kv.split())
    print(f"address_kv2 {address_kv}")
    address_kv = address_kv.split(" ")
    print(f"address_kv3 {address_kv}")
    # Квартиру брали с обратной стороны
    # try:
    #     address_kv = address_kv[-4]
    #     print(f"address_kv4 {address_kv}")
    # except IndexError:
    #     address_kv = address_kv[-1]
    #     print(f"address_kv5 {address_kv}")
    # Теперь считаем от начала
    address_kv = address_kv[2]
    print(f"address_kv4 {address_kv}")


    return [district, street.strip(), address_dom, address_kv]


# Убираем лишнее из улицы.
def cut_street(street):
    split_address = street.split(" ")
    lists = ["остров", "коса", "наб.", "пр.", "ул.", "б-р", "пр-д", "ш.", "пер.", "о-в"]
    # new_street = ""
    if split_address[-1] in lists:
        # В случае нахождения исключения берем все кроме последнего элемента.
        new_street = split_address[0:-1]
        new_street = " ".join(new_street)
        # new_street = split_address[0]
    elif street == "Набережная Фонтанки":
        new_street = "Фонтанки"
    elif street == "Воронцовский бульвар":
        new_street = "Воронцовский"
    elif street == "Воскресенская (Робеспьера)":
        new_street = "Воскресенская"

    else:
        new_street = street

    return new_street