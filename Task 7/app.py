from flask import Flask, jsonify
import requests
app = Flask(__name__)
@app.route("/")
def intro():
    return "<h1>Fun Fact & Joke Generator</h1><p>Navigate to /fetch-joke to get a random joke!</p>"
@app.route("/fetch-joke")
def get_joke_data():
    api_endpoint = "https://official-joke-api.appspot.com/random_joke"
    try:
        query_response = requests.get(api_endpoint, timeout=10)
        joke_payload = query_response.json()
        setup = joke_payload.get('setup', 'No setup found.')
        delivery = joke_payload.get('punchline', 'No punchline found.')
        html_output = f
        return html_output
    except Exception as e:
        return f"Error connecting to joke service: {str(e)}"
if __name__ == "__main__":
    app.run(debug=True)