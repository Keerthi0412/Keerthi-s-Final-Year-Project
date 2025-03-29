import requests
import datetime
import plotly.graph_objects as go
import dash
from dash import dcc, html

# Replace with your OpenWeatherMap API key
API_KEY = "629dd34c192f83ce451532277342f609"
CITY = input("Enter city name: ")

# Fetch weather data (5-day forecast)
URL = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

try:
    response = requests.get(URL)
    response.raise_for_status()  # Raise an error for bad status codes
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
    data = {}
except ValueError:
    print("Error: Received an invalid JSON response from API.")
    data = {}

# Extract date and temperature
timestamps = []
temperatures = []

if data.get("cod") == "200":
    if "list" in data:
        for entry in data["list"]:
            timestamps.append(datetime.datetime.fromtimestamp(entry["dt"]))
            temperatures.append(entry["main"]["temp"])
    else:
        print("Error: 'list' key not found in the API response.")
else:
    print(f"API Error: {data.get('message', 'Unknown error')}. Check API key and city name.")
    timestamps = []
    temperatures = []

# Create a Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(f"Weather Dashboard for {CITY}"),
    dcc.Graph(
        id="temperature-chart",
        figure={
            "data": [
                go.Scatter(x=timestamps, y=temperatures, mode='lines+markers', name="Temperature")
            ],
            "layout": go.Layout(title="Temperature Trend", xaxis_title="Date & Time", yaxis_title="Temperature (°C)", xaxis_tickangle=-45)
        }
    )
])

if __name__ == "__main__":
    if timestamps and temperatures:
        app.run_server(debug=True,port=8051)
    else:
        print("No data available. Dashboard will not run.")
