import flet as ft
from flet import *
import requests
import datetime as dt
import math

API_KEY = "32b2fb4e348d104cd7df383d1c2918b6"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
CITY = "Minsk"
COUNTRY = "BY"
lat = "33.44"
lon = "-94.04"
days_en = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
days_ru = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
#временный костыль для будущей смены языков
days = days_en
lang = "en"
languages = ['en', 'ru', 'fr', 'gr', 'jp']


def k_to_c_f(k):
    c = k - 273.15
    f = c * (9 / 5) + 32
    return c, f


url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
response = requests.get(url).json()
response2 = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly,minutely&appid={API_KEY}").json()

temp_k = response['main']['temp']
temp_c, temp_f = k_to_c_f(temp_k)

feels_like_k = response['main']['feels_like']
feels_like_c, feels_like_f = k_to_c_f(feels_like_k)

humidity = response['main']['humidity']
description = response['weather'][0]['description']

sunrise_time = dt.datetime.fromtimestamp(response['sys']['sunrise'] + response['timezone']).isoformat(' ')
sunset_time = dt.datetime.fromtimestamp(response['sys']['sunset'] + response['timezone']).isoformat(' ')
n = 11

sunrise_time = sunrise_time[n:]
sunset_time = sunset_time[n:]

wind_speed = response['wind']['speed']

cloudiness = response['clouds']['all']

if description == "overcast clouds":
    cloud_icon = './assets/Cloudy.png'
if description == "broken clouds":
    cloud_icon = './assets/Cloudy.png'
if description == "scattered clouds":
    cloud_icon = './assets/Cloudy.png'
if description == "few clouds":
    cloud_icon = './assets/Cloudy.png'
if description == "clear sky":
    cloud_icon = './assets/Sunny.png'


def main(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.window_width = 480
    page.window_height = 640
    page.window_resizable = False
    page.update()

    #language switch
    def _language():
        #временный костыль
        if lang == "en":
            days = days_en
        if lang == "ru":
            days = days_ru

    #animation
    def _expand(e):
        #!!! make sure to change the control index when doing the bottom portion of the app
        if e.data == "true":
            _c.content.controls[1].height = 500
            _c.content.controls[1].update()
        else:
            _c.content.controls[1].height = 640 * 0.6
            _c.content.controls[1].update()

    def _top():
        top = Container(
            width=480, height=640 * 0.60,
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=["purple500", "pink400"],
            ),
            border_radius=32,
            animate=animation.Animation(duration=400, curve="decelerate"),
            on_hover=lambda e: _expand(e),
            padding=16,
            content=Column(
                alignment='start',
                spacing=12,
                controls=[
                    Row(
                        alignment='center',
                        controls=[
                            Text(
                                f"{CITY}, {COUNTRY}", size=16, weight='w500',
                            )
                        ]
                    ),
                    Row(
                        alignment='center',
                        controls=[
                            Text(dt.datetime.today().strftime("%b %d, %Y %H:%M"), size=14)
                        ]
                    ),
                    Container(padding=padding.only(bottom=6)),
                    Row(
                        alignment='center',
                        spacing=30,
                        controls=[
                            Column(
                                controls=[
                                    Container(
                                        width=120,
                                        height=120,
                                        image_src=cloud_icon,
                                    ),
                                ]
                            ),
                            Column(
                                spacing=6,
                                horizontal_alignment='center',
                                controls=[
                                    Text(
                                        "Today",
                                        size=18,
                                        text_align='center',
                                    ),
                                    Row(
                                        vertical_alignment='start',
                                        spacing=0,
                                        controls=[
                                            Container(
                                                content=Text(f"{math.ceil(temp_c)}°C", size=52)
                                            )
                                        ]
                                    ),
                                    Text(description.title(), size=14, color='white54', text_align='center')
                                ],
                            )
                        ]
                    ),
                    Divider(height=8, thickness=1, color='white10'),
                    Row(
                        alignment='spaceAround',
                        controls=[
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image('./assets/Wind.png'),
                                            width=60,
                                            height=60,
                                        ),
                                        Text(f"{math.ceil(wind_speed)} m/s", size=14),
                                        Text("Wind", size=12, color='white54')
                                    ]
                                )
                            ),
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image('./assets/Humidity.png'),
                                            width=60,
                                            height=60,
                                        ),
                                        Text(f"{math.ceil(humidity)}%", size=14),
                                        Text("Humidity", size=12, color='white54')
                                    ]
                                )
                            ),
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image('./assets/Thermometer.png'),
                                            width=60,
                                            height=60,
                                        ),
                                        Text(f"{math.ceil(feels_like_c)}°C", size=14),
                                        Text("Feels Like", size=12, color='white54')
                                    ]
                                )
                            ),
                        ]
                    ),
                    Row(
                        alignment='spaceAround',
                        controls=[
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image('./assets/Sunrise.png'),
                                            width=60,
                                            height=60,
                                        ),
                                        Text(sunrise_time, size=14),
                                        Text("Sunrise", size=12, color='white54')
                                    ]
                                )
                            ),
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image('./assets/Sunset.png'),
                                            width=60,
                                            height=60,
                                        ),
                                        Text(sunset_time, size=14),
                                        Text("Sunset", size=12, color='white54')
                                    ]
                                )
                            ),
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image('./assets/Cloudy.png'),
                                            width=60,
                                            height=60,
                                        ),
                                        Text(f"{math.ceil(cloudiness)}%", size=14),
                                        Text("Cloudiness", size=12, color='white54')
                                    ]
                                )
                            )
                        ]
                    )
                ]
            )
        )
        return top

    # bottom data
    def _bot_data():
        _bot_data = []
        #range is a number of days for forecast => limited by the API key
        for index in range(1, 8):
            _bot_data.append(
                Row(
                    spacing=5,
                    alignment="spaceBetween",
                    controls=[
                        Row(
                            expand=1,
                            alignment="start",
                            controls=[
                                Container(
                                    alignment=alignment.center,
                                    content=Text(
                                        #week day display
                                        dt.datetime.weekday(
                                        dt.datetime.fromtimestamp(
                                            response2['daily'][index]['dt']
                                        )
                                        )
                                    )
                                )
                            ]
                        )
                    ]
                )
            )
        return _bot_data

    def _bottom():
        _bot_column = Column(
            alignment="center",
            horizontal_alignment="center",
            spacing=25,
        )

        for data in _bot_data():
            _bot_column.controls.append(data)

        bottom = Container(
            padding=padding.only(top=280, left=20, right=20, bottom=20),
            content=_bot_column
        )
        return bottom

    _c = Container(
        width=480,
        height=580,
        border_radius=32,
        bgcolor='grey900',
        padding=12,
        content=Stack(width=240, height=320, controls=[
            #first control is place at the bottom of the stack
            _bottom(),
            _top()]),
    )

    page.add(_c)


if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')
