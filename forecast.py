# get forecast
import datetime
import requests
import json
from tkinter import *

weather_api = 'f46b2843b9dd4dd4e8d1961bcb4838a6'
weather_lang = 'de'
weather_unit = 'auto'
lat = 47.2695
lon = 11.3971

weather_icons = {
    'clear-day': 'assets/Sun.png',
    'wind': 'assets/Wind.png',
    'cloudy': 'assets/Cloud.png',
    'partly-cloudy-day': "assets/PartlySunny.png",
    'rain': "assets/Rain.png",
    'snow': "assets/Snow.png",
    'snow-thin': "assets/Snow.png",
    'fog': "assets/Haze.png",
    'clear-night': "assets/Moon.png",
    'partly-cloudy-night': "assets/PartlyMoon.png",
    'thunderstorm': "assets/Storm.png",
    'tornado': "assests/Tornado.png",
    'hail': "assests/Hail.png"
}

class Forecast(Frame):
        def __init__(self, parent, *args, **kwargs):
            Frame.__init__(self, parent, bg='black')
            self.get_forecast()
            # Day Frames
            self.day1Frame = Frame(self, bg='black')
            self.day1Frame.pack(side=LEFT)
            self.day2Frame = Frame(self, bg='black')
            self.day2Frame.pack(side=LEFT)
            self.day3Frame = Frame(self, bg='black')
            self.day3Frame.pack(side=LEFT)
            #Weekday Labels
            self.weekday1 = Label(self.day1Frame, font=('Helvetica', text_small), fg='white', bg='black')
            self.weekday1.pack(side=TOP, anchor=N)
            self.weekday2 = Label(self.day2Frame, font=('Helvetica', text_small), fg='white', bg='black')
            self.weekday2.pack(side=TOP, anchor=N)
            self.weekday3 = Label(self.day3Frame, font=('Helvetica', text_small), fg='white', bg='black')
            self.weekday3.pack(side=TOP, anchor=N)
            # Temp Labels
            self.day1Temp = Label(self.day1Frame, font=('Helvetica', text_medium), fg='white', bg='black')
            self.day1Temp.pack(side=BOTTOM, anchor=S)
            self.day2Temp = Label(self.day2Frame, font=('Helvetica', text_medium), fg='white', bg='black')
            self.day2Temp.pack(side=BOTTOM, anchor=S)
            self.day3Temp = Label(self.day3Frame, font=('Helvetica', text_medium), fg='white', bg='black')
            self.day3Temp.pack(side=BOTTOM, anchor=S)
            # icon Labels
            self.day1Icon = Label(self.day1Frame)
            self.day1Icon.pack(side=TOP, anchor=S, padx=20, pady=20)
            self.day2Icon = Label(self.day2Frame)
            self.day1Icon.pack(side=TOP, anchor=S, padx=20, pady=20)
            self.day3Icon = Label(self.day3Frame)
            self.day1Icon.pack(side=TOP, anchor=S, padx=20, pady=20)
            # update values
            self.temperature1_max = ''
            self.temperature2_max = ''
            self.temperature3_max = ''

            self.temperature1_min = ''
            self.temperature2_min = ''
            self.temperature3_min = ''

            self.weekday1_text = ''
            self.weekday2_text = ''
            self.weekday3_text = ''

            self.icon1 = ''
            self.icon2 = ''
            self.icon3 = ''

        def get_days(self):
            tomorrow = str(today + datetime.timedelta(1)) + 'T14:00:00'
            in_two_days = str(today + datetime.timedelta(2)) +'T14:00:00'
            in_three_days = str(today + datetime.timedelta(3)) +'T14:00:00'

            forecast_days = [tomorrow, in_two_days, in_three_days]

            return forecast_days

        def get_forecast(self):
            forecast_data = []

            # loop through days and get forecasts
            for day in self.get_days():
                forecast_url = "https://api.darksky.net/forecast/%s/%s,%s,%s?lang=%s&units=%s" % (
                        weather_api, lat, lon, day, weather_lang, weather_unit)
                forecast_req = requests.get(forecast_url)

                day_forecast = json.loads(forecast_req.text)['daily']['data'][0]

                # minimum temperature
                day_min_temperature = '{}{}'.format(
                int(day_forecast['temperatureMin']), '°')
                day
                # maximum temperature
                day_max_temperature = '{}{}'.format(
                int(day_forecast['temperatureMax']), '°')
                day
                # icon
                day_icon = day_forecast['icon']

                forecast_data.append({
                    'min': day_min_temperature,
                    'max': day_max_temperature,
                    'icon': day_icon
                })
            
            print(forecast_data)

            if forecast_data[0]['icon'] in weather_icons:
                icon_day1 = weather_icons[forecast_data[0]['icon']]
            if forecast_data[1]['icon'] in weather_icons:
                icon_day2 = weather_icons[forecast_data[1]['icon']]
            if forecast_data[2]['icon'] in weather_icons:
                icon_day3 = weather_icons[forecast_data[2]['icon']]

            if icon_day1 is not None:
                if self.icon1 != icon_day1:
                    self.icon1 = icon_day1
                    image = Image.open(icon_day1)
                    image = image.resize((20, 20), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.day1Icon.config(image=photo)
                    self.day1Icon.image = photo

            if icon_day2 is not None:
                if self.icon2 != icon_day2:
                    self.icon2 = icon_day2
                    image = Image.open(icon_day2)
                    image = image.resize((20, 20), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.day2Icon.config(image=photo)
                    self.day2Icon.image = photo

            if icon_day3 is not None:
                if self.icon3 != icon_day3:
                    self.icon3 = icon_day3
                    image = Image.open(icon_day3)
                    image = image.resize((20, 20), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.day3Icon.config(image=photo)
                    self.day3Icon.image = photo

            
            if forecast_data[0]['min'] != self.temperature1_min or forecast_data[0]['max'] != self.temperature1_max:
                self.temperature1_min = forecast_data[0]['min']
                self.temperature1_max = forecast_data[0]['max']
                self.day1Temp.config(text=forecast_data[0]['min'] + ' - ' + forecast_data[0]['max'])

            if forecast_data[1]['min'] != self.temperature2_min or forecast_data[1]['max'] != self.temperature2_max:
                self.temperature2_min = forecast_data[1]['min']
                self.temperature2_max = forecast_data[1]['max']
                self.day2Temp.config(text=forecast_data[1]['min'] + ' - ' + forecast_data[1]['max'])

            if forecast_data[2]['min'] != self.temperature3_min or forecast_data[2]['max'] != self.temperature3_max:
                self.temperature3_min = forecast_data[2]['min']
                self.temperature3_max = forecast_data[2]['max']
                self.day3Temp.config(text=forecast_data[2]['min'] + ' - ' + forecast_data[2]['max'])

            # for weekday Label
            weekdays = ('Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag')
            today = datetime.date.today()
            weekday_today = datetime.date.weekday()

            if weekday_today <= 3:
                wd1 = weekdays[weekday_today + 1]
                wd2 = weekdays[weekday_today + 2]
                wd3 = weekdays[weekday_today +3]
            elif weekday_today == 4:
                wd1 = weekdays[weekday_today + 1]
                wd2 = weekdays[weekday_today + 2]
                wd3 = weekdays[0]
            elif weekday_today == 5:
                wd1 = weekdays[weekday_today + 1]
                wd2 = weekdays[0]
                wd3 = weekdays[1]
            elif: weekday_today == 6:
                wd1 = weekdays[0]
                wd2 = weekdays[1]
                wd3 = weekdays[2]

            if wd1 != self.weekday1_text:
                self.weekday1_text = wd1
                self.weekday1.config(text=wd1)
            if wd2 != self.weekday2_text:
                self.weekday2_text = wd2
                self.weekday2.config(text=wd2)
            if wd3 != self.weekday3_text:
                self.weekday3_text = wd3
                self.weekday3.config(text=wd3)




f = Forecast()