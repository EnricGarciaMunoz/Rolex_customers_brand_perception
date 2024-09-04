import pandas as pd # type: ignore
from textblob import TextBlob  # type: ignore
import os

# Get the absolute path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the full path for the input file
input_path = os.path.join(script_dir, '..', 'data', 'reviews.csv')

# Check if the input file exists
if not os.path.exists(input_path):
    raise FileNotFoundError(f"The input file does not exist at the path: {input_path}")

# Read the existing CSV file with the reviews
review_data = pd.read_csv(input_path)

# Initialize lists to store polarity and subjectivity
polarities = []
subjectivities = []

# Iterate over each review text in the 'Content' column
for text in review_data['Content']:
    # Create a TextBlob object for the text
    blob = TextBlob(text)
    # Get the polarity and subjectivity
    polarity = round(blob.sentiment.polarity, 2)  # Limit to 2 decimal places
    subjectivity = round(blob.sentiment.subjectivity, 2)  # Limit to 2 decimal places
    # Add the results to the corresponding lists
    polarities.append(polarity)
    subjectivities.append(subjectivity)

# Add the new columns to the DataFrame
review_data['Polarity'] = polarities
review_data['Subjectivity'] = subjectivities

# Build the full path for the output file
output_path = os.path.join(script_dir, '..', 'data', 'reviews_with_emotion_score.csv')

# Save the data to a new CSV file in the data folder
review_data.to_csv(output_path, index=False)

print(f"CSV with sentiment analysis saved as '{output_path}'")
