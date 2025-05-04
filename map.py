import os
from dotenv import load_dotenv

from tkinter import *
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from configparser import ConfigParser
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")

#API Call
base_url = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}"

def get_weather(city):
    url = base_url.format(city_name=city, API_key=API_KEY)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]
        temperature = main['temp'] - 273.15  # Convert from Kelvin to Celsius
        location = f"{data['name']}, {data['sys']['country']}"
        weather_description = weather['description']
        return location, temperature, weather_description
    else:
        return None

def show_weather():
    city = city_name.get()
    if city:
        weather_data = get_weather(city)
        if weather_data:
            location, temperature, weather_description = weather_data
            location_label.config(text=f"Location: {location}")
            temperature_label.config(text=f"Temperature: {temperature:.2f}°C")
            weather_label.config(text=f"Weather: {weather_description.capitalize()}")
        else:
            messagebox.showerror("Error", "City not found!")
    else:
        messagebox.showwarning("Input Error", "Please enter a city name.")


root = ttk.Window()
root.title("Weather App")
root.geometry("700x400+300+200")
# root.config(bg="#f0f0f0")



ttk.Label(root, text="Enter city name", font=("Arial", 14)).pack(pady=10)
city_name = StringVar()
enter_city = ttk.Entry(root, textvariable=city_name, bootstyle=SUCCESS, width=50)
enter_city.pack()
enter_city.focus()

search_button = ttk.Button(root, text="Search", bootstyle=SUCCESS, width=20, command=show_weather)
search_button.pack(padx=10, pady=10)

location_label = ttk.Label(root, text="", bootstyle=SUCCESS, font=("Arial", 18))
location_label.pack(pady=10)

temperature_label = ttk.Label(root, text="", font=("Arial", 18))
temperature_label.pack(pady=10)

weather_label = ttk.Label(root, text="", font=("Arial", 18))
weather_label.pack(pady=10)

root.mainloop()