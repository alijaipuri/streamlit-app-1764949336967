import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title='Weather Forecast App', page_icon='☁️')

st.title('🌞 Weather Forecast App')
st.markdown('Get the current weather and 7-day forecast for any city')

# API Key
api_key = 'YOUR_OPENWEATHERMAP_API_KEY'

# Function to get current weather
def get_current_weather(city):
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(base_url)
    weather_data = response.json()
    return weather_data

# Function to get 7-day forecast
def get_forecast(city):
    base_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    response = requests.get(base_url)
    forecast_data = response.json()
    return forecast_data

# Sidebar inputs
with st.sidebar:
    st.header('Settings')
    city = st.text_input('Enter city name')

# Main content
if st.button('Get Weather', type='primary'):
    try:
        # Get current weather
        current_weather = get_current_weather(city)
        st.write('Current Weather:')
        st.write(f'Temperature: {current_weather["main"]["temp"]}°C')
        st.write(f'Humidity: {current_weather["main"]["humidity"]} %')
        st.write(f'Wind Speed: {current_weather["wind"]["speed"]} m/s')
        st.write(f'Weather Condition: {current_weather["weather"][0]["description"]}')

        # Get 7-day forecast
        forecast = get_forecast(city)
        st.write('7-Day Forecast:')
        forecast_data = []
        for i in range(0, 40, 8):
            forecast_data.append({
                'Date': forecast['list'][i]['dt_txt'],
                'Temperature': forecast['list'][i]['main']['temp'],
                'Humidity': forecast['list'][i]['main']['humidity'],
                'Wind Speed': forecast['list'][i]['wind']['speed']
            })
        forecast_df = pd.DataFrame(forecast_data)
        st.write(forecast_df)

        # Visual charts
        st.write('Temperature Chart:')
        temp_chart = pd.DataFrame({
            'Date': forecast_df['Date'],
            'Temperature': forecast_df['Temperature']
        })
        st.line_chart(temp_chart)

        st.write('Humidity Chart:')
        humidity_chart = pd.DataFrame({
            'Date': forecast_df['Date'],
            'Humidity': forecast_df['Humidity']
        })
        st.line_chart(humidity_chart)

        st.write('Wind Speed Chart:')
        wind_speed_chart = pd.DataFrame({
            'Date': forecast_df['Date'],
            'Wind Speed': forecast_df['Wind Speed']
        })
        st.line_chart(wind_speed_chart)

    except Exception as e:
        st.error('Error: ' + str(e))

# Show example
with st.expander('See example'):
    st.write('Example city: London')
    st.write('Current weather and 7-day forecast will be displayed below')

# Location-based weather fetching
st.write('Location-based Weather Fetching:')
st.write('Please allow location access to get your current location\'s weather')
if st.button('Get Current Location Weather'):
    try:
        # Get current location
        url = 'https://ip-api.com/json'
        response = requests.get(url)
        location_data = response.json()
        city = location_data['city']
        current_weather = get_current_weather(city)
        st.write(f'Current weather in {city}:')
        st.write(f'Temperature: {current_weather["main"]["temp"]}°C')
        st.write(f'Humidity: {current_weather["main"]["humidity"]} %')
        st.write(f'Wind Speed: {current_weather["wind"]["speed"]} m/s')
        st.write(f'Weather Condition: {current_weather["weather"][0]["description"]}')
    except Exception as e:
        st.error('Error: ' + str(e))