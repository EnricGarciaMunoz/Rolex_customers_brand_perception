import pandas as pd
import os

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the CSV file located in the 'data' folder
csv_path = os.path.join(script_dir, '..', 'data', 'reviews_raw.csv')

# Check if the file exists
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"The file does not exist at the path: {csv_path}")

# Read the CSV file
df = pd.read_csv(csv_path)

# Function to clean the content
def clean_content(text):
    # Check if 'Date of experience:' is in the text
    if 'Date of experience:' in text:
        # Split the text and keep the part before 'Date of experience:'
        return text.split('Date of experience:')[0].strip()
    else:
        return text

# Apply the function to the 'Content' column
df['Content'] = df['Content'].apply(clean_content)

# Path to save the cleaned file as 'reviews.csv' in the 'data' folder
output_path = os.path.join(script_dir, '..', 'data', 'reviews.csv')

# Save the modified DataFrame to a new CSV file
df.to_csv(output_path, index=False)

print(f"Cleaned file saved at: {output_path}")
