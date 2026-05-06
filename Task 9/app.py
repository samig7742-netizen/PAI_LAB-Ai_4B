from textblob import TextBlob
def process_text_sentiment(input_string):
    analysis = TextBlob(input_string)
    positivity = analysis.sentiment.polarity
    bias_score = analysis.sentiment.subjectivity
    print("\n--- Sentiment Analysis Report ---")
    print(f"Input: {input_string}")
    print(f"Positivity Score (-1 to 1): {positivity:.2f}")
    print(f"Subjectivity Score (0 to 1): {bias_score:.2f}")
    if positivity > 0.1:
        sentiment = "Positive"
    elif positivity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    print(f"Overall Mood: {sentiment}")
    print("---------------------------------\n")
def main():
    user_input = input("Please enter a sentence to evaluate its mood: ")
    if user_input.strip():
        process_text_sentiment(user_input)
    else:
        print("Invalid input. Please provide some text.")
if __name__ == "__main__":
    main()