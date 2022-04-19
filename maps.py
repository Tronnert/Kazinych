import requests
import math


class Example:
    def __init__(self):
        self.r_major = 6378137.000
        self.r_minor = 6356752.3142
        self.param_l = 'map'
        self.inp = 'кипр'
        self.mapfile = 'static/img/map.png'
        self.point = ''
        self.z = 8
        self.toponym_longitude = ""
        self.toponym_lattitude = ""
        self.top()

    def change_layer(self, text):
        if text == 'Карта':
            self.param_l = 'map'
        elif text == 'Спутник':
            self.param_l = 'sat'
        elif text == 'Гибрид':
            self.param_l = 'sat,skl'
        self.regenerate()

    def top(self):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.inp,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            return
        json_response = response.json()
        resp = json_response["response"]
        geoobjcol = resp["GeoObjectCollection"]
        featmem = geoobjcol["featureMember"]
        if not featmem:
            return
        toponym = featmem[0]["GeoObject"]
        point = toponym["Point"]
        toponym_coodrinates = point["pos"]
        self.toponym_longitude, self.toponym_lattitude = toponym_coodrinates.split(" ")
        self.regenerate()

    def regenerate(self):
        map_params = {
            "ll": ",".join([self.toponym_longitude, self.toponym_lattitude]),
            "l": self.param_l,
            "z": str(self.z)
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        if not response:
            return
        with open(self.mapfile, "wb") as file:
            file.write(response.content)

    def move(self, event):
        if event == "Zoom-":
            self.z -= 1
            if self.z < 0:
                self.z = 0
            self.regenerate()
        elif event == "Zoom+":
            self.z += 1
            if self.z > 17:
                self.z = 17
            self.regenerate()
        elif event == "Up":
            y = self.merc_y(float(self.toponym_lattitude))
            new_lat = self.merc_lat((y * self.get_k() + 450 * 2) / self.get_k())
            if new_lat > 85.0842:
                new_lat = 85.0842
            self.toponym_lattitude = str(new_lat)
            self.regenerate()
        elif event == "Down":
            y = self.merc_y(float(self.toponym_lattitude))
            new_lat = self.merc_lat((y * self.get_k() - 450 * 2) / self.get_k())
            if new_lat < -85.0842:
                new_lat = -85.0842
            self.toponym_lattitude = str(new_lat)
            self.regenerate()
        elif event == "Left":
            x = self.merc_x(float(self.toponym_longitude))
            new_lon = self.merc_lon((x * self.get_k() - 600 * 2) / self.get_k())
            if new_lon < -180:
                new_lon = -180
            self.toponym_longitude = str(new_lon)
            self.regenerate()
        elif event == "Right":
            x = self.merc_x(float(self.toponym_longitude))
            new_lon = self.merc_lon((x * self.get_k() + 600 * 2) / self.get_k())
            if new_lon > 180:
                new_lon = 180
            self.toponym_longitude = str(new_lon)
            self.regenerate()

    def lonlat_distance(self, a, b):
        degree_to_meters_factor = 111 * 1000
        a_lon, a_lat = a
        b_lon, b_lat = b
        radians_lattitude = math.radians((a_lat + b_lat) / 2.)
        lat_lon_factor = math.cos(radians_lattitude)
        dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
        dy = abs(a_lat - b_lat) * degree_to_meters_factor
        distance = math.sqrt(dx * dx + dy * dy)
        return distance

    def merc_x(self, lon):
        return self.r_major * math.radians(lon)

    def merc_lon(self, x):
        return math.degrees(x / self.r_major)

    def merc_lat(self, y):
        iz_lon = y / self.r_major
        temp = self.r_minor / self.r_major
        eccent = math.sqrt(1 - temp ** 2)
        lon = 0
        for e in range(100):
            lon = -2 * math.atan((math.e ** -iz_lon) *
                                 (((1 - eccent * math.sin(lon)) / (1 + eccent * math.sin(lon))) ** (
                                         eccent / 2))) + math.pi / 2
        return round(math.degrees(lon), 7)

    def merc_y(self, lat):
        if lat > 89.5:
            lat = 89.5
        if lat < -89.5:
            lat = -89.5
        temp = self.r_minor / self.r_major
        eccent = math.sqrt(1 - temp ** 2)
        phi = math.radians(lat)
        sinphi = math.sin(phi)
        con = eccent * sinphi
        com = eccent / 2
        con = ((1.0 - con) / (1.0 + con)) ** com
        ts = math.tan((math.pi / 2 + phi) / 2) * con
        y = self.r_major * math.log(ts)
        return y

    def get_k(self):
        return 2 ** (8 + self.z) / self.r_major / math.pi


class Example1:
    def __init__(self):
        self.r_major = 6378137.000
        self.r_minor = 6356752.3142
        self.param_l = 'map'
        self.inp = 'тихиий+океан'
        self.mapfile = 'static/img/map1.png'
        self.point = ''
        self.z = 8
        self.toponym_longitude = ""
        self.toponym_lattitude = ""
        self.top()

    def change_layer(self, text):
        if text == 'Карта':
            self.param_l = 'map'
        elif text == 'Спутник':
            self.param_l = 'sat'
        elif text == 'Гибрид':
            self.param_l = 'sat,skl'
        self.regenerate()

    def top(self):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.inp,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            return
        json_response = response.json()
        resp = json_response["response"]
        geoobjcol = resp["GeoObjectCollection"]
        featmem = geoobjcol["featureMember"]
        if not featmem:
            return
        toponym = featmem[0]["GeoObject"]
        point = toponym["Point"]
        toponym_coodrinates = point["pos"]
        self.toponym_longitude, self.toponym_lattitude = toponym_coodrinates.split(" ")
        self.regenerate()

    def regenerate(self):
        map_params = {
            "ll": ",".join([self.toponym_longitude, self.toponym_lattitude]),
            "l": self.param_l,
            "z": str(self.z)
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        if not response:
            return
        with open(self.mapfile, "wb") as file:
            file.write(response.content)

    def move(self, event):
        if event == "Zoom-":
            self.z -= 1
            if self.z < 0:
                self.z = 0
            self.regenerate()
        elif event == "Zoom+":
            self.z += 1
            if self.z > 17:
                self.z = 17
            self.regenerate()
        elif event == "Up":
            y = self.merc_y(float(self.toponym_lattitude))
            new_lat = self.merc_lat((y * self.get_k() + 450 * 2) / self.get_k())
            if new_lat > 85.0842:
                new_lat = 85.0842
            self.toponym_lattitude = str(new_lat)
            self.regenerate()
        elif event == "Down":
            y = self.merc_y(float(self.toponym_lattitude))
            new_lat = self.merc_lat((y * self.get_k() - 450 * 2) / self.get_k())
            if new_lat < -85.0842:
                new_lat = -85.0842
            self.toponym_lattitude = str(new_lat)
            self.regenerate()
        elif event == "Left":
            x = self.merc_x(float(self.toponym_longitude))
            new_lon = self.merc_lon((x * self.get_k() - 600 * 2) / self.get_k())
            if new_lon < -180:
                new_lon = -180
            self.toponym_longitude = str(new_lon)
            self.regenerate()
        elif event == "Right":
            x = self.merc_x(float(self.toponym_longitude))
            new_lon = self.merc_lon((x * self.get_k() + 600 * 2) / self.get_k())
            if new_lon > 180:
                new_lon = 180
            self.toponym_longitude = str(new_lon)
            self.regenerate()

    def lonlat_distance(self, a, b):
        degree_to_meters_factor = 111 * 1000
        a_lon, a_lat = a
        b_lon, b_lat = b
        radians_lattitude = math.radians((a_lat + b_lat) / 2.)
        lat_lon_factor = math.cos(radians_lattitude)
        dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
        dy = abs(a_lat - b_lat) * degree_to_meters_factor
        distance = math.sqrt(dx * dx + dy * dy)
        return distance

    def merc_x(self, lon):
        return self.r_major * math.radians(lon)

    def merc_lon(self, x):
        return math.degrees(x / self.r_major)

    def merc_lat(self, y):
        iz_lon = y / self.r_major
        temp = self.r_minor / self.r_major
        eccent = math.sqrt(1 - temp ** 2)
        lon = 0
        for e in range(100):
            lon = -2 * math.atan((math.e ** -iz_lon) *
                                 (((1 - eccent * math.sin(lon)) / (1 + eccent * math.sin(lon))) ** (
                                         eccent / 2))) + math.pi / 2
        return round(math.degrees(lon), 7)

    def merc_y(self, lat):
        if lat > 89.5:
            lat = 89.5
        if lat < -89.5:
            lat = -89.5
        temp = self.r_minor / self.r_major
        eccent = math.sqrt(1 - temp ** 2)
        phi = math.radians(lat)
        sinphi = math.sin(phi)
        con = eccent * sinphi
        com = eccent / 2
        con = ((1.0 - con) / (1.0 + con)) ** com
        ts = math.tan((math.pi / 2 + phi) / 2) * con
        y = self.r_major * math.log(ts)
        return y

    def get_k(self):
          return 2 ** (8 + self.z) / self.r_major / math.pi


maps_dict = {'map': Example(),
             'map1': Example1()}
