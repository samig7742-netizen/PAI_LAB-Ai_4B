from flask import Flask, render_template, request
app = Flask(__name__)
KNOWLEDGE_BASE = {
    "admission": "To apply, you need at least 60% in FSC and must pass our entrance exam.",
    "deadline": "The final date for applications is typically in late August.",
    "program": "Our current degrees include BS in CS, Artificial Intelligence, and Software Engineering.",
    "fee": "Semester fees vary by department, usually ranging from 50k to 80k PKR.",
}
def generate_reply(query):
    query = query.lower()
    for key in KNOWLEDGE_BASE:
        if key in query:
            return KNOWLEDGE_BASE[key]
    return "I'm not sure about that. Try asking about our programs, fees, or deadlines."
@app.route("/", methods=["GET", "POST"])
def home_screen():
    bot_output = ""
    if request.method == "POST":
        raw_msg = request.form.get("message", "")
        bot_output = generate_reply(raw_msg)
    return render_template("index.html", reply_text=bot_output)
if __name__ == "__main__":
    app.run(debug=True)