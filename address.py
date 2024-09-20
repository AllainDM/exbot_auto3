
def address(adrs):
    # new_address = []

    # Разделим по "," для получения списка.
    new_address = adrs.split(",")

    # Выделим район, убрав "р-н".
    district = new_address[2][1:-4].strip()
    # Исключения для области.
    if district == "Кол":
        district = "Колпино"
    elif district == "Пу":
        district = "Пушкин"
    elif district == "Ломон":
        district = "Ломоносов"

    # Разберем улицу, для определения поселков.
    if new_address[3] == " Парголово" or \
            new_address[3] == " Шушары" or \
            new_address[3] == " Новое Девяткино дер." or \
            new_address[3] == " пос. Шушары" or \
            new_address[3] == " Кудрово" or \
            new_address[3] == " Мурино" or \
            new_address[3] == " Бугры пос." or \
            new_address[3] == " Репино" or \
            new_address[3] == " Сестрорецк" or \
            new_address[3] == " Янино-1" or \
            new_address[3] == " Янин" or \
            new_address[3] == " Песочный" or \
            new_address[3] == " Лисий" or \
            new_address[3] == " Горелово" or \
            new_address[3] == " Коммунар" or \
            new_address[3] == " Колпино" or \
            new_address[3] == " Горская" or \
            new_address[3] == " Понтонный" or \
            new_address[3] == " Тельмана" or \
            new_address[3] == " Тельмана пос." or \
            new_address[3] == " Стрельна" or \
            new_address[3] == " пос. Стрельна" or \
            new_address[3] == " Новогорелово" or \
            new_address[3] == " Новогорелово " or \
            new_address[3] == " Новогорелово пос.":
        street = new_address[4][1:-4]
        if new_address[4][-2] == 'ш':
            street = new_address[4][1:-3]
    else:
        # Обычно в конце строки "ул." или "б-р", тоесть 3 символа, но есть варианты с "ш."
        street = new_address[3][1:-4]
        if new_address[3][-2] == 'ш':
            street = new_address[3][1:-3]

    # Отдельно для Кудрово у ЕТ пропишем район как Кудрово
    if new_address[3] == " Кудрово":
        district = "Кудрово"

    # Дальше отфильтруем улицу на лишние слова общим фильтром
    street = street.strip()
    street = cut_street(street)

    # Ищем номер дома, при двойном адресе берем номер дома перед "вторым" адресом
    # Для счетчика при поиске домов с двойным адресом(там 2 раза упоминается страна).
    russia = adrs.replace(",", " ")
    russia = russia.split(" ")
    russia_count = russia.count("Россия")
    # print(f"russia_count {russia_count}")


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
        address_dom = new_address[-1].split()
        # print(f"address_dom {address_dom}")
        address_dom = address_dom[0]
        # print(f"address_dom {address_dom}")

    return [street]


# Убираем лишнее из улицы.
def cut_street(street):
    split_address = street.split(" ")
    lists = ["остров", "коса", "наб.", "пр.", "ул."]
    # new_street = ""
    if split_address[-1] in lists:
        new_street = split_address[0]
    elif street == "Набережная Фонтанки":
        new_street = "Фонтанки"
    elif street == "Воронцовский бульвар":
        new_street = "Воронцовский"
    # elif street == "Канонерский остров":
    #     new_street = "Канонерский"
    elif street == "Воскресенская (Робеспьера)":
        new_street = "Воскресенская"
    # elif street == "Петровская":
    #     new_street = "Петровская коса"
    # elif street == "Октябрьская":
    #     new_street = "Октябрьская наб."
    # elif street == "Волковский пр.":
    #     new_street = "Волковский"

    else:
        new_street = street

    return new_street