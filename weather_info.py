from datetime import datetime

import emoji
import requests

from mad_hatter.decorators import tool
from storage.plugins.weather_info.city_parser import get_city


def get_weather(api_key, city):
	base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
	response = requests.get(base_url)
	data = response.json()
	return data


def format_weather_markdown(weather_data):
	city_name = weather_data["name"]
	temperature = weather_data["main"]["temp"]
	description = weather_data["weather"][0]["description"].capitalize()
	icon = weather_data["weather"][0]["icon"]
	coordinates = weather_data["coord"]
	main_weather = weather_data["weather"][0]["main"]
	visibility = weather_data["visibility"]
	wind = weather_data["wind"]
	humidity = weather_data["main"]["humidity"]
	pressure = weather_data["main"]["pressure"]
	sunrise_utc = weather_data["sys"]["sunrise"]
	sunset_utc = weather_data["sys"]["sunset"]

	emoji_map = {
		"01d": emoji.emojize("☀️"),
		"02d": emoji.emojize("⛅️"),
		"03d": emoji.emojize("☁️"),
		"04d": emoji.emojize("☁️"),
		"09d": emoji.emojize("🌧️"),
		"10d": emoji.emojize("🌦️"),
		"11d": emoji.emojize("⛈️"),
		"13d": emoji.emojize("❄️"),
		"50d": emoji.emojize("🌫️"),
	}

	weather_emoji = emoji_map.get(icon, "")

	sunrise_local = datetime.utcfromtimestamp(sunrise_utc).strftime('%Y-%m-%d %H:%M:%S')
	sunset_local = datetime.utcfromtimestamp(sunset_utc).strftime('%Y-%m-%d %H:%M:%S')

	markdown = f"# Weather Report for {city_name}\n\n"
	markdown += f"Current Temperature: {temperature:.1f}°C\n"
	markdown += f"Description: {description} {weather_emoji}\n\n"
	markdown += "## Coordinates\n"
	markdown += f"Latitude: {coordinates['lat']}\n"
	markdown += f"Longitude: {coordinates['lon']}\n\n"
	markdown += "## Main Weather\n"
	markdown += f"Main Weather: {main_weather}\n\n"
	markdown += "## Visibility and Wind\n"
	markdown += f"Visibility: {visibility} meters\n"
	markdown += f"Wind Speed: {wind['speed']} m/s\n"
	markdown += f"Wind Direction: {wind['deg']}°\n\n"
	markdown += "## Additional Details\n"
	markdown += f"Humidity: {humidity}%\n"
	markdown += f"Pressure: {pressure} hPa\n"
	markdown += f"Sunrise: {sunrise_local} (local time)\n"
	markdown += f"Sunset: {sunset_local} (local time)\n"

	return markdown


@tool(return_direct=True)
def get_weather_forecast(question, bot):
	"""Retrieve the current weather and weather forecast for the specified city based on the provided weather-related query.
Replies to "What's the weather of Beijing?", "How is the Shanghai's weather", "上海天气怎么样？", "今天北京天气如何？" and similar questions.
Input is the weather-related query for the specified city.
"""

	api_key = "e151b86fbd2c8e1e48104492667ae97e"
	city = get_city(question)

	weather_data = get_weather(api_key, city)
	markdown_output = format_weather_markdown(weather_data)

	return markdown_output
