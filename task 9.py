# Import library
from textblob import TextBlob

# Take input from user
text = input("Enter your sentence: ")

# Create TextBlob object
analysis = TextBlob(text)

# Display results
print("\n--- Result ---")
print("Text:", text)
print("Polarity:", analysis.sentiment.polarity)
print("Subjectivity:", analysis.sentiment.subjectivity)

# Sentiment Classification
if analysis.sentiment.polarity > 0:
    print("Sentiment: Positive")
elif analysis.sentiment.polarity < 0:
    print("Sentiment: Negative")
else:
    print("Sentiment: Neutral")