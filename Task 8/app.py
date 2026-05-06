from flask import Flask, render_template, request
import requests
app = Flask(__name__)
OWM_TOKEN = "your_openweathermap_api_key_here"
@app.route("/", methods=["GET", "POST"])
def main_page():
    report = None
    if request.method == "POST":
        location_input = request.form.get("city", "").strip()
        clean_name = location_input.strip().title()
        endpoint = f"http://api.openweathermap.org/data/2.5/weather?q={clean_name}&appid={OWM_TOKEN}&units=metric"
        try:
            api_call = requests.get(endpoint, timeout=5)
            results = api_call.json()
            if str(results.get("cod")) == "200":
                report = {
                    "town": results.get("name", clean_name),
                    "celsius": round(results["main"]["temp"]),
                    "moisture": results["main"]["humidity"],
                    "summary": results["weather"][0]["description"].capitalize()
                }
            else:
                report = {
                    "err_msg": results.get("message", "Could not fetch data.")
                }
        except requests.exceptions.RequestException:
            report = {
                "err_msg": "Connection issue. Please check your internet."
            }
    return render_template("index.html", weather_info=report)
if __name__ == "__main__":
    app.run(debug=True)