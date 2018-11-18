import time
import locale
import requests
import json
import feedparser
import speech_recognition as sr 

from random import sample
from tkinter import *
from PIL import Image, ImageTk

from speech import Speech

# Lokalisierung
locale.setlocale(locale.LC_TIME, 'de_DE')

# Textgrößen
text_small = 20
text_medium = 25
text_big = 45
text_xlarge = 90

# Manuelle Ortsangabe (optional)
latitude = None
longitude = None

# Wetter
weather_api = 'f46b2843b9dd4dd4e8d1961bcb4838a6'
weather_lang = 'de'
weather_unit = 'auto'

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


class Time(Frame):

    def __init__(self, parent, *args, **krwargs):
        Frame.__init__(self, parent, bg='black')

        # Get Time
        self.time = time.strftime('%H:%M')
        self.date = time.strftime('%A, %d. %B')

        # Make Time Labels
        self.timeLabel = Label(self, font=(
            'Helvetica', text_big), text=self.time, fg='white', bg='black')
        self.dateLabel = Label(self, font=(
            'Helvetica', text_small), text=self.date, fg='white', bg='black')

        # Display Labels
        self.timeLabel.pack(side=TOP, anchor=W)
        self.dateLabel.pack(side=TOP, anchor=W)
        # self.timeLabel.grid(row=0, column=0, sticky=W)
        # self.dateLabel.grid(row=1, column=0, sticky=W)


class Weather(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # Init attributes
        self.temperature = ''
        self.location = ''
        self.weather_summary = ''
        self.weather_icon = None
        # Make Widgets
        self.weather_frame = Frame(self, bg='black')
        self.weather_frame.pack(side=TOP, anchor=W)

        self.tempLabel = Label(self.weather_frame, font=(
            'Helvetica', text_xlarge), fg='white', bg='black')
        self.tempLabel.pack(side=LEFT, anchor=N)

        self.iconLabel = Label(self.weather_frame, bg='black')
        self.iconLabel.pack(side=LEFT, anchor=N, padx=20, pady=20)

        self.summaryLabel = Label(self, font=(
            'Helvetica', text_small), fg='white', bg='black')
        self.summaryLabel.pack(side=TOP, anchor=E)

        self.locationLabel = Label(self, font=(
            'Helvetica', text_small), fg='white', bg='black')
        self.locationLabel.pack(side=TOP, anchor=E)

        self.get_weather()

    def get_ip(self):
        try:
            url = 'http://jsonip.com'
            req = requests.get(url)
            ip_json = json.loads(req.text)
            ip = ip_json['ip']
            return ip

        except Exception as e:
            return 'Error: %s. Cannot get ip'

    def get_weather(self):
        try:
            if latitude is None and longitude is None:
                # get location
                api_key = 'b2c0083cd5cabc313e8b70df8580d946'  # IP Stack Api Key
                url = f'http://api.ipstack.com/{self.get_ip()}?access_key={api_key}'
                req = requests.get(url)
                res = json.loads(req.text)

                # set location
                lat = res['latitude']
                lon = res['longitude']
                location2 = '%s' % (res['city'])

                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (
                    weather_api, lat, lon, weather_lang, weather_unit)
            else:
                location = ''
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (
                    weather_api, latitude, longitude, weather_lang, weather_unit)

            req = requests.get(weather_req_url)
            weather = json.loads(req.text)

            degree_sign = u'\N{DEGREE SIGN}'
            temperature2 = '{}{}'.format(
                int(weather['currently']['temperature']), degree_sign)
            weather_summary2 = weather['currently']['summary']
            icon_id = weather['currently']['icon']
            weather_icon2 = None

            if icon_id in weather_icons:
                weather_icon2 = weather_icons[icon_id]

            if weather_icon2 is not None:
                if self.weather_icon != weather_icon2:
                    self.weather_icon = weather_icon2
                    image = Image.open(weather_icon2)
                    image = image.resize((65, 65), Image.ANTIALIAS)
                    iamge = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLabel.config(image=photo)
                    self.iconLabel.image = photo
            else:
                # remove image
                self.iconLabel.config(image='')

            # set attributes
            if self.weather_summary != weather_summary2:
                self.weather_summary = weather_summary2
                self.summaryLabel.config(text=weather_summary2)

            if self.temperature != temperature2:
                self.temperature = temperature2
                self.tempLabel.config(text=temperature2)

            if self.location != location2:
                if location2 == ', ':
                    self.location = 'Cannot find location'
                    self.locationLabel.config(text='Cannot find location')
                else:
                    self.location = location2
                    self.locationLabel.config(text=location2)

        except Exception as e:
            print(f'Error {e}. Cannot get weather')

        self.after(60000, self.get_weather)


class News(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'News'

        self.newsLabel = Label(self, text=self.title, font=(
            'Helvetica', text_medium), fg='white', bg='black', pady=10)
        self.newsLabel.pack(side=TOP, anchor=W)

        self.headlinesContainer = Frame(self, bg='black')
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()

    def get_headlines(self):
        try:
            # remove all children
            for widget in self.headlinesContainer.winfo_children():
                widget.destroy()

            headline_urls = (
                'http://diepresse.com/rss/Techscience',
                'http://diepresse.com/rss/Wirtschaftsnachrichten',
                'http://diepresse.com/rss/Sport',
                'http://diepresse.com/rss/Politik',
                'http://diepresse.com/rss/Finanzen'
            )

            headlines = []

            for url in headline_urls:
                feed = feedparser.parse(url)
                for post in sample(feed.entries, 5):
                    headlines.append(post.title)

            chosen_headlines = sample(headlines, 5)

            for post in chosen_headlines:
                if post.endswith('[premium]'):
                    headline = NewsHeadline(
                        self.headlinesContainer, post[:-10])
                else:
                    headline = NewsHeadline(self.headlinesContainer, post)
                headline.pack(side=TOP, anchor=W)

        except Exception as e:
            print(f'Error: {e}. Cannot get News')

        self.after(60000, self.get_headlines)


class NewsHeadline(Frame):

    def __init__(self, parent, event_name=''):
        Frame.__init__(self, parent, bg='black')

        image = Image.open('assets/Newspaper.png')
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLabel = Label(self, bg='black', image=photo)
        self.iconLabel.image = photo
        self.iconLabel.pack(side=LEFT, anchor=N)

        self.event_name = event_name
        self.event_name = Label(self, text=self.event_name, font=(
            'Helvetica', text_small), fg='white', bg='black')
        self.event_name.pack(side=LEFT, anchor=N)


class Welcome(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.message_lookup = {
            'Morgen': 'Guten Morgen, Philipp!',
            'Mittag': 'Guten Tag, Philipp!',
            'Abend': 'Guten Abend, Philipp!',
            'Nacht': 'Noch immer wach?'
        }
        self.message = ''
        self.messageLabel = Label(self, font=(
            'Helvetica', text_big), fg='white', bg='black')
        self.messageLabel.pack(anchor=N, side=TOP)
        self.get_message()

    def get_message(self):
        current_time = int(time.strftime('%H'))
        if current_time > 5 and current_time < 10:
            message2 = self.message_lookup['Morgen']
        elif current_time > 10 and current_time < 18:
            message2 = self.message_lookup['Mittag']
        elif current_time > 18 and current_time < 23:
            message2 = self.message_lookup['Abend']
        else:
            message2 = self.message_lookup['Nacht']

        if self.message != message2:
            self.message = message2
            self.messageLabel.config(text=message2)


class Screen:

    def __init__(self):
        self.tk = Tk()
        self.state = False
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background='black')
        self.bottomFrame = Frame(self.tk, background='black')
        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)
        self.tk.bind('<Return>', self.toggle_fullscreen)
        self.tk.bind('<Escape>', self.end_fullscreen)

        self.time = Time(self.topFrame)
        self.time.pack(side=LEFT, anchor=N, padx=100, pady=60)

        self.weather = Weather(self.topFrame)
        self.weather.pack(side=RIGHT, anchor=N, padx=100, pady=60)

        self.news = News(self.bottomFrame)
        self.news.pack(side=LEFT, anchor=S, padx=100, pady=60)

        self.welcome = Welcome(self.topFrame)
        self.welcome.pack(side=BOTTOM, anchor=S)

    def quit(self):
    	self.tk.destroy()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes('-fullscreen', self.state)
        return 'break'

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes('-fullscreen', False)
        return 'break'


if __name__ == '__main__':
	mic = sr.Microphone()
	r = sr.Recognizer()
	s = Speech()

	print('Listening for keyword')
	word = s.recognize_speech(r, mic)

	if word['transcription'].lower() == 'starten':
		w = Screen()
		w.tk.after(120000, lambda: w.tk.destroy()) # fenster nach 120s automatisch schließen
		w.tk.mainloop()


	else:
		print('Falsches Wort')
