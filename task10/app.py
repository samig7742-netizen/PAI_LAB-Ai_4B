from flask import Flask, render_template, request

app = Flask(__name__)

def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hi" in user_input or "hello" in user_input:
        return "Hello 👋 Welcome to University Admission Help!"
    elif "admission" in user_input:
        return "Admissions are open. Apply before 30th August."
    elif "requirement" in user_input:
        return "You need Matric + Intermediate."
    elif "program" in user_input:
        return "We offer BSCS, BBA, BSIT."
    elif "fee" in user_input:
        return "Fee is around 50,000 PKR per semester."
    else:
        return "Sorry, I didn't understand."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_input = request.form["msg"]
    return chatbot_response(user_input)

if __name__ == "__main__":
    app.run(debug=True)