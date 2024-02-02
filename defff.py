def geocode():
    toponym_to_find = "г. Москва, ул. Профсоюзная 156 к6"

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    return toponym if toponym else None


def get_coordinates(toponym_to_find):
    toponym = geocode(toponym_to_find)
    if not toponym:
        return None, None
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    toponym_longitude = float(toponym_longitude)
    toponym_lattitude = float(toponym_lattitude)
    return toponym_longitude, toponym_lattitude


def get_ll_span(toponym_to_find):
    toponym = geocode(toponym_to_find)
    if not toponym:
        return None, None
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])
    left, bottom = toponym["boundeby"]["Envelope"]["upperCorner"].split(" ")
    right, top = toponym["boundeby"]["Envelope"]["upperCorner"].split(" ")

    dx = abs(float(left) - float(right)) / 2
    dy = abs(float(top) - float(bottom)) / 2
    span = f"{dx}, {dy}"
    return ll, span
