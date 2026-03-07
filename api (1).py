import requests
from flask import Flask, render_template, request

app = Flask(__name__)

api_key = "42cdf13a7cec4fa33a78ef263034b5dc"

@app.route("/", methods=["GET", "POST"])
def main():
    weather_data = None
    
    if request.method == "POST":
        city = request.form.get("city")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
        else:
            weather_data = {"error": "City not found!"}

    return render_template("index.html", data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)